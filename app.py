# coding=utf-8
import os
from base64 import encodebytes

import requests
import cloudconvert
from imgurpython import ImgurClient
from bottle import Bottle, request


def required_env(name):
    """
    Raise error, if environment variable can't be found, else return it's value
    """
    value = os.environ.get(name)
    if value is None:
        raise AttributeError("Environment variable %s is not set" % name)
    return value


CC_KEY = required_env("CLOUDCONVERT_KEY")

LIST_ID = int(required_env("MAILING_LIST_ID"))
MAILING_URI = "https://broadcast.vkforms.ru/api/v2/broadcast?token=" + required_env("MAILING_KEY")

app = Bottle()
cc = cloudconvert.Api(CC_KEY)
imgur = ImgurClient(IMGUR_KEY, IMGUR_SECRET)


def vk_send(image_url):
    data = dict(
        message=dict(
            images=[image_url]
        ),
        list_ids=[LIST_ID],
        run_now=1
    )
    requests.post(MAILING_URI, json=data)


def docx_to_image(doc):
    doc = encodebytes(doc).decode("utf-8")
    process = cc.createProcess(dict(
        inputformat="docx",
        outputformat="png"
    ))
    process.start(dict(
        outputformat="png",
        input="base64",
        file=doc,
        filename="timetable.docx",
        wait=True
    ))
    process.wait()
    return "https:" + process.data["output"]["url"]


@app.post('/send')
def send():
    image_url = docx_to_image(request.body.read())
    vk_send(image_url)


if os.environ.get("APP_LOCATION") == "heroku":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, server="gunicorn")
else:
    app.run(host="localhost", port=8080, debug=True)
