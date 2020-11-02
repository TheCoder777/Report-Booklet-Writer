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


# load system modules
import os
import pandas as pd

# load internal modules
from defines import paths
from models.messagequeue import MessageQueue
from defines import messages


def open_todolist(uid):
    return pd.read_json(os.path.join(paths.USER_PATH, str(uid), paths.TODOLIST_PATH))


def save_todolist(uid, df):
    msg = MessageQueue()
    if df.to_json(os.path.join(paths.USER_PATH, str(uid), paths.TODOLIST_PATH)):
        msg.add(messages.SAVED_TODO)
    return msg


def update(uid, df, keys):
    # reset all
    for i in range(len(df.columns)):
        df[i]["done"] = False
        for j in range(len(df[i]["blocks"])):
            df[i]["blocks"][j]["done"] = False
            for k in range(len(df[i]["blocks"][j]["body"])):
                df[i]["blocks"][j]["body"][k]["done"] = False

    # insert only returned
    for key in keys:
        if len(key) == 1:
            key = int(key)
            df[key]["done"] = True
            for j in range(len(df[key]["blocks"])):
                df[key]["blocks"][j]["done"] = True
                for k in range(len(df[key]["blocks"][j]["body"])):
                    df[key]["blocks"][j]["body"][k]["done"] = True

        elif len(key) == 3:
            l1, l2 = key.split(".")
            l1, l2 = int(l1), int(l2)
            df[l1]["blocks"][l2]["done"] = True
            for k in range(len(df[l1]["blocks"][l2]["body"])):
                df[l1]["blocks"][l2]["body"][k]["done"] = True

        elif len(key) == 5:
            l1, l2, l3 = key.split(".")
            l1, l2, l3 = int(l1), int(l2), int(l3)
            df[l1]["blocks"][l2]["body"][l3]["done"] = True

    msg = save_todolist(uid, df)
    return df, msg
