import sys
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor, QWebEngineUrlRequestInfo

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtCore import QUrl
from urllib.parse import urlparse
import requests
import threading


init_url = 'https://www.twitch.tv/directory'
captcha_request_payload = {
    'key': 'aeb9f9d48d5f07f50f8711cd825a57b8',
    'method': 'userrecaptcha',
    'pageurl': init_url,
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


def get_js(path):
    with open(path) as f:
        js = f.read()
        print(js)
        return js


def on_done():
    print(page.url())
    js = get_js("ddd.js")
    page.runJavaScript(js)


def check_and_post(id):
    captcha_response_payload.update({'id': id})
    r = requests.get(captcha_response_url, captcha_response_payload)


class TwitchInterceptor(QWebEngineUrlRequestInterceptor):
    def interceptRequest(self, ri):
        url = str(ri.requestUrl())
        if 'https://recaptcha.net/recaptcha/api2/anchor' in str(ri.requestUrl()):
            result = urlparse(url[url.index('https://'):])
            params = result.query.split('&')
            for param in params:
                if param.startswith('k='):
                    key = param[2:]
                    captcha_request_payload.update({'googlekey': key})
                    r = requests.get(captcha_request_url, captcha_request_payload)
                    request_id = r.json().get('request')
                    t = threading.Timer(5, check_and_post, request_id)
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
page.setUrl(QUrl(init_url))
view.show()
sys.exit(app.exec_())
