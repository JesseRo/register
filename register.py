import sys
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor, QWebEngineUrlRequestInfo

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtCore import QUrl


def on_done():
    print(page.url())
    with open('ddd.js') as f:
        js = f.read()
        print(js)
        page.runJavaScript(js)


class TwitchInterceptor(QWebEngineUrlRequestInterceptor):
    def interceptRequest(self, ri):
        if 'https://passport.twitch.tv/register' in str(ri.requestUrl()):
            pass


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
page.setUrl(QUrl("http://www.twitch.tv/directory"))
view.show()
sys.exit(app.exec_())
