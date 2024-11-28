import bisect
import os
import shutil

import numpy as np
# import matplotlib.pyplot as plt
import pandas as pd
import torch.nn.functional as F
import pickle
import torch
from torch.utils.tensorboard import SummaryWriter
from torch_geometric.data import Data
from torch_geometric.nn import GATConv, MLP, Linear
from math import sqrt

from utils.config_test import *
from utils.utils import mkdir

# # 解决中文乱码问题
# plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 指定默认字体：解决plot不能显示中文问题
# plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
# # -------------------------------

data_prefix = "./data/"
missing = -1
none_exist = -2

class GATClassifier(torch.nn.Module):
    def __init__(self, in_features, out_features, heads=1):
        super(GATClassifier, self).__init__()
        self.gatConv1 = GATConv(in_features, 128)
        self.linear = Linear(128, 128)
        self.gatConv2 = GATConv(128, 64)
        self.mlp = MLP([64, out_features])

    def forward(self, x, edge_index):
        # x, edge_index = data.x, data.edge_index
        x = F.relu(self.gatConv1(x, edge_index))
        x = self.linear(x)
        x = F.relu(self.gatConv2(x, edge_index))
        x = self.mlp(x)
        return F.log_softmax(x, dim=1)

class GATRegressor(torch.nn.Module):
    def __init__(self, in_features, out_features):
        super(GATRegressor, self).__init__()
        self.gatConv1 = GATConv(in_features, 128)
        self.linear = Linear(128, 32)
        self.gatConv2 = GATConv(32, 16)
        self.mlp = MLP([16, out_features])

    def forward(self, x, edge_index):
        # x, edge_index = data.x, data.edge_index
        x = F.relu(self.gatConv1(x, edge_index))
        x = self.linear(x)
        x = F.relu(self.gatConv2(x, edge_index))
        x = self.mlp(x)
        return x.squeeze()  # 输出形状调整

