# I. Introduction
### Nearest update: 3/11/2023
### Restriction: 
- Onnx of TTS Vits 1 models

## II. Build onnx
### 2.1 Installation
```commandline
pip install onnx
pip install onnxruntime
```

### 2.2 Convert onnx
```commandline
python convert_torch_to_onnx.py
```


## III. Infer onnx
```commandline
python infer2.py
```

## IV. Triton Ensemble
#### 1. Run triton server
```commandline
docker run --gpus=all -it --shm-size=1g --rm  -p8000:8000 -p8001:8001 -p8002:8002 -v ${PWD}:/workspace/ -v /home/thhiep/tts_tien_xu_ly/tts_tien_xu_ly/refactorcode/text-to-speech/onnx_triton/vits/model_repository:/models nvcr.io/nvidia/tritonserver:22.11-py3
docker run --gpus=all -it --shm-size=1g --rm  \                                       
  -p8000:8000 -p8001:8001 -p8002:8002 \
  -v ${PWD}:/workspace/ -v ${PWD}/model_repository:/models \
  nvcr.io/nvidia/tritonserver:22.11-py3
```
#### 2. Trong triton contaniner
đổi tên các file và đưa file trong onnx_convert  đưa vào model_repository
```commandline
pip install torch
tritonserver --model-repository=/models
```

To test from client:
```commandline
pip install tritonclient
python client.py
```

## V. Version changes
```commandline

```