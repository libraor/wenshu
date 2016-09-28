# -*- coding: utf-8 -*-

try:
    from PySide.QtGui import *
    from PySide.QtCore import *
    from PySide.QtWebKit import *
    from Side.QtNetwork import *

except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *
    from PyQt4.QtWebKit import *
import requests
import os
import sys
import lxml.html
import urllib2
import urlparse

def webkit_download(url): #抓取动态网页
    app = QApplication([])

    webview = QWebView()
    webview.request.setRawHeader ("User-Agent", "Mozilla 1.0")
    webview.loadFinished.connect(app.quit)
    webview.load(url)
    app.exec_() # delay here until download finished
    return webview.page().mainFrame().toHtml()


def parse(html):  #提取代码
    tree = lxml.html.fromstring(html)
   # print tree.cssselect('#result')[0].text_content()



def main():
    url = 'http://itslaw.com'
    #parse(webkit_download(url))
    print webkit_download(url)
    return

if __name__ == '__main__':
    main()
