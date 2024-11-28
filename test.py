import torch

if torch.cuda.is_available():
    # 当前设备
    print("Current device:", torch.cuda.current_device())
    # 可用 GPU 数量
    print("Number of GPUs:", torch.cuda.device_count())
    # GPU 名称
    print("Device name:", torch.cuda.get_device_name(torch.cuda.current_device()))
else:
    print("CUDA is not available. Running on CPU.")
