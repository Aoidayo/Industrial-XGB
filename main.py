from flask import Flask, jsonify
from flask_sockets import Sockets
from flask import request

from model.xgb.xgb import XGB
# from model.gat.gat import GAT
from utils.Processor.JFProcessor import JFProcessor

app = Flask(__name__)
sockets = Sockets(app)
jfProcessor = JFProcessor()

data_prefix = "./data/"
missing = -1
none_exist = -2

@app.route('/train', methods=["POST"])
def train():
    log = None
    try:
        json = request.get_json()
        print(json['algorithmName'], json['taskId'])
        model = None
        if (json['algorithmName'] == "xgb"):
            model = XGB(data_prefix)
        elif (json['algorithmName'] == "gat"):
            model = GAT(data_prefix)
        model.init_data("zhihu0605v5")
        log = model.train(str(json['taskId']))
    except Exception as e:
        return jsonify(log), 500
    return jsonify(log), 200

@app.route('/predict', methods=["POST"])
def prediction():
    data = None
    try:
        json = request.get_json()
        print(json)
        x = jfProcessor.jf_process(jf_json=json)
        print(x)
        # x = {"巷道用途": "轨道运输巷", "巷道埋深": 333, "直接顶岩性": ['粉砂岩'], "直接顶厚度": 4.75,
        #      "老顶岩性": ['石灰岩'], "老顶厚度": 4.65,
        #      "断面形状": '矩形', "巷道毛断面宽度": 3.7, "巷道毛断面高度": 2.4, "煤柱宽度": -1, "煤层厚度": 1.8}

        # if (json['algorithmName'] == "xgb"):
        xgb = XGB(data_prefix)
        data = xgb.predict(x, 'xgb')
    except Exception as e:
        return jsonify(data), 500
    return jsonify(data), 200


if __name__ == '__main__':
    # model = XGB(data_prefix)
    # model.init_data("zhihu0605v5")
    # model.train('xgb')


    # model = GAT(data_prefix)
    # model.init_data("zhihu0605v5")
    # model.train('gat')
    #
    # x = {"巷道用途": "轨道运输巷", "巷道埋深": 333, "直接顶岩性": ['粉砂岩'], "直接顶厚度": 4.75,
    #      "老顶岩性": ['石灰岩'], "老顶厚度": 4.65,
    #      "断面形状": '矩形', "巷道毛断面宽度": 3.7, "巷道毛断面高度": 2.4, "煤柱宽度": -1, "煤层厚度": 1.8}

    # model = GAT(data_prefix)
    # model.predict(x, 'xgb')


    app.run(host='0.0.0.0', port=20011, debug=True)