# Python Berichtsheft Auto Writer

Just let someone else write your Berichtsheft, don't do it by yourself, that's boring!

Start using Python Berichtsheft Auto Writer now!



## Installation

To use this tool, you first have to clone the Project:

```bash
git clone https://github.com/TheCoder777/Python-Berichtsheft-Auto-Writer.git
```

Then you need to install the dependencies, for example like this:

```bash
pip install pdfrw PyPDF2 flask gevent reportlab 
```

Maybe you want to customize your config.ini file to your needs. You can find it in the root directory of the Project!

```bash
.
├── Berichtsheft_template.pdf
├── config.ini	<------------- There is it!
├── LICENSE
├── pdfhandler.py
├── readme.md
├── server.py
├── static
│   ├── favicon.ico
│   └── styles
│       ├── edit.css
│       ├── general.css
│       └── index.css
├── templates
│   ├── edit.html
│   └── index.html
└── tmp
```



Finally, you can just run it:

```bash
python server.py
```

The program will mostly take care of itself during the checkup, so no need to worry!



## Debugging

You can easily debug the while project by using a --debug/-d flag when running:

```bash
python server.py --debug
```



## Configuration

Example config.ini file:

```bash
# config.ini

[date]
beginn=36
nr=1
year=1

[user]
surname=Musterman
name=Max
unit=Ausbildung
```

- 'beginn' is the first calender week of whatever you're doing right now

- 'nr' is the current number of your Berichtsheft, it will go up by itself!

The rest is pretty much self explanatory!

## Todo

- manual mode
- graphical config editor

------

Have fun!

Support is always appreciated!

@TheCoder777