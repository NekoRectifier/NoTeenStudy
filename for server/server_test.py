# -*- coding : utf-8-*-

import PIL.Image as Image
import io
import base64
import requests

data = {
    'url': 'http://124.222.5.227:8080?course=123456',
    'token': '#your screenmaster api token#',
    'width': '828',
    'height': '1366',
    'delay': '50',
    'device': 'mobile'
}

r = requests.post("https://www.screenshotmaster.com/api/v1/screenshot", data=data)

print(r.status_code)

print(r.encoding)

print(r.content)

img = Image.open(io.BytesIO(r.content))
img.show()
