# -*- coding: utf-8 -*-
# 导入程序运行必须模块
import os
import sys

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow,QGraphicsPixmapItem, QGraphicsScene
from main_window import Ui_MainWindow
from CourseRecommendExpertSystem import CourseRecommendExpertSystem
import xlrd
import requests
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3877.400 QQBrowser/10.8.4506.400'
}
#规则库线程类
class RulesThread(QThread):
    _signal = pyqtSignal(str)

    def __init__(self,courseName,graphicsView,label_course_name):
        self.courseName = courseName
        self.graphicsView = graphicsView
        self.label_course_name = label_course_name
        super(RulesThread,self).__init__()

    def run(self):
        course_list = self.getItem()
        #print(course_list)
        for course in course_list:
            if course['courseName'] == self.courseName:
                #获取课程main_graph_url
                main_graph_url = course['mainGraph']
                #对url发起请求获得图片
                try:
                    # 创建image文件夹
                    if not os.path.exists('./image'):
                        os.mkdir('./image')
                    picture_path = './image/' + self.courseName + '.jpg'
                    #如果图片不存在，则请求图片资源
                    if not os.path.exists(picture_path):
                        picture = requests.get(url=main_graph_url,headers=headers)
                        # 保存
                        with open(picture_path, 'wb') as f:
                            f.write(picture.content)
                    #Graphics View 控件显示图像
                    self.graphicsView.scene_img = QGraphicsScene()
                    self.imgShow = QPixmap()
                    self.imgShow.load(picture_path)
                    self.imgShowItem = QGraphicsPixmapItem()
                    self.imgShowItem.setPixmap(QPixmap(self.imgShow))
                    #self.imgShowItem.setPixmap(QPixmap(self.imgShow).scaled(131,  91))    #自己设定尺寸
                    self.graphicsView.scene_img.addItem(self.imgShowItem)
                    self.graphicsView.setScene(self.graphicsView.scene_img)
                    self.graphicsView.fitInView(QGraphicsPixmapItem(QPixmap(self.imgShow))) #图像自适应大小
                    #self.label_course_name.setText(self.courseName)
                    #发生送课程链接给主进程
                    text = "<style> a {text-decoration: none} </style> <a href=\"" + course['url'] + "\">" +course['courseName']
                    self._signal.emit(text)
                    #print(picture)
                except Exception as e:
                    print(e)
                    print("请求图片数据失败！")
                break

    #读取excel表,将每一行封装成字典，存入列表
    def getItem(self):
        data = xlrd.open_workbook("course_info.xlsx")
        table = data.sheets()[0]
        row = table.nrows
        col = table.ncols
        List = []
        for i in range(1, row):
            dict = {}
            for j in range(col):
                title = table.cell_value(0, j)
                value = table.cell_value(i, j)
                dict[title] = value
            List.append(dict)
        return List


#主窗口
class MyMainForm(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        self.conclusion.setPlaceholderText("请输入结论")
        self.premise1.setPlaceholderText("前提1")
        self.premise2.setPlaceholderText("前提2")
        self.premise3.setPlaceholderText("前提3")
        self.premise4.setPlaceholderText("前提4")
        self.premise5.setPlaceholderText("前提5")
        self.fact1.setPlaceholderText("事实1")
        self.fact2.setPlaceholderText("事实2")
        self.fact3.setPlaceholderText("事实3")
        self.fact4.setPlaceholderText("事实4")
        self.fact5.setPlaceholderText("事实5")
        # 调用CourseRecommendExpertSystem类中的read方法读取规则库
        self.CRESys = CourseRecommendExpertSystem(self.process)
        self.CRESys.read()
        rule_base = self.CRESys.rule_base
        #print(rule_base)
        for rule in rule_base:
            str_rule = '结论：'+rule[0][0]+' 前提：'
            for premise in rule[1]:
                str_rule += premise + ' '
            self.rules.append(str_rule+'\n')
        #开始推理按钮绑定信号
        self.startButton.clicked.connect(self.inference)
        #添加规则按钮绑定信号
        self.addButton.clicked.connect(self.add_rule)

    def inference(self):
        # 获取事实
        fact_list = []
        t = 0
        if self.fact1.text():
            fact_list.append(self.fact1.text())
            t = 1
        if self.fact2.text():
            fact_list.append(self.fact2.text())
            t = 1
        if self.fact3.text():
            fact_list.append(self.fact3.text())
            t = 1
        if self.fact4.text():
            fact_list.append(self.fact4.text())
            t = 1
        if self.fact5.text():
            fact_list.append(self.fact5.text())
            t = 1
        if not t:
            self.process.append("请输入至少一个事实！")
            self.process.moveCursor(self.process.textCursor().End)
            return
        #print(fact_list)
        courseName = self.CRESys.inference(fact_list)
        if courseName:
            #开启线程，获取课程相关信息
            #必须加self ,不然会闪退
            try:
                self.rules_thread = RulesThread(courseName,self.graphicsView,self.label_course_name)
                #绑定信号返回函数
                self.rules_thread._signal.connect(self.set_text)  # 进程连接回传到GUI的事件
                self.rules_thread.start()
            except:
                print("线程出错！")
    def set_text(self,text):
        self.label_course_name.setText(text)
        self.label_course_name.setOpenExternalLinks(True)

    def add_rule(self):
        #获取规则
        rules = []
        t = 0
        if self.conclusion.text():
            rules.append(self.conclusion.text())
        else:
            self.process.append("结论不能为空！")
            self.process.moveCursor(self.process.textCursor().End)
            return
        if self.premise1.text():
            t = 1
            rules.append(self.premise1.text())
        if self.premise2.text():
            t = 1
            rules.append(self.premise2.text())
        if self.premise3.text():
            t = 1
            rules.append(self.premise3.text())
        if self.premise4.text():
            t = 1
            rules.append(self.premise4.text())
        if self.premise5.text():
            t = 1
            rules.append(self.premise5.text())
        if not t:
            self.process.append("请输入至少一个前提！")
            self.process.moveCursor(self.process.textCursor().End)
            return
        #print(rules)
        try:
            self.CRESys.write(rules)
            self.process.append("规则添加成功！")
            self.process.moveCursor(self.process.textCursor().End)
            str_rule = '结论：' + rules[0] + ' 前提：'
            for i in range(len(rules)):
                if i == 0:
                    continue
                str_rule += rules[i] + ' '
            self.rules.append(str_rule + '\n')
            self.rules.moveCursor(self.rules.textCursor().End)
        except:
            self.process.append("规则添加失败！")
            self.process.moveCursor(self.process.textCursor().End)





if __name__ == "__main__":
    # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    # 初始化
    myWin = MyMainForm()
    #设置标题图标
    myWin.setWindowIcon(QIcon('./f.ico'))
    #设置标题
    #myWin.setWindowTitle('CET4_CET6真题一键下载(1989-2021)V1.2')
    # 将窗口控件显示在屏幕上
    myWin.show()
    # 程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())