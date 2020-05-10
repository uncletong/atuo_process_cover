import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import numpy as np
import cv2
import os
import ImgFrame
import descreen


def fast_set():
    h = entry_fast_height.get()
    w = entry_fast_width.get()
    for frame in img_frames:
        frame.h.set(h)
        frame.w.set(w)


def cv_imread(file_path):
    cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
    return cv_img


def clear_lists():
    for widget in img_process_frame.winfo_children():
        widget.destroy()
    imgs.clear()
    img_frames.clear()
    img_paths.clear()


def process():
    i = 1
    for frame in img_frames:
        h = int(100 * float(frame.img_h.get()))
        w = int(100 * float(frame.img_w.get()))
        img = frame.img
        # 勾选去网纹则进行去网纹处理
        if frame.is_descreen.get() == 1:
            img = descreen.descreen_img(img=img)
        else:
            img = img.transpose(1, 2, 0)
        img = cv2.resize(img, (w, h))
        cv2.imwrite(str(i) + ".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        i = i + 1

    tk.messagebox.showinfo(title="success!", message="处理完成！")


def screen():
    if flag[0]:
        for frame in img_frames:
            frame.descreen.select()
            flag[0] = False
    else:
        for frame in img_frames:
            frame.descreen.deselect()
            flag[0] = True


def img2frame():
    for i in range(len(imgs)):
        img_frame = ImgFrame.ImgFrame(imgs[i], img_paths[i], img_process_frame)
        img_frames.append(img_frame)
    # for img, img_path in zip(imgs, img_paths):
    #     img_frame = ImgFrame.ImgFrame(img, img_path, img_process_frame)


def is_img(ext):
    ext = ext.lower()
    if ext == 'jpg':
        return True
    elif ext == 'png':
        return True
    elif ext == 'jpeg':
        return True
    elif ext == 'bmp':
        return True
    else:
        return False


def open_img(paths):

    for path in paths:
        img = np.float32(cv_imread(path).transpose(2, 0, 1))
        imgs.append(img)
        img_paths.append(path)


def select_imgs():
    clear_lists()
    path = tk.filedialog.askopenfilenames(filetypes=[("PNG JPG", ".png .jpg"), ("*", ".")])
    # path.set(path_[0])
    # img = np.float32(cv2.imread(entry_path.get()).transpose(2, 0, 1))
    # height.set(str(img.shape[1] / 100))
    # width.set(str(img.shape[2] / 100))
    # imgs.append(img)

    # 添加图片
    open_img(path)
    img2frame()


def select_folder():
    clear_lists()
    path = tk.filedialog.askdirectory()
    files = os.listdir(path)
    paths = list()
    for file in files:
        if is_img(file.split(".")[-1]):
            paths.append(path + '/' + file)
    open_img(paths)
    img2frame()


if __name__ == '__main__':
    # 初始化变量
    flag = [True]  # 是否去网纹
    imgs = list()  # 图片
    img_paths = list()  # 图片路径
    img_frames = list()  # 图片frame list

    # 初始化窗口
    root = tk.Tk()
    root.title("Auto process scanned image")
    root.geometry('600x400')

    # 标题
    label_frame = tk.Frame(root)
    label_path = tk.Label(label_frame, text="文件名", width=40, anchor=tk.W).grid(row=0, column=0)
    label_height = tk.Label(label_frame, text="高（CM）", width=10, anchor=tk.W).grid(row=0, column=1)
    label_weight = tk.Label(label_frame, text="宽（CM）", width=10, anchor=tk.W).grid(row=0, column=2)
    label_screen = tk.Label(label_frame, text="去网纹", anchor=tk.W).grid(row=0, column=3)
    label_frame.pack()

    # canvas
    canvas = tk.Canvas(root, width=600, height=300, scrollregion=(0, 0, 300, 500))
    canvas.pack()

    # 图片frame
    img_process_frame = tk.Frame(canvas)
    img_process_frame.place(x=20, y=20)

    # Scrollbar
    vbar = tk.Scrollbar(canvas, orient=tk.VERTICAL)
    vbar.place(x=580, width=20, height=300)
    vbar.configure(command=canvas.yview)
    hbar = tk.Scrollbar(canvas, orient=tk.HORIZONTAL)  # 水平滚动条
    hbar.place(x=0, y=280, width=580, height=20)
    hbar.configure(command=canvas.xview)
    canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    canvas.create_window((90, 240), window=img_process_frame)

    # button frame
    button_frame = tk.Frame(root)
    button_frame.pack()

    # buttons
    btn_select_imgs = tk.Button(button_frame, text="选择图片", command=select_imgs).grid(row=0, column=0)
    btn_select_folder = tk.Button(button_frame, text="选择路径", command=select_folder).grid(row=0, column=1)
    btn_select_screen = tk.Button(button_frame, text="去网纹", command=screen).grid(row=0, column=2)
    btn_process = tk.Button(button_frame, text="处理", command=process).grid(row=0, column=3)

    # set height and width frame
    hw_frame = tk.Frame(root)
    hw_frame.pack()

    # widgets
    label_fast_height = tk.Label(hw_frame, text="高（CM）").grid(row=0, column=0)
    entry_fast_height = tk.Entry(hw_frame)
    entry_fast_height.grid(row=0, column=1)
    label_fast_width = tk.Label(hw_frame, text="宽（CM）").grid(row=0, column=2)
    entry_fast_width = tk.Entry(hw_frame)
    entry_fast_width.grid(row=0, column=3)
    btn_fast_set = tk.Button(hw_frame, text="快速设置", command=fast_set).grid(row=0, column=4)

    root.mainloop()
