import cv2
import numpy as np
import os


def draw_seg_annotations(label_PATH, image, thickness=2):
    """ Draw instance segmentation from given label_PATH and given image

    #TODO: 
        - give different color for every class

    Args:
        label_PATH: annotation label_PATH
        image: given image to draw annotations
        thickness: line thickness        
    Returns:
        image: annotated image
    """
    color = (255, 255, 0)  # Green color

    img_height, img_width, _ = image.shape

    # read the annotation file - Parse the YOLO annotation file
    with open(label_PATH, "r") as file:
        lines = file.readlines()

    for line in lines:
        data = line.strip().split()

        class_id = int(data[0])
        points = list(map(float, data[1:]))

        # split x and y. Also scale for image width and height
        x = np.array(points[0::2])*img_width
        y = np.array(points[1::2])*img_height

        # merge x and y as a points
        points = np.array(list(zip(x, y))).astype(int)

        # draw segmentations
        image = cv2.drawContours(image, [points], -1, color, thickness)

    return image


def draw_bbox_annotations(label_PATH, image, thickness=2):
    """ Draw Bounding Box annotation from given label_PATH and given image

    #TODO: 
    - give different color for every class

Args:
    label_PATH: annotation label_PATH
    image: given image to draw annotations
    thickness: line thickness        
Returns:
    image: annotated image
    """
    color = (255, 255, 0)  # Green color

    img_height, img_width, _ = image.shape

    # read the annotation file - Parse the YOLO annotation file
    with open(label_PATH, "r") as file:
        lines = file.readlines()

    for line in lines:
        data = line.strip().split()

        class_id, x_center_norm, y_center_norm, width_norm, height_norm = map(
            float, data)
        class_id = int(class_id)

    # Scale x, y, width and height for image
        x = x_center_norm*img_width
        y = y_center_norm*img_height
        w = width_norm*img_width
        h = height_norm*img_height

        # draw bounding box
        image = cv2.rectangle(image, (int(x-(w/2)), int(y-(h/2))), (int(x+(w/2)), int(y+(h/2))), color, thickness)

    return image


def rotate_segmentation_annotations(label_PATH,
                                    ouput_folder_PATH,
                                    image_name,
                                    image,
                                    cx=0.5, cy=0.5, angle=np.radians(-90)):
    """ Rotate instance segmentation annotations and images then save a file.

    Args:
            label_PATH: Label path to read annotation that is wanted rotated.
    ouput_folder_PATH: to save images and annotations. (train-test-val)
    image_name: name of the image. For example: vertical_1.jpg
    image: a numpy array for image
    cx (float): Rotation referance point's x, in this case center of the image. Default is 0.5 because of annotations are normalized.
            cy (float): Rotation referance point's y, in this case center of the image. Default is 0.5 because of annotations are normalized.
    angle (float PI number type): Angle, in radians ( rad equals 360 degrees). For example np.pi/2. it equals to 90 degree angle CCW
    Return:
            rotated_annotation_file_PATH: New rotated annotation file PATH

    """

    img_height, img_width, _ = image.shape

    # rotate and save the image
    rotated_image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    rotated_image_PATH = f"{ouput_folder_PATH}/images/{image_name}"
    cv2.imwrite(rotated_image_PATH, rotated_image)

    with open(label_PATH, "r") as file:
        lines = file.readlines()

    # create new annotation file
    rotated_annotation_file_PATH = f"{ouput_folder_PATH}/labels/{image_name.split('.')[0]}.txt"

    with open(rotated_annotation_file_PATH, "w") as file:

        for line in lines:
            data = line.strip().split()

            class_id = int(data[0])
            points = list(map(float, data[1:]))

            # split x and y. Also scale for image width and height
            x = np.array(points[0::2])
            y = np.array(points[1::2])

            x, y = rotate_point(x, y, cx=0.5, cy=0.5, angle=angle)

            flat_list = list(zip(x, y))   # merge x and y
            flat_list = [item for sublist in flat_list for item in sublist]

            annotation_line = f"{class_id} {(' '.join(map(str, flat_list)))}\n"
            file.write(annotation_line)

    # to test annotations is true uncomment these 4 lines
    test_image = draw_seg_annotations(
        rotated_annotation_file_PATH, rotated_image, thickness=2)
    test_rotated_image_PATH = f"{ouput_folder_PATH}/test_images/{image_name}"
    os.makedirs(f"{ouput_folder_PATH}/test_images", exist_ok=True)
    cv2.imwrite(test_rotated_image_PATH, test_image)

    return rotated_annotation_file_PATH, rotated_image_PATH


