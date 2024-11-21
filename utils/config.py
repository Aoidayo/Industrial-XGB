# 测量参数
celiangcanshu = ["巷道用途", "巷道埋深", "直接顶岩性", "直接顶厚度", "老顶岩性", "老顶厚度", "断面形状", "巷道毛断面宽度", "巷道毛断面高度", "煤柱宽度", "煤层厚度"]
celiangcanshu_py = ["hangdaoyongtu", "hangdaomaishen", "zhijiedingyanxing", "zhijiedinghoudu", "laodingyanxing",
                    "laodinghoudu", "duanmianxingzhuang", "hangdaomaoduanmiankuandu", "hangdaomaoduanmiangaodu", "meizhukuandu", "meicenghoudu"]
celiangcanshu_range = {
    '巷道用途':     ['下山', '回采巷道', '回风大巷', '胶带大巷', '胶带运输巷', '石门', '轨道运输巷', '开切眼', '开拓巷道', '上山', '轨道大巷', '撤架巷道回风大巷', '撤架巷道'],
    '巷道埋深':     [],
    "直接顶岩性":   ['粗中砂岩', '砂质页岩', '粗砂岩', '中砾砂岩', '粗粒砂岩', '粗砾砂岩', '泥岩', '天然焦', '粉细砂', '砂页岩', '高岭岩', '砂岩', '砂质泥岩', '炭质泥', '砂砾岩', '岩浆岩', '中粒砂岩', '粘土岩', '细沙岩', '粉细砂岩', '灰色粉', '砾岩', '粉砂岩', '炭质泥岩', '中砂岩', '高岭质泥岩', '煌斑岩', '石灰岩', '细砂岩', '中细砂岩', '细中砂岩', '中细粒砂岩', '泥质砂岩', '细粒砂岩'],
    "直接顶厚度":    [],
    "老顶岩性":     ['粗中砂岩', '砂质页岩', '粗砂岩', '中砾砂岩', '粗粒砂岩', '粗砾砂岩', '泥岩', '天然焦', '粉细砂', '砂页岩', '高岭岩', '砂岩', '砂质泥岩', '炭质泥', '砂砾岩', '岩浆岩', '中粒砂岩', '粘土岩', '细沙岩', '粉细砂岩', '灰色粉', '砾岩', '粉砂岩', '炭质泥岩', '中砂岩', '高岭质泥岩', '煌斑岩', '石灰岩', '细砂岩', '中细砂岩', '细中砂岩', '中细粒砂岩', '泥质砂岩', '细粒砂岩'],
    "老顶厚度":     [],
    "断面形状":     ['直墙半圆拱形', '矩形', '三心拱断面', '梯形', '半圆拱形'],
    "巷道毛断面宽度": [],
    "巷道毛断面高度": [],
    "煤柱宽度":     [],
    "煤层厚度":     [],
}

