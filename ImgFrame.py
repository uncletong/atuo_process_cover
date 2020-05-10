import tkinter as tk


class ImgFrame:
    def __init__(self, img, img_path, parent_frame):
        self.img = img
        self.frame = tk.Frame(parent_frame)
        self.frame.pack()

        # 路径
        self.img_label = tk.Label(self.frame, text=img_path.split('/')[-1], width=40, anchor=tk.W)
        self.img_label.grid(row=0, column=0)

        # 长和宽
        self.h = tk.DoubleVar()
        self.w = tk.DoubleVar()
        self.img_h = tk.Entry(self.frame, width=10, textvariable=self.h)
        self.img_h.bind('<Return>', self.print_key1)
        self.img_w = tk.Entry(self.frame, width=10, textvariable=self.w)
        self.img_w.bind('<Return>', self.print_key2)
        self.img_h.grid(row=0, column=1)
        self.img_w.grid(row=0, column=2)
        self.h.set(img.shape[1]/100)
        self.w.set(img.shape[2]/100)

        # 是否去网纹
        self.is_descreen = tk.IntVar()
        self.descreen = tk.Checkbutton(self.frame, text="去网纹", variable=self.is_descreen)
        self.descreen.grid(row=0, column=3)

    def print_key1(self, event):
        h = self.h.get()
        self.w.set(float(h) / self.img.shape[1] * self.img.shape[2])

    def print_key2(self, event):
        w = self.w.get()
        self.h.set(float(w) / self.img.shape[2] * self.img.shape[1])
