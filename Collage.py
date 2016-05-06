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
        copy_image.flip_horizontal()
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
                opacity = int((255 - (distance - attack)))
                if opacity < 0:
                    opacity = 0
                if opacity > 255:
                    opacity = 255
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
            if num%2 == 0:
                count += 1
            for n in range(0,num):
                count+=1
                box = (value_width*n, value_length*number, value_width*(n+1), value_length*(number+1))
                region = copy_image.image.crop(box)
                if (count%2 == 0):
                    self.image.paste(region,box)

    def write_text(self, font, font_size, word, colour):
        draw = ImageDraw.Draw(self.image)
        fnt = ImageFont.truetype(font,font_size)
        draw.text((50,self.length - 150), word, colour, font = fnt)

    def flip_horizontal(self):
        self.image = ImageOps.mirror(self.image)

    def flip_vertical(self):
        self.image = ImageOps.flip(self.image)

    def invert_image(self):
        self.image = ImageOps.invert(self.image)

    def check_fits(self,number):
        min = 4
        while (number % min) != 0:
            min +=1
        return min

    def blurry_pattern(self, length, width):
        number = self.check_fits(width)
        width_of_resized = int(width/number)
        box = (width_of_resized,length)
        empty_picture = Image.new("RGB", (width,length))
        for stamp in range(number):
            self.blurryface(stamp*3)
            region = self.image.resize(box)
            pasteBox = (width_of_resized*stamp,0, width_of_resized+(width_of_resized*stamp), length)
            empty_picture.paste(region, pasteBox)
        self.image = empty_picture

    def reflection(self,reflection_line):
        empty_picture= Image.new("RGB", (self.width, reflection_line*2))
        region = self.image.crop((0,0,self.width,reflection_line))
        empty_picture.paste(region,(0,0))
        y_count = reflection_line
        for y in range(reflection_line,self.length):
            x_count = 0
            for x in range(self.width):
                r, g, b = self.image.getpixel((x_count,y_count))
                self.image.putpixel((x,y), (r,g,b))
                x_count += 1
            y_count -= 1

    def paint_texture(self,intensity):
        self.image = self.image.filter(ImageFilter.ModeFilter(intensity))

class create_collage():

    def __init__(self, height, width, portrait_filename1, landscape_filename2, portrait_filename3, landscape_filename4):
        self.height = height
        self.width = width
        self.background = Image.new("RGB", (self.width, self.height), (255,255,255))
        self.picture1 = image_edit(portrait_filename1)
        self.picture2 = image_edit(landscape_filename2)
        self.picture3 = image_edit(portrait_filename3)
        self.picture4 = image_edit(landscape_filename4)

    def generate(self):
        self.picture1.vignetto(int(self.picture1.width-(self.picture1.width/3)),(0,0,0))
        region = self.picture1.image.resize((int((self.width/6)*4), int((self.height/4)*3)))
        self.background.paste(region,(0,0))
        resized_height = int(self.height/4)
        self.picture2.blurry_pattern(resized_height,self.width)
        box = (0, (self.height-resized_height), self.width, self.height)
        self.background.paste(self.picture2.image, box)
        self.picture3.checkerboard(5)
        region2 = self.picture3.image.resize((int((self.width/6)*2),int((resized_height*3)/5 *3)))
        self.background.paste(region2,(int((self.width/6)*4),0,self.width, (self.height - int(((resized_height*3)/5 *2)))-resized_height))
        self.picture4.reflection(int(self.picture4.length/2))
        region3 = self.picture4.image.resize((int((self.width/6)*2),int((resized_height*3)/5 *2)))
        self.background.paste(region3,(int((self.width/6)*4),((self.height - int(((resized_height*3)/5 *2)))-resized_height),self.width, (self.height - resized_height)))
        self.background.show()

"""background = image_edit("cat.jpg")
background.paint_texture(50)
animal = image_edit("animal.jpg")
animal.write_text("BRADHITC.TTF",100,"Myra", (0,0,0))
background.image.paste(animal.image, (10,0))
background.image.show()"""

collage1 = create_collage(2000,1500,"IMG_3443.JPG","IMG_3881.JPG", "IMG_4016.JPG", "IMG_3982.JPG")
collage1.generate() #This is going to take a while depending on the size of pictures you've chosen so prepare yourself.



