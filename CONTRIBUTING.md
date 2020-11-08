# Contributing to Report-Booklet-Writer

### First of all, thanks for being here!

> Your contribution means a lot for us and the growth of the project! It's people like you that make tools like the report booklet writer great!
>
> Long story short, [here](#tldr) is our TL;DR.

### Code of Conduct

Please note that all contributors have to follow the [Code of Conduct](https://github.com/TheCoder777/Report-Booklet-Writer/blob/master/CODE_OF_CONDUCT.md) of this project!

### Why should I even read this?

> Reading and following these guidelines keeps the code-base for this project consistent and easy to maintain! It also shows that you respect the time of the developers managing and developing this open source project!

### What contributions are we looking for?

We're looking for any kind of positive and forwarding development! This can be new features, bug fixes, documentation, translation and a lot more! Be creative and keep your eyes open!

# Ground Rules

### Expectations from this project

- Communicate with respect and consideration according to our [Code of Conduct](https://github.com/TheCoder777/Report-Booklet-Writer/blob/master/CODE_OF_CONDUCT.md)
- Fulfilling the current [PEP 8][pep8] code styles mostly (exceptions possible!)
- Using as less JavaScript as possible (currently 0%)
- Ensure cross-platform compatibility on Linux, Windows and Mac for every change made!



# Your First Contribution

Currently the most development time is spent on new features, and stabilizing the core, but writing test is also highly requested!

### Useful links for beginners

- If you've never contributed to an open source project, checkout [makeapullrequest](http://makeapullrequest.com/) and [firsttimersonly](https://www.firsttimersonly.com/)! ([here](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/about-pull-requests) is also an introduction to pull requests from github itself)
- If you think you messed up with git, checkout [ohshitgit](https://ohshitgit.com/) (or a more appropriate version at [dangitgit](https://dangitgit.com/))!

# Getting ready

Currently all contributions are welcome! We love to hear your ideas of new features that should be included in the project!

Make sure you don't overdo it and do one big pull request that addresses 10+ issues at once!

Smaller pull requests are always appreciated!

By contributing to this repository, you certify that:

- The containing code of your contribution is written only or in part by you and you have the rights to submit it.
- Your contribution underlies the conditions of the MIT License this project uses.
- If you added a feature, you submit corresponding, working tests in the same contribution!
- Your contribution improves the project and doesn't bring it in an instable/experimental build state!

If you fulfill these guidelines, you may proceed!

# TL;DR

Thats what you really wanted to see, right?

### Code guidelines

- All submitted Python code should mainly follow the [PEP 8][pep8] coding standards

- Structure imports as follows (example from [server.py][serverpy]):

  ```python
  # system modules first
  import bcrypt
  import functools
  import os
  import re
  import sys
  import time
  
  # external modules (need to be installed as a dependency)
  from flask import Flask, render_template, request, redirect, send_file, session, url_for, abort
  from flask_session import Session
  from gevent.pywsgi import WSGIServer
  
  # internal modules
  from defines.colors import RESET, BOLD, ERROR, WARNING, SUCCESS
  from defines.colormode import Colormode
  from defines import paths
  from defines import messages
  from handlers import pdfhandler, todolisthandler, dbhandler
  from models.messagequeue import MessageQueue
  ```

  Imports are split in 3 different groups:

  - system modules
  - external modules (dependencies)
  - internal modules (internal models, classes,...)

  All imports have to be sorted alphabetically under the three groups, the groups stay always in the above explained order (system, external and internal)!

  The license is only included in the core files ([server.py][serverpy] and [handlers/*.py][handlers] at the moment)!

  This section is still expanding!

# Contribution ideas

These are just some ideas that came to my mind while writing this:

- Try to use the project and give feedback
- add more comments to the code (more is always better here)
- correct grammatical mistakes/typos
- do the TODOs marked in the code (`# TODO: ...`)
- add more tests
- add features
- improve the overall code (being it style, performance, or just maintenance)
- make the project more stable (contributing to the core files)
- make up your own ideas, we're always open for them!

If you have any more questions/feedback, just reach out to me [@TheCoder777][author] (check my profile for contact info)

[pep8]: https://www.python.org/dev/peps/pep-0008/
[serverpy]: https://github.com/TheCoder777/Report-Booklet-Writer/blob/master/server.py
[author]: https://github.com/thecoder777
[handlers]: https://github.com/TheCoder777/Report-Booklet-Writer/tree/master/handlers