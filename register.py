from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl


page = None
def on_done():
    print(page.url())
    with open('ddd.js') as f:
        js = f.read()
        print(js)
        page.runJavaScript(js)


app = QApplication([])
view = QWebEngineView()
page = view.page()
view.page().profile().clearHttpCache()
view.page().profile().clearAllVisitedLinks()
pCookie = view.page().profile().cookieStore()
pCookie.deleteAllCookies()
pCookie.deleteSessionCookies()

view.load(QUrl("http://www.twitch.tv/directory"))
# view.load(QUrl("http://baidu.com"))
view.show()
page.setDevToolsPage(view.page())

view.loadFinished.connect(on_done)
app.exec_()