from PIL import ImageTk
from tkinter import Tk, Label, BOTH
from tkinter.ttk import Frame


class ImageWindow(Frame):
    def __init__(self, img):
        parent = Tk()
        Frame.__init__(self, parent)
        self.pack(fill=BOTH, expand=1)
        label1 = Label(self)
        label1.photo = ImageTk.PhotoImage(img)
        label1.config(image=label1.photo)
        label1.pack(fill=BOTH, expand=1)
        parent.mainloop()


def calculate_camera_variables(eye, lookat, up, fov, aspect_ratio, fov_is_vertical=False):
    import numpy as np
    import math

    W = np.array(lookat) - np.array(eye)
    wlen = np.linalg.norm(W)
    U = np.cross(W, np.array(up))
    U /= np.linalg.norm(U)
    V = np.cross(U, W)
    V /= np.linalg.norm(V)

    if fov_is_vertical:
        vlen = wlen * math.tan(0.5 * fov * math.pi / 180.0)
        V *= vlen
        ulen = vlen * aspect_ratio
        U *= ulen
    else:
        ulen = wlen * math.tan(0.5 * fov * math.pi / 180.0)
        U *= ulen
        vlen = ulen * aspect_ratio
        V *= vlen

    return U, V, W
