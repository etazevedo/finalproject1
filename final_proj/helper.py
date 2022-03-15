import cv2
import pytesseract as tess
import docx
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from docx2pdf import convert

# Input to output functions

def open_image(img):
    """function to open the image saved in our uploads direc"""
    image = cv2.imread(img)
    return image

def image_to_text(image):
    """function to transform the image into text"""
    text = tess.image_to_string(Image.open(image), lang="por")
    return text

def display_text(text):
    """function to display the extracted test and show it in a rendered template"""

    display = display(text)
    return display

def create_document(text):
    """function to create a word doc with the extracted text"""
    document = docx.Document()
    document.add_paragraph(text)
    save = document.save('extracted_text.docx')
    return save


def create_pdf(save):
    """function to convert the docx to pdf"""
    pdf = convert(save)
    return pdf


# Preprocessing functions

def display(im_path):
    """function display the image before preprocessing"""
    dpi = 80
    im_data = plt.imread(im_path)
    height, width = im_data.shape[:2]
    # What size does the figure need to be in inches to fit the image?
    figsize = width / float(dpi), height / float(dpi)
    # Create a figure of the right size with one axes that takes up the full figure
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])
    # Hide spines, ticks, etc.
    ax.axis('off')
    # Display the image.
    ax.imshow(im_data, cmap='gray')
    return plt.show()


def binarize(image):
    """function to transform a color image into a binarized image"""
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh, im_bw = cv2.threshold(gray_image, 210, 230, cv2.THRESH_BINARY)
    binarized = cv2.imwrite("temp/bw_image.jpg", im_bw)
    return binarized


def getSkewAngle(image) -> float:
    """function to find the angle of skewness"""

    # Prep image, copy, convert to gray scale, blur, and threshold
    newImage = image.copy()
    gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Apply dilate to merge text into meaningful lines/paragraphs.
    # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
    # But use smaller kernel on Y axis to separate between different blocks of text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=2)

    # Find all contours
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    for c in contours:
        rect = cv2.boundingRect(c)
        x, y, w, h = rect
        cv2.rectangle(newImage, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Find largest contour and surround in min area box
    largestContour = contours[0]
    print(len(contours))
    minAreaRect = cv2.minAreaRect(largestContour)
    cv2.imwrite("temp/boxes.jpg", newImage)
    # Determine the angle. Convert it to the value that was originally used to obtain skewed image
    angle = minAreaRect[-1]
    if angle < -45:
        angle = 90 + angle
    return -1.0 * angle


def rotateImage(image, angle: float):
    """function to rotate the image"""
    newImage = image.copy()
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return newImage


def deskew(newImage):
    """function deskew the image"""
    angle = getSkewAngle(newImage)
    rotated = rotateImage(newImage, -1.0 * angle)
    return rotated

def write_deskew(rotated):
    """function to write deskew the image"""
    fixed = deskew(rotated)
    deskew_image = cv2.imwrite("temp/deskew_image.jpg", fixed)
    return deskew_image

def noise_removal(image):
    """function to remove image grain"""
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)
    no_noise = noise_removal(image)
    cv2.imwrite("temp/no_noise.jpg", no_noise)
    return no_noise





