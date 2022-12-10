from quart import Quart, request, jsonify, redirect
import json
import os
import importlib
import drivers.base
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--configure", action="store_true")

n = parser.parse_args()


def configure():
    import drivers

    http_bind = input("Enter http bind (127.0.0.1): ") or "127.0.0.1"
    print("http bind is: %s" % http_bind)

    print()

    http_port = input("Enter http port (5001): ") or 5001
    print("http port is: %s" % http_port)

    print()

    authorization = input("Enter authorization: ")
    print("authorization key is: <NOT DISPLAYED>")

    print()
    print("#" * 30)
    print()

    print("Available database drivers:\n" + "\n".join(
        f"({i}): {name.NAME}" for i, name in enumerate(drivers.CUSTOM_DRIVERS)))

    _driver = int(input("(Number) >>> "))
    driver_class = drivers.CUSTOM_DRIVERS[_driver]
    print("Database driver is: %s" % driver_class.NAME)

    print()

    print("Driver configuration:")
    driver_config = {}
    for arg in driver_class.REQUIRED_ARGS:
        arg_opt = "[REQUIRED] " if arg["required"] else ""
        arg_disp = arg["display"]
        arg_def = f" ({(arg['default'])})" if arg.get("default") else ""

        print('\"\"\"', arg["description"], '\"\"\"')
        value = arg["type"](input(f"{arg_opt}{arg_disp}{arg_def}: ") or arg.get("default"))
        print(

        )

        driver_config[arg["name"]] = value

    with open("config.json", "w") as file:
        data = {
            "http_bind": http_bind,
            "http_port": http_port,
            "authorization": authorization,
            "driver": "drivers.%s" % driver_class.NAME,
            "driver_config": driver_config
        }
        json.dump(data, file, indent=4)

    print()
    print("#"*30)
    print()
    print("Configuration done!")
    print("Run program again.")
    exit(0)


if not os.path.isfile("config.json") or n.configure:
    configure()
    # end

with open("config.json", "r") as f:
    config = json.load(f)

driver: drivers.base.BaseDriver = importlib.import_module(config["driver"]).Driver(**config["driver_config"])
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
