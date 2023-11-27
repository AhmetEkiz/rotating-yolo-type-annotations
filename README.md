# Rotating Yolo-Type Annotations

**Rotating segmentation annotations and images of type Yolo.** If you want to rotate images and segmentation annotations, you can use this repo. It also works with bounding boxes.
- Just works with **CCW 90** right now.

![before_after.png](./images/before_after.png)

## How to Use

Edit `rotate_segmentation_dataset.py` for the dataset path, and run the code. It will create a new dataset folder named with `{your_dataset_path}_rotated` and its subfolders (train, test, val)/(images/labels). 

- For Bounding Box Datasets: `rotate_bbox_dataset.py`
- Notebooks can be examined to see how the codes work.

```bash
python rotate_segmentation_dataset.py

python rotate_bbox_dataset.py
```

- Also, this generates annotated images for each train/test/val folder with the `test_images` name.
```
├───train
│   ├───images
│   │       vertical_1.jpg
│   │       vertical_2.jpg
│   │
│   ├───labels
│   │       vertical_1.txt
│   │       vertical_2.txt
│   │
│   └───test_images
│           vertical_1.jpg
│           vertical_2.jpg
```
# TODO

- [x] Fix for object detection dataset rotation.
- [x] Give different colors for every class.
- [ ] Put text on annotation on drawing function.
- [ ] Drawing Segmentation annotations from folder main code.
- [ ] Drawing Bounding Box annotations from folder main code.
- [ ] ~~Changing Rotation Degree.~~