# 预测参数 -zh
# yucecanshu_head = ["顶", "工作面帮", "煤柱帮"]
# yucecanshu_tail = ["锚杆类型", "锚杆杆体强度", "锚杆直径", "锚杆长度", "锚杆钻孔直径", "锚杆间距", "锚杆排距", "锚杆钢带类型", "锚杆钢带宽度", "锚杆钢带长度", "锚杆钢带厚度",
#                    "锚索类型", "锚索杆体强度", "锚索直径", "锚索长度", "锚索钻孔直径", "锚索间距", "锚索排距", "锚索钢带类型", "锚索钢带宽度", "锚索钢带长度", "锚索钢带厚度",
#                    "网类型",   "网铁丝直径"]
# yucecanshu_other = ["支护形式", "钢棚型号", "钢棚间距", "喷浆材料", "喷浆厚度"]
yucecanshu = ['支护形式',

              '顶锚杆类型', '顶锚杆杆体强度', '顶锚杆直径', '顶锚杆长度', '顶锚杆钻孔直径', '顶锚杆间距', '顶锚杆排距',
              '顶锚杆钢带类型', '顶锚杆钢带宽度', '顶锚杆钢带长度', '顶锚杆钢带厚度',
              '顶锚索类型', '顶锚索杆体强度', '顶锚索直径', '顶锚索长度', '顶锚索钻孔直径', '顶锚索间距', '顶锚索排距',
              '顶锚索钢带类型', '顶锚索钢带宽度', '顶锚索钢带长度', '顶锚索钢带厚度',
              '顶板网类型', '顶板网铁丝直径',

              '工作面帮锚杆类型', '工作面帮锚杆杆体强度', '工作面帮锚杆直径', '工作面帮锚杆长度', '工作面帮锚杆钻孔直径', '工作面帮锚杆间距', '工作面帮锚杆排距',
              '工作面帮锚杆钢带类型', '工作面帮锚杆钢带宽度', '工作面帮锚杆钢带长度', '工作面帮锚杆钢带厚度',
              '工作面帮锚索类型', '工作面帮锚索杆体强度', '工作面帮锚索直径', '工作面帮锚索长度', '工作面帮锚索钻孔直径', '工作面帮锚索间距', '工作面帮锚索排距',
              '工作面帮锚索钢带类型', '工作面帮锚索钢带宽度', '工作面帮锚索钢带长度', '工作面帮锚索钢带厚度',
              '工作面帮网类型', '工作面帮网铁丝直径',

              '煤柱帮锚杆类型', '煤柱帮锚杆杆体强度', '煤柱帮锚杆直径', '煤柱帮锚杆长度', '煤柱帮锚杆钻孔直径', '煤柱帮锚杆间距', '煤柱帮锚杆排距',
              '煤柱帮锚杆钢带类型', '煤柱帮锚杆钢带宽度', '煤柱帮锚杆钢带长度', '煤柱帮锚杆钢带厚度',
              '煤柱帮锚索类型', '煤柱帮锚索杆体强度', '煤柱帮锚索直径', '煤柱帮锚索长度', '煤柱帮锚索钻孔直径', '煤柱帮锚索间距', '煤柱帮锚索排距',
              '煤柱帮锚索钢带类型', '煤柱帮锚索钢带宽度', '煤柱帮锚索钢带长度', '煤柱帮锚索钢带厚度',
              '煤柱帮网类型', '煤柱帮网铁丝直径',

              '钢棚型号', '钢棚间距',
              '喷浆材料', '喷浆厚度']
