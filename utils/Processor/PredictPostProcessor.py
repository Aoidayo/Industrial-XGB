import utils.Processor.PredictPostPorcessorConfig as config
'''
处理乙方的输出 为 甲方需要的输出
    1. predict zh2en
    2. compute en 预赋值
    3. compute 计算
'''

class PredictPostProcessor:
    def __init__(self):
        self.config = config

    def predict_zh2en(self, predict_json: dict) -> dict:
        predict_zh2en = self.config.predict_zh2en
        predict_en_json = {}
        for zh_key, _v in predict_json.items():
            predict_en_json[predict_zh2en[zh_key]] = _v
        return predict_en_json

    def compute_pre_assign(self, predict_en_json: dict):
        # 计算参数预赋值 -2
        compute_zh2en = self.config.compute_zh2en
        for _, en_key in compute_zh2en.items():
            predict_en_json[en_key] = -2
        return predict_en_json

    def compute(self, predict_json: dict, raw_x: dict) -> dict:
        # 每一份后置处理的规则, 使用todo记录
        # todo [ rule 4 ]
        if raw_x['煤层厚度-平均'] > 5:
            zhijiaheightMax = raw_x['煤层厚度-最大'] - 0.2
            zhijiaheightMin = raw_x['煤层厚度-最小'] - 0.1
        else:
            zhijiaheightMax = raw_x['煤层厚度-最大'] + 0.2
            zhijiaheightMin = raw_x['煤层厚度-最小'] + 0.1
        # predict_json['basic'], predict_json['workingResistance'] = getBasicType(raw_x['煤田片区'], raw_x['采煤工艺'],
        #                                                                         predict_json['workingResistance'],
        #                                                                         zhijiaheightMin, zhijiaheightMax)
        predict_json['basic'] = "ZY4800/09/21"
        predict_json['workingResistance'] = 4800
        if raw_x['煤层倾角'] < 10:
            predict_json['baseBottomAdjustmentStructure'] = -2
        elif 10 < raw_x['煤层倾角'] < 25:
            predict_json['baseBottomAdjustmentStructure'] = '单底调'
        else:
            predict_json['baseBottomAdjustmentStructure'] = '底调梁'

        if zhijiaheightMax < 2.4:
            predict_json['telescopicBeamJackSpecification'] = -2
            predict_json['firstLevelGuardJackSpecification'] = -2
            predict_json['secondLevelGuardJackSpecification'] = -2
            predict_json['thirdLevelGuardJackSpecification'] = -2
        else:
            predict_json['topBeamStructureForm'] = predict_json['topBeamStructureForm'] + '+伸缩梁'
            if 2.4 < zhijiaheightMax < 4.5:
                predict_json['topBeamStructureForm'] = predict_json['topBeamStructureForm'] + '+一级帮部'
                predict_json['secondLevelGuardJackSpecification'] = -2
                predict_json['thirdLevelGuardJackSpecification'] = -2
            elif 4.5 < zhijiaheightMax < 6.5:
                predict_json['topBeamStructureForm'] = predict_json['topBeamStructureForm'] + '+二级帮部'
                predict_json['thirdLevelGuardJackSpecification'] = -2
            elif zhijiaheightMax >= 6.5:
                predict_json['topBeamStructureForm'] = predict_json['topBeamStructureForm'] + '+三级帮部'
        thicknessAvg = raw_x['煤层厚度-平均']
        obliqueLength = raw_x['工作面长度']
        outputByYear = raw_x['工作面年产量']
        if 1.2 < thicknessAvg < 1.8 and obliqueLength == 200 and 60 < outputByYear < 120:
            predict_json['shearerDevice'] = 'MG2×160（100/125）/730（490/590）-AWD'
            predict_json['scraperConveyor'] = 'SGZ730/2×250'
            predict_json['backScraperConveyor'] = 'SGZ730/2×250'
            predict_json['loaderDevice'] = 'SZZ730/250'
            predict_json['crusherDevice'] = 'PLM1000'
        elif 1.3 < thicknessAvg < 2.6 and obliqueLength == 250 and 100 < outputByYear < 200:
            predict_json['shearerDevice'] = 'MG2×200/930-WD'
            predict_json['scraperConveyor'] = 'SGZ800/2×525'
            predict_json['backScraperConveyor'] = 'SGZ800/2×525'
            predict_json['loaderDevice'] = 'SZZ800/315'
            predict_json['crusherDevice'] = 'PLM2000'
        elif 1.6 < thicknessAvg < 2.6 and obliqueLength == 250 and 200 < outputByYear < 250:
            predict_json['shearerDevice'] = 'MG2×250/1200-WD'
            predict_json['scraperConveyor'] = 'SGZ900/2×700'
            predict_json['backScraperConveyor'] = 'SGZ900/2×700'
            predict_json['loaderDevice'] = 'SZZ900/400'
            predict_json['crusherDevice'] = 'PLM2000'
        elif 1.6 < thicknessAvg < 2.6 and obliqueLength == 300 and 200 < outputByYear < 250:
            predict_json['shearerDevice'] = 'MG2×250/1200-WD'
            predict_json['scraperConveyor'] = 'SGZ1000/3×1000'
            predict_json['backScraperConveyor'] = 'SGZ1000/3×1000'
            predict_json['loaderDevice'] = 'SZZ1000/525'
            predict_json['crusherDevice'] = 'PLM3000'
        elif 2.5 < thicknessAvg < 3.6 and obliqueLength == 200 and 150 < outputByYear < 200:
            predict_json['shearerDevice'] = 'MG300/730-WD'
            predict_json['scraperConveyor'] = 'SGZ764/2×525'
            predict_json['backScraperConveyor'] = 'SGZ764/2×525'
            predict_json['loaderDevice'] = 'SZZ764/250'
            predict_json['crusherDevice'] = 'PLM1000'
        elif 2.5 < thicknessAvg < 3.6 and obliqueLength == 300 and 200 < outputByYear < 250:
            predict_json['shearerDevice'] = 'MG300/730-WD'
            predict_json['scraperConveyor'] = 'SGZ800/2×700'
            predict_json['backScraperConveyor'] = 'SGZ1000/2×700'
            predict_json['loaderDevice'] = 'SZZ800/250'
            predict_json['crusherDevice'] = 'PLM1000'
        elif 1.8 < thicknessAvg < 3.6 and obliqueLength == 250 and 300 < outputByYear < 400:
            predict_json['shearerDevice'] = 'MG480/1162-WD'
            predict_json['scraperConveyor'] = 'SGZ800/2×525'
            predict_json['backScraperConveyor'] = 'SGZ800/2×525'
            predict_json['loaderDevice'] = 'SZZ1000/525'
            predict_json['crusherDevice'] = 'PLM3000'
        elif 2.5 < thicknessAvg < 3.6 and obliqueLength == 300 and 400 < outputByYear < 500:
            predict_json['shearerDevice'] = 'MG480/1162-WD'
            predict_json['scraperConveyor'] = 'SGZ800/2×700'
            predict_json['backScraperConveyor'] = 'SGZ1000/2×1000'
            predict_json['loaderDevice'] = 'SZZ 1200/700'
            predict_json['crusherDevice'] = 'PLM4000'
        elif 2.5 < thicknessAvg < 3.6 and obliqueLength == 300 and 400 < outputByYear < 500:
            predict_json['shearerDevice'] = 'MG480/1162-WD'
            predict_json['scraperConveyor'] = 'SGZ800/2×700'
            predict_json['backScraperConveyor'] = 'SGZ1000/2×1000'
            predict_json['loaderDevice'] = 'SZZ1200/700'
            predict_json['crusherDevice'] = 'PLM4000'
        elif 2.8 < thicknessAvg < 3.5 and obliqueLength == 300 and 500 < outputByYear < 800:
            predict_json['shearerDevice'] = 'MG610/1470-WD'
            predict_json['scraperConveyor'] = 'SGZ1000/2×1000'
            predict_json['backScraperConveyor'] = 'SGZ1000/2×1000'
            predict_json['loaderDevice'] = 'SZZ1200/700'
            predict_json['crusherDevice'] = 'PLM4000'
        elif 3.5 < thicknessAvg < 5.3 and obliqueLength == 300 and 500 < outputByYear < 800:
            predict_json['shearerDevice'] = 'MG750/2125-WD'
            predict_json['scraperConveyor'] = 'SGZ1000/3×1000'
            predict_json['backScraperConveyor'] = 'SGZ1200/3×1000'
            predict_json['loaderDevice'] = 'SZZ1200/700'
            predict_json['crusherDevice'] = 'PLM4000'
        elif 4 < thicknessAvg < 6.8 and obliqueLength == 300 and 800 < outputByYear < 1200:
            predict_json['shearerDevice'] = 'MG860/2415-WD'
            predict_json['scraperConveyor'] = 'SGZ1200/3×1000'
            predict_json['backScraperConveyor'] = 'SGZ1200/3×1000'
            predict_json['loaderDevice'] = 'SZZ1350/700'
            predict_json['crusherDevice'] = 'PLM4500'
        elif 6.8 < thicknessAvg < 8.8 and obliqueLength == 300 and 800 < outputByYear < 1200:
            predict_json['shearerDevice'] = 'MG1100/2985-WD'
            predict_json['scraperConveyor'] = 'SGZ1400/3×1600'
            predict_json['backScraperConveyor'] = 'SGZ1400/3×1600'
            predict_json['loaderDevice'] = 'SZZ1350/700'
            predict_json['crusherDevice'] = 'PLM4500'
        if raw_x['煤田片区'] in ['大同地区', '薛家湾地区', '准格尔地区'] and raw_x['采煤工艺'] == '放顶煤':
            zhushu = '四柱'
        else:
            zhushu = '两柱'
        if zhushu == '两柱':
            valid_values = [3200, 8800, 15000, 21000, 29000]
            center_distances = [1250, 1500, 1750, 2050, 2400]
            # 判断工作阻力是否在 valid_values 中
            if predict_json['workingResistance'] not in valid_values:
                # 如果不在，找到与工作阻力值最接近的一个值
                workingResistance = min(valid_values, key=lambda x: abs(x - predict_json['workingResistance']))
                index = valid_values.index(workingResistance)
                predict_json['hydraulicSupportCenterDistance'] = center_distances[index]
        else:
            valid_values = [3600, 13000, 25000]
            center_distances = [1250, 1500, 1750]
            # 判断工作阻力是否在 valid_values 中
            if predict_json['workingResistance'] not in valid_values:
                workingResistance = min(valid_values, key=lambda x: abs(x - predict_json['workingResistance']))
                index = valid_values.index(workingResistance)
                predict_json['hydraulicSupportCenterDistance'] = center_distances[index]

        # todo [ rule 4 采煤方式 ] : 采煤方式为一次采全高时, 不存在后部刮板机、拉后溜千斤顶、尾梁千斤顶、插板千斤顶
        if (raw_x['采煤工艺'] == '一次采全高'):
            predict_json['backScraperConveyor'] = -2
            predict_json['rearFlowPullJackSpecification'] = -2
            predict_json['tailBeamJackSpecification'] = -2
            predict_json['insertPlateJackSpecification'] = -2
        # todo [ rule 4 基本架型号 ]
        print(f"predict_json['baisc'] : [{predict_json['basic']}]")
        first_part = predict_json['basic'].split('/')[0]
        # todo [ rule 4 基本架型号 ] : 没有液压支架后立柱、后立柱数量，没有尾梁千斤顶、插板千斤顶和拉后溜千斤顶和，没有后部刮板机。
        if (first_part == 'ZY'):
            predict_json['hydraulicSupportRearColumnSpecification'] = -2
            predict_json['tailBeamJackSpecification'] = -2
            predict_json['insertPlateJackSpecification'] = -2
            predict_json['rearFlowPullJackSpecification'] = -2
            predict_json['backScraperConveyor'] = -2
        # todo [ rule 4 基本架型号 ] : 没有尾梁千斤顶、插板千斤顶和拉后溜千斤顶
        elif (first_part == 'ZZ'):
            predict_json['tailBeamJackSpecification'] = -2
            predict_json['insertPlateJackSpecification'] = -2
            predict_json['rearFlowPullJackSpecification'] = -2
        # todo [ rule 4 基本架型号 ] : 没有"液压支架中心距": "hydraulicSupportCenterDistance",
        elif (first_part == 'ZFY'):
            predict_json['hydraulicSupportRearColumnSpecification'] = -2
        # todo [ rule 4 基本架型号 ] : 不是ZY和ZFY的支架, 没有"平衡千斤顶规格": "balanceJackSpecification"
        if (not first_part.startswith('ZY') and not first_part.startswith('ZFY')):
            predict_json['balanceJackSpecification'] = -2
        return predict_json

    def serialize(self,predict_json:dict) -> dict :
        for key,value in predict_json.items():
            predict_json[key] = str(value)
        return predict_json

    def predict_post_process(self, predict_json: dict, raw_x: dict) -> dict:
        # 1. predict zh -> en
        # 2. compute pre assign
        # 3. 甲方 预定义 规则
        # 4.
        predict_en_json = self.predict_zh2en(predict_json)
        predict_en_json = self.compute_pre_assign(predict_en_json)
        predict_en_json = self.compute(predict_en_json, raw_x)
        return self.serialize(predict_en_json)
