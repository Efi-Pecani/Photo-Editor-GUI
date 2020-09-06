#   Name: Efi Pecani
#   ID: 307765230 

from tkinter import *         #import all of this stuff in order to wor kwith tkinter methods
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import ImageTk , ImageFilter
from PIL import Image
import os, sys
import tkinter.font as tkFont

#_________________________________________________
def rotatePicture(sourceImagePath, targetImagePath):   #1st function
    im = Image.open(sourceImagePath)#.convert('L')
    w,h = im.size
    new = im.copy()
    mat = im.load()
    mat_new = new.load()
    for i in range(w):
        for j in range(h):
            mat_new[i,j] =mat[w-i-1,h-j-1]
    if targetImagePath != "":
        new.save(targetImagePath)
        print("saved")
    else:
        return new
#______________________________________________
def mirrorPicture(sourceImagePath, targetImagePath):   #2nd function
    im = Image.open(sourceImagePath)#.convert('L') optional for gray image
    w,h = im.size
    new = im.copy()
    mat = im.load()
    mat_new = new.load()
    for i in range(w):
        for j in range(h):
            mat_new[i,j] = mat[w-i-1,j]
    if targetImagePath != "":
        new.save(targetImagePath)
        print("saved")
    else:
        return new
#_________________________________________________
def resizePicture(sourceImagePath, targetImagePath):  #3rd function
    im = Image.open(sourceImagePath).convert('L')
    w,h = im.size
    #w=int(w/2)
    #h=int(h/2)
    mat = im.load()#im.copy()#
    newpic = Image.new('L', (int(w/2), int(h/2)))
    newmat = newpic.load()
    for x in range(int(w/2)):
        for y in range(int(h/2)):
            newmat[x,y] = (mat[x*2, y*2]+mat[x*2+1, y*2]+mat[x*2, y*2+1]+mat[x*2+1, y*2+1]//4)
 #           newdata[x,y]=(0)
    if targetImagePath != "":
        newpic.save(targetImagePath)
 #       print("saved")  for self checking
    else:
        return newpic
#_________________________________________________

def edge(sourceImagePath, targetImagePath ,threshold): #4th function 
    im = Image.open(sourceImagePath).convert('L')
    w,h = im.size
    data = im.load()
    new = Image.new('L', (w, h))
    newdata = new.load()
    for i in range(w-1):
        for j in range(1, h):
            if abs(data[i, j]-data[i+1, j]) > threshold or abs(data[i, j]-data[i, j-1]) > threshold:
                newdata[i, j] = 255
            else:
                newdata[i, j] = 0
    if targetImagePath != "": #the condition
        new.save(targetImagePath)
        print("saved")
    else:
        return new
#_________________________________________________
def MyAlgorithm1(sourceImagePath,targetImagePath):# 5th function create a Primary Colors version of the image
    im = Image.open(sourceImagePath)
    width, height = im.size
    new =im.copy()
    new = Image.new("RGB", (width, height), "white")
    pixels = new.load()
    # Transform to primary
    for i in range(width):
        for j in range(height):
            pixel = get_pixel(im, i, j)# Get Pixel
            red =   pixel[0] # Get R, G, B values (This are int from 0 to 255)
            green = pixel[1]
            blue =  pixel[2]
            if red > 127:# Transform to primary
                red = 255
            else:
                red = 0
            if green > 127:
                green = 255
            else:
                green = 0
            if blue > 127:
                blue = 255
            else:
                blue = 0
            pixels[i, j] = (int(red), int(green), int(blue)) #sets pixel in new image
    if targetImagePath != "":   #the condition for saving-->if saved button was pressed should work
        new.save(targetImagePath)
        print("saved")
    else:
        return new

        
#_________________________________________________

def MyAlgorithm2(sourceImagePath,targetImagePath):# 5th function  
    im = Image.open(sourceImagePath)                #creates a Half-tone version of the image
    width, height = im.size
 #  new =im.copy()
    new = Image.new("RGB", (width, height), "white")
    pixels = new.load()
    for i in range(0, width, 2):# transform to half tones
        for j in range(0, height, 2):
      
            p1 = get_pixel(im, i, j) # get Pixels
            p2 = get_pixel(im, i, j + 1)
            p3 = get_pixel(im, i + 1, j)
            p4 = get_pixel(im, i + 1, j + 1)
            gray1 = (p1[0] * 0.299) + (p1[1] * 0.587) + (p1[2] * 0.114) # Transform to grayscale
            gray2 = (p2[0] * 0.299) + (p2[1] * 0.587) + (p2[2] * 0.114)
            gray3 = (p3[0] * 0.299) + (p3[1] * 0.587) + (p3[2] * 0.114)
            gray4 = (p4[0] * 0.299) + (p4[1] * 0.587) + (p4[2] * 0.114)
            sat = (gray1 + gray2 + gray3 + gray4) / 4           # saturation percentage  ("revaya shel gavan")
            if sat > 223:
                pixels[i, j]         = (255, 255, 255) # White
                pixels[i, j + 1]     = (255, 255, 255) # White
                pixels[i + 1, j]     = (255, 255, 255) # White
                pixels[i + 1, j + 1] = (255, 255, 255) # White
            elif sat > 159:
                pixels[i, j]         = (255, 255, 255) # White
                pixels[i, j + 1]     = (0, 0, 0)       # Black
                pixels[i + 1, j]     = (255, 255, 255) # White
                pixels[i + 1, j + 1] = (255, 255, 255) # White
            elif sat > 95:
                pixels[i, j]         = (255, 255, 255) # White
                pixels[i, j + 1]     = (0, 0, 0)       # Black
                pixels[i + 1, j]     = (0, 0, 0)       # Black
                pixels[i + 1, j + 1] = (255, 255, 255) # White
            elif sat > 32:
                pixels[i, j]         = (0, 0, 0)       # Black
                pixels[i, j + 1]     = (255, 255, 255) # White
                pixels[i + 1, j]     = (0, 0, 0)       # Black
                pixels[i + 1, j + 1] = (0, 0, 0)       # Black
            else:
                pixels[i, j]         = (0, 0, 0)       # Black
                pixels[i, j + 1]     = (0, 0, 0)       # Black
                pixels[i + 1, j]     = (0, 0, 0)       # Black
                pixels[i + 1, j + 1] = (0, 0, 0)       # Black
                
    if targetImagePath != "":
        new.save(targetImagePath)
        print("saved")
    else:
        return new

#_________________________________________________
def gaussBlur(sourceImagePath, targetImagePath):  #6th extra functions built in just for fun and color
    im = Image.open(sourceImagePath)
    new = im.copy()
    new=new.filter(ImageFilter.GaussianBlur(20))
    if targetImagePath != "":
        new.save(targetImagePath)
        print("saved")
    else:
        return new
#_________________________________________________

def minFilter(sourceImagePath, targetImagePath):  #7th function extra
    fact=7
    im = Image.open(sourceImagePath)
    new = im.copy()
    new=new.filter(ImageFilter.MinFilter(fact))
    if targetImagePath != "":
        new.save(targetImagePath)
        print("saved")
    else:
        return new
#_________________________________________________

def sharpen(sourceImagePath, targetImagePath):  #8th function extra
    im = Image.open(sourceImagePath)
    new = im.copy()
    new=new.filter(ImageFilter.UnsharpMask)
    if targetImagePath != "":
        new.save(targetImagePath)
        print("saved")
    else:
        return new
#_________________________________________________

def contour(sourceImagePath, targetImagePath):  #9th function extra
    im = Image.open(sourceImagePath)
    new = im.copy()
    new=new.filter(ImageFilter.CONTOUR)
    if targetImagePath != "":
        new.save(targetImagePath)
        print("saved")
    else:
        return new

#_________________________________________________

def detail(sourceImagePath, targetImagePath):  #10th function extra 
    im = Image.open(sourceImagePath)
    new = im.copy()
    new=new.filter(ImageFilter.DETAIL)
    if targetImagePath != "":
        new.save(targetImagePath)
        print("saved")
    else:
        return new
#_________________________________________________

def edgeEnhanceMore(sourceImagePath, targetImagePath):  #11th function extra
    im = Image.open(sourceImagePath)
    new = im.copy()
    new=new.filter(ImageFilter.EDGE_ENHANCE_MORE)
    if targetImagePath != "":
        new.save(targetImagePath)
        print("saved")
    else:
        return new
#_________________________________________________

def emboss(sourceImagePath, targetImagePath):  #12th function extra
    im = Image.open(sourceImagePath)
    new = im.copy()
    new=new.filter(ImageFilter.EMBOSS)
    if targetImagePath != "":
        new.save(targetImagePath)
        print("saved")
    else:
        return new
#_________________________________________________

def kernelSmooth(sourceImagePath, targetImagePath):  #13th function extra
    im = Image.open(sourceImagePath)
    new = im.copy()
    new=new.filter(ImageFilter.Kernel((3, 3), [1, 2, 1, 2, 4, 2, 1, 2, 1], 16))
    if targetImagePath != "":
        new.save(targetImagePath)
        print("saved")
    else:
        return new

#_________________________________________________
    
'''@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Auxilary Functions @@@@@@@@@@'''
#_________________________________________________

def add(sourceImagePath,k):  #learning from the class
    im = Image.open(sourceImagePath).convert('L')
    w,h = im.size
    new = im.copy()
    mat = im.load()
    mat_new = new.load()
    for x in range(w):
        for y in range(h):
            mat_new[x,y] = min((mat[x,y]+k), 256)
    return new
#_______________________________________
def open_image(path):# Open an Image
  newImage = Image.open("./my_image.jpg")
  return newImage
#_______________________________________

def save_image(image, path):# Save Image
  image.save(path, 'jpg')
#_______________________________________

def create_image(i, j):
  image = Image.new("RGB", (i, j), "white")
  return image
#_______________________________________

def get_pixel(image, i, j):# Get the pixel from the given image
    # Inside image bounds?
    width, height = image.size
    if i > width or j > height:
      return None

    # get Pixel
    pixel = image.getpixel((i, j))
    return pixel
#_______________________________________

path="./my_image1.jpg"
target="./newIm.jpg"

# display
#newIm=rotatePicture(path, target)# עובד
#newIm=mirrorPicture(path, target)  עובד
#newIm= edge (path, target,15 ) # עובד
#newIm= gaussBlur(path, target) #עובד
#im = Image.open(path) 
#newIm=im.copy()
#newIm=resizePicture(path,"") #עובד
#newIm.show()
#newPic.show()

