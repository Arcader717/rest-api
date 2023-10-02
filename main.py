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
    'url': '/ping/post',
    'method': 'POST',
    'parameters': ["newMessage"]
  }
}

# Configurate and setup the apps
config = Config()
app = Flask(__name__)
config.bind = "0.0.0.0:3750"


# Base Website Links
@app.route("/")
def index():
  return render_template("index.html"), 403


# Rest Api Links
@app.get("/ping")
def pong():
  message = { 'message': f'{pingMsg}'}
  return jsonify(message), 200

@app.post("/ping/post")
def pongPost():
  r = json.loads(request.data)
  pingMsg = r['newMessage']
  mes = { 'message': 'Thanks for testing the Post method'}
  return jsonify(mes), 200

@app.get("/api")
def apiGet():
  return jsonify(apiDict)


# Run Commands
asyncio.run(serve(app, config))