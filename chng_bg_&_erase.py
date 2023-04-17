from rembg import remove
from PIL import Image
import easygui as eg
import cv2
from PIL import Image, ImageTk
import tkinter as tk


input_path = eg.fileopenbox(title='Select image file')
output_path = 'masked.png'
input = Image.open(input_path)
output = remove(input)
output.save(output_path)
img = str(output_path[29:])
img_copy = str(input_path[29:])

img_path = str(input_path)
spl_path = img_path.split()
print(spl_path)


img = cv2.imread("Stencil_4.jpg")


def concat_tile(im_list_2d):
    return cv2.vconcat([cv2.hconcat(im_list_h) for im_list_h in im_list_2d])


im1_s = cv2.resize(img, dsize=(0, 0), fx=0.1, fy=0.1)
im_tile = concat_tile([[im1_s, im1_s, im1_s, im1_s],
                       [im1_s, im1_s, im1_s, im1_s],
                       [im1_s, im1_s, im1_s, im1_s]])
cv2.imwrite('concat.jpg', im_tile)

background_image = 'concat.jpg'
background_image = Image.open(background_image)

background_image = background_image.resize((input.width, input.height))

foreground_img = Image.open(output_path)
background_image.paste(foreground_img, (0, 0), foreground_img)
background_image.save('result.jpg')

IMAGE1_DIR = "frame2.jpg"
IMAGE2_DIR = 'result.jpg'
IMAGE3_DIR = 'concat.jpg'
BRUSH = 20


def create_image(filename, width=0, height=0):
    img = Image.open(filename, mode="r")

    if not width and not height:
        return img
    elif width and height:
        return img.resize((int(width), int(height)), Image.ANTIALIAS)
    else:
        w, h = img.size
        scale = width/float(w) if width else height/float(h)
        return img.resize((int(w*scale), int(h*scale)), Image.ANTIALIAS)


class Home(object):
    def __init__(self, master, screen):
        self.screen = w, h = screen
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        self.can = tk.Canvas(self.frame, width=w, height=h)
        self.can.pack()
        self.image1 = create_image(IMAGE1_DIR, w, h)
        self.image2 = create_image(IMAGE2_DIR, w, h)
        self.image3 = create_image(IMAGE3_DIR, w, h)
        self.center = w//2, h//2
        self.photo = False
        self.draw()
        self.master.bind("<Return>", self.reset)
        self.master.bind("<B1-Motion>", self.erase)
        self.master.bind("<Key>", self.draw_texture)

    def draw(self):
        if self.photo:
            self.can.delete(self.photo)
            self.label.destroy()

        p = ImageTk.PhotoImage(image=self.image2)
        self.photo = self.can.create_image(self.center, image=p)
        self.label = tk.Label(image=p)
        self.label.image = p

    def reset(self, event):
        self.frame.destroy()
        self.__init__(self.master, self.screen)

    def erase(self, event):
        for x in range(event.x-BRUSH, event.x+BRUSH+1):
            for y in range(event.y-BRUSH, event.y+BRUSH+1):
                try:
                    p = self.image1.getpixel((x, y))
                    self.image2.putpixel((x, y), p)
                except IndexError:
                    pass

        self.draw()

    def draw_texture(self, event):
        for x in range(event.x-BRUSH, event.x+BRUSH+1):
            for y in range(event.y-BRUSH, event.y+BRUSH+1):
                try:
                    p = self.image3.getpixel((x, y))
                    self.image2.putpixel((x, y), p)
                except IndexError:
                    pass

        self.draw()


def main(screen=(500, 500)):
    root = tk.Tk()
    root.resizable(0, 0)
    Home(root, screen)
    root.mainloop()


if __name__ == '__main__':
    main()
