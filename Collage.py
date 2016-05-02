from PIL import Image, ImageFilter, ImageEnhance, ImageFont, ImageDraw, ImageOps
import os, sys
import math

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
        copy_image.flip()
        value_length = int(round(self.length/num))
        for number in range(0, num):
            box = (0, value_length*number, self.width, value_length*(number+1))
            region = copy_image.image.crop(box)
            if number%2 == 0:
                self.image.paste(region,box)

    def blurryface(self, intensity):
        self.image = self.image.filter(ImageFilter.GaussianBlur(intensity))

    def enhancedface(self, intensity):
        enhancer = ImageEnhance.Sharpness(self.image)
        self.image = enhancer.enhance(intensity)

    def vignetto(self,attack,colour):
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
        empty_image = Image.new("RGB", (self.width, self.length), colour)
        self.image = Image.composite(self.image, empty_image, vignette_filter)

    def checkerboard(self, num):
        count = 0
        copy_image = image_edit(self.filename)
        copy_image.grey_scale()
        value_width = int(round(self.width/num))
        value_length = int(round(self.length/num))
        for number in range(0, num):
            for n in range(0,num):
                count+=1
                box = (value_width*n, value_length*number, value_width*(n+1), value_length*(number+1))
                region = copy_image.image.crop(box)
                if (count%2 == 0):
                    self.image.paste(region,box)

    def write_text(self, font, font_size, word, colour, ):
        draw = ImageDraw.Draw(self.image)
        fnt = ImageFont.truetype(font,font_size)
        draw.text((50,self.length - 150), word, colour, font = fnt)

    def flip_horizontal(self):
        self.image = ImageOps.mirror(self.image)

    def flip_vertical(self):
        self.image = ImageOps.flip(self.image)

    def invert_image(self):
        self.image = ImageOps.invert(self.image)

    def blurry_pattern(self):
        box = (300, 168)
        number = math.ceil(1200/300)
        empty_picture = Image.new("RGB", (1200,168))
        for stamp in range(4):
            self.blurryface(stamp*3)
            region = self.image.resize(box)
            pasteBox = (300*stamp,0, 300+(300*stamp), 168)
            empty_picture.paste(region, pasteBox)
        self.image = empty_picture
class create_collage():

    def __init__(self, height, width, portrait_filename1, landscape_filename2, filename3, filename4):
        self.height = height
        self.width = width
        self.background = Image.new("RGB", (self.width, self.height), (255,255,255))
        self.picture1 = image_edit(portrait_filename1)
        self.picture2 = image_edit(landscape_filename2)
        self.picture3 = image_edit(filename3)
        self.picture4 = image_edit(filename4)

    def generate(self):
        self.picture1.vignetto(400,(0,0,0))
        region = self.picture1.image.resize((800,1000))
        self.background.paste(region,(0,0))
        self.background.show()



"""background = image_edit("cat.jpg")
background.checkerboard(5)
animal = image_edit("animal.jpg")
animal.write_text("BRADHITC.TTF",100,"Myra", (0,0,0))
#background.image.paste(animal.image, (10,0)) # ORDER OF FILTERS IS IMPORTANT. ANY FILTER ON BACKGROUND AFTER PASTED IMAGE WILL ALSO APPLY FILTER ON PASTED IMAGE
background.image.show()"""

collage1 = create_collage(1200,1200,"panda.jpg","animal.jpg", "cat.jpg", "rabbit.jpg")
collage1.generate()