# 预测参数 -py
# yucecanshu_head_py = ["ding", "gongzuomianbang", "meizhubang"]
# yucecanshu_tail_py = ["maoganleixing", "maogangantiqiangdu", "maoganzhijing", "maoganchangdu", "maoganzuankongzhijing", "maoganjianju", "maoganpaiju",
#                       "maogangangdaileixing", "maogangangdaikuandu", "maogangangdaichangdu", "maogangangdaihoudu",
#                       "maosuoleixing", "maosuogantiqiangdu", "maosuozhijing", "maosuochangdu", "maosuozuankongzhijing", "maosuojianju", "maosuopaiju",
#                       "maosuogangdaileixing", "maosuogangdaikuandu", "maosuogangdaichangdu", "maosuogangdaihoudu",
#                       "wangleixing", "wangtiesizhijing"]
# yucecanshu_other_py = ['zhihuxingshi', 'gangpengxinghao', 'gangpengjianju', 'penjiangcailiao', 'penjianghoudu']
yucecanshu_py = [ 'zhihuxingshi',

                  'dingmaoganleixing', 'dingmaogangantiqiangdu', 'dingmaoganzhijing', 'dingmaoganchangdu', 'dingmaoganzuankongzhijing', 'dingmaoganjianju', 'dingmaoganpaiju',
                  'dingmaogangangdaileixing', 'dingmaogangangdaikuandu', 'dingmaogangangdaichangdu', 'dingmaogangangdaihoudu',
                  'dingmaosuoleixing', 'dingmaosuogantiqiangdu', 'dingmaosuozhijing', 'dingmaosuochangdu', 'dingmaosuozuankongzhijing', 'dingmaosuojianju', 'dingmaosuopaiju',
                  'dingmaosuogangdaileixing', 'dingmaosuogangdaikuandu', 'dingmaosuogangdaichangdu', 'dingmaosuogangdaihoudu',
                  'dingbanwangleixing', 'dingbanwangtiesizhijing',

                  'gongzuomianbangmaoganleixing', 'gongzuomianbangmaogangantiqiangdu', 'gongzuomianbangmaoganzhijing', 'gongzuomianbangmaoganchangdu', 'gongzuomianbangmaoganzuankongzhijing', 'gongzuomianbangmaoganjianju', 'gongzuomianbangmaoganpaiju',
                  'gongzuomianbangmaogangangdaileixing', 'gongzuomianbangmaogangangdaikuandu', 'gongzuomianbangmaogangangdaichangdu', 'gongzuomianbangmaogangangdaihoudu',
                  'gongzuomianbangmaosuoleixing', 'gongzuomianbangmaosuogantiqiangdu', 'gongzuomianbangmaosuozhijing', 'gongzuomianbangmaosuochangdu', 'gongzuomianbangmaosuozuankongzhijing', 'gongzuomianbangmaosuojianju', 'gongzuomianbangmaosuopaiju',
                  'gongzuomianbangmaosuogangdaileixing', 'gongzuomianbangmaosuogangdaikuandu', 'gongzuomianbangmaosuogangdaichangdu', 'gongzuomianbangmaosuogangdaihoudu',
                  'gongzuomianbangwangleixing', 'gongzuomianbangwangtiesizhijing',

                  'meizhubangmaoganleixing', 'meizhubangmaogangantiqiangdu', 'meizhubangmaoganzhijing', 'meizhubangmaoganchangdu', 'meizhubangmaoganzuankongzhijing', 'meizhubangmaoganjianju', 'meizhubangmaoganpaiju',
                  'meizhubangmaogangangdaileixing', 'meizhubangmaogangangdaikuandu', 'meizhubangmaogangangdaichangdu', 'meizhubangmaogangangdaihoudu',
                  'meizhubangmaosuoleixing', 'meizhubangmaosuogantiqiangdu', 'meizhubangmaosuozhijing', 'meizhubangmaosuochangdu', 'meizhubangmaosuozuankongzhijing', 'meizhubangmaosuojianju', 'meizhubangmaosuopaiju',
                  'meizhubangmaosuogangdaileixing', 'meizhubangmaosuogangdaikuandu', 'meizhubangmaosuogangdaichangdu', 'meizhubangmaosuogangdaihoudu',
                  'meizhubangwangleixing', 'meizhubangwangtiesizhijing',

                  'gangpengxinghao', 'gangpengjianju',
                  'penjiangcailiao', 'penjianghoudu']
