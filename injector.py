from PyQt5.QtWebEngineWidgets import QWebEnginePage

from metas import *
from ng import ng

__all__ = [
    'get_js',
    'AbstractInjector', 'UrlContainsInjector', 'TwitchInjector', 'AmazonRegisterInjector',
    'AmazonSigninInjector', 'BindInjector', 'CardInjector'
]


def get_js(path):
    with open(path) as f:
        js = f.read()
        return js


class AbstractInjector:
    def diagnose(self, url: str):
        raise NotImplementedError('subclass must override this method..')

    def inject(self):
        raise NotImplementedError('subclass must override this method..')


class UrlContainsInjector(AbstractInjector):
    def __init__(self, url):
        self.url = url

    def inject(self):
        raise NotImplementedError('subclass must override this method..')

    def diagnose(self, url: str):
        return self.url in url


class TwitchInjector(UrlContainsInjector):
    def __init__(self):
        super().__init__(twitch_url)

    def inject(self):
        return get_js("inject/twitch.js")


class AmazonSigninInjector(UrlContainsInjector):
    def __init__(self):
        super().__init__(amazon_url_signin)

    def inject(self):
        return get_js('inject/amazonLogin.js')


class AmazonRegisterInjector(UrlContainsInjector):
    def __init__(self):
        super().__init__(amazon_url_register)

    def inject(self):
        js = get_js('inject/amazonRegister.js')
        payload = amazon_register_payload.copy()
        payload['username'] = ng.get_user_name()
        payload['email'] = ng.get_email()
        return js.replace('${account}', jsonEncoder.encode(payload))


class BindInjector(UrlContainsInjector):
    def __init__(self):
        super().__init__(bind_url)

    def inject(self):
        return """document.querySelector('[value="Confirm"]').click();"""


class CardInjector(UrlContainsInjector):
    def __init__(self):
        super().__init__(card_url)

    def inject(self):
        js = get_js('inject/bind.js')
        payload = card_bind_payload.copy()
        payload['number'] = cards[0]
        return js.replace('${card}', jsonEncoder.encode(payload))
