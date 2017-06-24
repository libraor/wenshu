#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 23:42:40 2017

@author: Leon-zedalawyer
"""

from selenium import webdriver #webdriver 方法 用于抓取页面
from bs4 import BeautifulSoup #BeautifulSoup 方法 用于解析页面
import re  #正则表达式模块
import urllib #转换网址编码
import pandas

def num(key):   #取得关键词的页数，key为关键词，页数为返回值
    #driver = webdriver.PhantomJS() #开启浏览器
    key = urllib.parse.urlencode({'':key})  #关键词转码 urlencode转化必须为字典形式
    url = "http://www.legalminer.com/search/cases?t" + str(key)
    driver.get(url)
    num = int(re.findall('搜索共找到 (.*?) 份裁判文书',driver.page_source)[0])//10+1  #整除取页数+1
    #print(num)
    return num


def url(key,num):   #把关键字转化为网址，key为关键词，url为返回值
    key = urllib.parse.urlencode({'':key})  #关键词转码 urlencode转化必须为字典形式
    url = []
    for i in range(1,num+1): #生成关键词网址列表数组 i为网址中的页码
        url = url +[ "http://www.legalminer.com/ajax_search/get_html?t" + str(key) + "&status=false&userId=&page=" + str(i) + "&searchType=cases&sortField=judgeDate&UserId=&sortType=DESC"] #案例按由新到旧排列
    return url

def list(data):  #从网页解析代码，并生成案例页网页链接列表
    list1 = re.findall('cases\?id=(.*?)&amp;amp;t=',data) #获取链接id 方案一
    list2 = [] #去重
    [list2.append(i) for i in list1 if not i in list2] 
    #print (list2)
    
    def foo(lst,s): #还原链接
        return [s + str(i) for i in lst]
    
    s = 'http://www.legalminer.com/cases?id=' #增加字段
    list3 = foo(list2,s) #理脉链接列表
    #print(list3)
    return list3

def content(links): #解析理脉-links 返回标题列表
    title = [] #返回标题列表
    for i in range(0,len(links)): #遍历links中的链接
        driver.get(links[i])  #链接到第i个案例
        content = driver.page_source
        #print (data)
        
        #提取各关键字段 正则 BeautifulSoup
        #title = (BeautifulSoup(re.findall('<div class=\"title fontc6 mb10\">(.*?)</div>',content)[0],'html.parser')).text
        
        #anhao = (BeautifulSoup(re.findall('<div style=\"TEXT-ALIGN: right; LINE-HEIGHT: 25pt; MARGIN: 0.5pt 0cm;  FONT-FAMILY: 宋体;FONT-SIZE: 12pt; ">(.*?)</div>',content)[0],'html.parser')).text #存在溢出情况，暂不使用
        #yuangao = re.findall('<div class="title fontc6 mb10">(.*?)与',content) #暂无法准确提取
        #beigao = re.findall('被告(.*?)["，""。"]',content) #暂无法准确提取
        
        #dangshiren = (BeautifulSoup(re.findall('<span litigantpart=\"\">(.*?)</div><div class=\"section\" id=\"proceeding\">',content)[0],'html.parser')).text
        #proceeding = (BeautifulSoup(re.findall('<span proceeding=\"\">(.*?)<div class=\"section\" id=\"argued\">',content)[0],'html.parser')).text
        #argued =  (BeautifulSoup(re.findall('<span argued=\"\">(.*?)<div class=\"section\" id=\"fact\"',content)[0],'html.parser')).text
        #fact = (BeautifulSoup(re.findall('<span fact=\"\">(.*?)<div class=\"section\" id=\"courtconsider\"',content)[0],'html.parser')).text
        #courtconsider = (BeautifulSoup(re.findall('<span courtconsider=\"\">(.*?)<div class=\"section\" id=\"result\"',content)[0],'html.parser')).text
        #result = (BeautifulSoup(re.findall('<span result=\"\">(.*?)<div class=\"col-xs-12 col-sm-3 col-md-3 cont_right_nav pos\">',content,re.S)[0],'html.parser')).text #re.S .可匹配换行符
        
        #print(title)
        #print(yuangao,beigao)
        #print(dangshiren,proceeding,argued,fact,courtconsider,result)
        
        title = title + [(BeautifulSoup(re.findall('<div class=\"title fontc6 mb10\">(.*?)</div>',content)[0],'html.parser')).text]
    return title

driver = webdriver.PhantomJS() #开启浏览器


key = '建设银行'  #关键词
num = num(key) #生成关键词页数
if num >= 2: #控制检索网页数量
    num = 2
#print(num)

url = url(key,num) #生成关键词网址

links = [] #具体内容网址列表
for i in range(0,len(url)): #遍历链接
    driver.get(url[i]) #载入页面
    data = driver.page_source #载入页面源码
    links = links + list(data) #从网页解析代码，并生成案例页网页链接列表

#print(links)

content = content(links)


df = pandas.DataFrame(content)
df.to_excel('title.xlsx')




driver.quit() #关闭浏览器



