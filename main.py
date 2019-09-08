import cv2
import glob
import xml.etree.ElementTree as ET
import os
import numpy as np

new_size = [176, 176]
folder_path = "bike_left/"
xml_ext = "xml"
jpg_ext = "jpg"
asterisk = "*"
dot = "."


def xml_file(img, scale_width, scale_height):

    xml = folder_path + img.split('\\')[1].split(dot + jpg_ext)[0] + dot + xml_ext

    tree = ET.parse(xml)
    root = tree.getroot()

    for size in root.findall('size'):
        width = size.find('width')
        height = size.find('height')

        width.text = str(new_size[1])
        height.text = str(new_size[0])

    for f in root.findall('object'):
        bndbox = f.find('bndbox')
        xmin = bndbox.find('xmin')
        xmax = bndbox.find('xmax')
        ymin = bndbox.find('ymin')
        ymax = bndbox.find('ymax')

        xmin.text = str(np.round(int(xmin.text) * scale_width)).split(dot)[0]
        xmax.text = str(np.round(int(xmax.text) * scale_width)).split(dot)[0]
        ymin.text = str(np.round(int(ymin.text) * scale_height)).split(dot)[0]
        ymax.text = str(np.round(int(ymax.text) * scale_height)).split(dot)[0]

    tree.write(xml)
    return img.split('\\')[1].split(dot + jpg_ext)[0]


def convert():
    images_path = folder_path + asterisk + dot + jpg_ext
    image_files = glob.glob(images_path)

    for img in image_files:
        image = cv2.imread(img)

        scale_height = new_size[0] / image.shape[0]
        scale_width = new_size[1] / image.shape[1]

        image = cv2.resize(image, (new_size[0], new_size[1]))

        image_name = xml_file(img, scale_width, scale_height)

        cv2.imwrite(os.path.join(folder_path, dot.join([image_name, jpg_ext])), image)


convert()
