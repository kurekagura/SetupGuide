#CUDA 11.0
#pip install torch==1.7.1+cu110 torchvision==0.8.2+cu110 torchaudio==0.7.2 -f https://download.pytorch.org/whl/torch_stable.html
#CUDA 11.7
#pip install torch==1.13.0 torchvision==0.14.0 torchaudio==0.13.0 --extra-index-url https://download.pytorch.org/whl/cu117
import sys
import torch

print(f"sys.version => {sys.version}")
print(f"torch.__version__ => {torch.__version__}")

print(f"torch.cuda.is_available() => {torch.cuda.is_available()}")
device = "cuda" if torch.cuda.is_available() else "cpu"

if device == "cuda":
    print(f"torch.cuda.device_count() => {torch.cuda.device_count()}")
    print(f"torch.cuda.current_device() => {torch.cuda.current_device()}")

    torch_device = torch.device(f"cuda:{torch.cuda.current_device()}")
    print(f"torch.cuda.get_device_name({torch_device}) => {torch.cuda.get_device_name(torch_device)}")
    print(f"torch.cuda.get_device_capability(torch_device) => {torch.cuda.get_device_capability(torch_device)}")

    print(f"torch.backends.cudnn.version() => {torch.backends.cudnn.version()}")
