from rbwriter import create_app

"""
This file provides an interface to the uwsgi module.

The uwsgi module would normally read the 'Flask(__name__)' or 'app' instance directly from the module itself.
However, this isn't possible due to the use of the flask app_factory in this project.

To make it still work, this interface imports the app_factory and creates a application object (alias to 'app').
Note that this is only for running from the rbwriter script!
"""

# by default, uwsgi reads 'application' instead of 'app'
application = create_app()
