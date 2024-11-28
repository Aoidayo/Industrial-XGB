import bisect
import os

# from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import pickle

from xgboost import XGBClassifier, XGBRegressor

from utils.config_test import *
from utils.utils import rmse, mkdir

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
        self.x = None
        self.y = {}
        self.data_path = data_path
        # 测量参数
        self.celiangcanshu = list(celiangcanshu_range.keys())
        self.l_celiangcanshu = len(self.celiangcanshu)
        self.celiangcanshu_range = celiangcanshu_range
        # 预测参数
        self.yucecanshu = list(yucecanshu_range.keys())
        self.l_yucecanshu = len(self.yucecanshu)
        self.yucecanshu_range = yucecanshu_range
        # 转换
        self.yucecanshu2py = yucecanshu2py
        self.yucecanshu_clt = yucecanshu_clt
        self.yucecanshu_str = list(yucecanshu_clt.keys())
        self.yucecanshu_oth_val = yucecanshu_oth_val

    # 获取二进制编码
    def _bin_encode(self, description: str, lst: list) -> int:
        description = str(description)
        if (description == str(missing) or description == str(none_exist)):
            return int(description)
        ans = 0
        for _ in range(len(lst)):
            if description.find(lst[_]) != -1:
                ans |= (1 << _)
        assert ans != 0
        return missing if ans == 0 else ans

    # 数值化一条测量参数
    def _symbolize_x(self, x: dict) -> list:
        x_lst = []
        for _ in self.celiangcanshu:
            if (self.celiangcanshu_range[_]):
                if (_.endswith('岩性')):
                    code = self._bin_encode(x[_], self.celiangcanshu_range[_])
                    x_lst.append(code)
                else:
                    code = self.celiangcanshu_range[_].index(x[_]) if x[_] in self.celiangcanshu_range[_] else -1
                    x_lst.append(code)
            else:
                x_lst.append(x[_])
        return x_lst

    # 初始化测量参数
    def _add_x(self, data: pd.DataFrame) -> None:
        x = []
        for _r in range(data.shape[0]):
            _x = {}
            for _c in self.celiangcanshu:
                _x[_c] = data.loc[_r, _c]
            x.append(self._symbolize_x(_x))
        self.x = np.array(x)

    # 初始化预测参数
    def _add_y(self, data: pd.DataFrame) -> None:
        for _ in self.yucecanshu:
            lst = []
            if (_ in self.yucecanshu_str):
               for _type in data[_]:
                    if (_type != none_exist):
                       _type = str(_type)
                    code = self.yucecanshu_range[_].index(_type) if _type in self.yucecanshu_range[_] else missing   # 缺失
                    lst.append(code)
               # print(_, list(set(lst)), max(list(set(lst))))
               # assert len(list(set(lst))) == max(list(set(lst))) + 1
            else:
               lst = data[_]
            self.y[_] = np.array(lst)

    # 初始化数据
    def init_data(self, dataset_name: str) -> None:
        dataset_path = self.data_path + "dataset/" + dataset_name + '.xlsx'
        data = pd.read_excel(io=dataset_path)
        self._add_x(data)
        self._add_y(data)

    # 训练
    def train(self, task_id: str) -> str:
        log_info = []
        mkdir(self.data_path + "model/" + task_id)
        self.model_path = self.data_path + "model/{}/{}.pkl".format(task_id, task_id)
        self.log_path = self.data_path + "model/{}/{}.log".format(task_id, task_id)
        if (os.path.exists(self.log_path)):
            os.remove(self.log_path)
        # impGraph_path = self.data_path + "model/{}/xgb.jpg".format(task_id)
        # 模型参数
        params_classifier_adjust = {'max_depth': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'min_child_weight': [1, 2, 3, 4, 5, 6]}
        params_classifier_fixed = {'learning_rate': 0.1, 'n_estimators': 500, 'max_depth': 2,
                                   'objective': 'multi:softmax'}  # reg:squarederror
        params_regression_adjust = {'reg_alpha': np.arange(0, 3, 0.5), 'reg_lambda': np.arange(0, 3, 0.5)}
        params_regression_fixed = {'learning_rate': 0.1, 'n_estimators': 2000, 'max_depth': 4,
                             'objective': 'reg:squarederror'}
        # 分参数拟合模型
        xgb_dict, choose_dict = {}, {}
        for _ in self.yucecanshu:
            if (_ in self.yucecanshu_str):
                choose = self.y[_] != missing
                _x = self.x[choose, :]
                _y = self.y[_][choose]
                print(_)
                xgb = XGBClassifier(**params_classifier_fixed, num_class=len(self.yucecanshu_range[_])).fit(_x, _y)
            else:
                # best_params = self._model_adjust_parameters(_x, _y, params_regression_adjust, params_regression_fixed, yucecanshu[_])
                choose = self.y[_] >= 0
                _x = self.x[choose, :]
                _y = self.y[_][choose]
                print(_)
                xgb = XGBRegressor(**params_regression_fixed).fit(_x, _y)
            xgb_dict[_], choose_dict[_] = xgb, choose
        # 保存模型
        with open(self.model_path, 'wb') as file:
            pickle.dump(xgb_dict, file)
        # 计算损失
        for _ in self.yucecanshu:
            _y = xgb_dict[_].predict(self.x[choose_dict[_], :])
            if (_ in self.yucecanshu_str):
                accuracy = sum(1 if _yc == _yp else 0 for _yc, _yp in zip(self.y[_][choose_dict[_]], _y)) / len(_y)
                log_info.append("{} accuracy : {}".format(_, accuracy))
                with open(self.log_path, 'a', encoding='utf-8') as f:
                    f.write("{} accuracy : {} <br/>".format(_, accuracy))
            else:
                _rmse = rmse(self.y[_][choose_dict[_]], _y)
                log_info.append("{} rmse : {}".format(_, _rmse))
                with open(self.log_path, 'a', encoding='utf-8') as f:
                    f.write("{} rmse : {} <br/>".format(_, _rmse))
        # 画出参数重要性
        # params_importance = dict(sorted(self._get_labeled_importance(xgb_dict['支护形式'].fit(self.x, self.y['支护形式']))
        #                                  .items(), key=lambda _: _[1], reverse=True))
        # log_info.append("参数重要性: " + str(params_importance) + "<br/>")
        # self._draw_importance(params_importance, impGraph_path)
        # log_info.append("<img style='width: 100%; height: 100%' src='http://127.0.0.1:9000/ruoyi/aiplat/importance/{}'>"
        #               .format(impGraph_path[impGraph_path.rfind('/') + 1:]))
        print('\n'.join(log_info))
        return ' <br/>'.join(log_info)

    # 预测
    def predict(self, raw_x: dict, task_id: str) -> dict:
        model_path = self.data_path + "model/{}/{}.pkl".format(task_id, task_id)
        x = [self._symbolize_x(raw_x)]
        print(x)
        res = {}
        # 支护预测
        eps = 0.001
        xgb_dict = pickle.load(open(model_path, 'rb'))
        # 处理字符串型参数与受影响的数值型参数
        for _type, _param_lst in self.yucecanshu_clt.items():
            # 处理类型
            xgb = xgb_dict[_type]
            val = xgb.predict(x)[0]
            print(_type, val)
            val_range = self.yucecanshu_range[_type]
            res[_type] = val_range[val]
            assert res[_type] != -1
            for _param in _param_lst:
                xgb = xgb_dict[_param]
                val = xgb.predict(x)[0]
                val_range = self.yucecanshu_range[_param]
                assert val >= 0
                print(_param, val)
                if (val in val_range):
                    res[_param] = val
                elif (_param.endswith('距')):
                    val *= 1 + eps
                    res[_param] = val_range[max(bisect.bisect_left(val_range, val) - 1, 0)]
                else:
                    val *= 1 - eps
                    res[_param] = val_range[min(bisect.bisect_left(val_range, val), len(val_range) - 1)]
        # 处理不受字符串型参数影响的数值型参数
        for _param in self.yucecanshu_oth_val:
            xgb = xgb_dict[_param]
            val = xgb.predict(x)[0]
            val_range = self.yucecanshu_range[_param]
            assert val >= 0
            print(_param, val)
            if (val in val_range):
                res[_param] = val_range[val_range.index(val)]
            elif (_param.endswith('距')):
                val *= 1 + eps
                res[_param] = val_range[max(bisect.bisect_left(val_range, val) - 1, 0)]
            else:
                val *= 1 - eps
                res[_param] = val_range[min(bisect.bisect_left(val_range, val), len(val_range) - 1)]
        # 处理参数不存在的情况
        for _type, _param_lst in self.yucecanshu_clt.items():
            if (res[_type] == none_exist):
                for _param in _param_lst:
                    res[_param] = -2
        print(res, len(res))
        res_py = {}
        for _k, _v in res.items():
            # if (_v != -2):
                res_py[self.yucecanshu2py[_k]] = _v
        print(res_py, len(res_py))
        return res_py