class GAT:
    # 初始化
    def __init__(self, data_path):
        self.x = None
        self.y = {}
        self.pos = None
        self.edge_index = {}
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

    # 添加坐标
    def _add_pos(self, zhihu_data: pd.DataFrame) -> None:
        self.pos = zhihu_data[['煤矿经度', '煤矿纬度']].values

    # 初始化数据
    def init_data(self, dataset_name: str) -> None:
        dataset_path = self.data_path + "dataset/" + dataset_name + '.xlsx'
        data = pd.read_excel(io=dataset_path)
        self._add_x(data)
        self._add_y(data)
        self._add_pos(data)

    def _train_regressor(self, data: Data, yucecanshu: str):
        data = data.to("cuda:0")
        # 设置优化器，损失函数
        model = GATRegressor(self.l_celiangcanshu, 1).cuda()
        optimizer = torch.optim.Adam(model.parameters(), lr=0.001, weight_decay=5e-4)
        mse_loss = torch.nn.MSELoss()
        early_stopping_patience, patience_counter = 10, 0
        best_model, best_loss = None, float('inf')

        # 训练模型
        model.train()
        for epoch in range(100):  # 先尝试较少的 epoch
            optimizer.zero_grad()
            pred = model(data.x, data.edge_index)
            loss = mse_loss(pred, data.y)
            loss.backward()
            optimizer.step()
            self.writer.add_scalar('Loss/' + yucecanshu, loss.item(), epoch)

            # 早停机制
            if loss.item() < best_loss:
                best_loss = loss.item()
                best_model = model
                patience_counter = 0
            else:
                patience_counter += 1

            if patience_counter >= early_stopping_patience:
                break
        return best_model.cpu()

    def _train_classifier(self, data: Data, yucecanshu: str):
        data = data.to("cuda:0")
        # 设置优化器，损失函数
        model = GATClassifier(self.l_celiangcanshu, len(self.yucecanshu_range[yucecanshu]), 4).cuda()
        optimizer = torch.optim.Adam(model.parameters(), lr=0.001, weight_decay=5e-4)
        ce_loss = torch.nn.CrossEntropyLoss()
        early_stopping_patience, patience_counter = 10, 0
        best_model, best_loss = None, float('inf')

        # 训练模型
        model.train()
        for epoch in range(1000):  # 先尝试较少的 epoch
            optimizer.zero_grad()
            pred = model(data.x, data.edge_index)
            loss = ce_loss(pred, data.y)
            loss.backward()
            optimizer.step()
            self.writer.add_scalar('Loss/' + yucecanshu, loss.item(), epoch)

            # 早停机制
            if loss.item() < best_loss:
                best_loss = loss.item()
                best_model = model
                patience_counter = 0
            else:
                patience_counter += 1

            if patience_counter >= early_stopping_patience:
                break
        return best_model.cpu()

    def _build_graph(self, pos: np.array) -> torch.Tensor:
        def dis(x: np.array, y: np.array) -> float:
            return np.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)
        eps = 1e-4
        edge_index = []
        for _i in range(len(pos)):
            for _j in range(_i, len(pos)):
                if (dis(pos[_i], pos[_j]) <= eps):
                    edge_index.append([_i, _j])
                    edge_index.append([_j, _i])
        return torch.tensor(edge_index, dtype=torch.long).t().contiguous()

    def _predict_classifier(self, gat: GATClassifier, x: torch.Tensor, pos: torch.Tensor) -> torch.Tensor:
        gat.eval()
        with torch.no_grad():
            pred = gat(x, self._build_graph(pos))
            pred = pred.argmax(dim=1)
        return pred

    def _predict_regressor(self, gat: GATRegressor, x: torch.Tensor, pos: torch.Tensor) -> torch.Tensor:
        gat.eval()
        with torch.no_grad():
            pred = gat(x, self._build_graph(pos))
        return pred

    # 训练
    def train(self, task_id: str) -> str:
        log_info = []
        mkdir(self.data_path + "model/" + task_id)
        self.model_path = self.data_path + "model/{}/{}.pkl".format(task_id, task_id)
        self.log_path = self.data_path + "model/{}".format(task_id, task_id)
        if os.path.exists(self.log_path):
            shutil.rmtree(self.log_path)
        self.writer = SummaryWriter(self.log_path)
        # impGraph_path = self.data_path + "model/{}/{}.jpg".format(task_id, task_id)
        # 分参数拟合模型
        gat_dict, choose_dict = {}, {}
        for _ in self.yucecanshu:
            print(_)
            if (_ in self.yucecanshu_str):
                choose = self.y[_] != missing
                _x = torch.tensor(self.x[choose, :], dtype=torch.float)
                _y = torch.tensor(self.y[_][choose], dtype=torch.long)
                _edge_index = self._build_graph(self.pos[choose, :])
                # print(_x, _y)
                gat = self._train_classifier(Data(x=_x, edge_index=_edge_index, y=_y), _)
                if (_ == '支护形式'):
                    self.writer.add_graph(gat, [_x, _edge_index])
            else:
                choose = self.y[_] >= 0
                _x = torch.tensor(self.x[choose, :], dtype=torch.float)
                _y = torch.tensor(self.y[_][choose], dtype=torch.float)
                _edge_index = self._build_graph(self.pos[choose, :])
                # print(_x, _y)
                gat = self._train_regressor(Data(x=_x, edge_index=_edge_index, y=_y), _)
            gat_dict[_], choose_dict[_] = gat, choose
        self.writer.close()
        # 保存模型
        with open(self.model_path, 'wb') as file:
            pickle.dump(gat_dict, file)
        # 计算损失
        for _ in self.yucecanshu:
            gat = gat_dict[_]
            if (_ in self.yucecanshu_str):
                _x = torch.tensor(self.x[choose_dict[_], :], dtype=torch.float)
                _y = torch.tensor(self.y[_][choose_dict[_]], dtype=torch.long)
                _pos = self.pos[choose_dict[_], :]
                pred = self._predict_classifier(gat, _x,  _pos)
                accuracy = (pred == _y).sum().item() / _x.shape[0]
                log_info.append("{} accuracy : {}".format(_, accuracy))
                # with open(self.log_path, 'a', encoding='utf-8') as f:
                #     f.write("{} accuracy : {} <br/>".format(_,accuracy))
            else:
                _x = torch.tensor(self.x[choose_dict[_], :], dtype=torch.float)
                _y = torch.tensor(self.y[_][choose_dict[_]], dtype=torch.long)
                _pos = self.pos[choose_dict[_], :]
                pred = self._predict_regressor(gat, _x, _pos)
                mse_loss = torch.nn.MSELoss()
                rmse = sqrt(mse_loss(pred, _y))
                log_info.append("{} rmse : {}".format(_, rmse))
                # with open(self.log_path, 'a', encoding='utf-8') as f:
                #     f.write("{} rmse : {} <br/>".format(_, rmse))

        print('\n'.join(log_info))
        return ' <br/>'.join(log_info)

    # 预测
    # def predict(self, x: dict) -> dict:
    #     model_path = self.data_path + "model/gat/gat"
    #     x = torch.tensor([self._symbolize_x(x)], dtype=torch.float)
    #     res = {}
    #     # 支护预测
    #     eps_zhihu = 0.001
    #     # xgb_list = self.minioUtils.download_file(model_path + '.pkl')
    #     gat_dict = pickle.load(open(model_path + '.pkl', 'rb'))
    #     for _type, _params_lst in yucecanshu_clt.items():
    #         # 处理类型
    #         gat = gat_dict[_type]
    #         print(gat)
    #         val = self._predict_classifier(gat, x, _type)
    #         print(_type, val)
    #         exit(0)
    #         val_range = self.yucecanshu_range[_type]
    #         res[_type] = val_range[val]
    #         assert res[_type] != -1
    #         if (res[_type] == none_exist):
    #             for _params in _params_lst:
    #                 res[_params] = -2
    #         else:
    #             for _params in _params_lst:
    #                 gat = gat_dict[_params]
    #                 val = self._predict_regressor(gat, x, _type).item()
    #                 val_range = self.yucecanshu_range[_params]
    #                 val = max(val, 0)
    #                 assert val >= 0
    #                 print(_type, val)
    #                 if (val in val_range):
    #                     res[_params] = val
    #                 elif (_params.endswith('锚索间距') or _params.endswith('锚索排距')):
    #                     res[_params] = res[_params.replace('索', '杆')] << 1
    #                 elif (_params.endswith('距')):
    #                     val *= 1 + eps_zhihu
    #                     res[_params] = val_range[max(bisect.bisect_left(val_range, val) - 1, 0)]
    #                 else:
    #                     val *= 1 - eps_zhihu
    #                     res[_params] = val_range[min(bisect.bisect_left(val_range, val), len(val_range) - 1)]
    #     # print(res_py)
    #     print(res, len(res))
    #     res_py = {}
    #     for _k, _v in res.items():
    #         if (_v != -2):
    #             res_py[self.yucecanshu2py[_k]] = _v
    #     print(res_py, len(res_py))
    #     return res_py
