---
layout: post
title: "Python PDB Memo"
tagline : "Python PDB Memo"
description: "Python PDB Memo"
category: "python"
tags: [python, pdb, debug]
---
{% include JB/setup %}

Save `pdb` tips that are not included directly in [tutorial](http://pythonconquerstheuniverse.wordpress.com/2009/09/10/debugging-in-python/). Just for convenience of looking up.

How to begin debugging

* Insert `import pdb; pdb.set_trace()` into code， then `python <your-program>`. Or
* python -m pdb <your-program>

Command tips

* `where` / `w`: show where you are in call stack.
* `dir()` / `locals()` / `globals()`: show all varibales.
* `continue`: continue running.
* Use `time.sleep(N)` to switch processes in PDB. Refer to [here](http://stackoverflow.com/questions/12219231/how-to-switch-between-processes-in-pdb)

Other References

* [How to execute multi-line statements within PDB?](http://stackoverflow.com/questions/5967241/how-to-execute-multi-line-statements-within-pythons-own-debugger-pdb)
* [PDB tutorial](http://pythonconquerstheuniverse.wordpress.com/2009/09/10/debugging-in-python/)
