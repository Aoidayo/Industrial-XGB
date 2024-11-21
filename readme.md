## 目录结构
```
ml-framework
 |-- data  # 数据模型文件夹
 |    |-- dataset   # 数据集文件夹
 |    |    |-- zhihu0605v4.xlsx # 支护数据v5
 |    |    |-- test.xlsx    # 测试数据
 |    |-- model  # 模型文件夹
 |    |    |-- test # 测试模型的文件夹    
 |    |    |-- xgb  # 算法xgb的模型文件夹
 |-- model  # 算法文件夹
 |    |-- xgb   # 算法xgb的文件夹
 |    |    |-- xgb_v3.py    # 算法xgbv3
 |-- utils  # 工具文件夹
 |    |-- config.py # 配置项
 |    |-- config_test.py    # 测试配置项
 |    |-- utils.py  # 常用工具
 |-- .gitignore
 |-- env.yml        # 环境文件
 |-- main.py    # 主启动代码    
 |-- main_test.py   # 测试启动代码
 |-- readme.md 
 |-- requirement.txt    # 包需求
 |-- test.py    # 无关代码
```

# 环境
```bash
conda create -n ml-framework python=3.11
pip install -r requirements.txt
```

# 注意

-1 表示缺失；-2 表示不存在

数值型一定可以成功预测，除非违反逻辑

字符型预测视情况可以预测出不存在（-2）