yucecanshu2py = {'支护形式': 'zhihuxingshi', '顶锚杆类型': 'dingmaoganleixing', '顶锚杆杆体强度': 'dingmaogangantiqiangdu', '顶锚杆直径': 'dingmaoganzhijing', '顶锚杆长度': 'dingmaoganchangdu', '顶锚杆钻孔直径': 'dingmaoganzuankongzhijing', '顶锚杆间距': 'dingmaoganjianju', '顶锚杆排距': 'dingmaoganpaiju', '顶锚杆钢带类型': 'dingmaogangangdaileixing', '顶锚杆钢带宽度': 'dingmaogangangdaikuandu', '顶锚杆钢带长度': 'dingmaogangangdaichangdu', '顶锚杆钢带厚度': 'dingmaogangangdaihoudu', '顶锚索类型': 'dingmaosuoleixing', '顶锚索杆体强度': 'dingmaosuogantiqiangdu', '顶锚索直径': 'dingmaosuozhijing', '顶锚索长度': 'dingmaosuochangdu', '顶锚索钻孔直径': 'dingmaosuozuankongzhijing', '顶锚索间距': 'dingmaosuojianju', '顶锚索排距': 'dingmaosuopaiju', '顶锚索钢带类型': 'dingmaosuogangdaileixing', '顶锚索钢带宽度': 'dingmaosuogangdaikuandu', '顶锚索钢带长度': 'dingmaosuogangdaichangdu', '顶锚索钢带厚度': 'dingmaosuogangdaihoudu', '顶板网类型': 'dingbanwangleixing', '顶板网铁丝直径': 'dingbanwangtiesizhijing', '工作面帮锚杆类型': 'gongzuomianbangmaoganleixing', '工作面帮锚杆杆体强度': 'gongzuomianbangmaogangantiqiangdu', '工作面帮锚杆直径': 'gongzuomianbangmaoganzhijing', '工作面帮锚杆长度': 'gongzuomianbangmaoganchangdu', '工作面帮锚杆钻孔直径': 'gongzuomianbangmaoganzuankongzhijing', '工作面帮锚杆间距': 'gongzuomianbangmaoganjianju', '工作面帮锚杆排距': 'gongzuomianbangmaoganpaiju', '工作面帮锚杆钢带类型': 'gongzuomianbangmaogangangdaileixing', '工作面帮锚杆钢带宽度': 'gongzuomianbangmaogangangdaikuandu', '工作面帮锚杆钢带长度': 'gongzuomianbangmaogangangdaichangdu', '工作面帮锚杆钢带厚度': 'gongzuomianbangmaogangangdaihoudu', '工作面帮锚索类型': 'gongzuomianbangmaosuoleixing', '工作面帮锚索杆体强度': 'gongzuomianbangmaosuogantiqiangdu', '工作面帮锚索直径': 'gongzuomianbangmaosuozhijing', '工作面帮锚索长度': 'gongzuomianbangmaosuochangdu', '工作面帮锚索钻孔直径': 'gongzuomianbangmaosuozuankongzhijing', '工作面帮锚索间距': 'gongzuomianbangmaosuojianju', '工作面帮锚索排距': 'gongzuomianbangmaosuopaiju', '工作面帮锚索钢带类型': 'gongzuomianbangmaosuogangdaileixing', '工作面帮锚索钢带宽度': 'gongzuomianbangmaosuogangdaikuandu', '工作面帮锚索钢带长度': 'gongzuomianbangmaosuogangdaichangdu', '工作面帮锚索钢带厚度': 'gongzuomianbangmaosuogangdaihoudu', '工作面帮网类型': 'gongzuomianbangwangleixing', '工作面帮网铁丝直径': 'gongzuomianbangwangtiesizhijing', '煤柱帮锚杆类型': 'meizhubangmaoganleixing', '煤柱帮锚杆杆体强度': 'meizhubangmaogangantiqiangdu', '煤柱帮锚杆直径': 'meizhubangmaoganzhijing', '煤柱帮锚杆长度': 'meizhubangmaoganchangdu', '煤柱帮锚杆钻孔直径': 'meizhubangmaoganzuankongzhijing', '煤柱帮锚杆间距': 'meizhubangmaoganjianju', '煤柱帮锚杆排距': 'meizhubangmaoganpaiju', '煤柱帮锚杆钢带类型': 'meizhubangmaogangangdaileixing', '煤柱帮锚杆钢带宽度': 'meizhubangmaogangangdaikuandu', '煤柱帮锚杆钢带长度': 'meizhubangmaogangangdaichangdu', '煤柱帮锚杆钢带厚度': 'meizhubangmaogangangdaihoudu', '煤柱帮锚索类型': 'meizhubangmaosuoleixing', '煤柱帮锚索杆体强度': 'meizhubangmaosuogantiqiangdu', '煤柱帮锚索直径': 'meizhubangmaosuozhijing', '煤柱帮锚索长度': 'meizhubangmaosuochangdu', '煤柱帮锚索钻孔直径': 'meizhubangmaosuozuankongzhijing', '煤柱帮锚索间距': 'meizhubangmaosuojianju', '煤柱帮锚索排距': 'meizhubangmaosuopaiju', '煤柱帮锚索钢带类型': 'meizhubangmaosuogangdaileixing', '煤柱帮锚索钢带宽度': 'meizhubangmaosuogangdaikuandu', '煤柱帮锚索钢带长度': 'meizhubangmaosuogangdaichangdu', '煤柱帮锚索钢带厚度': 'meizhubangmaosuogangdaihoudu', '煤柱帮网类型': 'meizhubangwangleixing', '煤柱帮网铁丝直径': 'meizhubangwangtiesizhijing', '钢棚型号': 'gangpengxinghao', '钢棚间距': 'gangpengjianju', '喷浆材料': 'penjiangcailiao', '喷浆厚度': 'penjianghoudu'}

