from types import SimpleNamespace


# -- input / x
# 保持和数据集中的column相同. 只保留用于cls和reg的
# 在训练config中保持en_key-zh_key的原因是 防止出现字段不对应的情况
# 我们只使用 中文 key
input : SimpleNamespace = SimpleNamespace()
input.input_en2zh = {
    # ---
    # xgb - cls
    "mineArea": "煤田片区",
    "miningMethod": "采煤工艺",
    "roofCondition": "顶板条件",
    "chassisBase": "底板条件",
    # ---

    # ---
    # xgb - reg
    "longitude": "经度",
    "latitude": "纬度",
    "obliqueLength": "工作面长度",
    "yield": "工作面年产量",
    "thicknessMin": "煤层厚度-最小",
    "thicknessMax": "煤层厚度-最大",
    "thicknessAvg": "煤层厚度-平均",
    "depthMin": "煤层埋深-最小",
    "depthMax": "煤层埋深-最大",
    "depthAvg": "煤层埋深-平均",
    "hardnessMin": "煤层硬度-最小",
    "hardnessMax": "煤层硬度-最大",
    "hardnessAvg": "煤层硬度-平均",
    # "roadwayType": "巷道类型", （预测时发挥作用）
    "rectangleLength": "机巷断面-高",  # 矩形 巷道尺寸高
    "rectangleWidth": "机巷断面-宽",  # 矩形 巷道尺寸宽
    "archLength": "风巷断面-高",  # 拱形 巷道尺寸高
    "archWidth": "风巷断面-宽",  # 拱形 巷道尺寸宽
    "dipAngle": "煤层倾角",
}
# 输入 分类 字符型取值范围
input.input_zh_cls_range = {
    "煤田片区": ['七台河矿区', '万利矿区', '乌海矿区', '乡宁矿区', '五九矿区', '五彩湾矿区', '五间房矿区', '伊敏矿区', '克布尔碱矿区', '六枝黑塘矿区', '准格尔矿区', '双鸭山矿区', '和什托洛盖矿区', '大同矿区', '平朔矿区', '平顶山矿区', '开滦矿区', '彬长矿区', '恩洪矿区', '扎赉诺尔矿区', '拜城矿区', '新街矿区', '昌吉白杨河矿区', '昭苏矿区', '昭通矿区', '晋城矿区', '普兴矿区', '榆横矿区', '榆神矿区', '水城矿区', '永夏矿区', '永陇矿区', '汾西矿区', '河保偏矿区', '济宁矿区', '淮北矿区', '淮南矿区', '潞安矿区', '澄合矿区', '灵武矿区', '盘江矿区', '神东矿区东胜区', '神东矿区神府区', '离柳矿区', '红沙岗矿区', '织纳矿区', '绍根矿区', '老厂矿区', '西山矿区', '轩岗矿区', '邯郸矿区', '铜川矿区', '镇雄矿区', '阜康矿区', '阳泉矿区', '阿艾矿区', '霍东矿区', '霍州矿区', '韩城矿区', '马家滩矿区', '鱼卡矿区', '鸡西矿区', '黄陵矿区', '黔北矿区'],
    "采煤工艺": ['一次采全高', '放顶煤'],
    "顶板条件": ['破碎、不稳定', '稳定、不易破碎', '中等稳定'],
    "底板条件": ['破碎、不稳定',  '软多底板', '一般底板', '中等稳定', '稳定、不易破碎'],
}
# 输入 回归 xgb数值取值范围
input.input_zh_reg_minmax = {
    "经度": [0, 132.0577],
    "纬度": [0, 56.664824],
    "工作面长度": [0, 6000],
    "工作面年产量": [0, 1200],
    "煤层厚度-最小": [0, 90.0],
    "煤层厚度-最大": [0, 140.0],
    "煤层厚度-平均": [0, 100.0],
    "煤层埋深-最小": [0, 1567],
    "煤层埋深-最大": [0, 1669],
    "煤层埋深-平均": [0, 1618],
    "煤层硬度-最小": [0, 22.0],
    "煤层硬度-最大": [0, 25.0],
    "煤层硬度-平均": [0, 23.0],
    "机巷断面-高": [0, 3800.0],
    "机巷断面-宽": [0, 6000.0],
    "风巷断面-高": [0, 3800.0],
    "风巷断面-宽": [0, 6000.0],
    "煤层倾角": [0, 85]
}
# 输入 中文keys
input.input_zh_keys = list(input.input_en2zh.values())
# 输入 分类参数 中文keys
input.input_zh_cls_keys = list(input.input_zh_cls_range.keys())
input.input_zh_cls_minmax = {key: list(range(len(val))) for key,val in input.input_zh_cls_range.items()}
input.input_zh_reg_keys = list(input.input_zh_reg_minmax.keys())


