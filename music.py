# -*- coding: utf-8 -*-
# @Time    : 2020/11/14 16:15
# @Author  : Joker_Jackson(罗忠诚)
# @Email   : ms_Joker_Jackson@163.com
# @File    : music.py
# @Software: PyCharm

import tkinter as tk
import os
from selenium import webdriver
import requests
from webdriver_manager.chrome import ChromeDriverManager

# https://music.163.com/#/search/m/?&s={}&type=1
# http://music.163.com/song/media/outer/url?id={}.mp3
# http://m10.music.126.net/
# 20201114165957/2f6dcd4610745bf29bf80607c1e804db/
# ymusic/ad08/7769/5699/430f13296206ea6a2bebf8335aa05178.mp3

# 第一部分
# 下载歌曲
def song_load(item):
    song_id = item['song_id']
    song_name = item['song_name']
    song_url = 'http://music.163.com/song/media/outer/url?id={}.mp3'.format(song_id)

    os.makedirs('music', exist_ok=True)
    path = 'music\{}.mp3'.format(song_name)
    # 文本框
    text.insert(tk.END,'歌曲：{}，正在下载...'.format(song_name))
    # 文本框滚动
    text.see(tk.END)
    # 更新
    text.update()
    song = requests.get(song_url).content
    with open(path,'ab') as fp:
        fp.write(song)
        fp.flush()
    # 文本框
    text.insert(tk.END,'下载完毕：{}，请试听...'.format(song_name))
    # 文本框滚动
    text.see(tk.END)
    # 更新
    text.update()


# 获取歌曲id
def get_music_name():
    name = entry.get()
    url = 'https://music.163.com/#/search/m/?&s={}&type=1'.format(name)
    # 隐藏浏览器
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=option)
    driver.get(url=url)
    driver.switch_to.frame('g_iframe')

    # 获取歌曲id
    req = driver.find_element_by_id('m-search')
    #     /html/body/div[3]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/div/a
    a_id = req.find_element_by_xpath('.//div[@class="item f-cb h-flag  "]/div[2]//a').get_attribute('href')
    song_id = a_id.split("=")[-1]
    song_name = req.find_element_by_xpath('.//div[@class="item f-cb h-flag  "]/div[2]//b').get_attribute('title')
    item = {}
    item['song_id'] = song_id
    item['song_name'] = song_name
    print(item.values())
    song_load(item)

# 第二部分
# 创建可视化界面
# 创建界面
root = tk.Tk()

# 添加标题
root.title("网易云音乐")
# 设置窗口大小
root.geometry("519x435")
# 标签空间
label = tk.Label(root,text="请输入下载歌曲：",font=('华文行楷',20))
# 标签定位
label.grid()  # 默认 row = 0, columns = 0
# 输入框
entry = tk.Entry(root, font=('隶书',20))
# grid网格
entry.grid(row=0,column=1)
# 列表框
text = tk.Listbox(root,font=('华文行楷',16),width=56,height=15)
text.grid(row=1,columnspan=2) # columnspan横跨两列
# 开始下载按钮框
btn1 = tk.Button(root, text='下载歌曲',font=('华文行楷',20),command=get_music_name)
btn1.grid(row=2, column=0,sticky=tk.W)
# 退出程序
btn2 = tk.Button(root, text='退出程序',font=('华文行楷',20),command=root.quit)
btn2.grid(row=2, column=1,sticky=tk.E)

# 显示界面
root.mainloop()

# pyinstaller -F -w(去除命令行窗口) -i 图片路径 py文件