# 根据类型分类 （类型存在，该类型的描述字段才存在）
yucecanshu_clt = {
    '支护形式': [],

    '顶锚杆类型': ['顶锚杆杆体强度', '顶锚杆直径', '顶锚杆长度', '顶锚杆钻孔直径', '顶锚杆间距', '顶锚杆排距'],
    '顶锚杆钢带类型': ['顶锚杆钢带宽度', '顶锚杆钢带长度', '顶锚杆钢带厚度'],
    '顶锚索类型': ['顶锚索杆体强度', '顶锚索直径', '顶锚索长度', '顶锚索钻孔直径', '顶锚索间距', '顶锚索排距'],
    '顶锚索钢带类型': ['顶锚索钢带宽度', '顶锚索钢带长度', '顶锚索钢带厚度'],
    '顶板网类型': ['顶板网铁丝直径'],

    '工作面帮锚杆类型': ['工作面帮锚杆杆体强度', '工作面帮锚杆直径', '工作面帮锚杆长度', '工作面帮锚杆钻孔直径', '工作面帮锚杆间距', '工作面帮锚杆排距'],
    '工作面帮锚杆钢带类型': ['工作面帮锚杆钢带宽度', '工作面帮锚杆钢带长度', '工作面帮锚杆钢带厚度'],
    '工作面帮锚索类型': ['工作面帮锚索杆体强度', '工作面帮锚索直径', '工作面帮锚索长度', '工作面帮锚索钻孔直径', '工作面帮锚索间距', '工作面帮锚索排距'],
    '工作面帮锚索钢带类型': ['工作面帮锚索钢带宽度', '工作面帮锚索钢带长度', '工作面帮锚索钢带厚度'],
    '工作面帮网类型': ['工作面帮网铁丝直径'],

    '煤柱帮锚杆类型': ['煤柱帮锚杆杆体强度', '煤柱帮锚杆直径', '煤柱帮锚杆长度', '煤柱帮锚杆钻孔直径', '煤柱帮锚杆间距', '煤柱帮锚杆排距'],
    '煤柱帮锚杆钢带类型': ['煤柱帮锚杆钢带宽度', '煤柱帮锚杆钢带长度', '煤柱帮锚杆钢带厚度'],
    '煤柱帮锚索类型': ['煤柱帮锚索杆体强度', '煤柱帮锚索直径', '煤柱帮锚索长度', '煤柱帮锚索钻孔直径', '煤柱帮锚索间距', '煤柱帮锚索排距'],
    '煤柱帮锚索钢带类型': ['煤柱帮锚索钢带宽度', '煤柱帮锚索钢带长度', '煤柱帮锚索钢带厚度'],
    '煤柱帮网类型': ['煤柱帮网铁丝直径'],

    '钢棚型号': ['钢棚间距'],
    '喷浆材料': ['喷浆厚度']
}
# 根据排距、长度分类 （锚杆排距、锚索排距：三个排距取最小，锚杆长度：三个长度取最大）
yucecanshu_clpc = {
    '锚杆排距': ['顶锚杆排距', '工作面帮锚杆排距', '煤柱帮锚杆排距'],
    '锚索排距': ['顶锚索排距', '工作面帮锚索排距', '煤柱帮锚索排距'],

    '锚杆长度': ['顶锚杆长度', '工作面帮锚杆长度', '煤柱帮锚杆长度'],
    '锚索长度': ['顶锚索长度', '工作面帮锚索长度', '煤柱帮锚索长度'],
    '锚索直径': ['顶锚索直径', '工作面帮锚索直径', '煤柱帮锚索直径'],
    # '锚杆直径': ['顶锚杆直径', '工作面帮锚杆直径', '煤柱帮锚杆直径'],
}