# -- output / predict / y
'''
预测参数: 数值型和字符型
    初始化:  将字符型索引为index数值, 
    训练时:  
            字符型参数 XGBClassifier, 在predict_zh_range规定的几个class中拟合
            数值型参数 XGBRegressor, 直接拟合
    预测时: 
            字符型分类数值 用index取predict_zh_range中的支护参数
            数值型回归数值 在列表中biscet_left到列表的数值中(升序,注意向上取值和向下取值的逻辑)
'''
predict = SimpleNamespace()
predict.predict_zh2en = {

    # "基本架型号": "basic",
    "过渡架型号": "transition",
    "端头架型号": "end",
    "机巷超前支架型号": "advanceFrameOfMachineLane",
    "风巷超前支架型号": "advanceFrameOfAirTunnel",
    # "采煤机型号": "shearerDevice",

    # "前刮板机型号": "scraperConveyor",
    # "后刮板机型号": "backScraperConveyor",
    # "破碎机型号": "crusherDevice",
    # "转载机型号": "loaderDevice",
    # "乳化泵型号": "emulsionPump",
    "基本架工作阻力": "workingResistance",
    "卸载压力": "unloadPressure",
    "泵站压力": "pumpPressure",
    "初撑力": "initialBracingForce",
    "平均支护强度-最大值": "supportStrengthOfBasicFrameMax",
    "平均支护强度-最小值": "supportStrengthOfBasicFrameMin",
    "平均对底板比压-最大值": "pressureOnBottomPlateAvg",
    # "平均对底板比压-最大值": "avgPressureOnBottomPlateMax",
    # "平均对底板比压-最小值": "avgPressureOnBottomPlateMin",
    "最大对底板比压": "pressureOnBottomPlateMax",
    "移架步距": "movingDistance",
    # "操作方式": "operateMethod",
    "基本架重量": "singleWeight",
    # "液压支架中心距": "hydraulicSupportCenterDistance",
    "顶梁结构形式": "topBeamStructureForm",

    "底座推杆结构形式": "basePushRodStructureForm",
    "底座抬底结构形式": "baseLiftBottomStructure",
    # "底座底调结构形式": "baseBottomAdjustmentStructure",
    "液压支架前立柱规格": "hydraulicSupportFrontColumnSpecification",
    "液压支架后立柱规格": "hydraulicSupportRearColumnSpecification",
    "平衡千斤顶规格": "balanceJackSpecification",
    "推移千斤顶规格": "pushJackSpecification",
    "前梁千斤顶规格": "frontBeamJackSpecification",
    "尾梁千斤顶规格": "tailBeamJackSpecification",
    "伸缩梁千斤顶规格": "telescopicBeamJackSpecification",
    "一级护帮千斤顶规格": "firstLevelGuardJackSpecification",
    "二级护帮千斤顶规格": "secondLevelGuardJackSpecification",
    "三级护帮千斤顶规格": "thirdLevelGuardJackSpecification",
    "前梁侧推千斤顶规格": "frontBeamSidePushJackSpecification",
    "顶梁侧推千斤顶规格": "topBeamSidePushJackSpecification",
    "掩护梁侧推千斤顶规格": "protectionBeamSidePushJackSpecification",
    "抬底千斤顶规格": "bottomLiftJackSpecification",
    "底调千斤顶规格": "bottomAdjustmentJackSpecification",
    "拉后溜千斤顶规格": "rearFlowPullJackSpecification",
    "插板千斤顶规格": "insertPlateJackSpecification",
    "尾梁侧推千斤顶规格": "tailBeamSidePushJackSpecification",
    "架间多通块规格": "interFrameMultiPassBlockSpecification",
    "立柱控制阀流量": "pillarControlValveFlow",
    "立柱安全阀1流量": "pillarSafetyValveOneFlow",
    "立柱安全阀2流量": "pillarSafetyValveTwoFlow",
    "平衡安全阀流量": "balanceSafetyValveFlow",
    "推移安全阀流量": "pushSafetyValveFlow",
    "推移液控单向锁流量": "pushHydraulicControlOneWayLockFlow",
    "其余单向锁流量": "otherOneWayLockFlow",
    "四连杆结构" :   "fourLinkStructure"

}
predict.predict_zh_range = {
    "过渡架型号": ['ZCG12000/22/40D', 'ZCG5000/9.5/18D', 'ZFG10000/19/32', 'ZFG10000/19/32D', 'ZFG10000/22/36H', 'ZFG10000/23/38', 'ZFG10000/23/42', 'ZFG10000/24/45D', 'ZFG12000/25/42D', 'ZFG13000/21/36D', 'ZFG13000/23/37D', 'ZFG13000/23/42', 'ZFG13000/23/42D', 'ZFG13000/24/36D', 'ZFG13000/24/40D', 'ZFG13000/25/38', 'ZFG13000/25/42D', 'ZFG13000/26/40', 'ZFG13000/26/40D', 'ZFG15000/28/45', 'ZFG17000/29/42D', 'ZFG18000/26/42D', 'ZFG18000/27/40', 'ZFG18000/29/45', 'ZFG21000/26/42D', 'ZFG21000/29/42', 'ZFG21000/30/45', 'ZFG22000/30/50D', 'ZFG22000/31/52D', 'ZFG24000/27/40D', 'ZFG3200/18/28', 'ZFG5200/18/28', 'ZFG6000/22/35', 'ZFG6400/18/35D', 'ZFG6400/20.5/33', 'ZFG6500/19/32', 'ZFG6500/19/32D', 'ZFG6800/19/32', 'ZFG6800/20/32', 'ZFG7000/18/30', 'ZFG7200/20/35D', 'ZFG7200/22/32', 'ZFG7600/18/31D', 'ZFG8000/17/32', 'ZFG8000/19/35', 'ZFG8000/19/35D', 'ZFG8000/20/34D', 'ZFG8000/20/35', 'ZFG8000/22/35', 'ZFG8000/22/35D', 'ZFG8000/22/38', 'ZFG9000/22/35', 'ZFG9600/20/32D', 'ZFG9600/23/42', 'ZFG9600/25/47', 'ZFP13800/29/45D', 'ZFYG21000/26/42D', 'ZY15000/27/57D', 'ZY5200/12/28', 'ZY6400/17/38', 'ZY7200/15/37D', 'ZY8000/12/25D', 'ZY9000/26/55', 'ZYA12000/16/40D', 'ZYG10000/17/35', 'ZYG10000/22/45', 'ZYG10000/24/50', 'ZYG10000/26/55', 'ZYG10000/28/62', 'ZYG11000/26/55D', 'ZYG12000/13/25D', 'ZYG12000/13/26D', 'ZYG12000/15/28', 'ZYG12000/16/32D', 'ZYG12000/17/35D', 'ZYG12000/18/35', 'ZYG12000/18/37', 'ZYG12000/18/37D', 'ZYG12000/25/50', 'ZYG12000/25/50D', 'ZYG12000/26/55', 'ZYG12000/26/55D', 'ZYG12000/26/56', 'ZYG12000/28/62D', 'ZYG12000/30/68D', 'ZYG13000/15/38D', 'ZYG13000/22/45', 'ZYG13000/28/60D', 'ZYG13000/29/63D', 'ZYG13000/30/65', 'ZYG15000/21/36D', 'ZYG15000/29.5/63', 'ZYG15000/30/65', 'ZYG15900/19/39', 'ZYG16000/19/35', 'ZYG18000/34/73D', 'ZYG19000/28/53D', 'ZYG21000/28/55', 'ZYG21000/29/58DA', 'ZYG21000/30/63', 'ZYG21000/33.5/70', 'ZYG21000/35/74', 'ZYG21000/36.5/80', 'ZYG21000/38/83D', 'ZYG26000/32/60D', 'ZYG26000/32/60DA', 'ZYG3200/10/24', 'ZYG3400/08/20', 'ZYG3400/14/32', 'ZYG3800/20/38D', 'ZYG4000/09/21', 'ZYG4000/10/24', 'ZYG4000/12/28', 'ZYG4000/14/32D', 'ZYG4000/15/32', 'ZYG5200/08/18', 'ZYG5200/09/19D', 'ZYG5200/10/24', 'ZYG5200/10/24D', 'ZYG5200/11/26', 'ZYG5200/12/28', 'ZYG5200/13/30', 'ZYG5200/14/32', 'ZYG5200/14/32D', 'ZYG5200/15/35', 'ZYG5200/17/38', 'ZYG5200/18/40D', 'ZYG6000/15/35', 'ZYG6000/15/35D', 'ZYG6000/17/38', 'ZYG6000/19/43', 'ZYG6800/11/22D', 'ZYG6800/12/25D', 'ZYG6800/13/28', 'ZYG6800/20/42', 'ZYG6800/21/45', 'ZYG6800/24/50', 'ZYG7200/11/22', 'ZYG7200/13/28', 'ZYG7200/14/32', 'ZYG7200/14/32D', 'ZYG7200/17/35D', 'ZYG7200/17/38', 'ZYG7200/18/38', 'ZYG7200/18/38D', 'ZYG7200/18/40D', 'ZYG8000/13/28D', 'ZYG8000/14/30', 'ZYG8000/18/40', 'ZYG8000/20/40D', 'ZYG8000/20/42', 'ZYG8000/24/50', 'ZYG8200/09/16D', 'ZYG9000/13/28', 'ZYG9000/20/40D', 'ZYG9000/22/45', 'ZYG9000/24/50', 'ZYG9000/26/55', 'ZZG10000/24/50', 'ZZG13000/24/50', 'ZZG13000/24/52D', 'ZZG16000/25/50', 'ZZG6500/21/47', 'ZZG7200/17/35', 'ZZG7200/19/40D', 'ZZG8000/20/42D', 'ZZG8000/22/48D'],
    "端头架型号": ['ZCT12000/22/40D', 'ZFP21000/26/41D', 'ZFT20000/25/40', 'ZFT27200/24/40D', 'ZFT32500/25/45D', 'ZFT42000/21/36D', 'ZFT42000/24/36D', 'ZFT42000/27/42D', 'ZQL2X6750/27/52D', 'ZT10000/18/35', 'ZT10000/22/45', 'ZT10000/25/40', 'ZT11000/25/50D', 'ZT12000/30/68D', 'ZT12800/18/35', 'ZT12800/25/40', 'ZT13600/19/38', 'ZT14400/16/30', 'ZT14400/18/35', 'ZT14400/18/40D', 'ZT14400/20/40', 'ZT14400/20/40D', 'ZT14400/22/45', 'ZT14400/22/45D', 'ZT14400/25/40', 'ZT14400/25/50', 'ZT14400/25/50D', 'ZT14400/28/45D', 'ZT15000/18/35', 'ZT15000/22/35', 'ZT15000/23/42D', 'ZT15000/27/55', 'ZT18400/24/45', 'ZT19200/18/35', 'ZT19200/18/35D', 'ZT19200/20/40D', 'ZT19200/22/35', 'ZT19200/22/45', 'ZT19200/25/50', 'ZT20000/18/35', 'ZT20000/20/40', 'ZT20000/22/35D', 'ZT20000/22/45', 'ZT20000/25/40', 'ZT20000/25/50', 'ZT2200/25/40D', 'ZT24000/26/42', 'ZT25000/22/45D', 'ZT25600/22/45', 'ZT25600/25/40', 'ZT25600/25/50', 'ZT25600/27/40D', 'ZT27000/29/45D', 'ZT3000/20/35D', 'ZT30000/25/42D', 'ZT36000/26/40', 'ZT36000/26/40D', 'ZT38000/26/40', 'ZT45600/25/40', 'ZT6400/16/30', 'ZT7200/22/40', 'ZT7600/24/38', 'ZT9600/16/30', 'ZT9600/18/35', 'ZT9600/18/35D', 'ZT9600/20/40', 'ZT9600/22/35', 'ZT9600/22/45', 'ZTCY10000/20/34D', 'ZTHQ8400/15/28D', 'ZTZ15000/20/38D', 'ZTZ15000/29/63D', 'ZTZ16000/19/35D', 'ZTZ16000/19/36D', 'ZTZ25000/23/42D', 'ZTZ30000/25/50D', 'ZTZ32960/26/40D', 'ZTZ6800/28/55D', 'ZY13000/28/60D', 'ZY19000/24/42D', 'ZY21000/28/53D', 'ZY4000/12/24', 'ZY5600/14/32D', 'ZY9000/17/35D', 'ZYP12000/19/40D', 'ZYP12000/21/42D', 'ZYT10000/17/35', 'ZYT10000/24/50', 'ZYT12000/14/28D', 'ZYT12000/15/28', 'ZYT12000/15/38D', 'ZYT12000/16/32D', 'ZYT12000/18/35', 'ZYT12000/18/37', 'ZYT12000/22/49', 'ZYT12000/25/45', 'ZYT12000/26/55', 'ZYT12000/26/55D', 'ZYT13000/15/38D', 'ZYT13000/26/55', 'ZYT13000/28/60D', 'ZYT15000/22/40D', 'ZYT15000/23/45', 'ZYT15000/29.5/58D', 'ZYT15900/19/39', 'ZYT16000/19/35', 'ZYT18000/28/55', 'ZYT18000/30/55D', 'ZYT21000/28/55', 'ZYT21000/30/55D', 'ZYT26000/32/50D', 'ZYT3800/20/38D', 'ZYT4000/13/28D', 'ZYT4000/14/32', 'ZYT5200/14/32', 'ZYT5200/14/32D', 'ZYT6000/19/43', 'ZYT6800/13/28', 'ZYT6800/15/32D', 'ZYT7200/13/28', 'ZYT7200/17/35', 'ZYT7200/18/38', 'ZYT8000/19/42', 'ZYT8000/20/42', 'ZYT8500/13/30.5D', 'ZYT9000/15/32D', 'ZYT9000/18/38', 'ZZT7200/18/38', 'ZZT7200/19/40D'],
    "机巷超前支架型号": ['ZC10000/18/35D', 'ZCG12000/22/40D', 'ZZ13000/25/42D', 'ZZ14000/26/42D'],
    "风巷超前支架型号": ['2×ZQ4000/20/42', '2×ZQL2×6500/20/35D', 'ZCZH10000/31/55D', 'ZHL2×3600/22/32', 'ZLH2×4800/30/45D', 'ZQ22500/28/55D', 'ZQ4000/20.6/45', 'ZQ6400/16/32D', 'ZQ9600/22/45D', 'ZQL2X6750/27/52D', 'ZQL2×3200/16/30', 'ZQL2×3200/18/35', 'ZQL2×3200/22/35D', 'ZQL2×3200/22/40D', 'ZQL2×3200/25/40', 'ZQL2×32960/26/40D', 'ZQL2×3600/29/50D', 'ZQL2×4000/18/35D', 'ZQL2×4000/19/36D', 'ZQL2×4000/26/45D', 'ZQL2×4600/24/45', 'ZQL2×4800/16/30', 'ZQL2×4800/18/35', 'ZQL2×4800/18/35D', 'ZQL2×4800/20/40', 'ZQL2×4800/20/40D', 'ZQL2×4800/22/45', 'ZQL2×4800/22/45D', 'ZQL2×4800/25/40', 'ZQL2×4800/25/45', 'ZQL2×4800/25/50', 'ZQL2×4800/25/50D', 'ZQL2×4800/27/55', 'ZQL2×4800/28/45D', 'ZQL2×5000/18/35', 'ZQL2×5000/20/40', 'ZQL2×5000/20/40D', 'ZQL2×5000/21/36D', 'ZQL2×5000/22/45', 'ZQL2×5000/23/42', 'ZQL2×5000/25/40', 'ZQL2×5000/27/55', 'ZQL2×6000/25/50D', 'ZQL2×6400/19/35', 'ZQL2×6400/23/45', 'ZQL2×6400/24/48', 'ZQL2×6400/25/50', 'ZQL2×6400/26/40', 'ZQL2×6500/25/45D', 'ZQL2×6500/25/47D', 'ZQL2×6500/25/50D', 'ZTC12500/25/45D', 'ZTCH20000/27/50D', 'ZTYC1600/15/29D'],
    # "乳化泵型号": [-2],
    "基本架工作阻力": [3200, 3400, 3800, 4000, 4200, 4400, 4600, 4800, 5000, 5200, 5300, 5600, 6000, 6400, 6500, 6800, 7000, 7200, 7600, 8000, 8200, 8500, 8600, 8800, 9000, 9200, 10000, 10800, 11000, 12000, 13000, 13600, 15000, 16000, 17000, 18000, 19000, 20000, 21000, 28000],
    "卸载压力": [12.6, 33.4, 33.6, 33.7, 34.6, 34.8, 35.0, 35.3, 36.5, 36.6, 36.7, 36.8, 36.9, 37.3, 37.4, 37.5, 37.7, 38.2, 38.5, 38.7, 38.8, 39.1, 39.3, 39.6, 39.7, 39.8, 40.1, 40.4, 40.6, 40.7, 40.9, 41.0, 41.3, 41.4, 42.2, 42.3, 42.5, 42.6, 42.8, 43.0, 43.1, 43.3, 43.5, 43.7, 43.8, 44.1, 44.2, 44.5, 44.7, 44.8, 45.0, 45.2, 45.8, 46.0, 46.2, 46.3, 46.9, 47.2, 47.4, 47.6, 47.7, 47.75, 47.8, 49.1, 469.0],
    "泵站压力": [31.5, 35.0, 37.5],
    "初撑力": [989, 2532, 2616, 2626, 3092, 3204, 3876, 3877, 3878, 3880, 3940, 3956, 3958, 4450, 5064, 5066, 5147, 5232, 5234, 5298, 5300, 5717, 5886, 5888, 5890, 6026, 6028, 6030, 6032, 6168, 6182, 6184, 6185, 6409, 6412, 6413, 7010, 7141, 7144, 7145, 7258, 7630, 7660, 7758, 7759, 7760, 7912, 7913, 7916, 8312, 8724, 8728, 8796, 8867, 8901, 8944, 10014, 10015, 10020, 10120, 10128, 10132, 10492, 11254, 11762, 11773, 11780, 11922, 11928, 12370, 12819, 12820, 13572, 13899, 14283, 14322, 14328, 15270, 15435, 15825, 15832, 16544, 16546, 17003, 17058, 17721, 23367, 58866],
    "平均支护强度-最大值": [0.43, 0.45, 0.5, 0.52, 0.53, 0.55, 0.56, 0.6, 0.61, 0.62, 0.63, 0.65, 0.66, 0.68, 0.69, 0.7, 0.71, 0.72, 0.74, 0.75, 0.76, 0.78, 0.8, 0.82, 0.83, 0.85, 0.87, 0.88, 0.89, 0.9, 0.92, 0.93, 0.94, 0.95, 0.96, 0.98, 0.99, 1.0, 1.02, 1.03, 1.05, 1.06, 1.07, 1.08, 1.09, 1.1, 1.11, 1.12, 1.13, 1.14, 1.15, 1.16, 1.17, 1.18, 1.2, 1.22, 1.23, 1.24, 1.25, 1.26, 1.27, 1.28, 1.29, 1.3, 1.32, 1.34, 1.37, 1.39, 1.4, 1.45, 1.46, 1.48, 1.49, 1.52, 1.55, 1.56, 1.59, 1.6, 1.64, 1.68, 1.71, 1.72, 1.74, 1.77, 1.78, 1.85, 1.87, 1.9, 1.99, 11.03],
    "平均支护强度-最小值": [0.35, 0.36, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.5, 0.52, 0.53, 0.54, 0.55, 0.58, 0.6, 0.61, 0.62, 0.64, 0.65, 0.66, 0.68, 0.7, 0.72, 0.73, 0.75, 0.76, 0.77, 0.78, 0.8, 0.83, 0.84, 0.85, 0.87, 0.89, 0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 1.0, 1.01, 1.02, 1.03, 1.04, 1.05, 1.06, 1.07, 1.1, 1.11, 1.12, 1.13, 1.14, 1.15, 1.16, 1.17, 1.18, 1.19, 1.2, 1.21, 1.22, 1.24, 1.26, 1.29, 1.3, 1.32, 1.35, 1.36, 1.37, 1.4, 1.43, 1.45, 1.46, 1.48, 1.5, 1.6, 1.63, 1.65, 1.66, 1.67, 1.68, 1.69, 1.71, 1.75, 1.8, 1.83],
    "平均对底板比压-最大值": [1.15, 1.28, 1.4, 1.49, 1.5, 1.51, 1.55, 1.6, 1.64, 1.7, 1.87, 1.89, 1.9, 1.93, 1.95, 1.96, 2.1, 2.15, 2.17, 2.2, 2.26, 2.3, 2.35, 2.4, 2.42, 2.45, 2.5, 2.56, 2.58, 2.59, 2.6, 2.62, 2.65, 2.68, 2.7, 2.78, 2.8, 2.86, 2.9, 2.94, 2.98, 3.0, 3.1, 3.2, 3.21, 3.3, 3.33, 3.4, 3.45, 3.5, 3.6, 3.7, 3.8, 3.85, 3.9, 4.0, 4.2, 4.4, 4.48, 4.5, 4.9, 5.0, 5.5, 5.6, 5.68, 23.7, 385.0],
    # "平均对底板比压-最小值": [0.8, 1.2, 1.29, 1.3, 1.35, 1.38, 1.4, 1.5, 1.55, 1.56, 1.6, 1.7, 1.78, 1.8, 1.9, 1.95, 1.96, 2.0, 2.04, 2.08, 2.1, 2.11, 2.18, 2.2, 2.21, 2.25, 2.26, 2.3, 2.32, 2.4, 2.49, 2.5, 2.58, 2.6, 2.63, 2.68, 2.7, 2.8, 2.88, 2.9, 2.93, 3.0, 3.08, 3.1, 3.14, 3.17, 3.2, 3.29, 3.3, 3.32, 3.4, 3.5, 3.6, 3.9, 3.92, 4.0, 4.02, 4.1, 5.14, 22.0],
    "最大对底板比压": [1.3, 1.4, 1.5, 1.7, 1.8, 1.95, 2.0, 2.2, 2.26, 2.3, 2.4, 2.42, 2.5, 2.58, 2.7, 2.8, 2.86, 2.9, 2.94, 3.0, 3.1, 3.2, 3.21, 3.3, 3.4, 3.5, 3.6, 3.7, 3.77, 3.8, 3.85, 3.9, 3.96, 4.0, 4.1, 4.2, 4.3, 4.34, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0, 5.2, 5.3, 5.5, 5.68, 5.7, 5.8, 5.83, 5.96, 6.0, 6.2, 6.8, 7.2, 8.0, 35.0],
    "移架步距": [630, 700, 800, 865, 1000, 1100],
    "基本架重量": [2.0, 9.0, 9.5, 10.0, 10.2, 10.5, 10.8, 11.0, 11.1, 11.2, 11.4, 11.5, 11.6, 11.7, 11.9, 12.0, 12.2, 12.5, 12.7, 12.8, 13.0, 13.2, 13.3, 13.5, 13.8, 14.0, 14.3, 14.5, 14.7, 14.8, 15.0, 15.2, 15.4, 15.5, 15.6, 15.7, 15.8, 16.0, 16.2, 16.5, 16.6, 16.7, 17.0, 17.2, 17.4, 17.5, 17.6, 17.8, 18.0, 18.2, 18.3, 18.5, 18.7, 18.8, 19.0, 19.2, 19.3, 19.5, 19.6, 19.7, 20.0, 20.5, 20.8, 21.0, 21.5, 21.6, 21.8, 22.0, 22.2, 22.3, 22.5, 23.0, 23.5, 23.8, 24.0, 24.5, 24.8, 25.0, 25.2, 25.4, 25.5, 26.0, 26.2, 26.3, 26.5, 26.6, 26.8, 27.0, 27.3, 27.5, 27.6, 27.8, 28.0, 28.5, 29.0, 29.5, 30.0, 30.5, 30.9, 31.0, 31.5, 32.0, 32.5, 32.8, 33.0, 33.32, 33.5, 33.8, 34.0, 34.5, 35.0, 35.2, 35.5, 35.7, 36.5, 36.6, 37.0, 37.5, 38.0, 38.5, 39.0, 39.5, 39.8, 40.0, 40.5, 40.7, 41.0, 41.5, 42.0, 42.5, 43.0, 43.5, 43.6, 43.7, 45.0, 45.5, 46.0, 46.3, 46.5, 47.0, 47.3, 47.5, 48.0, 49.0, 50.0, 50.4, 50.5, 52.0, 52.8, 53.0, 53.5, 54.0, 54.2, 55.0, 56.0, 60.0, 66.0, 67.0, 67.3, 68.5, 70.0, 70.5, 71.0, 74.5, 76.0, 77.0, 79.0, 80.0, 84.0, 89.8],
    "顶梁结构形式": ['整体顶梁', '铰接前梁'],
    "底座推杆结构形式": ['整体短推杆', '整体长推杆', '铰接推杆'],
    "底座抬底结构形式": ['卧式结构', '套筒结构', '顶架+滑靴结构'],
    "液压支架前立柱规格": [180, 200, 230, 250, 280, 300, 320, 340, 345, 360, 380, 400, 420, 450, 480, 500, 530, 600],
    "液压支架后立柱规格": [-2, 180, 200, 230, 250, 280, 300, 320, 345, 360, 380, 400],
    "平衡千斤顶规格": [-2, 125, 140, 160, 180, 200, 230, 250, 280, 320],
    "推移千斤顶规格": [-2, 125, 140, 160, 180, 200, 230, 250],
    "前梁千斤顶规格": [-2, 140, 160, 180, 200],
    "尾梁千斤顶规格": [-2, 140, 160, 180, 200],
    "伸缩梁千斤顶规格": [-2, 80, 100, 125, 140],
    "一级护帮千斤顶规格": [-2, 80, 100, 125, 140, 160],
    "二级护帮千斤顶规格": [-2, 63, 80, 100, 125],
    "三级护帮千斤顶规格": [-2, 80],
    "前梁侧推千斤顶规格": [-2, 63],
    "顶梁侧推千斤顶规格": [63, 80, 100, 125],
    "掩护梁侧推千斤顶规格": [63, 80, 100, 125],
    "抬底千斤顶规格": [-2, 100, 110, 125, 129, 140, 160, 168, 180, 200, 230],
    "底调千斤顶规格": [-2, 10, 40, 80, 90, 100, 125, 129, 140, 160, 180, 200, 230],
    "拉后溜千斤顶规格": [-2, 100, 125, 140],
    "插板千斤顶规格": [-2, 63, 80, 100, 125],
    "尾梁侧推千斤顶规格": [-2, 60, 63, 80],
    "架间多通块规格": ['DN25/DN32/DN20', 'DN25/DN32/DN25', 'DN32G/DN38/DN25', 'DN38G/DN51/DN25', 'DN38G/DN51/DN32', 'DN40G/DN50/DN25', 'DN40G/DN50/DN32', 'DN50G/DN50/DN32', 'DN50G/DN65/DN32', 'DN51G/DN51/DN25', 'DN51G/DN65/DN32'],
    "立柱控制阀流量": [200, 400, 480, 500, 630, 800, 1000],
    "立柱安全阀1流量": [125, 250, 500, 1000, 4000],
    "立柱安全阀2流量": [125, 250, 500],
    "平衡安全阀流量": [125, 250, 500],
    "推移安全阀流量": [125, 250, 480, 500],
    "推移液控单向锁流量": [200, 400, 480, 500],
    "其余单向锁流量": [125, 200],
    "四连杆结构":["前双后双","前单后双"]
}
predict.predict_cls_keys = [
    "过渡架型号",
    "端头架型号",
    "机巷超前支架型号",
    "风巷超前支架型号",
    "顶梁结构形式",
    "底座推杆结构形式",
    "底座抬底结构形式",
    "架间多通块规格",
    "四连杆结构"
]
predict.predict_reg_keys = [
    # "乳化泵型号",
    "基本架工作阻力",
    "卸载压力",
    "泵站压力",
    "初撑力",
    "平均支护强度-最大值",
    "平均支护强度-最小值",
    "平均对底板比压-最大值",
    # "平均对底板比压-最小值",
    "最大对底板比压",
    "移架步距",
    "基本架重量",
    "液压支架前立柱规格",
    "液压支架后立柱规格",
    "平衡千斤顶规格",
    "推移千斤顶规格",
    "前梁千斤顶规格",
    "尾梁千斤顶规格",
    "伸缩梁千斤顶规格",
    "一级护帮千斤顶规格",
    "二级护帮千斤顶规格",
    "三级护帮千斤顶规格",
    "前梁侧推千斤顶规格",
    "顶梁侧推千斤顶规格",
    "掩护梁侧推千斤顶规格",
    "抬底千斤顶规格",
    "底调千斤顶规格",
    "拉后溜千斤顶规格",
    "插板千斤顶规格",
    "尾梁侧推千斤顶规格",
    "立柱控制阀流量",
    "立柱安全阀1流量",
    "立柱安全阀2流量",
    "平衡安全阀流量",
    "推移安全阀流量",
    "推移液控单向锁流量",
    "其余单向锁流量"
]
# 中文转换可以配置到PredictPostProcessor中
predict.predict_zh_keys = list(predict.predict_zh2en.keys())


