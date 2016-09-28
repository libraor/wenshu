from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import *

USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1"


def customuseragent(url):
    print 'called for %s' % url
    return 'custom ua'


#inside a class
# class WebRequest(QWebView) ## the definition of the class uncomment to make use of the inheritance.

## from this tutorial
self={}
self.request = QNetworkRequest()
self.request.setUrl(QUrl(url))
self.request.setRawHeader("User-Agent",USER_AGENT)

## modified version of the original design
self.webkit = QtWebKit.QWebView()
self.webkit.page().userAgentForUrl = customuseragent
self.webkit.load(self.request)