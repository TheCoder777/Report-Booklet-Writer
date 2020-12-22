# Report Booklet Writer

[![CodeFactor](https://www.codefactor.io/repository/github/thecoder777/report-booklet-writer/badge)](https://www.codefactor.io/repository/github/thecoder777/report-booklet-writer)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/TheCoder777/Report-Booklet-Writer/blob/master/LICENSE)
[![PyPI version](https://badge.fury.io/py/rbwriter.svg)](https://badge.fury.io/py/rbwriter)

Never write a report booklet on your own again, Report Booklet Writer does it for you!

[Only supports German (DE) standard report booklets right now]



## About

This Project let's you save all your reports from single weeks into one big database, and when you feel like it, you can export all weeks correctly ordered and pixel perfect aligned into one PDF. Isn't that awesome?



## Features

- Native Nginx & UWSGI support
- Native Docker & Buildah support (relatively untested, be careful!)

- Multi-User-Management
- Todolist integration
- Report Booklet Overview
- Export-Everything-Button



## Installation

### From PyPI (recommended):

```bash
pip install rbwriter

# Run it
# -> make sure ~/.local/bin is on your PATH or you installed it with sudo for all users
rbwriter
```



### From GitHub (build from source):

```bash
# First clone the project
git clone https://github.com/TheCoder777/Report-Booklet-Writer.git

# Change directory
cd Report-Booklet-Writer

# OPTIONAL: checkout the release you want
# git checkout v0.1-alpha.1

# Install requirements
pip install .

# Run it 
# -> make sure ~/.local/bin is on your PATH or you installed it with sudo for all users
rbwriter
```



### From GitHub releases:

- [Download](https://github.com/TheCoder777/Report-Booklet-Writer/releases) the wheel (.whl) file from the releases section  (get the release you want)
- install with `pip install *.whl`
- run with `rbwriter`



### With Docker:

```Python
# First clone the project
git clone https://github.com/TheCoder777/Report-Booklet-Writer.git

# Change directory
cd Report-Booklet-Writer

# OPTIONAL: checkout the release you want
# git checkout v0.1-alpha.1

# build container (make sure Docker is installed and working!)
docker build -t "some-example-tag" .

# run container
docker run -p 80:80 "some-example-tag"

# stop container
docker stop "some-example-tag"
```



### With Podman / Buildah:

```Python
# First clone the project
git clone https://github.com/TheCoder777/Report-Booklet-Writer.git

# Change directory
cd Report-Booklet-Writer

# OPTIONAL: checkout the release you want
# git checkout v0.1-alpha.1

# build container (make sure Buildah and Podman are installed and working!)
buildah build-using-dockerfile -t "some-example-tag"

# run container
podman run "some-example-tag"

# stop container
podman stop "some-example-tag"
```



## Usage

Start rbwriter, go to [localhost:80](localhost:80) (current default) and either click on 'create account' click the quickedit icon on sidebar (try to hover for a little bit!) or click on 'Use as Guest'.

That's it!

You can now either download the single PDFs in 'edit' mode, or export all to one PDF in the overview tab!




## Users

Every account has a nickname that can be changed in the settings (it's pretty useless right now, but you'll use this to login later!)

You Email needs to be in a `name@provider.domain` format

Your password needs to have:

- 8 characters
- one capital letter
- one number
- one special character

Now you're logged in! **Congratulations!**




## Configuration

You can configure all settings via the web interface on /settings or by clicking on the settings icon in the sidebar!

Do me a favor and be careful with some settings like `start week` and `start year`, this often gets easily messed up.



If you like the extreme, or you just want to mess around, you may also edit the `defines/configs.py` file. (Do this on your own risk!)

You'll be notified if everything went the correct way when you click the save button!

To reset the configuration, just click the reset button! (This is to reset the values you put in since the last refresh)

The 'reset to default button' will hard reset your configuration to absolute defaults, with **no chance to restore your data**, so please be careful with that!



## Troubleshooting

### The `rbwriter` command doesn't exist:

 If the `rbwriter` command doesn't exist, you probably haven't set up your PATH correctly.

Make sure that `~/.local/bin` (local installation) and `/usr/lib/pythonx.x/site-packages/` (global installation) are both on your PATH!

You can check your path with `echo $PATH`.




## Debugging

You can easily debug the project by using a 'debug' flag when running:

```bash
rbwriter debug
```

This will launch an instance of the flask development server on the default [localhost:5000](localhost:5000).

#### Flask flags:

All flags given to `rbwriter` will be handed over directly to the `flask run` command!



## Long-Term Todos

- Use a different Database structure!
  - Maybe SQLAlchemy
  - Every user has its own table (not a completely different database...)
- Mail server (just wait for it, you'll see)
- Private/Public Profile setting
- all TODOs in the code (`# TODO: ...`)
- More flexible export (e.g. export from week 45 to 51 in 2021)
- Multiple PDF templates
  - Mappings for easier support
  - Select the PDF template before export (standard template in settings)
- New Frontend (right now it's pretty un-scalable for further features)
- Recommended Todolist-tasks to tick after saving a report booklet
- Progress of how much of the Todolist is done (on the Todolist page / stats page)
- Make a stats page with cool stats (how much words written or something like this)
- Search-bars everywhere



## License

The project is licensed under the [MIT license](https://github.com/TheCoder777/Report-Booklet-Writer/blob/stable/LICENSE).



------

This project has guidelines for:

- [Code of Conduct](https://github.com/TheCoder777/Report-Booklet-Writer/blob/stable/CODE_OF_CONDUCT.md) 
- [Contributing](https://github.com/TheCoder777/Report-Booklet-Writer/blob/stable/CONTRIBUTING.md) 



Current maintainer and owner: [TheCoder777](https://github.com/thecoder777)

**Cheers!**

