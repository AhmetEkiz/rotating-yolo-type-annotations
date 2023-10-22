# Rotating Yolo-Type Annotations

Rotating segmentation annotations and images of type Yolo. In case you want to rotate images and annotations, you can use this repo. It also works with bounding boxes. 

![before_after.png](./images/before_after.png)

## How to Use

Edit `rotate_dataset.py` for dataset path, and run the code. It will create new dataset folder named with `{your_dataset_path}_rotated` and its subfolders (train, test, val)/(images/labels). 

- Notebooks can be examined to see how the codes work.

```bash
python rotate_dataset.py
```
