from model.xgb.xgb_v3 import XGB

data_prefix = "./data/"


if __name__ == '__main__':
    model = XGB(data_prefix)
    model.init_data("test")
    model.train('test')

    x = {"测量一": -1, "测量二": 4}
    xgb = XGB(data_prefix)
    xgb.predict(x, 'test')