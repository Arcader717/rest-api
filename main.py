import asyncio
import json

from hypercorn.config import Config
from hypercorn.asyncio import serve
from flask import Flask, render_template, jsonify, request

pingMsg = "Pong!" # the response to the "/ping" http request


apiDict = { # A dict containing the avaliable api links
  'ping': {
    'url': '/ping',
    'method': 'GET'
  },
  'Change Ping Response': {
    'url': '/ping/post'
  }
}
config = Config()
app = Flask(__name__)
config.bind = "0.0.0.0:3750"

@app.route("/")
def index():
  return render_template("index.html")

@app.get("/ping")
def pong():
  return render_template("")

asyncio.run(serve(app, config))