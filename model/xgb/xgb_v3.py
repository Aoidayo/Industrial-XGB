import bisect
import os
import random
import shutil

# from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import pickle

from xgboost import XGBClassifier, XGBRegressor

from utils.config import *

# # 解决中文乱码问题
# plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 指定默认字体：解决plot不能显示中文问题
# plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
# # -------------------------------

data_prefix = "./data/"
missing = -1
none_exist = -2

def rmse(prediction, target):
   # rmse 计算
   assert len(prediction) == len(target)
   alpha = 1.0 / prediction.shape[0]
   return np.sqrt(np.sum(np.square(prediction - target)) * alpha)

def mkdir(dir_path):
    # 新建目录
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

class XGB:
    # 初始化
    def __init__(self, data_path):
        self.x = None
        self.y = {}
        self.data_path = data_path
        # 测量参数
        self.celiangcanshu = celiangcanshu
        self.l_celiangcanshu = len(celiangcanshu)
        self.celiangcanshu_range = celiangcanshu_range
        # 预测参数
        self.yucecanshu = yucecanshu
        self.l_yucecanshu = len(yucecanshu)
        self.yucecanshu_range = yucecanshu_range
        # 转换
        self.yucecanshu2py = yucecanshu2py

    # 获取岩性编码
    def _get_yanxing(self, description: str, yanxing_lst: list) -> int:
        description = str(description)
        if (description == str(missing) or description == str(none_exist)):
            return int(description)
        ans = 0
        for _ in range(len(yanxing_lst)):
            if description.find(yanxing_lst[_]) != -1:
                ans |= (1 << _)
        assert ans != 0
        return missing if ans == 0 else ans

    # 数值化一条测量参数
    def _symbolize_x(self, x: dict) -> list:
        x_lst = []
        for _ in self.celiangcanshu:
            if (self.celiangcanshu_range[_]):
                if (_.endswith('岩性')):
                    code = self._get_yanxing(x[_], self.celiangcanshu_range[_])
                    x_lst.append(code)
                else:
                    assert x[_] != -2
                    code = self.celiangcanshu_range[_].index(x[_]) if x[_] in self.celiangcanshu_range[_] else -1
                    x_lst.append(code)
            else:
                x_lst.append(x[_])
        return x_lst

    # 初始化测量参数
    def _add_x(self, zhihu_data: pd.DataFrame) -> None:
        x = []
        for _r in range(zhihu_data.shape[0]):
            _x = {}
            for _c in self.celiangcanshu:
                _x[_c] = zhihu_data.loc[_r, _c]
            x.append(self._symbolize_x(_x))
        self.x = np.array(x)

    # 初始化预测参数
    def _add_y(self, zhihu_data: pd.DataFrame) -> None:
        for _ in self.yucecanshu:
            lst = []
            if (_.endswith("类型") or _ == '支护形式' or _ == '钢棚型号' or _ == '喷浆材料'):
               for _type in zhihu_data[_]:
                    code = self.yucecanshu_range[_].index(_type) if _type in self.yucecanshu_range[_] else missing   # 缺失
                    lst.append(code)
               # print(_, list(set(lst)), max(list(set(lst))))
               # assert len(list(set(lst))) == max(list(set(lst))) + 1
            else:
               lst = zhihu_data[_]
            self.y[_] = np.array(lst)

    # 初始化数据
    def init_data(self, dataset_name: str) -> None:
        dataset_path = self.data_path + "dataset/" + dataset_name + '.xlsx'
        zhihu_data = pd.read_excel(io=dataset_path)
        self._add_x(zhihu_data)
        self._add_y(zhihu_data)

    # 训练
    def train(self, task_id: str) -> str:
        log_info = []
        mkdir(self.data_path + "model/" + task_id)
        self.model_path = self.data_path + "model/{}/{}.pkl".format(task_id, task_id)
        self.log_path = self.data_path + "model/{}/{}.log".format(task_id, task_id)
        if os.path.exists(self.log_path):
            os.remove(self.log_path)
        # impGraph_path = self.data_path + "model/{}/xgb.jpg".format(task_id)
        # 模型参数
        params_classifier_adjust = {'max_depth': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'min_child_weight': [1, 2, 3, 4, 5, 6]}
        params_classifier_fixed = {'learning_rate': 0.1, 'n_estimators': 500, 'max_depth': 2,
                                   'objective': 'multi:softmax  num_class=n'}  # reg:squarederror
        params_regression_adjust = {'reg_alpha': np.arange(0, 3, 0.5), 'reg_lambda': np.arange(0, 3, 0.5)}
        params_regression_fixed = {'learning_rate': 0.1, 'n_estimators': 2000, 'max_depth': 4,
                             'objective': 'reg:squarederror'}
        # 分参数拟合模型
        xgb_dict, choose_dict = {}, {}
        for _ in self.yucecanshu:
            print(_)
            if (_.endswith("类型") or _ == '支护形式' or _ == '钢棚型号' or _ == '喷浆材料'):
                choose = self.y[_] != missing
                _x = self.x[choose, :]
                _y = self.y[_][choose]
                xgb = XGBClassifier(**params_classifier_fixed).fit(_x, _y)
            else:
                # best_params = self._model_adjust_parameters(_x, _y, params_regression_adjust, params_regression_fixed, yucecanshu[_])
                choose = self.y[_] >= 0
                _x = self.x[choose, :]
                _y = self.y[_][choose]
                # print(_x, _y)
                xgb = XGBRegressor(**params_regression_fixed).fit(_x, _y)
            xgb_dict[_], choose_dict[_] = xgb, choose
        # 保存模型
        with open(self.model_path, 'wb') as file:
            pickle.dump(xgb_dict, file)
        # 计算损失
        for _ in self.yucecanshu:
            _y = xgb_dict[_].predict(self.x[choose_dict[_], :])
            if (_.endswith("类型") or _ == '支护形式' or _ == '钢棚型号' or _ == '喷浆材料'):
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
        print(' <br/>'.join(log_info))
        return ' <br/>'.join(log_info)

    # 预测
    def predict(self, raw_x: dict, task_id: str) -> dict:
        model_path = self.data_path + "model/{}/{}.pkl".format(task_id, task_id)
        x = [self._symbolize_x(raw_x)]
        print(x)
        res = {}
        # 支护预测
        eps_zhihu = 0.001
        xgb_dict = pickle.load(open(model_path, 'rb'))
        # 假设所有数值型参数都存在
        for _type, _param_lst in yucecanshu_clt.items():
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
                elif (_param.endswith('锚索间距') or _param.endswith('锚索排距')):
                    # 1.锚索间距/排距 = 锚杆间距/排距 * 2 （锚杆存在的条件下）
                    res[_param] = res[_param.replace('索', '杆')] << 1
                elif (_param.endswith('距')):
                    val *= 1 + eps_zhihu
                    res[_param] = val_range[max(bisect.bisect_left(val_range, val) - 1, 0)]
                else:
                    val *= 1 - eps_zhihu
                    res[_param] = val_range[min(bisect.bisect_left(val_range, val), len(val_range) - 1)]
        # 8.回采巷道没有喷浆
        if (raw_x['巷道用途'] == '回采巷道'):
            res['喷浆材料'] = none_exist
        # 9.煤柱帮应有锚杆
        if (res['煤柱帮锚杆类型'] == none_exist):
            res['煤柱帮锚杆类型'] = meizhubangmaoganleixing[random.randint(0, len(meizhubangmaoganleixing) - 1)]
        if (raw_x['巷道埋深'] >= 1000):
            # 7.如果巷道埋深超过1000的
            # 则满足下面条件
            # 锚杆直径22、钢号500 - 600、锚杆间距700 - 800、锚杆排距700 - 800、锚索直径21.8、
            # 锚索间距1400 - 1600、锚索排距1400 - 1600
            for _param, _param_lst in hangdaomaishen_extreme.items():
                if (_param.endswith('锚索间距') or _param.endswith('锚索排距')):
                    res[_param] = res[_param.replace('索', '杆')] << 1
                else:
                    res[_param] = _param_lst[random.randint(0, len(_param_lst) - 1)]
        for _key, _param_lst in yucecanshu_clpc.items():
            if (_key.endswith('排距')):
                # 2.顶锚杆排距 = 工作面帮锚杆排距 = 煤柱帮锚杆排距（min）
                #   顶锚索排距 = 工作面帮锚索排距 = 工作面帮锚索排距（min）
                mn = float('INF')
                for _param in _param_lst:
                    mn = min(mn, res[_param])
                for _param in _param_lst:
                    res[_param] = mn
            elif (_key.endswith('长度') or _key.endswith('直径')):
                # 3.顶锚杆长度 = 工作面帮锚杆长度 = 煤柱帮锚杆长度（max）
                # 顶锚索长度 = 工作面帮锚索长度 = 煤柱帮锚索长度（max）
                # 顶锚索直径 = 工作面帮锚索直径 = 煤柱帮锚索直径（max）
                mx = -float('INF')
                for _param in _param_lst:
                    mx = max(mx, res[_param])
                for _param in _param_lst:
                    res[_param] = mx
        # 顶锚杆直径 = max(顶锚杆直径, 工作面帮锚杆直径, 煤柱帮锚杆直径)
        res['顶锚杆直径'] = max(res['顶锚杆直径'], res['工作面帮锚杆直径'], res['煤柱帮锚杆直径'])
        # 4.煤柱帮锚索长度 <= 煤柱宽度（mm）
        res['煤柱帮锚索长度'] = min(res['煤柱帮锚索长度'], raw_x['煤柱宽度'] * 1000)
        if (res['工作面帮网类型'] != none_exist and res['煤柱帮网类型'] != none_exist and res['工作面帮网类型'] != res['煤柱帮网类型']):
            # 5.工作面帮网类型 = 煤柱帮网类型
            res['煤柱帮网类型'] = res['工作面帮网类型']

        if (raw_x['巷道埋深'] >= 400):
            # 6.顶板锚杆直径>=22且埋深超过400时要有金属网
            if (res['顶锚杆类型'] == none_exist):
                res['顶锚杆类型'] = '左旋无纵筋螺纹钢锚杆' if random.randint(0,1) else '左旋纵筋螺纹钢锚杆(树脂锚杆)'
            if (res['顶锚杆直径'] >= 22 and res['顶板网类型'] == none_exist):
                res['顶板网类型'] = '钢筋网' if random.randint(0,1) else '菱形金属网'
        #10 除（回采巷道、胶带运输巷、轨道运输巷、开切眼）外，煤柱帮的值赋值给工作面帮
        if (raw_x['巷道用途'] in huicaihangdao):
            for _yucecanshu in yucecanshu[::-1]:
                if (_yucecanshu.startswith('工作面帮')):
                    res[_yucecanshu] = res[_yucecanshu.replace('工作面帮', '煤柱帮')]
        #11 工作面帮不需要锚索
        res['工作面帮锚索类型'] = none_exist
        # 处理参数不存在的情况
        for _type, _param_lst in yucecanshu_clt.items():
            if (res[_type] == none_exist):
                for _param in _param_lst:
                    res[_param] = -2
        # print(res_py)
        print(res, len(res))
        res_py = {}
        for _k, _v in res.items():
            # if (_v != -2):
                res_py[self.yucecanshu2py[_k]] = _v
        print(res_py, len(res_py))
        return res_py
