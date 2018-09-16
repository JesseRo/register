import json
import random
import sys
from PyQt5 import QtNetwork

from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor, QWebEngineCookieStore

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtCore import QUrl
from urllib.parse import urlparse
import requests
import threading
import logging as logger

jsonEncoder = json.JSONEncoder()

cards = [4347696262018939, 4347696262018947,
         4347696262018954,
         4347696262018962,
         4347696262018970,
         4347696262018988,
         4347696262018996,
         4347696262019002,
         4347696262019010,
         4347696262019028,
         4347696262019036,
         4347696262019044,
         4347696262019051,
         4347696262019069,
         4347696262019077,
         4347696262019085,
         4347696262019093,
         4347696262019101,
         4347696262019119,
         4347696262019127,
         4347696262019135,
         4347696262019143,
         4347696262019150,
         4347696262019168,
         4347696262019176,
         4347696262019184,
         4347696262019192,
         4347696262019200,
         4347696262019218,
         4347696262019226,
         4347696262019234,
         4347696262019242,
         4347696262019259,
         4347696262019267,
         4347696262019275,
         4347696262019283,
         4347696262019291,
         4347696262019309,
         4347696262019317
         ]


class NameGenerator:
    def __init__(self):
        self.name = None
        self.mail = None

    def get_user_name(self, new=False):
        if new or self.name is None:
            name = alpha_beta[random.randint(0, len(alpha_beta) - 11)]
            for i in range(15):
                name += alpha_beta[random.randint(0, len(alpha_beta) - 1)]
            self.name = name
            return self.name
        else:
            return self.name

    def get_email(self, new=False):
        if new or self.mail is None:
            mail = alpha_beta[random.randint(0, len(alpha_beta) - 11)]
            for i in range(10):
                mail += alpha_beta[random.randint(0, len(alpha_beta) - 1)]
            mail += '@'
            for i in range(5):
                mail += alpha_beta[random.randint(0, len(alpha_beta) - 1)]
            mail += '.com'
            self.mail = mail
            return self.mail
        else:
            return self.mail


ng = NameGenerator()

alpha_beta = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890'

twitch_url = 'https://www.twitch.tv/directory'
amazon_url = 'https://twitch.amazon.com/'
amazon_url_signin = 'https://www.amazon.com/ap/signin'
amazon_url_register = 'https://www.amazon.com/ap/register'
bind_url = 'https://twitch.amazon.com/link'
card_url = 'https://www.amazon.com/gp/prime/pipeline/membersignup'

proxy_provider_url = "http://ip.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=0&fa=0" \
                     "&fetch_key=&qty=1&time=1&pro=&city=&port=1&format=txt&ss=1&css=&dt=1&specialTxt=3&specialJson= "

captcha_request_payload = {
    'key': 'aeb9f9d48d5f07f50f8711cd825a57b8',
    'method': 'userrecaptcha',
    'pageurl': twitch_url,
    'googlekey': None,
    'json': 1
}
captcha_response_payload = {
    'key': 'aeb9f9d48d5f07f50f8711cd825a57b8',
    'action': 'get',
    'id': None,
    'json': 1
}
captcha_request_url = 'http://2captcha.com/in.php'
captcha_response_url = 'http://2captcha.com/res.php'

post_payload = {
    "username": None,
    "password": "12345678",
    "email": None,
    "birthday": {
        "day": 11,
        "month": 8,
        "year": 1988
    },
    "client_id": None,
    "captcha": {
        "key": None,
        "value": None
    }
}

amazon_register_payload = {
    "username": None,
    "password": 123456,
    "email": None,
    "repeat": 123456
}

card_bind_payload = {
    "name": "Walter",
    "number": None,
    "month": 6,
    "year": 2020
}


def get_js(path):
    with open(path) as f:
        js = f.read()
        print(js)
        return js


def on_done():
    logger.info(str(page.url()))
    url = str(page.url())
    if twitch_url in url:
        js = get_js("inject/twitch.js")
        page.runJavaScript(js)
        page.profile().cookieStore().loadAllCookies()
    elif amazon_url in url or amazon_url_signin in url:
        js = get_js('inject/amazonLogin.js')
        page.runJavaScript(js)
        page.profile().cookieStore().loadAllCookies()
    elif amazon_url_register in url:
        js = get_js('inject/amazonRegister.js')
        payload = amazon_register_payload.copy()
        payload['username'] = ng.get_user_name()
        payload['email'] = ng.get_email()
        js = js.replace('${account}', jsonEncoder.encode(payload))
        page.runJavaScript(js)
        page.profile().cookieStore().loadAllCookies()
    elif bind_url in url:
        js = "document.querySelector('[value=\"Confirm\"]').click();"
        page.runJavaScript(js)
        page.profile().cookieStore().loadAllCookies()
    elif card_url in url:
        js = get_js('inject/bind.js')
        payload = card_bind_payload.copy()
        payload['number'] = cards[0]
        js = js.replace('${card}', jsonEncoder.encode(payload))
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
    payload['client_id'] = 'kimne78kx3ncx6brgo4mv6wki5h1ko'
    payload['captcha']['key'] = key
    payload['captcha']['value'] = captcha
    payload['email'] = ng.get_email(True)
    js = js.replace('${payload}', jsonEncoder.encode(payload))
    logger.debug("payload：%r" % payload)
    logger.debug("js: %s" % js)
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
# profile.clearHttpCache()
# profile.clearAllVisitedLinks()
# pCookie = profile.cookieStore()
# pCookie.deleteAllCookies()
# pCookie.deleteSessionCookies()
profile.setRequestInterceptor(interceptor)

page = QWebEnginePage(profile, view)
page.loadFinished.connect(on_done)
view.setPage(page)
page.setUrl(QUrl(twitch_url))
view.show()
sys.exit(app.exec_())
