import numpy as np
import os

def rmse(prediction, target):
   # rmse 计算
   assert len(prediction) == len(target)
   alpha = 1.0 / prediction.shape[0]
   return np.sqrt(np.sum(np.square(prediction - target)) * alpha)

def mkdir(dir_path):
    # 新建目录
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def convert_numpy(obj):
    if isinstance(obj, (np.float32)):
        return float(obj)
    # elif isinstance(obj, (np.int32, np.int64)):
    #     return int(obj)
    # elif isinstance(obj, np.ndarray):
    #     return obj.tolist()