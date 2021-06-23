# Camera plan scale


## Getting started

- Python 3.6
- CUDA 10.0+
- Clone repository
```bash
git clone https://git.miem.hse.ru/gchkabisov2/camera-plan-scale.git
```
- Install requirements
```bash
pip install -r requirements.txt
```
## Usage

Camera plan
```bash
python yoloface_gpu.py --video stream --method area
```

## YOLOv3's architecture

Credit: https://towardsdatascience.com/yolo-v3-object-detection-53fb7d3bfe6b
Arxiv: https://arxiv.org/abs/1804.02767

## Model Weights
You need to download weights from https://drive.google.com/file/d/1LGOd-1TfBBYDiYCc0uWUMD5p2Tfsjc88/view?usp=sharing and place them into model-weights.

## References
The code was taken as a basis from https://github.com/sthanhng/yoloface - pretrained yolo for face detection.