# Function to rotate a point (x, y) around a given center (cx, cy) by angle (in radians)
def rotate_point(x, y, cx=0.5, cy=0.5, angle=np.radians(-90)):
    """ Rotate a point (x, y) around a given center (cx, cy) by angle (in radians)

    Args:
    label_PATH: Label PATH of annotation for an image
            x : a numpy array or float for x 
            y : a numpy array or float for y
            cx (float): Rotation referance point's x, in this case center of the image. Default is 0.5 because of annotations are normalized.
            cy (float): Rotation referance point's y, in this case center of the image. Default is 0.5 because of annotations are normalized.
            angle (float PI number type): Angle, in radians ( rad equals 360 degrees). For example np.pi/2. it equals to 90 degree angle CCW

    Returns:
            x_new, y_new: the rotated point
    """

    cos_theta = np.cos(angle)
    sin_theta = np.sin(angle)
    x_new = cos_theta * (x - cx) - sin_theta * (y - cy) + cx
    y_new = sin_theta * (x - cx) + cos_theta * (y - cy) + cy

    return x_new, y_new


def rotate_bbox_annotations(label_PATH,
                            ouput_folder_PATH,
                            image_name,
                            image,
                            cx=0.5, cy=0.5, angle=np.radians(-90)):
    """ Rotate bounding box annotations and images then save a file.

    Args:
            label_PATH: Label path to read annotation that is wanted rotated.
    ouput_folder_PATH: to save images and annotations. (train-test-val)
    image_name: name of the image. For example: vertical_1.jpg
    image: a numpy array for image
    cx (float): Rotation referance point's x, in this case center of the image. Default is 0.5 because of annotations are normalized.
            cy (float): Rotation referance point's y, in this case center of the image. Default is 0.5 because of annotations are normalized.
    angle (float PI number type): Angle, in radians ( rad equals 360 degrees). For example np.pi/2. it equals to 90 degree angle CCW
    Return:
            rotated_annotation_file_PATH: New rotated annotation file PATH

    """

    img_height, img_width, _ = image.shape

    # rotate and save the image
    rotated_image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    rotated_image_PATH = f"{ouput_folder_PATH}/images/{image_name}"
    cv2.imwrite(rotated_image_PATH, rotated_image)

    with open(label_PATH, "r") as file:
        lines = file.readlines()

    # create new annotation file
    rotated_annotation_file_PATH = f"{ouput_folder_PATH}/labels/{image_name.split('.')[0]}.txt"

    with open(rotated_annotation_file_PATH, "w") as file:

        for line in lines:
            data = line.strip().split()

            class_id, x_center_norm, y_center_norm, width_norm, height_norm = map(float, data)
            class_id = int(class_id)

            # rotate center point
            x_center_norm_new, y_center_norm_new = rotate_point(
                x_center_norm, y_center_norm, cx=0.5, cy=0.5, angle=angle)

            # width, height of bounding box
            width_new_norm = height_norm
            height_new_norm = width_norm

            annotation_line = f"{class_id} {x_center_norm_new} {y_center_norm_new} {width_new_norm} {height_new_norm}\n"

            file.write(annotation_line)

    # to test annotations is true uncomment these 4 lines
    # TODO: Draw bbox annotations
    test_image = draw_bbox_annotations(rotated_annotation_file_PATH, rotated_image, thickness=2)
    test_rotated_image_PATH = f"{ouput_folder_PATH}/test_images/{image_name}"
    os.makedirs(f"{ouput_folder_PATH}/test_images", exist_ok=True)
    cv2.imwrite(test_rotated_image_PATH, test_image)

    return rotated_annotation_file_PATH, rotated_image_PATH
