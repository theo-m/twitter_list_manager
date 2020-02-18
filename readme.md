# Twitter list manager

Twitter lists are an appealing feature, but very poorly served by the web UI.
This is a CLI tool to make and manage twitter lists.

It expects you to fill a `.env` file like so, head to [this page](https://python-twitter.readthedocs.io/en/latest/getting_started.html) to get your secrets:
```shell script
ACCESS_TOKEN='<your secret>'
ACCESS_TOKEN_SECRET='<your secret>'
API_KEY='<your secret>'
API_SECRET_KEY='<your secret>'
```

Then simply
```shell script
$ ./list_manager.py
```

---
## "Screenshots"
```text
Enter a command or a list number: n
[  24] @numpy_team 'NumPy' - https://twitter.com/numpy_team
NumPy is the fundamental package for numerical computing with Python. they/them
---

[  0]:   friends
[  1]: * science
[  2]:   art
[  3]:   your
[  4]:   lists
[  5]:   as 
[  6]:   you 
[  7]:   create them
[  8]:   the
[  9]:   asterisk
[ 10]:   denotes 
[ 11]:   user
[ 12]:   membership
[ 13]: * software

---
[r]: refresh lists
[c]: create a new list
[u]: unfollow
[n|⏎]: next
[p]: previous
[g]: go to index
[q]: quit

Enter a command or a list number:
```

