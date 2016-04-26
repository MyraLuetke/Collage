from PIL import Image, ImageFilter, ImageEnhance, ImageFont, ImageDraw, ImageOps
import os, sys


class collage_image():

    def __init__(self, file):
        im = Image.open(file)
        self.width, self.length = (im.size)
        self.image = im

    def red_green_or_blue(self, y, colour):
        for x in range(self.width):
            r, g, b = self.image.getpixel((x,y))
            if colour == "r":
                new_pixel = (r,g-50,b-50)
                self.image.putpixel((x,y),new_pixel)
            elif colour == "g":
                new_pixel = (r-0,g,b-20)
                self.image.putpixel((x,y),new_pixel)
            else:
                new_pixel = (0,0,b)
                self.image.putpixel((x,y),new_pixel)

    def negate_red(self):
        for y in range(self.length):
            for x in range(self.width):
                r, g, b = self.image.getpixel((x,y))
                negate_red_pixel = (255-r, g, b)
                self.image.putpixel((x,y), negate_red_pixel)

    def grey_scale(self):
        self.image = ImageOps.grayscale(self.image)

    def create_uno_band(self, count, original_value,value, colour1, colour2):
        if count%2 == 0:
            for y in range(original_value,value):
                self.red_green_or_blue(y,colour1)
        else:
            for y in range(original_value,value):
                self.red_green_or_blue(y,colour2)

    def horizontal_colour_bands(self, num, colour1, colour2):
        value = int(self.length/num)
        for loop in range(1,(num+1)):
            self.create_uno_band(loop,value*(loop-1),value*loop, colour1, colour2)

    """def vertical_contrast_bands(self, bandCount):
        bandWidth = int(self.width / bandCount)
        startX = 0;
        for stamp in range(0,bandCount):
            box = (startX + (bandWidth*stamp), 0, bandWidth + (startX + (bandWidth*stamp)), 1300)
            region = self.image.crop(box)
            enhancer = ImageEnhance.Contrast(region)
            if (stamp%2 ==0):
                region = enhancer.enhance(100)
            box= (bandWidth * stamp, 1000, (bandWidth*stamp) + bandWidth, 2300)
            im.paste(region, box)"""


    def blurryface(self, intensity): #heh heh heh
        self.image = self.image.filter(ImageFilter.GaussianBlur(intensity))

    def enhancedface(self, intensity):
        enhancer = ImageEnhance.Sharpness(self.image)
        self.image = enhancer.enhance(intensity)

    def stupid_vignette(self):
        #Go away

    def checkerboard(self):
        county = 0
        countx = 0
        for x in range(self.width):
            countx += 1
            for y in range(self.length):
                county+=1
                if county == 10:
                    county = 0
                    self.image.putpixel((x,y), (0,0,0))
                    #I don't know what I'm doing


    def write_text(self):
        txt=Image.new("RGB", self.image.size, (255,255,255))
        fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 40)
        draw = ImageDraw.Draw(txt)
        draw.text((10,10), "Cool", font=fnt,fill=(255,255,255))
        self.image = Image.alpha_composite(self.image, txt)

    def flip(self):
        self.image = ImageOps.mirror(self.image)

background = collage_image("cat.jpg")
animal = collage_image("animal.jpg")
                                    #ORDER OF FILTERS IS IMPORTANT. ANY FILTER ON BACKGROUND AFTER
                                   #PASTED IMAGE WILL ALSO APPLY FILTER ON PASTED IMAGE
background.image.paste(animal.image,(10,10))
background.image.show()


"""
im = Image.open("rabbit.jpg")
source = im.split()
R, G, B = 0, 1, 2
mask = source[R].point(lambda i: i <100 and 255)
out = source[G].point(lambda i: i * 0.7)
source[G].paste(out, None, mask)
im = Image.merge(im.mode, source)

im.show()"""


"""region = im2.crop(box)
for stamp in range(6):

    region = region.filter(ImageFilter.GaussianBlur(stamp))
    pasteBox = ((stamp*300),500, 300+ (300*stamp), 668)
    im.paste(region, pasteBox) """

"""
im = Image.open("cat.jpg")
im2 = Image.open("dog.jpg")

sourceSize = im2.size
sourceWidth = sourceSize[0]
sourceHeight = sourceSize[1]

box = (600, 700, 1100, 1300)
region = im2.crop(box)
bandCount = 50
bandWidth = int(sourceWidth / bandCount)
startX = 0;
for stamp in range(0,bandCount):
    box = (startX + (bandWidth*stamp), 0, bandWidth + (startX + (bandWidth*stamp)), 1300)
    region = im2.crop(box)
    enhancer = ImageEnhance.Contrast(region)
    #if (stamp%2 ==0):
     #   region = enhancer.enhance( stamp/bandCount)
    if (stamp%2 ==0):
        region = enhancer.enhance(100)
    box= (bandWidth * stamp, 1000, (bandWidth*stamp) + bandWidth, 2300)
    im.paste(region, box)

im.show()"""