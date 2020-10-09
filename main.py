#!/usr/bin/env python
# _*_ coding:utf-8 _*_

# @Author: Merack
# @Email: merack@qq.com
import os
import sys
import schoolNet
import configparser
import config as cfg


class Menu():
    def __init__(self):
        self.config = configparser.ConfigParser()
        if not os.path.exists(cfg.config_path + cfg.config_name):
            self.config["account"] = {
                "studentID": '',
                "password": '',
                "service": ''
            }
            with open(cfg.config_path + cfg.config_name, 'w', encoding='utf-8') as f:
                self.config.write(f)

        if cfg.debug:
            self.config.read(cfg.config_path + cfg.dev_config_name, encoding='utf-8')
        else:
            self.config.read(cfg.config_path + cfg.config_name, encoding='utf-8')

        self.studentID = self.config['account']['studentID']
        self.password = self.config['account']['password']
        self.service = self.config['account']['service']
        self.cookie = None
        self.serviceList = ['电信', '移动', '联通']
        self.choices = {
            "1": self.offline,
            "2": self.login,
            "3": self.showDevices,
            "4": self.offlineALL,
            "5": self.changeInfo,
            "q": self.quit
        }

    def displayMenu(self):
        print("""
        Operation Menu:
        1. 下线设备
        2. 登陆校园网
        3. 列出在线设备
        4. 下线所有设备
        5. 修改配置文件
        q. 退出程序
""")

    def run(self):
        self.check()
        self.cookie = schoolNet.serviceLogin(self.studentID, self.password)
        # self.test()
        while True:
            os.system('cls')
            self.displayMenu()
            try:
                choice = input("Enter an option: ")
            except Exception as e:
                print("Please input a valid option!")
                continue

            choice = str(choice).strip()
            action = self.choices.get(choice)
            if action:
                action()
            else:
                print("{0} is not a valid choice".format(choice))

    def test(self):
        print(self.studentID, self.password, self.service, self.cookie)
        input()

    def check(self):
        if not self.studentID or not self.password or not self.service:
            print("未在配置文件 " + os.path.abspath(cfg.config_path + cfg.config_name) + " 中检测到账号/密码/运营商,")
            self.changeInfo()

    def quit(self):
        print("\nThank you for using this script!\n")
        sys.exit(0)

    def offline(self):
        re = schoolNet.offline(self.studentID, self.cookie)
        if re != -1:
            print(re)
            os.system('pause')

    def offlineALL(self):
        choice = input("您确定要下线所有设备吗(yes/no)")
        if choice == 'yes' or choice == 'y':
            re = schoolNet.offline(self.studentID, self.cookie, True)
            if re != -1:
                print(re)
                os.system('pause')

    def login(self):
        print(schoolNet.login(self.studentID, self.password, self.service))
        os.system('pause')

    def showDevices(self):
        schoolNet.showDevices(None, self.cookie)
        os.system('pause')
        # input

    def getService(self):
        try:
            index = int(input("请选择运营商id: "))
            service = self.serviceList[index]
        except Exception as e:
            print("输入非法, 请输入正确的数值")
            return self.getService()
        else:
            return service

    def changeInfo(self):
        print("请手动输入信息~")
        self.studentID = input("学号: ")
        self.password = input("密码: ")
        print("""
运营商列表: 
    0. 电信
    1. 移动
    2. 联通
        """)

        self.service = self.getService()

        self.config['account']['studentID'] = self.studentID
        self.config['account']['password'] = self.password
        self.config['account']['service'] = self.service
        if cfg.debug:
            with open(cfg.config_path + cfg.dev_config_name, 'w', encoding='utf-8') as f:
                self.config.write(f)
        else:
            with open(cfg.config_path + cfg.config_name, 'w', encoding='utf-8') as f:
                self.config.write(f)
        print("配置文件写入成功, 路径:" + os.path.abspath(cfg.config_path + cfg.config_name))
        print("按任意键进入菜单")
        input()


if __name__ == '__main__':
    Menu().run()