# 极端情况锚杆锚索
hangdaomaishen_extreme = {
                '顶锚杆类型': ['左旋纵筋螺纹钢锚杆', '左旋纵筋螺纹钢锚杆(树脂锚杆)'],
                '顶锚杆直径': [22.0],
                '顶锚杆杆体强度': [500, 600],
                '顶锚杆间距': [700, 750, 800],
                '顶锚杆排距': [700, 750, 800],
                '顶锚索类型': ['钢绞线锚索'],
                '顶锚索直径': [21.8],
                '顶锚索杆体强度': [1860],
                '顶锚索间距': [],
                '顶锚索排距': [],

                '工作面帮锚杆类型': ['右旋纵筋螺纹钢锚杆', '左旋纵筋螺纹钢锚杆(树脂锚杆)', '左旋纵筋螺纹钢锚杆(树脂锚杆)', '左旋纵筋螺纹钢锚杆(树脂锚杆)'],
                '工作面帮锚杆直径': [22.0],
                '工作面帮锚杆杆体强度': [500, 600],
                '工作面帮锚杆间距': [700, 750, 800],
                '工作面帮锚杆排距': [700, 750, 800],
                '工作面帮锚索类型': ['钢绞线锚索'],
                '工作面帮锚索直径': [21.8],
                '工作面帮锚索杆体强度': [1860],
                '工作面帮锚索间距': [],
                '工作面帮锚索排距': [],

                '煤柱帮锚杆类型': ['右旋纵筋螺纹钢锚杆', '左旋纵筋螺纹钢锚杆(树脂锚杆)'],
                '煤柱帮锚杆直径': [22.0],
                '煤柱帮锚杆杆体强度': [500, 600],
                '煤柱帮锚杆间距': [700, 750, 800],
                '煤柱帮锚杆排距': [700, 750, 800],
                '煤柱帮锚索类型': ['钢绞线锚索'],
                '煤柱帮锚索直径': [21.8],
                '煤柱帮锚索杆体强度': [1860],
                '煤柱帮锚索间距': [],
                '煤柱帮锚索排距': [],
                }
