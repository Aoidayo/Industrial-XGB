from types import SimpleNamespace
'''
处理乙方的输出
    1. predict zh2en
    2. compute en 预赋值
    3. compute 计算
'''


# -- predict en2zh
predict_zh2en = {

    # "基本架型号": "basic",
    "过渡架型号": "transition",
    "端头架型号": "end",
    "机巷超前支架型号": "advanceFrameOfMachineLane",
    "风巷超前支架型号": "advanceFrameOfAirTunnel",
    # "采煤机型号": "shearerDelengthvice",

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

# -- compute
# 解耦到 PredictPostProcessor
compute_zh2en = {
    "基本架型号": "basic",
    "采煤机型号": "shearerDevice",
    "前刮板机型号": "scraperConveyor",
    "后刮板机型号": "backScraperConveyor",
    "破碎机型号": "crusherDevice",
    "转载机型号": "loaderDevice",
    "乳化泵型号": "emulsionPump",
    "操作方式": "operateMethod",
    "液压支架中心距": "hydraulicSupportCenterDistance",
    "底座底调结构形式": "baseBottomAdjustmentStructure",
}