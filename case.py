# -*- coding:utf-8 -*-
# @FileName  :design.py
# @Time      :17/08/2021 16:40
# @Author    :Alexation
import os
import sys
import requests
import parsel
import time
from random import randint
from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon
from PySide2.QtCore import Signal, QObject
from threading import Thread


class MySignals(QObject):
    text_print = Signal(str)


class Wallpaper:
    sort = 0
    signal_1 = 2
    signal_2 = 0
    sorts_name = ['动漫', '女生动漫', '明日方舟', '城市', '简约'
        , '科幻', '繁星', '英雄联盟', '太空', '航海王', '天空', '风景']

    def __init__(self):
        self.wp = QUiLoader().load('wallpaper.ui')
        self.wp.button.clicked.connect(self.handleCalc)
        self.wp.cb.currentIndexChanged.connect(self.selectionchange)
        self.wp.cb.addItems(self.sorts_name)
        self.wp.cb.addItems(self.sorts_name)
        self.wp.ms = MySignals()
        self.wp.ms.text_print.connect(self.gui)

    def selectionchange(self, i):
        self.sort = i

    def handleCalc(self):
        page = [2763, 2678, 58, 315, 539, 418, 208, 151, 336, 38, 764, 1311]
        anime = 'https://wallhaven.cc/search?q=id%3A1&page={}'.format(page[0])
        anime_girl = 'https://wallhaven.cc/search?q=id%3A5&sorting' \
                     '=random&ref=fp&seed=iYVJUK&page={}'.format(page[1])
        ark_nights = 'https://wallhaven.cc/search?q=id%3A85254&sorting' \
                     '=random&ref=fp&seed=AjNdEt&page={}'.format(page[2])
        cityscape = 'https://wallhaven.cc/search?q=id%3A13&sorting' \
                    '=random&ref=fp&seed=WWTFni&page={}'.format(page[3])
        minimalism = 'https://wallhaven.cc/search?q=id%3A2278&sorting' \
                     '=random&ref=fp&seed=lWjAhf&page={}'.format(page[4])
        science = 'https://wallhaven.cc/search?q=id%3A14&sorting' \
                  '=random&ref=fp&seed=WTiQci&page={}'.format(page[5])
        stars = 'https://wallhaven.cc/search?q=id%3A245&page={}'.format(page[6])
        legends = 'https://wallhaven.cc/search?q=id%3A537&sorting' \
                  '=random&ref=fp&seed=QYIBFK&page={}'.format(page[7])
        space = 'https://wallhaven.cc/search?q=id%3A32&page={}'.format(page[8])
        one_peace = 'https://wallhaven.cc/search?q=id%3A1394&page={}'.format(page[9])
        sky = 'https://wallhaven.cc/search?q=id%3A2729&page={}'.format(page[10])
        landscape = 'https://wallhaven.cc/search?q=id%3A711&sorting' \
                    '=random&ref=fp&seed=KMjcYz&page={}'.format(page[11])

        if self.wp.check.isChecked():
            self.signal_1 += 1
            if self.signal_1 % 2 == 1:
                self.wp.button.setText('停止')
                sorts = [anime, anime_girl, ark_nights, cityscape, minimalism, science
                    , stars, legends, space, one_peace, sky, landscape]

                base_url = sorts[self.sort]
                fold_name = self.sorts_name[self.sort]
                fold_path = self.sorts_name[self.sort] + '\\'

                thread = Thread(target=self.threadSend,
                                args=(base_url, fold_name, fold_path))
                thread.start()
            if self.signal_1 % 2 == 0:
                self.wp.button.setText('开始')
        else:
            msgBox1 = QMessageBox()
            msgBox1.setWindowTitle("( ゜-゜)つロ")
            msgBox1.setText('记得勾选"我已阅读《使用手册》"哦~')
            msgBox1.setStandardButtons(QMessageBox.Ok)
            msgBox1.setDefaultButton(QMessageBox.Ok)
            ret = msgBox1.exec_()

    def gui(self, text):
        self.wp.infoBox.append(str(text))
        self.wp.infoBox.ensureCursorVisible()

    def threadSend(self, base_url, fold_name, fold_path):
        try:
            self.signal_2 = 1
            sleep_time = randint(1, 201)
            ua = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) '
                 'Gecko/20100101 Firefox/91.0')
            headers = {'User-Agent': ua}

            response = requests.get(url=base_url, headers=headers)
            response.encoding = response.apparent_encoding

            data = response.text
            html_data = parsel.Selector(data)

            data_list = html_data.xpath('//section[@class="thumb-listing-page"]'
                                        '/ul/li/figure/a/@href').extract()

            self.wp.ms.text_print.emit(f"即将下载"
                    f"{self.sorts_name[self.sort]}壁纸，占存较大，客官可先小睡下哦~~~")
            for any_list in data_list:
                if self.signal_1 % 2 == 1:
                    if not os.path.exists(fold_name):
                        os.mkdir(fold_name)
                    response_2 = requests.get(url=any_list, headers=headers).text
                    response_2_data = parsel.Selector(response_2)
                    img_url = response_2_data.xpath('//div[@class="scrollbox"]/img/@src').extract_first()
                    img_data = requests.get(url=img_url, headers=headers).content
                    file_name = 'Downloading: ' + img_url.split('/')[-1]
                    with open(fold_path + img_url.split('/')[-1], mode='wb') as f:
                        self.wp.ms.text_print.emit(file_name)
                        f.write(img_data)
                    time.sleep(sleep_time / 100)
                else:
                    break

            self.wp.ms.text_print.emit("感谢使用本程序")
            self.signal_2 = 0
        except requests.URLRequired as e:
            self.wp.ms.text_print.emit("出现异常，请查看网络连接或过段时间重试\n")
        except requests.ConnectionError as e:
            self.wp.ms.text_print.emit("出现异常，请查看网络连接或过段时间重试\n")
        except requests.HTTPError as e:
            self.wp.ms.text_print.emit("出现异常，请查看网络连接或过段时间重试\n")
        except requests.Timeout as e:
            self.wp.ms.text_print.emit("出现异常，请查看网络连接或过段时间重试\n")


app = QApplication(sys.argv)
app.setWindowIcon(QIcon('logo.png'))
wallpaper_catch = Wallpaper()
wallpaper_catch.wp.show()

msgBox = QMessageBox()
msgBox.setWindowTitle("Warning")
msgBox.setText("退出程序前一定要停止下载！")
msgBox.setInformativeText("不然我会偷偷下载的！(严肃")
msgBox.setStandardButtons(QMessageBox.Ok)
msgBox.setDefaultButton(QMessageBox.Ok)
ret = msgBox.exec_()

sys.exit(app.exec_())

if __name__ == "__main__":
    run_code = 0
