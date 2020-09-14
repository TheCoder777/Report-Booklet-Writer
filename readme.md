# Python Berichtsheft Auto Writer

Just let someone else write your Berichtsheft, don't do it yourself, that's boring!



## Installation


To use this tool, just run:

```python
python server.py
```

You can install the dependencies like that:

```bash
pip install pdfrw PyPDF2 flask gevent reportlab 
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

and the rest is pretty much self explained!



Have fun!

Support the project if you like!

@TheCoder777