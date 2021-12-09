# -*-coding:utf-8-*-
"""
初始化运行数据，ini文件管理
"""

import configparser
import os


class ProjectData:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.CurrentProject = {}
        self.column_name = []
        self.init_fail = False
        self.hide_while_run = "0"
        self.retry = "1"
        try:
            self.read_init()
        except Exception as e:
            print(e)
            self.init_fail = True
            self.base_data()
            self.read_init()

    def read_init(self):
        self.config.read("project.ini", encoding="utf-8")
        self.CurrentProject["dir"] = self.config.get("CurrentProject", "CurrentProjectDir")
        self.CurrentProject["name"] = self.config.get("CurrentProject", "CurrentProjectName")
        self.CurrentProject["path"] = self.CurrentProject["dir"] + "\\" + self.CurrentProject["name"]
        self.init_fail = os.path.exists(self.CurrentProject["path"])
        self.CurrentProject["status"] = "old"
        self.column_name = [self.config.get("ColumnName", "%d" % i) for i in range(1, 4)]
        self.hide_while_run = self.config.get("RunArgs", "HideWhileRun")
        self.retry = self.config.get("RunArgs", "ReTry")
        if self.init_fail:
            pass
        else:
            raise IOError("文件不存在 %s " % self.CurrentProject["path"])

    def update_project_att(self, option_type="path"):
        if option_type == "path":
            self.CurrentProject["name"] = os.path.basename(self.CurrentProject["path"])
            self.CurrentProject["dir"] = os.path.dirname(self.CurrentProject["path"])
        elif option_type == "init":
            self.CurrentProject["path"] = self.CurrentProject["dir"] + "\\" + self.CurrentProject["name"]
        print(self.CurrentProject)

    def save_project_data(self):
        print(self.CurrentProject)
        self.config.set("CurrentProject", "CurrentProjectDir", self.CurrentProject["dir"])
        self.config.set("CurrentProject", "CurrentProjectName", self.CurrentProject["name"])
        self.config.set("RunArgs", "HideWhileRun", self.hide_while_run)
        self.config.set("RunArgs", "ReTry", self.retry)
        self.config.write(open("project.ini", "w", encoding="utf-8"), )

    def base_data(self):
        if self.init_fail:
            data = """[CurrentProject]
CurrentProjectDir = %s
CurrentProjectName = script

[ColumnName]
1 = 指令类型
2 = 内容
3 = 重复次数

[RunArgs]
HideWhileRun = 0
ReTry = 1
""" % os.path.realpath("./")
            with open("project.ini", "w", encoding="utf-8") as f:
                f.write(data)
            os.makedirs("./script", exist_ok=True)
        else:
            pass
