from PIL import Image, ImageFilter, ImageEnhance, ImageFont, ImageDraw, ImageOps
import os, sys


class image_edit():

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
        copy_image = image_edit(self.filename)
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
        copy_image = image_edit(self.filename)
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

class create_collage():

    def __init__(self, height, width, filename1,filename2,filename3,filename4):
        self.height = height
        self.width = width
        self.background = Image.new("RGB", (self.width, self.height), (255,255,255))
        #perhaps it takes in file names, makes them image objects and then always creates the same format

    def blurry_pattern(self, im_file):
        pass #makes the copied image pattern of progressive blurriness like in the code below




background = image_edit("cat.jpg")
animal = image_edit("animal.jpg")
 #ORDER OF FILTERS IS IMPORTANT. ANY FILTER ON BACKGROUND AFTER
box = (0, 0, 300, 168)
region = animal.image.crop(box)
for stamp in range(6):
   region = region.filter(ImageFilter.GaussianBlur(stamp))
   pasteBox = ((stamp*300),(background.length - 168), 300+(300*stamp), 0)
   background.image.paste(region, pasteBox)                                  #PASTED IMAGE WILL ALSO APPLY FILTER ON PASTED IMAGE

background.image.show()

"""collage1 = create_collage(10000,10000)
collage1.blurry_pattern("animal.jpg")
collage1.image.show()"""


