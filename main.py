from quart import Quart, request, jsonify, redirect
import json
import os
import importlib
import drivers.base
import argparse

if not os.path.isfile("config.json"):
    print("Please run the configure.py file in order to create a configuration file.")
    print("Please run the configure.py file in order to create a configuration file.")
    print("Please run the configure.py file in order to create a configuration file.")
    exit(0)

with open("config.json", "r") as f:
    config = json.load(f)

driver: drivers.base.BaseDriver = importlib.import_module(
    config["driver_config"]["driver"]
).Driver(
    **config["driver_config"]["args"]
)
app = Quart(__name__)


@app.before_serving
async def before_serving():
    await driver.setup()


@app.route("/create", methods=["POST"])
async def create():
    authorization = request.headers.get("authorization")
    if authorization != config["authorization"]:
        return jsonify({"message": "Unauthorized"}), 401

    body = await request.form
    url = body.get("url")
    if url is None:
        return jsonify({"message": "Missing Data"}), 405

    shortened_url = await driver.create_url(url)

    return jsonify({"message": "Success", "code": shortened_url}), 200


@app.route("/<string:code>", methods=["GET"])
async def get(code):
    url = await driver.get_url(code)
    if url is None:
        return 404
    return redirect(url, 302)


app.run(
    host=config["http_bind"],
    port=config["http_port"],
    use_reloader=False,
    debug=False
)
