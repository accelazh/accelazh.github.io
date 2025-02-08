---
layout: post
title: "Python PDB Memo"
tagline : "Python PDB Memo"
description: "Python PDB Memo"
category: "Language"
tags: [python, pdb, debug]
---
{% include JB/setup %}

Save `pdb` tips that are not included directly in [tutorial](http://pythonconquerstheuniverse.wordpress.com/2009/09/10/debugging-in-python/). Just for convenience of looking up.

__How to begin debugging__

* Insert `import pdb; pdb.set_trace()` into code， then `python <your-program>`. Or
* python -m pdb <your-program>

__Command tips__

* `where` / `w`: show where you are in call stack.
* `dir()` / `locals()` / `globals()`: show all varibales.
* `continue`: continue running.
* Use `time.sleep(N)` to switch processes in PDB. Refer to [here](http://stackoverflow.com/questions/12219231/how-to-switch-between-processes-in-pdb)

__How to debug multiprocess program__

I use remote debugger for this. [Winpdb and rpdb2](http://stackoverflow.com/questions/543196/how-do-i-attach-a-remote-debugger-to-a-python-process). To install and launch a debug session (referred to [here](http://stackoverflow.com/questions/12367183/rpdb2-how-to-connect-to-a-pid)):

```
# == On host side, where you program ====

# Install wxpython from http://www.wxpython.org/download.php#msw
...
# If you see Mac says wxpython package damaged, temporarily turn off Gatekeeper, see http://stackoverflow.com/questions/21223717/install-wxpython-on-mac-os-mavericks
...

# Install winpdb
wget https://winpdb.googlecode.com/files/winpdb-1.4.8.tar.gz
tar -xzvf winpdb-1.4.8.tar.gz
cd winpdb-1.4.8
sudo python setup.py install -f

#pip install winpdb  # Don't use this because it installs an early version with problem http://stackoverflow.com/questions/3464013/winpdb-error-debugging-django-ctimeouthttp-instance-has-no-attribute-getresp

# Start winpdb
winpdb

# == On dev machine, where you run python ==

# Install winpdb but no need for wxpython
... # like the above

# Embed debug breakpoint in code
print 'hello'
import rpdb2; rpdb2.start_embedded_debugger('your_password')
print 'world'

# You can use rpdb2 on localhost
rpdb2
> password 'your_password'
> attach
...  # list of wait debugees and pids
> attach <pid>
> thread  # to show threads
> thread <n>  # to switch thread

# == On host side ==

# On winpdb GUI, set password and attach
...
```

You can run rpdb2 right on the dev machine, from another ssh session. Note that rpdb2 command set is a bit different from pdb. This helps when you want to use rpdb2 only and avoid remove connection.

__Other References__

* [How to execute multi-line statements within PDB?](http://stackoverflow.com/questions/5967241/how-to-execute-multi-line-statements-within-pythons-own-debugger-pdb)
* [PDB tutorial](http://pythonconquerstheuniverse.wordpress.com/2009/09/10/debugging-in-python/)
