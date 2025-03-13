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
 |    |    |-- xgb.py    # 算法xgbv3
 |    |    |-- config.py # input / predict config; 与data.csv保持同一
 |-- utils  # 工具文件夹
 |    |-- utils.py  # 常用工具
 |    |-- Processor  
 |    |    |-- JFProcessor.py #  将甲方en输入处理为模型预测zh输入; filter unnecessary JF_input ; 
 |    |    |-- PredictPostProcessor.py #  将模型预测zh输出处理为甲方需要的en输出; 预置甲方规则**硬编码** 
 |    |    |-- JFProcessorConfig.py 
 |    |    |-- PredictPostProcessorConfig.py 
 |-- .gitignore
 |-- env.yml        # 环境文件
 |-- main.py    # 主启动代码    
 |-- main_test.py   # 测试启动代码
 |-- readme.md 
 |-- requirement.txt    # 包需求
 |-- test.py    # 无关代码
```

# 环境
~~什么年代了, 还conda呢?~~
替换:
- miniforge: https://github.com/conda-forge/miniforge/releases
  - 推荐miniforge, 可以和conda混用, 支持pycharm调试
- micromamba : https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html#windows
  - 如果只在linux环境下使用, 且不要求调试, 可选择这个 
```bash
mamba create -n ml-framework python=3.11
mamba config set custom_channels.pytorch https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/
mamba config set custom_channels.nvidia https://mirrors.cernet.edu.cn/anaconda-extra/cloud/
mamba install pytorch-cuda=12.1 -c pytorch -c nvidia
mamba install pytorch=2.4.0=py3.11_cuda12.1_cudnn9_0 
pip install -r requirements.txt
```

# 注意

-1 表示缺失；-2 表示不存在

数值型一定可以成功预测，除非违反逻辑

字符型预测视情况可以预测出不存在（-2）