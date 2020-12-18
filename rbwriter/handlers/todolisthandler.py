
# system modules
import os
import pandas as pd

# internal modules
from ..defines import messages, paths
from ..models.messagequeue import MessageQueue


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
