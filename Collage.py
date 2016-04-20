from PIL import Image, ImageFilter, ImageEnhance
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
                new_pixel = (r,0,0)
                self.image.putpixel((x,y),new_pixel)
            elif colour == "g":
                new_pixel = (0,g,0)
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
        for y in range(self.length):
            for x in range(self.width):
                r, g, b = self.image.getpixel((x,y))
                average = int((r + g + b) / 3)
                greyscale = (average, average, average)
                self.image.putpixel((x,y), greyscale)

    def check_if_bands_fit(self,number, num):
        while number%num != 0:
            num+=1
        return num

    def create_uno_band(self, count, original_value,value):
        if count%2 == 0:
            for y in range(original_value,value):
                self.red_green_or_blue(y,"r")
        else:
            for y in range(original_value,value):
                self.red_green_or_blue(y,"b")

    def bands(self, num):
        num_of_bands = self.check_if_bands_fit(self.length, num)
        value = int(self.length/num_of_bands)
        for loop in range(1,(num_of_bands+1)):
            self.create_uno_band(loop,value*(loop-1),value*loop)

    def stupid_vignette(self):
        pass #blegh

    def blurryface(self): #heh heh heh
        pass

    def enhancedface(self):
        pass

    def checkerboard(self):
        pass

    def my_own_choice(self):
        pass

background = collage_image("cat.jpg")
animal = collage_image("animal.jpg")
    #ORDER OF FILTERS IS IMPORTANT. ANY FILTER ON BACKGROUND AFTER
background.bands(3)      #PASTED IMAGE WILL ALSO APPLY FILTER ON PASTED IMAGE
background.image.paste(animal.image,(0,0))
background.image.show()


#im2 = Image.open("dog.jpg")
#im3 = Image.open("rabbit.jpg")

#box = (0, 0, 300, 168)

"""source = im.split()
R, G, B = 0, 1, 2
mask = source[R].point(lambda i: i <100 and 255)
out = source[G].point(lambda i: i * 0.7)
source[G].paste(out, None, mask)
im = Image.merge(im.mode, source)"""

#enhancer = ImageEnhance.Sharpness(im3)
#enhancer = enhancer.enhance(2.0).show("Sharpness %f" % 2.0)

"""region = im2.crop(box)
for stamp in range(6):

    region = region.filter(ImageFilter.GaussianBlur(stamp))
    pasteBox = ((stamp*300),500, 300+ (300*stamp), 668)
    im.paste(region, pasteBox) """

