#!/usr/bin/env python3
# coding=utf-8

import io
import os

import requests
import cloudconvert
from bottle import Bottle, request, template


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


def vk_send(image_urls):
    data = dict(
        message=dict(
            images=image_urls
        ),
        list_ids=[LIST_ID],
        run_now=1
    )
    requests.post(MAILING_URI, json=data)


def docx_to_image(doc):
    doc = io.BufferedReader(doc)
    process = cc.createProcess(dict(
        inputformat="docx",
        outputformat="png"
    ))
    process.start(dict(
        outputformat="png",
        input="upload",
        file=doc,
        filename="timetable.docx",
        wait="true",
        save="true"
    ))
    process.wait()

    download_url = "https:{url}".format(**process.data["output"])
    if "files" not in process.data["output"]:
        return [download_url]
    return ["{0}/{1}".format(download_url, filename) for filename in process["output"]["files"]]


@app.get("/")
def browser_page():
    return template("upload.html")


@app.post("/send")
def send():
    upload = request.files.get("file").file
    image_urls = docx_to_image(upload)
    vk_send(image_urls)


port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port, server="gunicorn")
