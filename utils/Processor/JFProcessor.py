import utils.Processor.JFProcessorConfig as config
'''
处理甲方的输入为我们需要的输入
'''
class JFProcessor:
    def __init__(self):
        self.config = config
        pass

    def jf_process(self,jf_json):
        # 1. filter
        import copy
        yf_json = copy.deepcopy(jf_json)
        if yf_json['roadwayType'] == "rectangle":
            yf_json['archLength'] = yf_json['rectangleLength']
            yf_json['archWidth'] = yf_json['rectangleWidth']
        elif yf_json['roadwayType'] == "arch":
            yf_json["rectangleLength"] = yf_json['archLength']
            yf_json['rectangleWidth'] = yf_json['archWidth']

        # 预定义埋深和硬度的最大最小值
        replaceKeys = ["depth", "hardness"]
        replaceDict = {
            "depth": {
                "1": "0~100~200",
                "2": "200~300~400",
                "3": "400~500~600",
                "4": "600~700~800",
                "5": "1000~1000~1000",
            },
            "hardness": {
                "1": "0.65~0.65~0.65",
                "2": "1.15~1.15~1.15",
                "3": "2.25~2.25~2.25",
                "4": "3~3~3"},
        }
        for key in replaceKeys:
            if key in yf_json.keys():
                # 如果传递 则修改, 没有传递,则不添加
                # option 可以是1或者"1"
                option = yf_json[key]
                yf_json[key + "Min"], yf_json[key + "Avg"], yf_json[key + "Max"] = replaceDict[key][
                    str(option)].split("~")

        # del keys
        for key in config.filter_jf2yf['delete']:
            if key in yf_json.keys():
                del yf_json[key]

        # parseFloat
        floatField = list(config.filter_jf2yf['parseFloat'].keys())
        for key in floatField:
            if key in yf_json.keys():
                yf_json[key] = float(yf_json[key])

        # 2. en2zh
        yf_x = {}
        for _k, _v in config.yf_input_en2zh.items():
            yf_x[_v] = yf_json[_k]

        # # 3. reserve
        # reserve_json = {}
        # # jf
        # for key in list(config.reserve_en2zh['jf_input'].keys()):
        #     reserve_json[key] = jf_json[key]
        # for key in list(config.reserve_en2zh['yf_input'].keys()):
        #     reserve_json[key] = yf_json[key]

        # return yf_x, reserve_json
        return yf_x