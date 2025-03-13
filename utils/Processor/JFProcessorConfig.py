'''
处理前端输入
    1. filter : 甲方输入 过滤为 乙方输入 （涉及硬编码）
    2. en2zh : 甲方en 2 乙方数据集zh
    3. reserve : 保留 甲方输入必须字段, 准备预测后的back_process
    note: dict 便于理解英文意思和编码
'''

# 1
filter_jf2yf = {
    "convert":{ # 转换
        "roadWayType":["archLength","archWidth","rectangleLength","rectangleWidth"],
        "depth":["depthMin","depthMax","depthAvg"],
        "hardness":["hardnessMin","hardnessMax","hardnessAvg"]
    },
    "delete": # 删除
    [
        'depth','hardness',"roadwayType","selectionMethod"
         "mineName", # 煤矿名称去重仍保留80%，弃用该字段进行训练
        "superiorCompanyName"
    ],
    "parseFloat":{
        # reg
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
        "rectangleLength": "机巷断面-高",  # 矩形 巷道尺寸高
        "rectangleWidth": "机巷断面-宽",  # 矩形 巷道尺寸宽
        "archLength": "风巷断面-高",  # 拱形 巷道尺寸高
        "archWidth": "风巷断面-宽",  # 拱形 巷道尺寸宽
        "dipAngle": "煤层倾角",
        # --
        # 保留平均值的, 将最小最大设置为均值

        # --
    }
}

# 2
yf_input_en2zh = {
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

# 3
# search in zmjv3forsearch / search数据集和train数据集分开
# reserve_en2zh = {
#     "jf_input":{
#         "superiorCompanyName" : "上级公司",
#         "aroundLength":"周边长度"
#     },
#     "yf_input":{
#         "longitude": "经度",
#         "latitude": "纬度",
#         "obliqueLength": "工作面长度",
#         "yield": "工作面年产量",
#         "thicknessMin": "煤层厚度-最小",
#         "thicknessMax": "煤层厚度-最大",
#         "thicknessAvg": "煤层厚度-平均",
#         "depthMin": "煤层埋深-最小",
#         "depthMax": "煤层埋深-最大",
#         "depthAvg": "煤层埋深-平均",
#         "hardnessMin": "煤层硬度-最小",
#         "hardnessMax": "煤层硬度-最大",
#         "hardnessAvg": "煤层硬度-平均",
#         "rectangleLength": "机巷断面-高",  # 矩形 巷道尺寸高
#         "rectangleWidth": "机巷断面-宽",  # 矩形 巷道尺寸宽
#         "archLength": "风巷断面-高",  # 拱形 巷道尺寸高
#         "archWidth": "风巷断面-宽",  # 拱形 巷道尺寸宽
#         "dipAngle": "煤层倾角",
#     }
# }