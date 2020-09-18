# MIT License
#
# Copyright (c) 2020 TheCoder777
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import configparser


CONFIG_PATH = "./config.ini"


def get_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    return config


def write_config(config):
    try:
        with open(CONFIG_PATH, "w") as configfile:
            config.write(configfile)
    except FileNotFoundError:
        print(e, "problems occurred while trying to update config!\nThe file doesn't exist!")
    except:
        print(Error_msg.UNKNOWN_ERR)


def update_config(data):
    config = get_config()

    config["date"]["kw"] = data["kw"]
    config["date"]["nr"] = data["nr"]
    config["date"]["year"] = data["year"]
    config["user"]["surname"] = data["surname"]
    config["user"]["name"] = data["name"]
    config["user"]["unit"] = data["unit"]
    write_config(config)


def parse_config():
    config = get_config()

    try:
        data = {}
        for c in config.sections():
            for v in config[c].items():
                data[v[0]] = v[1]
        return data
    except:
        pass


def add_config_nr():
    config = get_config()
    config["date"]["nr"] = str(int(config["date"]["nr"]) + 1)
    write_config(config)


def reset_config():
    # default values
    kw = "36"
    nr = "1"
    year = "1"
    surname = "Musterman"
    name = "Max"
    unit = "Ausbildung"

    config = get_config()

    config["date"]["kw"] = kw
    config["date"]["nr"] = nr
    config["date"]["year"] = year
    config["user"]["surname"] = surname
    config["user"]["name"] = name
    config["user"]["unit"] = unit
    write_config(config)
