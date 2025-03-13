import bisect
import os
import numpy as np
import pandas as pd
import pickle
from xgboost import XGBClassifier, XGBRegressor
from model.xgb.config import input, predict
from utils.utils import rmse, mkdir
from utils.Processor.PredictPostProcessor import PredictPostProcessor
predictPostProcessor = PredictPostProcessor()

# # 解决中文乱码问题
# plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 指定默认字体：解决plot不能显示中文问题
# plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
# # -------------------------------

data_prefix = "./data/"
missing = -1
none_exist = -2

class XGB:
    # 初始化
    def __init__(self, data_path):
        # 初始化训练参数
        self.x = None
        self.y = {}
        self.data_path = data_path


        # 输入参数 (处理中文数据集, )
        self.input_zh_keys = input.input_zh_keys # 输入参数中文
        self.input_zh_cls_keys = input.input_zh_cls_keys   # 分类参数中文名
        self.input_zh_reg_keys = input.input_zh_reg_keys # 回归参数中文名
        self.input_zh_cls_range = input.input_zh_cls_range  # 分类参数 字符型取值范围
        self.input_zh_cls_minmax = input.input_zh_cls_minmax  # 分类参数 xgb数值取值范围
        self.input_zh_reg_minmax = input.input_zh_reg_minmax  # 回归参数 xgb数值取值范围

        # 输出 (contain 预测 and 计算)
        # 预测参数 (处理中文数据集, )
        self.predict_zh_range = predict.predict_zh_range
        self.predict_zh_keys = predict.predict_zh_keys
        self.predict_cls_keys = predict.predict_cls_keys
        self.predict_reg_keys = predict.predict_reg_keys
        self.predict_zh2en = predict.predict_zh2en


    # 获取二进制编码
    def _bin_encode(self, description: str, lst: list) -> int:
        description = str(description)
        if description == str(missing) or description == str(none_exist):
            return int(description)
        ans = 0
        for _ in range(len(lst)):
            if description.find(lst[_]) != -1:
                ans |= (1 << _)
        assert ans != 0
        return missing if ans == 0 else ans

    # 数值化一条输入参数
    def _symbolize_x(self, x: dict) -> list:
        x_lst = []
        for key in self.input_zh_cls_keys:
            if key.endswith('描述'):
                code = self._bin_encode(x[key], self.input_zh_cls_range[key])
                x_lst.append(code)
            else:
                code = self.input_zh_cls_range[key].index(x[key]) if x[key] in self.input_zh_cls_range[key] else -1
                x_lst.append(code)
        for key in self.input_zh_reg_keys:
            x_lst.append(x[key])
        # print(x_lst)
        return x_lst

    # 初始化测量参数
    def _add_x(self, data: pd.DataFrame) -> None:
        # x: 所有x数据, _x: 单条x
        #################################/ old part   /#################################
        # x = []
        # for _r in range(data.shape[0]): # _r : row_idx
        #     _x = {}
        #     for _c in self.input_zh_keys: # _c : col
        #         _x[_c] = data.loc[_r, _c]
        #     x.append(self._symbolize_x(_x))
        # self.x = np.array(x)
        #################################/ old part end   /#################################
        # 使用 itertuples 来遍历 DataFrame
        rows = list(data.iterrows())
        # rows = data.itertuples(index=False)
        # 使用列表推导式来生成 x, 减少使用loc重复索引
        x = [self._symbolize_x({col: getattr(row, col) for col in self.input_zh_keys}) for idx,row in rows]
        self.x = np.array(x)


    def _add_x_parallel(self, data: pd.DataFrame, num_processes: int = 4) -> None:
        # _add_x并行化支持
        from multiprocessing import Pool
        def process_row(row):
            return self._symbolize_x({col: getattr(row, col) for col in self.input_zh_keys})
        with Pool(num_processes) as pool:
            x = pool.map(process_row, data.itertuples(index=False))
        self.x = np.array(x)



    def _add_y(self, data: pd.DataFrame) -> None:
        # 初始化预测参数: for xgb only numeric value can train
        for zh_key in self.predict_zh_keys:
            lst = []
            if zh_key in self.predict_cls_keys:
               for _type in data[zh_key]:
                    _type = str(_type)
                    code = self.predict_zh_range[zh_key].index(_type) if _type in self.predict_zh_range[zh_key] else missing   # 缺失
                    lst.append(code)
            elif zh_key in self.predict_reg_keys:
                lst = data[zh_key]
            else:
                raise RuntimeError(f"Unkown zh_key {zh_key}")
            self.y[zh_key] = np.array(lst)


    # 初始化数据
    def init_data(self, dataset_name: str) -> None:
        '''

        Init:
            self.x ( len_rows, len(self.input_zh_keys) )
            self.y dict
                    key = (str) predict_key
                    value = (len_rows,)
        '''
        dataset_path = self.data_path + "dataset/" + dataset_name + '.csv'
        data = pd.read_csv(dataset_path, encoding='gbk')
        self._add_x(data)
        self._add_y(data)

    # 训练
    def train(self, task_id: str, second=False, log_front=False) -> str:
        log_info = []
        mkdir(self.data_path + "model/" + task_id)
        self.model_path = self.data_path + "model/{}/{}.pkl".format(task_id, task_id)
        self.log_path = self.data_path + "model/{}/{}.log".format(task_id, task_id)
        if os.path.exists(self.log_path):
            os.remove(self.log_path)
        impGraph_path = self.data_path + "model/{}/{}.jpg".format(task_id, task_id)
        # 模型参数
        params_classifier_adjust = {'max_depth': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'min_child_weight': [1, 2, 3, 4, 5, 6]}
        params_regression_adjust = {'reg_alpha': np.arange(0, 3, 0.5), 'reg_lambda': np.arange(0, 3, 0.5)}
        ## 固定模型参数
        if second:
            # 次优模型训练
            params_classifier_fixed = {'learning_rate': 0.1, 'n_estimators': 400, 'max_depth': 2,
                                       'objective': 'multi:softmax'}  # reg:squarederror
            params_regression_fixed = {'learning_rate': 0.1, 'n_estimators': 1500, 'max_depth': 4,
                                       'objective': 'reg:squarederror'}
        else:
            params_classifier_fixed = {'learning_rate': 0.1, 'n_estimators': 500, 'max_depth': 2,
                                       'objective': 'multi:softmax'}  # reg:squarederror
            params_regression_fixed = {'learning_rate': 0.1, 'n_estimators': 2000, 'max_depth': 4,
                                       'objective': 'reg:squarederror'}
        # 分参数拟合模型
        xgb_dict, choose_dict = {}, {}
        for zh_key in self.predict_zh_keys:
            if zh_key in self.predict_cls_keys:
                choose = self.y[zh_key] != missing # y[zh_key]中 不缺失的行
                # x,y 同步取不缺失行
                _x = self.x[choose, :]
                _y = self.y[zh_key][choose]
                print(f"{zh_key} train start")
                xgb = XGBClassifier(**params_classifier_fixed, num_class=len(self.predict_zh_range[zh_key])).fit(_x, _y)
            else:
                # best_params = self._model_adjust_parameters(_x, _y, params_regression_adjust, params_regression_fixed, yucecanshu[_])
                choose = self.y[zh_key] >= 0
                _x = self.x[choose, :]
                _y = self.y[zh_key][choose]
                print(f"{zh_key} train start")
                xgb = XGBRegressor(**params_regression_fixed).fit(_x, _y)
            xgb_dict[zh_key], choose_dict[zh_key] = xgb, choose
        # 保存模型
        with open(self.model_path, 'wb') as file:
            pickle.dump(xgb_dict, file)
        log_symbol = " <br/>" if log_front else "\n"

        #todo 计算损失
        for zh_key in self.predict_zh_keys:
            _y = xgb_dict[zh_key].predict(self.x[choose_dict[zh_key], :])
            if zh_key in self.predict_cls_keys:
                accuracy = sum(1 if _yc == _yp else 0 for _yc, _yp in zip(self.y[zh_key][choose_dict[zh_key]], _y)) / len(_y)
                log_info.append("{} accuracy : {}".format(zh_key, accuracy))
                with open(self.log_path, 'a', encoding='utf-8') as f:
                    f.write("{} accuracy : {} {}".format(zh_key, accuracy, log_symbol))
            else:
                _rmse = rmse(self.y[zh_key][choose_dict[zh_key]], _y)
                log_info.append("{} rmse : {}".format(zh_key, _rmse))
                with open(self.log_path, 'a', encoding='utf-8') as f:
                    f.write("{} rmse : {} {}".format(zh_key, _rmse, log_symbol))
        # 画出参数重要性
        # params_importance = dict(sorted(self._get_labeled_importance(xgb_dict["推移千斤顶规格"].fit(self.x, self.y["推移千斤顶规格"]))
        #                                  .items(), key=lambda _: _[1], reverse=True))
        # print(params_importance)
        # log_info.append("参数重要性: " + str(params_importance) + "<br/>")
        # self._draw_importance(params_importance, impGraph_path)
        print('\n'.join(log_info))
        return log_symbol.join(log_info)

    # 预测
    def predict(self, raw_x: dict, task_id: str) -> dict:
        '''

        :param raw_x: 与训练数据相同的key, { zh_key: val }
        :param task_id:
        :return:
        '''
        model_path = self.data_path + "model/{}/{}.pkl".format(task_id, task_id)
        x = [self._symbolize_x(raw_x)]

        # 预测
        res = {}
        eps = 0.001
        xgb_dict = pickle.load(open(model_path, 'rb'))

        # 处理分类参数
        for cls_key in self.predict_cls_keys:
            # 处理类型
            xgb = xgb_dict[cls_key]
            val = xgb.predict(x)[0]
            print(cls_key, val)
            val_range = self.predict_zh_range[cls_key]
            res[cls_key] = val_range[val]
            assert res[cls_key] != -1

        # 处理回归参数
        for reg_key in self.predict_reg_keys:
            xgb = xgb_dict[reg_key]
            val = xgb.predict(x)[0]
            val_range = self.predict_zh_range[reg_key]
            assert val >= 0
            print(reg_key, val)
            if val in val_range:
                res[reg_key] = val
            elif reg_key.endswith('距'):
                val *= 1 + eps
                # bisect_left : first val index >= val  [0, len]
                res[reg_key] = val_range[max(bisect.bisect_left(val_range, val) - 1, 0)]
            else:
                val *= 1 - eps
                res[reg_key] = val_range[min( bisect.bisect_left(val_range, val), len(val_range) - 1)]
        # 处理参数不存在时,置其子依赖参数不存在
        # predict_cls_keys的子keys
        # for _type, _param_lst in self.yucecanshu_clt.items():
        #     if (res[_type] == none_exist):
        #         for _param in _param_lst:
        #             res[_param] = -2
        print(res, len(res))
        res_py = predictPostProcessor.predict_post_process(res, raw_x)
        return res_py
