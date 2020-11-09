# Author:: Paul S. (thecoder777.github@gmail.com)
# Copyright:: Copyright (c) 2020, TheCoder777
# License:: MIT
#
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

__author__ = "Paul S."
__copyright__ = "Copyright (c) 2020, TheCoder777"
__license__ = "MIT"

# pre-checkup to create necessary directories
from rbwriter.checks import checkup

checkup()

# system modules
import sys

# external modules
from flask import Flask
from flask_session import Session

# internal modules
from rbwriter.defines import paths
from rbwriter import views


def create_app():
    # TODO: make a server config file in root for HOST and PORT (and maybe debug ?)
    # TODO: add --clean/-c flag to delete all db/user/tmp files at startup, but ask for confirmation
    # TODO: maybe add a --reload flag to load cookies, and make it standard to delete cookies at startup?

    app = Flask(__name__)
    HOST = "localhost"
    PORT = 8000
    DEBUG = False
    FLASK_ENV = "production"

    print(f"\nRunning on http://{HOST}:{PORT}/\n", file=sys.stderr)

    if len(sys.argv) > 1:
        if sys.argv[1] in ["--debug", "debug", "-d", "d"]:
            FLASK_ENV = "development"
            DEBUG = True

    app.register_blueprint(views.std_bp)
    app.register_blueprint(views.sec_bp)
    app.register_blueprint(views.user_bp)

    app.config.from_mapping(
        HOST=HOST,
        PORT=PORT,
        DEBUG=DEBUG,
        FLASK_ENV=FLASK_ENV,
        SESSION_TYPE="filesystem",
        SESSION_FILE_DIR=paths.COOKIE_PATH,
        SECRET_KEY="dev",
    )
    Session(app)

    return app
