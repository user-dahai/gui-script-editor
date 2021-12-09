# -*-coding:utf-8-*-

"""
截屏程序
"""

from win32 import win32api, win32gui, win32print
from win32.lib import win32con

from win32.win32api import GetSystemMetrics

import tkinter as tk
from PIL import ImageGrab
from io import BytesIO
import win32clipboard as clip
import time


def get_real_resolution():
    """获取真实的分辨率"""
    hDC = win32gui.GetDC(0)
    # 横向分辨率
    w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    # 纵向分辨率
    h = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    return w, h


def get_screen_size():
    """获取缩放后的分辨率"""
    w = GetSystemMetrics(0)
    h = GetSystemMetrics(1)
    return w, h


real_resolution = get_real_resolution()
screen_size = get_screen_size()

# Windows 设置的屏幕缩放率
# ImageGrab 的参数是基于显示分辨率的坐标，而 tkinter 获取到的是基于缩放后的分辨率的坐标
screen_scale_rate = round(real_resolution[0] / screen_size[0], 2)


class Box:

    def __init__(self):
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None

    def is_none(self):
        return self.start_x is None or self.end_x is None

    def set_start(self, x, y):
        self.start_x = x
        self.start_y = y

    def set_end(self, x, y):
        self.end_x = x
        self.end_y = y

    def box(self):
        lt_x = min(self.start_x, self.end_x)
        lt_y = min(self.start_y, self.end_y)
        rb_x = max(self.start_x, self.end_x)
        rb_y = max(self.start_y, self.end_y)
        return lt_x, lt_y, rb_x, rb_y

    def center(self):
        center_x = (self.start_x + self.end_x) / 2
        center_y = (self.start_y + self.end_y) / 2
        return center_x, center_y


class SelectionArea:

    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.area_box = Box()

    def empty(self):
        return self.area_box.is_none()

    def set_start_point(self, x, y):
        self.canvas.delete('area', 'lt_txt', 'rb_txt')
        self.area_box.set_start(x, y)
        # 开始坐标文字
        self.canvas.create_text(
            x, y - 10, text=f'({x}, {y})', fill='red', tag='lt_txt')

    def update_end_point(self, x, y):
        self.area_box.set_end(x, y)
        self.canvas.delete('area', 'rb_txt')
        box_area = self.area_box.box()
        # 选择区域
        self.canvas.create_rectangle(
            *box_area, fill='black', outline='red', width=2, tags="area")
        self.canvas.create_text(
            x, y + 10, text=f'({x}, {y})', fill='red', tag='rb_txt')


class ScreenShot():

    def __init__(self, path, scaling_factor=2):
        self.win = tk.Tk()
        # self.win.tk.call('tk', 'scaling', scaling_factor)
        self.width = self.win.winfo_screenwidth()
        self.height = self.win.winfo_screenheight()

        # 无边框，没有最小化最大化关闭这几个按钮，也无法拖动这个窗体，程序的窗体在Windows系统任务栏上也消失
        self.win.overrideredirect(True)
        self.win.attributes('-alpha', 0.25)

        self.path = path
        self.is_selecting = False
        # self.path = path
        # 绑定按 右键 确认, Esc 退出
        self.win.bind('<Escape>', self.exit)
        self.win.bind('<Button-3>', self.confirm_screen_shot)
        self.win.bind('<ButtonPress-1>', self.select_start)
        self.win.bind('<B1-Motion>', self.select_done)
        self.win.bind('<Return>', self.change_selection_area)

        self.canvas = tk.Canvas(self.win, width=self.width,
                                height=self.height)
        self.canvas.pack()
        self.area = SelectionArea(self.canvas)
        self.win.mainloop()

    def exit(self, event):
        self.win.destroy()

    def clear(self):
        self.canvas.delete('area', 'lt_txt', 'rb_txt')
        self.win.attributes('-alpha', 0)

    def capture_image(self):
        if self.area.empty():
            return None
        else:
            box_area = [x * screen_scale_rate for x in self.area.area_box.box()]
            self.clear()
            print(f'Grab: {box_area}')
            img = ImageGrab.grab(box_area)
            return img

    def copy_image(self, img):

        output = BytesIO()
        img.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()
        clip.OpenClipboard()  # 打开剪贴板
        clip.EmptyClipboard()  # 先清空剪贴板
        clip.SetClipboardData(win32con.CF_DIB, data)  # 将图片放入剪贴板
        clip.CloseClipboard()

    def copy_text(self, text):

        clip.OpenClipboard()  # 打开剪贴板
        clip.EmptyClipboard()  # 先清空剪贴板
        clip.SetClipboardData(win32con.CF_UNICODETEXT, text)  # 将文本放入剪贴板
        clip.CloseClipboard()
        print(text)

    def confirm_screen_shot(self, event):
        img = self.capture_image()
        self.win.destroy()

        if img is not None:
            img_name = "%d.png" % time.time()
            img_file = self.path + "//" + img_name
            img.save(img_file)
            # self.copy_image(img)

            self.copy_text(img_name)
            img.close()
            # img.show()

    def select_start(self, event):
        self.is_selecting = True
        self.area.set_start_point(event.x, event.y)
        # print('Select', event)

    def change_selection_area(self, event):
        if self.is_selecting:
            self.area.update_end_point(event.x, event.y)
            # print(event)

    def select_done(self, event):
        self.area.update_end_point(event.x, event.y)
        self.is_selecting = False


def main(path):
    ScreenShot(path)


# 获取按下的建
"""
root = tk.Tk()
def func(event):
    print(event.keysym)
root.bind("<Key>", func)
root.mainloop()
"""

if __name__ == '__main__':
    main(path="../")
