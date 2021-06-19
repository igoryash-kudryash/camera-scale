# Camera plan scale


## Getting started

- Python версии 3.6
- CUDA версии 10.0 и видеокарта с поддержкой CUDA
- Клонирование репозитория
```bash
git clone https://git.miem.hse.ru/gchkabisov2/camera-plan-scale.git
```
- Установка зависимостей
```bash
pip install -r requirements.txt
```
## Usage

Определение крупности плана съемки с веб-камеры
```bash
python yoloface_gpu.py --video stream --method area
```
## Анализ

## YOLOv3's architecture

Credit: https://towardsdatascience.com/yolo-v3-object-detection-53fb7d3bfe6b
Arxiv: https://arxiv.org/abs/1804.02767

## Model Weights
Для работы с моделью необходимо скачать веса модели отсюда https://drive.google.com/file/d/1LGOd-1TfBBYDiYCc0uWUMD5p2Tfsjc88/view?usp=sharing и поместить в папку model-weights.

## References
За основу был взят код https://github.com/sthanhng/yoloface - модель YoLo, обученная на детекцию человеческих лиц.
