import asyncio
from dataclasses import dataclass
import json

from hypercorn.asyncio import serve
from hypercorn.config import Config
from quart import Quart, jsonify, render_template, request, abort
from quart_schema import Info, QuartSchema, deprecate, hide, validate_request

pingMsg = "Pong!" # The response to the "/ping" http request


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

info = Info(title="Basic REST API", version="1.0.0")
# Configurate and setup the apps
config = Config()
app = Quart(__name__)
config.bind = "0.0.0.0:3750"
QuartSchema(app, info=info)  


# Schema dataclasses
@dataclass
class pPostD:
  newMessage: str


# Base Website Links
@app.route("/")
@hide
async def index():
  return await render_template("index.html"), 403


# Rest Api Links
@app.get("/api/v1/ping")
async def pong():
    if request.headers['accept'] == "application/json":      
      message = { 'message': f'{pingMsg}' }
      return jsonify(message), 200
    else:
      abort(400)

@app.post("/api/v1/ping")
@validate_request(pPostD)
async def pongPost():
    r = json.loads(await request.data)
    pingMsg = r['newMessage']
    mes = { 'message': f'Got it! New Message: {pingMsg}. The new message will not actually be implemented, though' }
    return jsonify(mes), 200

@app.get("/api/v1")
async def apiGet():
    return jsonify(apiDict)

@app.post("/api/v1/math")
async def mathGet():
    requestDict = json.loads(await request.data)
    Num1 = requestDict['firstNum']
    num2 = requestDict['secondNum']
    oper = requestDict['operation']
    if oper == "+":
      ans = Num1 + num2
    elif oper == "-":
      ans = Num1 - num2
    elif oper == "x":
      ans = Num1 * num2
    elif oper == "/":
      ans = Num1 / num2
    elif oper == "^":
      ans = Num1 ** num2
    else:
      return abort(400)
    return jsonify({
      'equation': f'{str(Num1)}{oper}{str(num2)}',
      'answer': ans
    }), 200
    
    
# Run commands
asyncio.run(serve(app, config))
"""if __name__ == "__main__":
  app.run("0.0.0.0", 3750)"""