from PIL import Image, ImageFilter, ImageEnhance, ImageFont, ImageDraw, ImageOps
import os, sys


class collage_image():

    def __init__(self, file):
        im = Image.open(file)
        self.width, self.length = (im.size)
        self.image = im
        self.filename = file

    def negate_red(self):
        for y in range(self.length):
            for x in range(self.width):
                r, g, b = self.image.getpixel((x,y))
                negate_red_pixel = (255-r, g, b)
                self.image.putpixel((x,y), negate_red_pixel)

    def grey_scale(self):
        self.image = ImageOps.grayscale(self.image)

    def horizontal_bands(self, num):
        copy_image = collage_image(self.filename)
        copy_image.grey_scale()
        value_length = int(round(self.length/num))
        for number in range(0, num):
            box = (0, value_length*number, self.width, value_length*(number+1))
            region = copy_image.image.crop(box)
            if number%2 == 0:
                self.image.paste(region,box)

    def blurryface(self, intensity): #heh heh heh
        self.image = self.image.filter(ImageFilter.GaussianBlur(intensity))

    def enhancedface(self, intensity):
        enhancer = ImageEnhance.Sharpness(self.image)
        self.image = enhancer.enhance(intensity)

    def vignetto(self,attack,r,g,b):
        vignette_filter = Image.new('RGBA',(self.width, self.length))
        for x in range(self.width):
            for y in range(self.length):
                x_values = (x, int(self.width/2))
                y_values = (y, int(self.length/2))
                distance = int(((max(x_values)-min(x_values))**2 + (max(y_values)-min(y_values))**2)**0.5)
                opacity = 255 - (distance - attack)
                if opacity < 0:
                    opacity = 0
                vignette_filter.putpixel((x,y), (0,0,0,opacity))
        empty_image = Image.new("RGB", (self.width, self.length), (r,g,b))
        self.image = Image.composite(self.image, empty_image, vignette_filter)

    def checkerboard(self, num):
        count = 0
        copy_image = collage_image(self.filename)
        copy_image.grey_scale()
        value_width = int(round(self.width/num))
        value_length = int(round(self.length/num))
        for number in range(0, num):
            count+=1
            for n in range(0,num):
                count+=1
                box = (value_width*n, value_length*number, value_width*(n+1), value_length*(number+1))
                region = copy_image.image.crop(box)
                if (count%2 == 0):
                    self.image.paste(region,box)

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
background.vignetto(500,204,0,204)                                    #ORDER OF FILTERS IS IMPORTANT. ANY FILTER ON BACKGROUND AFTER
                                   #PASTED IMAGE WILL ALSO APPLY FILTER ON PASTED IMAGE
background.image.paste(animal.image,(10,0))
print (background.width)
print (background.length)
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