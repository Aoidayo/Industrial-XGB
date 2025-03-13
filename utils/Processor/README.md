# 0x01. Processor
必须包含的是
- `JFProcessor`
  - 将甲方的输入数据(en), 处理为我们预测需要的输入数据(zh)
- `PredictPostProcessor`
  - 将我们预测的输出(zh), 使用甲方预置规则处理, 处理为甲方需要的输出(en)

两个`Config`必须包含，甲方预定义规则只能使用硬编码实现。