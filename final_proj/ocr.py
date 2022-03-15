#Import libraries for opening, manipulating, #extracting text from image and saving it
from bs4 import BeautifulSoup as soup
from PIL import Image
import cv2
import pytesseract as tess
from docx import Document

im_file = "br_pt_n1_1899.jpeg"

im = Image.open(im_file)

print(im)
print(im.size)
im.show()
