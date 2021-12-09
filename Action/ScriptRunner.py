# -*-coding:utf-8-*-

"""
脚本运行器，入口
base on b站 up 不高兴就喝水
"""

import pyautogui
import time
import xlrd
import pyperclip
import os


class ScriptRunner:
    signal = None
    pause = True

    def mouse_click(self, click_times, l_or_r, img, re_try, msg):
        """
        定义鼠标事件
        pyautogui库其他用法 https://blog.csdn.net/qingfengxd1/article/details/108270159
        """
        if re_try == 1:
            while True:
                if self.pause is False:
                    break
                location = pyautogui.locateCenterOnScreen(img, confidence=0.9)
                if location is not None:
                    pyautogui.click(location.x, location.y, clicks=click_times,
                                    interval=0.2, duration=0.2, button=l_or_r)
                    self.debug_print(msg)
                    break
                error = "未找到匹配图片,0.1秒后重试"
                self.debug_print(error)
                time.sleep(0.1)
        elif re_try == -1:
            i = 1
            while True:
                if self.pause is False:
                    break
                location = pyautogui.locateCenterOnScreen(img, confidence=0.9)
                if location is not None:
                    pyautogui.click(location.x, location.y, clicks=click_times,
                                    interval=0.2, duration=0.2, button=l_or_r)
                    self.debug_print(msg)
                error = "死循环第%d次：未找到匹配图片" % i
                self.debug_print(error)
                i = i + 1
                time.sleep(0.1)
        elif re_try > 1:
            i = 1
            while i < re_try + 1:
                if self.pause is False:
                    break
                location = pyautogui.locateCenterOnScreen(img, confidence=0.9)
                if location is not None:
                    pyautogui.click(location.x, location.y, clicks=click_times,
                                    interval=0.2, duration=0.2, button=l_or_r)
                self.debug_print(msg)
                error = "重复%d次: 第%d次" % (re_try, i)
                self.debug_print(error)
                i += 1
                time.sleep(0.1)

    def data_check(self, sheet):
        """
        数据检查
        cmdType.value  1.0 左键单击    2.0 左键双击  3.0 右键单击  4.0 输入  5.0 等待  6.0 滚轮
        ctype     空：0
                  字符串：1
                  数字：2
                  日期：3
                  布尔：4
                  error：5
        """
        check_cmd = True
        # 行数检查
        if sheet.nrows < 2:
            msg = "没数据啊哥"
            self.debug_print(msg)
            check_cmd = False
            return check_cmd

        # 每行数据检查
        i = 1
        while i < sheet.nrows:
            if self.pause is False:
                self.debug_print("停止运行")
                check_cmd = False
                break
            # 第1列 操作类型检查
            cmd_type = sheet.row(i)[0]
            if cmd_type.ctype != 2 or (cmd_type.value != 1.0 and cmd_type.value != 2.0 and cmd_type.value != 3.0
                                       and cmd_type.value != 4.0 and cmd_type.value != 5.0 and cmd_type.value != 6.0):
                msg = "第%d行,指令类型数据错误，指令类型（1 单击  2 双击  3 右键  4 输入  5 等待  6滚轮）" % i
                self.debug_print(msg)
                check_cmd = False
            # 第2列 内容检查
            cmd_value = sheet.row(i)[1]
            # 读图点击类型指令，内容必须为字符串类型
            if cmd_type.value == 1.0 or cmd_type.value == 2.0 or cmd_type.value == 3.0:
                if cmd_value.ctype != 1:
                    msg = "第%d行,内容数据错误，点击类型指令，内容必须为图片名称" % i
                    self.debug_print(msg)
                    check_cmd = False
            # 输入类型，内容不能为空
            if cmd_type.value == 4.0:
                if cmd_value.ctype == 0:
                    msg = "第%d行,内容数据错误，输入类型，内容不能为空" % i
                    self.debug_print(msg)
                    check_cmd = False
            # 等待类型，内容必须为数字
            if cmd_type.value == 5.0:
                try:
                    float(cmd_value.value)
                except Exception as e:
                    print(e)
                    msg = "第%d行,内容数据错误，等待事件，内容必须为数字" % i
                    self.debug_print(msg)
                    check_cmd = False
            # 滚轮事件，内容必须为数字
            if cmd_type.value == 6.0:
                try:
                    float(cmd_value.value)
                except Exception as e:
                    msg = "第%d行,内容数据错误，滚轮事件，内容必须为数字" % i
                    self.debug_print(msg)
                    check_cmd = False
            i += 1
        return check_cmd

    # 任务
    def main_work(self, sheet, path):
        i = 1
        while i < sheet.nrows:
            if self.pause is False:
                self.debug_print("停止运行")
                break
            # 取本行指令的操作类型
            cmd_type = sheet.row(i)[0]
            if cmd_type.value == 1.0:
                # 取图片名称
                img = path + "//" + sheet.row(i)[1].value
                re_try = 1
                if sheet.row(i)[2].ctype == 2 and sheet.row(i)[2].value != 0:
                    re_try = sheet.row(i)[2].value
                msg = "左键单击：" + img
                self.mouse_click(1, "left", img, re_try, msg)
            # 2代表双击左键
            elif cmd_type.value == 2.0:
                # 取图片名称
                img = path + "//" + sheet.row(i)[1].value
                # 取重试次数
                re_try = 1
                if sheet.row(i)[2].ctype == 2 and sheet.row(i)[2].value != 0:
                    re_try = sheet.row(i)[2].value
                msg = "左键双击：" + img
                self.mouse_click(2, "left", img, re_try, msg)

            # 3代表右键
            elif cmd_type.value == 3.0:
                # 取图片名称
                img = path + "//" + sheet.row(i)[1].value
                # 取重试次数
                re_try = 1
                msg = "右键单击：" + img
                if sheet.row(i)[2].ctype == 2 and sheet.row(i)[2].value != 0:
                    re_try = sheet.row(i)[2].value
                self.mouse_click(1, "right", img, re_try, msg)

                # 4代表输入
            elif cmd_type.value == 4.0:
                input_value = sheet.row(i)[1].value
                pyperclip.copy(input_value)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.5)
                msg = "输入：" + input_value
                self.debug_print(msg)
                # 5代表等待
            elif cmd_type.value == 5.0:
                # 取图片名称
                wait_time = float(sheet.row(i)[1].value)
                time.sleep(wait_time)
                msg = "等待%d秒" % wait_time
                self.debug_print(msg)
            # 6代表滚轮
            elif cmd_type.value == 6.0:
                # 取图片名称
                scroll = sheet.row(i)[1].value
                pyautogui.scroll(int(scroll))
                msg = "滚轮滑动%d距离" % int(scroll)
                self.debug_print(msg)
            i += 1

    def debug_print(self, msg):
        if self.signal is None:
            print(msg)
        else:
            print(msg)
            self.signal.emit(msg)

    def main(self, file, signal=None, key=1):
        try:
            self.signal = signal
            # 打开文件
            f = xlrd.open_workbook(filename=file)
            # 通过索引获取表格sheet页
            sheet = f.sheet_by_index(0)
            path = os.path.dirname(file)

            self.debug_print('\n====================start====================')

            # 数据检查
            self.debug_print("数据检查中...")
            check_cmd = self.data_check(sheet)

            if check_cmd:
                self.debug_print("脚本准备就绪，运行%d次" % key)
                # 循环拿出每一行指令
                for i in range(key):
                    self.debug_print("\n第%d次运行" % (i+1))
                    self.main_work(sheet, path)

                    time.sleep(0.1)
                    self.debug_print("等待0.1秒，第%d次运行结束\n" % (i+1))
            else:
                msg = '输入有误或者已经退出!'
                self.debug_print(msg)

        except Exception as e:
            self.debug_print(e.__str__())


if __name__ == '__main__':
    # 打开文件
    wb = xlrd.open_workbook("../cmd.xls")
    # 通过索引获取表格sheet页
    sheet1 = wb.sheet_by_index(0)
    runner = ScriptRunner()
    runner.main(sheet1)
