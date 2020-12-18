"""
Author:: Paul S. (thecoder777.github@gmail.com)
Copyright:: Copyright (c) 2020, TheCoder777
License:: MIT

MIT License

Copyright (c) 2020 TheCoder777

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


Debugging
---------

Do not use this for debugging!
For debugging you need to set environment variables:
```
FLASK_APP=rbwriter
FLASK_ENV=development
```

and start like this:

```
flask run --debug
```

.. seealso:: Flask app factories https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/
"""

__author__ = "Paul S."
__email__ = "thecoder777.github@gmail.com"
__copyright__ = "Copyright (c) 2020, TheCoder777"
__license__ = "MIT"

# pre-checkup to create necessary directories for db initialization
from rbwriter.checks import checkup

# external modules
import click
from flask import Flask
from flask_session import Session

# internal modules
from rbwriter.defines.paths import COOKIE_PATH, SECRET_KEY
from rbwriter.views import sec_bp, std_bp, user_bp


def __read_secret_key():
    with open(SECRET_KEY, "rb") as f:
        return f.read()


@click.command("start")
def start_server():

    import subprocess
    from rbwriter.defines import paths

    # running server (needs sudo to change socket permissions)
    subprocess.Popen(f"sudo uwsgi --ini {paths.UWSGI_CONFIG_DEST}".split())


def create_app():
    # TODO: add --clean/-c flag/click command to delete all db/user/tmp files at startup, but ask for confirmation
    # TODO: maybe add a --reload flag/click command to load cookies, and make it standard to delete cookies at startup?

    app = Flask(__name__)

    app.register_blueprint(std_bp)
    app.register_blueprint(sec_bp)
    app.register_blueprint(user_bp)

    app.config.from_mapping(
        SESSION_TYPE="filesystem",
        SESSION_FILE_DIR=COOKIE_PATH,
        SECRET_KEY=__read_secret_key(),
    )
    Session(app)

    app.cli.add_command(start_server)

    return app
