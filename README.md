# ts-xmake-gui

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/3e71f53ba7774984929858de3490f1d9)](https://www.codacy.com/app/TitanSnow/ts-xmake-gui?utm_source=github.com&utm_medium=referral&utm_content=TitanSnow/ts-xmake-gui&utm_campaign=badger)
[![Build status](https://ci.appveyor.com/api/projects/status/4rvf8go6kjy6ds9l?svg=true)](https://ci.appveyor.com/project/TitanSnow/ts-xmake-gui)

An ugly xmake gui :beer:

## branches

* dev branches
    * *legacy* (not recommended)
    * *posix* (for posix users, recommended)
    * *nt* (for Windows users, recommended)
    * *3* (the python3 version of branch legacy)
    * *4* (the python3 version of branch posix)
* release branches
    * *r1f1* (release 1f1, from branch legacy)
    * *r2* (release 2, from branch posix)

<sub>the reason why release branches exist is that dev branches usually have xmake bundled that hasn't released yet, so releases degrade it</sub>

## require
python with tkinter is required

on my ubuntu:
```console
$ sudo apt install python python-tk
```

## usage
### installation
```console
$ git clone -b <branch_name> https://github.com/TitanSnow/ts-xmake-gui.git    #specify branch in <branch_name>
$ cd ts-xmake-gui
$ git submodule update --init
$ make build
$ sudo make install
```

### run
in console
```
/path/to/ts-xmake-gui$ ./ts-xmake-gui.py
```
or any other way to run it you like

### for windows users
just download the exe file from lastest release then run it

## demo
*note: this demo is out of date*

![demo.gif](docs/demo.gif)
