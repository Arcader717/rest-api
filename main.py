from quart import Quart, render_template
from hypercorn.config import Config
from hypercorn.asyncio import serve
import asyncio


config = Config()
app = Quart(__name__)
config.bind = "0.0.0.0:3750"

@app.route("/")
async def index():
  return await render_template("index.html")

@app.get("/ping")
async def pong():
  return await render_template("")

asyncio.run(serve(app, config))