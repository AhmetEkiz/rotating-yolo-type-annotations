

# More information can be found : notebooks/rotate_segmentations.ipynb

from src import utils
import cv2
import matplotlib.pyplot as plt
import numpy as np

import glob
from tqdm import tqdm
import os
import shutil

import sys
sys.path.append('../src')


# reading annotations from files and draw o image


def rotate_and_save_dataset(dataset_PATH, output_folder_PATH=" "):

    # create rotated dataset directory
    output_folder_PATH = f"{dataset_PATH}_rotated"
    os.makedirs(output_folder_PATH, exist_ok=True)
    # save the data.yaml file
    shutil.copy(f'{dataset_PATH}/data.yaml', f'{output_folder_PATH}/data.yaml')

    # find all images and annotations in the train, test, and val folders if they exist
    for folder in glob.glob(dataset_PATH+"/*/"):

        # it suppose to be train, test, val
        folder_name = folder.split("\\")[-2]
        print(f"Processing in {folder_name}...")

        # creating subfolders - train-test-val / images-labels
        ouput_sub_folder_PATH = f"{output_folder_PATH}/{folder_name}"
        ouput_sub_folder_images_PATH = f"{output_folder_PATH}/{folder_name}/images"
        ouput_sub_folder_labels_PATH = f"{output_folder_PATH}/{folder_name}/labels"
        # create new train test val directory if they exist
        os.makedirs(ouput_sub_folder_PATH, exist_ok=True)
        print(ouput_sub_folder_PATH, "created")
        os.makedirs(ouput_sub_folder_images_PATH, exist_ok=True)
        print(ouput_sub_folder_images_PATH, "created")
        os.makedirs(ouput_sub_folder_labels_PATH, exist_ok=True)
        print(ouput_sub_folder_labels_PATH, "created")

        # PATH of train, test, val folders
        sub_folder_PATH = f"{dataset_PATH}/{folder_name}/"

        for image_PATH in tqdm(glob.glob(sub_folder_PATH+"/images/*")):
            image_name = image_PATH.split("\\")[-1]
            label_PATH = f"{sub_folder_PATH}/labels/{image_name.split('.')[0]}.txt"
            # print(image_PATH)

            # # Before Rotating
            # image = utils.draw_seg_annotations(label_PATH, image)   # draw annotations

            # Starting Rotating
            ouput_sub_folder_labels_PATH = f"{output_folder_PATH}/{folder_name}/labels"

            # Rotate annotations and images. CCW 90 degree
            # TODO: Angle just works with -90 degree right now.
            image = cv2.imread(image_PATH)
            rotated_annotation_file_PATH, rotated_image_PATH = utils.rotate_segmentation_annotations(label_PATH,
                                                                                                     ouput_sub_folder_PATH,
                                                                                                     image_name,
                                                                                                     image,
                                                                                                     cx=0.5,
                                                                                                     cy=0.5,
                                                                                                     angle=np.radians(-90))


def main():

    dataset_PATH = "./data/example_dataset_1_YOLO"

    rotate_and_save_dataset(dataset_PATH)
    print("Test Images Printed. Comment utils.rotate_annotations, if you don't want to print test images lines.")


if __name__ == "__main__":
    main()
