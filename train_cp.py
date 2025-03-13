from model.xgb.xgb import XGB

data_prefix = "./data/"

def best_model_start():
    model = XGB(data_prefix)
    model.init_data("zmjv3")
    model.train("xgb")

def second_model_start():
    model = XGB(data_prefix)
    model.init_data("zmjv3")
    model.train("zmj_cp",second=True)

if __name__ == '__main__':
    # best_model_start()
    best_model_start()