import json
import argparse
import os.path

parser = argparse.ArgumentParser()
parser.add_argument("--driver", action="store_true")
parser.add_argument("--http-bind", action="store_true")
parser.add_argument("--http-port", action="store_true")
parser.add_argument("--authorization", action="store_true")

args = parser.parse_args()


# noinspection PyTypeChecker
def configure_driver(config: dict):
    import drivers.base

    print("#" * 30)
    print()
    print("Driver configuration")
    print()
    print("#" * 30)
    print()

    driver_config = {}

    print(
        "Available database drivers:\n" +
        "\n".join(
            f"({i}): {name.NAME}" for i, name in enumerate(drivers.CUSTOM_DRIVERS)
        )
    )

    driver_class: drivers.base.BaseDriver = None
    _done = False
    while not _done:
        print()
        _driver = input("(Number) >>> ")
        try:
            _driver = int(_driver)
        except ValueError:
            print(f"{_driver!r} is not a number.")
            continue

        if not 0 <= _driver <= len(drivers.CUSTOM_DRIVERS) - 1:
            print(f"Please choose a number between 0 and {len(drivers.CUSTOM_DRIVERS) - 1}")
            continue

        driver_class = drivers.CUSTOM_DRIVERS[_driver]
        _done = True

    print()
    print(f"You selected >>> {driver_class.NAME}")
    driver_config["driver"] = "drivers." + driver_class.NAME

    print()
    print("#" * 30)
    print()
    print(f"{driver_class.NAME} driver configuration")
    print()
    print("#" * 30)
    print()

    driver_config["args"] = {}
    for arg in driver_class.REQUIRED_ARGS:
        arg_opt = "[REQUIRED] " if arg["required"] else ""
        arg_disp = arg["display"]
        arg_def = f" ({(arg['default'])})" if arg.get("default") else ""

        print('\"\"\"', arg["description"], '\"\"\"')
        value = arg["type"](input(f"{arg_opt}{arg_disp}{arg_def}: ") or arg.get("default"))
        print(

        )

        driver_config["args"][arg["name"]] = value

    config["driver_config"] = driver_config
    return config


def configure_http_bind(config: dict):
    if config.get("http_bind") is None:
        config["http_bind"] = "127.0.0.1"
    http_bind = input(f"Enter http bind ({config['http_bind']}): ") or config['http_bind']
    print("http bind is: %s" % http_bind)
    print()
    config["http_bind"] = http_bind
    return config


def configure_http_port(config: dict):
    if config.get("http_port") is None:
        config["http_port"] = 5001
    http_port = int(input(f"Enter http port ({config['http_port']}): ") or config['http_port'])
    print("http port is: %s" % http_port)
    print()
    config["http_port"] = http_port
    return config


def configure_authorization(config: dict):
    authorization = input(f"Enter authorization: ")
    print("authorization is: <hidden>")
    print()
    config["authorization"] = authorization
    return config


def configure_base(config: dict):
    print("#" * 30)
    print()
    print("Base configuration")
    print()
    print("#" * 30)
    print()

    config = configure_http_bind(config)
    config = configure_http_port(config)
    config = configure_authorization(config)

    return config


def full_config(config: dict):
    config = configure_base(config)
    config = configure_driver(config)

    return config


def done():
    print("#" * 30)
    print()
    print("Configuration done!")
    print("You can now run the main program.")
    print()
    print("#" * 30)
    exit(0)


if not os.path.isfile("config.json"):
    with open("config.json", "w") as f:
        json.dump(full_config({}), f, indent=4)
    done()

with open("config.json", "r") as f:
    _config = json.load(f)

d = False
if args.driver:
    _config = configure_driver(_config)
    d = True
if args.http_bind:
    _config = configure_http_bind(_config)
    d = True
if args.http_port:
    _config = configure_http_port(_config)
    d = True
if args.authorization:
    _config = configure_authorization(_config)
    d = True
if not d:
    _config = full_config(_config)

with open("config.json", "w") as f:
    json.dump(_config, f, indent=4)

done()
