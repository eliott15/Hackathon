import pytesseract
import dateparser
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter
import imageio
import os
import cv2
import tempfile
import imutils


def image_processing(img_path, resize_1=None, Gauss=None, resize_2=None, inter_AREA=None):
    """
    Preprocess images in different way to use in the get_date_product_img function to amplify recognition
    input : img_path
    output : Image Preprocessed
    """
    img = cv2.imread(img_path)
    if resize_1 and not inter_AREA:
        img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    if resize_1 and inter_AREA:
        img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_AREA)
    if Gauss:
        img = cv2.GaussianBlur(img, (5, 5), 0)
    if resize_2 and inter_AREA:
        img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_AREA)
    if resize_2 and not inter_AREA:
        img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    image_file = Image.fromarray(img)
    image_file = image_file.convert('L')
    return image_file


def get_date_product_img(image_file):
    """
    Find a date in a image.
    input : an image file
    output : a date if recognize
    """
    a = pytesseract.image_to_string(image_file)
    b = []
    dates = []
    for i in a.split('\n'):
        data = dateparser.parse(i)
        if data is not None:
            b.append(data)
    if len(b) == 0:
        return None
    elif len(b) >= 1:
        for date in b:
            if 2018 < date.year < 2025:
                dates.append(date)
        if len(dates) != 0:
            return max(dates)
        else:
            return None
    else:
        return b[0]


def get_best(dates):
    """
    Get best date for find_date function
    """
    best_dates = []
    for date in dates:
        if date != date.today():
            best_dates.append(date)
    return max(best_dates)


def find_date(img_path):
    """
    Recognize if there is an expiration date in the picture and return it if so.
    input : image path
    return : The expiory date of the product if recognize
    """
    dates = []
    image_file = image_processing(img_path, resize_1=None, Gauss=None, resize_2=None, inter_AREA=None)
    if get_date_product_img(image_file) is not None:
        dates.append(get_date_product_img(image_file))
    image_file = image_processing(img_path, resize_1=True, Gauss=None, resize_2=None, inter_AREA=None)
    if get_date_product_img(image_file) is not None:
        dates.append(get_date_product_img(image_file))
    image_file = image_processing(img_path, resize_1=True, Gauss=True, resize_2=None, inter_AREA=None)
    if get_date_product_img(image_file) is not None:
        dates.append(get_date_product_img(image_file))
    image_file = image_processing(img_path, resize_1=True, Gauss=True, resize_2=True, inter_AREA=None)
    if get_date_product_img(image_file) is not None:
        dates.append(get_date_product_img(image_file))
    image_file = image_processing(img_path, resize_1=True, Gauss=True, resize_2=True, inter_AREA=True)
    if get_date_product_img(image_file) is not None:
        dates.append(get_date_product_img(image_file))
    image_file = image_processing(img_path, resize_1=True, Gauss=None, resize_2=True, inter_AREA=None)
    if get_date_product_img(image_file) is not None:
        dates.append(get_date_product_img(image_file))
    image_file = image_processing(img_path, resize_1=True, Gauss=None, resize_2=True, inter_AREA=True)
    if get_date_product_img(image_file) is not None:
        dates.append(get_date_product_img(image_file))
    if len(list(set(dates))) == 1:
        return list(set(dates))[0].strftime("%d/%m/%Y")
    if len(list(set(dates))) == 0:
        return None
    else:
        return get_best(list(set(dates))).strftime("%d/%m/%Y")
