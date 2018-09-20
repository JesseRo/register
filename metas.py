import json

twitch_url = 'https://www.twitch.tv/directory'
amazon_url_signin = 'https://www.amazon.com/ap/signin'
amazon_url_register = 'https://www.amazon.com/ap/register'
bind_url = 'https://twitch.amazon.com/link'
card_url = 'https://www.amazon.com/gp/prime/pipeline/membersignup'
final_url = ''

proxy_provider_url = "http://api.ip.data5u.com/api/get.shtml?order=9dabc31d95ab426645346f9660f6189d&num=1&area=%E9%9D" \
                     "%9E%E4%B8%AD%E5%9B%BD&carrier=0&protocol=0&an1=1&an2=2&an3=3&sp1=1&sp2=2&sp3=3&sort=1&system=1" \
                     "&distinct=0&rettype=1&seprator=%0D%0A "

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

jsonEncoder = json.JSONEncoder()
