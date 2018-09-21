import sys
from PyQt5 import QtNetwork

from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtCore import QUrl
from urllib.parse import urlparse
import requests
import threading
import logging as logger
from metas import *
from ng import ng
from injector import *


class Terminator(UrlContainsInjector):
    def __init__(self):
        super().__init__(final_url)

    def inject(self):
        profile.clearHttpCache()
        profile.clearAllVisitedLinks()
        pCookie.deleteAllCookies()
        pCookie.deleteSessionCookies()
        page.setUrl(QUrl('http://zhihu.com'))


injectors = [
    TwitchInjector(), AmazonSigninInjector(), AmazonRegisterInjector(), BindInjector(), CardInjector(), Terminator()
]
logger.getLogger().setLevel(10)


def finish():
    name = ng.get_user_name()
    password = '12345678'
    with open('result', "a+") as result:
        result.write("%s, %s" % (name, password))
        result.flush()
        result.close()


def on_done():
    logger.info(str(page.url()))
    url = str(page.url())

    for injector in injectors:
        if injector.diagnose(url):
            js = injector.inject()
            if isinstance(js, str):
                page.runJavaScript(js)
                page.profile().cookieStore().loadAllCookies()


def check_and_post(_id, key):
    captcha_response_payload.update({'id': _id})
    r = requests.get(captcha_response_url, captcha_response_payload)
    jn = r.json()
    if jn.get('status', 0) == 1:
        captcha = jn.get('request')
        logger.debug("captcha: " + captcha)
        on_captcha_resolved(key, captcha)
    else:
        t = threading.Timer(5, check_and_post, args=[_id, key])
        t.start()


def on_captcha_resolved(key, captcha):
    js = get_js('inject/post.js')
    payload = post_payload.copy()
    payload['username'] = ng.get_user_name(True)
    payload['client_id'] = 'pogofhumlor5rsdq403j17gs8a52iom'
    payload['captcha']['key'] = key
    payload['captcha']['value'] = captcha
    payload['email'] = ng.get_email(True)
    js = js.replace('${payload}', jsonEncoder.encode(payload))
    logger.debug("payload：%r" % payload)
    logger.info("js: %s" % js)
    page.runJavaScript(js)


class TwitchInterceptor(QWebEngineUrlRequestInterceptor):
    def interceptRequest(self, ri):
        url = str(ri.requestUrl())
        if 'https://recaptcha.net/recaptcha/api2/anchor' in str(ri.requestUrl()):
            result = urlparse(url[url.index('https://'):])
            params = result.query.split('&')
            logger.debug("captcha url params: %r" % params)
            for param in params:
                if param.startswith('k='):
                    key = param[2:]
                    logger.debug(key)
                    captcha_request_payload.update({'googlekey': key})
                    r = requests.get(captcha_request_url, captcha_request_payload)
                    request_id = r.json().get('request')
                    t = threading.Timer(5, check_and_post, args=[request_id, key])
                    t.start()


app = QApplication(sys.argv)
view = QWebEngineView()

res = requests.get(proxy_provider_url)
ip = res.text.split(":")
port = ip[1]
ip = ip[0]

proxy = QtNetwork.QNetworkProxy()
# Http访问代理
proxy.setType(QtNetwork.QNetworkProxy.HttpProxy)
# 代理ip地址HttpProxy
proxy.setHostName(ip)
# 端口号
proxy.setPort(int(port))
QtNetwork.QNetworkProxy.setApplicationProxy(proxy)

interceptor = TwitchInterceptor()
profile = QWebEngineProfile()
profile.clearHttpCache()
profile.clearAllVisitedLinks()
pCookie = profile.cookieStore()
pCookie.deleteAllCookies()
pCookie.deleteSessionCookies()
profile.setRequestInterceptor(interceptor)

profile.setPersistentCookiesPolicy(QWebEngineProfile.ForcePersistentCookies)

page = QWebEnginePage(profile, view)
page.loadFinished.connect(on_done)
view.setPage(page)
page.setUrl(QUrl(twitch_url))
view.show()
sys.exit(app.exec_())
