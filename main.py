from typing import Optional

from quart import Quart, request, jsonify, redirect, abort
import json
import os
import importlib
import drivers.base_driver

if not os.path.isfile("config.json"):
    print("Please run the configure.py file in order to create a configuration file.")
    print("Please run the configure.py file in order to create a configuration file.")
    print("Please run the configure.py file in order to create a configuration file.")
    exit(0)

with open("config.json", "r") as f:
    config = json.load(f)

driver: drivers.base_driver.BaseDriver = importlib.import_module(
    config["driver"]["using"]
).Driver(
    **config["driver"][config["driver"]["using"]]
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
    url: Optional[str] = body.get("url")
    if url is None:
        return jsonify({"message": "Missing Data"}), 405

    name: Optional[str] = body.get("name") or None

    shortened_url = await driver.create_url(url, name)

    return jsonify({"message": "Success", "code": shortened_url}), 200


@app.route("/<string:code>", methods=["GET"])
async def get(code):
    url = await driver.get_url(code)
    if url is None:
        abort(404)
    return redirect(url, 302)


app.run(
    host=config["http_bind"],
    port=config["http_port"],
    use_reloader=False,
    debug=False
)
