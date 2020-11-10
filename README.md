# Report Booklet Writer

[![CodeFactor](https://www.codefactor.io/repository/github/thecoder777/report-booklet-writer/badge)](https://www.codefactor.io/repository/github/thecoder777/report-booklet-writer)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/TheCoder777/Report-Booklet-Writer/blob/master/LICENSE)
[![PyPI version](https://badge.fury.io/py/rbwriter.svg)](https://badge.fury.io/py/rbwriter)

Never write a report booklet on your own again, Report Booklet Writer does it for you!

[Only supports German (DE) standard report booklets right now]



## About

This Project let's you save all your reports from single weeks into one big database, and when you feel like it, you can export all weeks correctly ordered and pixel perfect aligned into one PDF. Isn't that awesome?

### Warning:

The current default server is the flask development server! This is not recommended for a productive environment with more users!



## Installation

### From PyPI (recommended):

```bash
pip install rbwriter

# Run it (make sure ~/.local/bin is on your PATH)
rbwriter
```

### From GitHub (build from source):

```bash
# First clone the project
git clone https://github.com/TheCoder777/Report-Booklet-Writer.git

# Change directory
cd Report-Booklet-Writer

# Install requirements
pip install .

# Finally run it (make sure ~/.local/bin is on your PATH)
rbwriter
```

### From GitHub releases:

- [Download](https://github.com/TheCoder777/Report-Booklet-Writer/releases) the wheel (.whl) file from the releases section  (get the release you want)
- install with `pip install *.whl`
- run with `rbwriter`



## Usage

If you load it up, go to [localhost:8000](localhost:8000) (current default) and either click on 'create account', or click the quickedit icon on sidebar (try to hover for a little bit!)

You can either download the single PDFs in edit mode, or export all to one PDF in the overview tab!

It's as easy as that!




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

You can easily debug the project by using a --debug/-d flag when running:

```bash
rbwriter --debug
```

#### Flask flags:

All flags given to `rbwriter` will be handed over directly to the `flask run` command!



## Todo

- Mail server (just wait for it, you'll see)
- Private/Public Profile setting
- all TODOs in the code (`# TODO: ...`)



## License

The project is licensed under the MIT license.



------

This project has guidelines for:

- [Code of Conduct](https://github.com/TheCoder777/Report-Booklet-Writer/blob/master/CODE_OF_CONDUCT.md) 
- [Contributing](https://github.com/TheCoder777/Report-Booklet-Writer/blob/master/CONTRIBUTING.md) 



Current maintainer and owner: [TheCoder777](https://github.com/thecoder777)

**Cheers!**