# 煤柱帮锚杆类型取值
meizhubangmaoganleixing = ['左旋无纵筋螺纹钢锚杆', '左旋纵筋螺纹钢锚杆(树脂锚杆)', '圆钢麻花头']
# 预测参数的范围
yucecanshu_range = {
                     "支护形式": ['锚网索带喷注棚', '锚索', '棚', '锚网带', '锚索柱', '锚网索带', '锚网索带喷棚', '锚网索注', '索', '锚网索带棚', '锚网带喷', '锚网索带注', '锚网索喷', '柱', '锚带喷棚', '锚索带柱', '锚索带', '锚网喷', '锚网索带柱', '锚网索带喷', '锚网', '锚网带棚', '锚索带喷', '砌', '喷棚砌', '锚网索', '锚索带棚', '锚网索喷棚'],
                     # 顶
                     "顶锚杆类型": [-2, '左旋螺纹钢锚杆', '左旋无纵筋螺纹钢锚杆', '左旋纵筋螺纹钢锚杆', '蛇形锚杆', '让压锚杆', '玻璃钢锚杆', '左旋纵筋螺纹钢锚杆(树脂锚杆)', '耦合让压应力显示锚杆'],
                     "顶锚杆杆体强度": [335, 400, 500, 600],
                     "顶锚杆直径": [16, 18, 20, 22],
                     "顶锚杆长度": [_ for _ in range(1500, 3600, 100)],
                     "顶锚杆钻孔直径": [28, 30, 32],
                     "顶锚杆间距": [_ for _ in range(600, 1300, 50)],
                     "顶锚杆排距": [_ for _ in range(600, 1300, 50)],
                     "顶锚杆钢带类型": [-2, 'π型', 'W钢带', '钢筋梯', 'W型'],
                     "顶锚杆钢带宽度": [_ for _ in range(150, 305, 5)],
                     "顶锚杆钢带长度": [_ for _ in range(100, 6550, 50)],
                     "顶锚杆钢带厚度": [2, 3, 4],

                     "顶锚索类型": [-2, '钢绞线锚索', '鸟窝锚索', '钢绞线', '让均压锚索'],
                     "顶锚索杆体强度": [1860],
                     "顶锚索直径": [17.8, 21.6, 21.8],
                     "顶锚索长度": [_ for _ in range(1500, 12100, 100)],
                     "顶锚索钻孔直径": [28, 30, 32],
                     "顶锚索间距": [],
                     "顶锚索排距": [],
                     "顶锚索钢带类型": [-2, 'JW型', 'T形', 'W钢带', 'W型', '钢筋梯'],
                     "顶锚索钢带宽度": [_ for _ in range(150, 405, 5)],
                     "顶锚索钢带长度": [_ for _ in range(400, 5550, 50)],
                     "顶锚索钢带厚度": [3, 4, 5],

                     "顶板网类型": [-2, '钢筋网', '塑料网', '菱形金属网', '金属网', '焊接经纬网', '金属菱形网'],
                     "顶板网铁丝直径": [_ / 2 for _ in range(8, 21)],
                     # 工作面帮
                     "工作面帮锚杆类型": [-2, '圆钢麻花头', '左旋无纵筋螺纹钢锚杆', '左旋螺纹钢锚杆', '左旋纵筋螺纹钢锚杆', '蛇形锚杆', '让压锚杆', '等强全螺纹钢锚杆', '玻璃钢锚杆', '左旋纵筋螺纹钢锚杆(树脂锚杆)', '圆钢端锚树脂锚杆', '右旋纵筋螺纹钢锚杆'],
                     "工作面帮锚杆杆体强度": [335, 400, 500, 600],
                     "工作面帮锚杆直径": [16, 18, 20, 22],
                     "工作面帮锚杆长度": [_ for _ in range(1500, 3600, 100)],
                     "工作面帮锚杆钻孔直径": [28, 30, 32],
                     "工作面帮锚杆间距": [_ for _ in range(600, 1300, 50)],
                     "工作面帮锚杆排距": [_ for _ in range(600, 1300, 50)],
                     "工作面帮锚杆钢带类型": [-2, 'W钢带', 'π型', 'W型', '钢筋梯', 'W型钢带'],
                     "工作面帮锚杆钢带宽度": [_ for _ in range(150, 305, 5)],
                     "工作面帮锚杆钢带长度": [_ for _ in range(100, 6550, 50)],
                     "工作面帮锚杆钢带厚度": [2, 3, 4],

                     "工作面帮锚索类型": [-2, '钢绞线锚索', '低松弛钢绞线', '钢绞线', '低松驰钢绞线'],
                     "工作面帮锚索杆体强度": [1860],
                     "工作面帮锚索直径": [17.8, 21.6, 21.8],
                     "工作面帮锚索长度": [_ for _ in range(1500, 12100, 100)],
                     "工作面帮锚索钻孔直径": [28, 30, 32],
                     "工作面帮锚索间距": [],
                     "工作面帮锚索排距": [],
                     "工作面帮锚索钢带类型": [-2, 'W型', '钢筋梯'],
                     "工作面帮锚索钢带宽度": [_ for _ in range(150, 405, 5)],
                     "工作面帮锚索钢带长度": [_ for _ in range(400, 5550, 50)],
                     "工作面帮锚索钢带厚度": [3, 4, 5],

                     "工作面帮网类型": [-2, '塑料网', '菱形网', '菱形金属网', '菱形金属网、塑料网', '金属网', '钢筋网'],
                     "工作面帮网铁丝直径": [_ / 2 for _ in range(8, 21)],
                     # 煤柱帮
                     "煤柱帮锚杆类型": [-2, '圆钢麻花头', '左旋无纵筋螺纹钢锚杆', '左旋纵筋螺纹钢锚杆', '蛇形锚杆', '螺纹钢锚杆', '让压锚杆', '左旋纵径螺纹钢锚杆', '玻璃钢锚杆', '左旋纵筋螺纹钢锚杆(树脂锚杆)', '右旋纵筋螺纹钢锚杆'],
                     "煤柱帮锚杆杆体强度": [335, 400, 500, 600],
                     "煤柱帮锚杆直径": [16, 18, 20, 22],
                     "煤柱帮锚杆长度": [_ for _ in range(1500, 3600, 100)],
                     "煤柱帮锚杆钻孔直径": [28, 30, 32],
                     "煤柱帮锚杆间距": [_ for _ in range(600, 1300, 50)],
                     "煤柱帮锚杆排距": [_ for _ in range(600, 1300, 50)],
                     "煤柱帮锚杆钢带类型": [-2, 'W型', 'W钢带', '钢筋梯'],
                     "煤柱帮锚杆钢带宽度": [_ for _ in range(150, 305, 5)],
                     "煤柱帮锚杆钢带长度": [_ for _ in range(100, 6550, 50)],
                     "煤柱帮锚杆钢带厚度": [2, 3, 4],

                     "煤柱帮锚索类型": [-2, '钢绞线锚索', '低松弛钢绞线', '鸟窝锚索', '钢绞线'],
                     "煤柱帮锚索杆体强度": [1860],
                     "煤柱帮锚索直径": [17.8, 21.6, 21.8],
                     "煤柱帮锚索长度": [_ for _ in range(1500, 12100, 100)],
                     "煤柱帮锚索钻孔直径": [28, 30, 32],
                     "煤柱帮锚索间距": [],
                     "煤柱帮锚索排距": [],
                     "煤柱帮锚索钢带类型": [-2, 'W型', '钢筋梯'],
                     "煤柱帮锚索钢带宽度": [_ for _ in range(150, 405, 5)],
                     "煤柱帮锚索钢带长度": [_ for _ in range(400, 5550, 50)],
                     "煤柱帮锚索钢带厚度": [3, 4, 5],

                     "煤柱帮网类型": [-2, '菱形金属网', '钢筋网', '塑料网'],
                     "煤柱帮网铁丝直径": [_ / 2 for _ in range(8, 21)],
                     # 钢棚
                     "钢棚型号": [-2, '18#工字钢', 'U29', '11#工字钢', 'U36'],
                     "钢棚间距": [_ for _ in range(300, 1550, 50)],
                     # 喷浆
                     "喷浆材料": [-2, '初喷', '喷射混凝土', '水泥砂浆', '混凝土'],
                     "喷浆厚度": [_ for _ in range(50, 310, 10)],
                     }
