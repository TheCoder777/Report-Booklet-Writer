# Python Berichtsheft Auto Writer

Just let someone else write your Berichtsheft, don't do it by yourself, that's boring!

Start using Python Berichtsheft Auto Writer now!



## Installation

**Disclaimer: You need to have python 3.8 installed, otherwise it wont work!**

To use this tool, you first have to clone the Project:

```bash
git clone https://github.com/TheCoder777/Python-Berichtsheft-Auto-Writer.git
```

Then you need to install the dependencies, for example like this:

```bash
pip install pdfrw PyPDF2 flask gevent reportlab colored Flask-Session bcrypt pandas
```

Finally, you can just run it with:

```bash
python server.py

# alternative

./server.py
```

The program will mostly take care of itself during the checkup, so no need to worry!

If you want to configure your name and personal info, checkout  [`configuration`](#configuration).



## Usage

1. If you load it up, go to [localhost:8000](localhost:8000) (current default) and click on the start button!
2. You can enter as much information as you want, and finally click on download!
3. Your browser will now download a perfectly filled out pdf!
4. It's as easy as that!



## Users

You can create a user if you click on "create user" on the login page.

Email validation will come soon!

Edit your user specific settings on the settings page!

You can login with either your email address or your nickname!



## Configuration

You can configure all settings via the web interface  on [Domain]/settings or by clicking on the settings icon in the top right of the start page!

You'll be notified if everything went correctly when you click the save button!

To reset the configuration, just click the reset button!

The 'reset to default button' will hard reset your configuration to absolute defaults!

**Be careful with that!**



## Debugging

You can easily debug the project by using a --debug/-d flag when running:

```bash
python server.py --debug
```



## Todo

- Content overview (export all PDFs at once)
- Mail server (just wait for it, you'll see)
- Private/Public Profile setting
- Dashboard

------

Have fun!

Support is always appreciated!

[@TheCoder777](https://github.com/thecoder777)
