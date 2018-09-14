import json
import sys
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor, QWebEngineUrlRequestInfo

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtCore import QUrl
from urllib.parse import urlparse
import requests
import threading
import logging as logger

jsonEncoder = json.JSONEncoder()


twitch_url = 'https://www.twitch.tv/directory'
amazon_url = 'https://twitch.amazon.com/'
amazon_url_signin = 'https://www.amazon.com/ap/signin'
amazon_url_register = 'https://www.amazon.com/ap/register'
bind_url = 'https://twitch.amazon.com/link'
card_url = 'https://www.amazon.com/gp/prime/pipeline/membersignup'

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
    "email": "43221@asfsda.com",
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
    "email": '43221@asfsda.com"',
    "repeat": 123456
}


def get_js(path):
    with open(path) as f:
        js = f.read()
        print(js)
        return js


def get_user_name(new=False):
    if new:
        return ''
    else:
        return 'jlfksfjl123u78432'


def on_done():
    logger.info(page.url())
    url = page.url()
    if twitch_url in url:
        js = get_js("inject/twitch.js")
        page.runJavaScript(js)
    elif amazon_url in url or amazon_url_signin in url:
        js = get_js('inject/amazonLogin.js')
        page.runJavaScript(js)
    elif amazon_url_register in url:
        js = get_js('inject/amazonRegister.js')
        payload = amazon_register_payload.copy()
        payload['username'] = get_user_name()
        js = js.replace('${account}', jsonEncoder.encode(payload))
        page.runJavaScript(js)
    elif bind_url in url:
        js = "$('[value=Confirm]').click()"
        page.runJavaScript(js)
    elif card_url in url:
        js = get_js('inject/bind.js')


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
    payload['username'] = get_user_name()
    payload['client_id'] = 'kimne78kx3ncx6brgo4mv6wki5h1ko'
    payload['captcha']['key'] = key
    payload['captcha']['value'] = captcha
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