# 回采巷道(胶带运输巷、轨道运输巷、开切眼)
huicaihangdao = ['回采巷道', '胶带运输巷', '轨道运输巷', '开切眼']
yucecanshu_py2py2 = {'dingmaoganleixing': 'db_mao_gan_type', 'dingmaoganzhijing': 'db_mao_gan_diameter', 'dingmaoganjianju': 'db_mao_gan_jj', 'dingmaoganpaiju': 'db_mao_gan_pj', 'dingmaoganchangdu': 'db_mao_gan_length', 'dingmaosuoleixing': 'db_mao_suo_type', 'dingmaosuozhijing': 'db_mao_suo_diameter', 'dingmaosuojianju': 'db_mao_suo_jj', 'dingmaosuopaiju': 'db_mao_suo_pj', 'dingmaosuochangdu': 'db_mao_suo_length', 'dingbanwangleixing': 'db_net_type', 'gongzuomianbangmaoganleixing': 'gzm_mao_gan_type', 'gongzuomianbangmaoganzhijing': 'gzm_mao_gan_diameter', 'gongzuomianbangmaoganjianju': 'gzm_mao_gan_jj', 'gongzuomianbangmaoganpaiju': 'gzm_mao_gan_pj', 'gongzuomianbangmaoganchangdu': 'gzm_mao_gan_length', 'gongzuomianbangmaosuoleixing': 'gzm_mao_suo_type', 'gongzuomianbangmaosuozhijing': 'gzm_mao_suo_diameter', 'gongzuomianbangmaosuojianju': 'gzm_mao_suo_jj', 'gongzuomianbangmaosuopaiju': 'gzm_mao_suo_pj', 'gongzuomianbangmaosuochangdu': 'gzm_mao_suo_length', 'gongzuomianbangwangleixing': 'gzm_net_type', 'meizhubangmaoganleixing': 'mzm_mao_gan_type', 'meizhubangmaoganzhijing': 'mzm_mao_gan_diameter', 'meizhubangmaoganjianju': 'mzm_mao_gan_jj', 'meizhubangmaoganpaiju': 'mzm_mao_gan_pj', 'meizhubangmaoganchangdu': 'mzm_mao_gan_length', 'meizhubangmaosuoleixing': 'mzm_mao_suo_type', 'meizhubangmaosuozhijing': 'mzm_mao_suo_diameter', 'meizhubangmaosuojianju': 'mzm_mao_suo_jj', 'meizhubangmaosuopaiju': 'mzm_mao_suo_pj', 'meizhubangmaosuochangdu': 'mzm_mao_suo_length', 'meizhubangwangleixing': 'mzm_net_type'}
