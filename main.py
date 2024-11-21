from flask import Flask
from flask_sockets import Sockets
from flask import request

from model.xgb.xgb_v3 import XGB

app = Flask(__name__)
sockets = Sockets(app)

data_prefix = "./data/"
missing = -1
none_exist = -2

@app.route('/train', methods=["POST"])
def train():
    json = request.get_json()
    print(json['algorithmName'], json['taskId'])
    model = XGB(data_prefix)
    model.init_data("zhihu0605v4")
    return model.train(str(json['taskId']))

@app.route('/predict', methods=["POST"])
def prediction():
    json = request.get_json()
    print(json)

    x = {
        "巷道用途": json['hangdaoyongtu'], "巷道埋深": json['hangdaomaishen'],
        "直接顶岩性": json['zhijiedingyanxing'], "直接顶厚度": json['zhijiedinghoudu'],
        "老顶岩性": json['laodingyanxing'], "老顶厚度": json['laodinghoudu'],
        "断面形状": json['duanmianxingzhuang'],
        "巷道毛断面宽度": json['hangdaomaoduanmiankuandu'], "巷道毛断面高度": json['hangdaomaoduanmiangaodu'],
        "煤柱宽度": json['meizhukuandu'], "煤层厚度": json['meicenghoudu'],
    }
    # x = {"巷道用途": "轨道运输巷", "巷道埋深": 333, "直接顶岩性": ['粉砂岩'], "直接顶厚度": 4.75,
    #      "老顶岩性": ['石灰岩'], "老顶厚度": 4.65,
    #      "断面形状": '矩形', "巷道毛断面宽度": 3.7, "巷道毛断面高度": 2.4, "煤柱宽度": -1, "煤层厚度": 1.8}
    print(x)
    xgb = XGB(data_prefix)
    # print(xgb.predict(x, str(json['id'])))
    return xgb.predict(x, 'xgb')

if __name__ == '__main__':
    model = XGB(data_prefix)
    model.init_data("zhihu0605v5")
    model.train('xgb')

    x = {"巷道用途": "轨道运输巷", "巷道埋深": 333, "直接顶岩性": ['粉砂岩'], "直接顶厚度": 4.75,
         "老顶岩性": ['石灰岩'], "老顶厚度": 4.65,
         "断面形状": '矩形', "巷道毛断面宽度": 3.7, "巷道毛断面高度": 2.4, "煤柱宽度": -1, "煤层厚度": 1.8}
    print(x)
    xgb = XGB(data_prefix)
    # print(xgb.predict(x, str(json['id'])))
    xgb.predict(x, 'xgb')

    # app.run(host='0.0.0.0', port=20010, debug=True)