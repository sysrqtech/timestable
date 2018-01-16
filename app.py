import os
from urllib import parse

import cloudconvert
from imgurpython import ImgurClient
from bottle import Bottle, request

CC_KEY = "JwP_NWhtTamM56Edy67QbM8Zn-p1uWjxffgd9qzmem8RkJBUbafcVLCOszxV83dWXoYsmQqDoQdw0Umk0CNIrw"

IMGUR_KEY = "fd74deb2e272b12"
IMGUR_SECRET = "7f777d5fb7109bacc24e2d1667ed32494a6754a5"

MAILING_KEY = "api_8794_huFozpVbH5mKfOIkpgLKUaML"
MAILING_URI = "https://broadcast.vkforms.ru/api/v2/broadcast?"
LIST_ID = 193621

app = Bottle()
cc = cloudconvert.Api(CC_KEY)
imgur = ImgurClient(IMGUR_KEY, IMGUR_SECRET)


def send_mailing(image):



def docx_to_image(doc):
    process = cc.convert(dict(
        inputformat="docx",
        outputformat="png",
        input="upload",
        save=True,
        file=doc
    ))
    process.wait()
    return process.data


@app.post('/send')
def process():
    img = docx_to_image(request.body)


if os.environ.get("APP_LOCATION") == "heroku":
    port=int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, server="gunicorn")
else:
    app.run(host="localhost", port=8080, debug=True)
