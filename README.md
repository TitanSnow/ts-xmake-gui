# ts-xmake-gui

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/3e71f53ba7774984929858de3490f1d9)](https://www.codacy.com/app/TitanSnow/ts-xmake-gui?utm_source=github.com&utm_medium=referral&utm_content=TitanSnow/ts-xmake-gui&utm_campaign=badger)
[![Build status](https://ci.appveyor.com/api/projects/status/4rvf8go6kjy6ds9l?svg=true)](https://ci.appveyor.com/project/TitanSnow/ts-xmake-gui)

An ugly xmake gui :tada:

## branches

* *legacy* (not recommended)
* *posix* (for posix users, recommended)
* *nt* (for Windows users, *not* recommended)
* *3* (the python3 version of branch legacy)
* *4* (the python3 version of branch posix)
* *newnt* (new Windows version! recommended)

## on posix
```console
$ ./configure
```

## on Windows
just download the file from [release](https://github.com/TitanSnow/ts-xmake-gui/releases)

<sub>note: not support Windows XP but you could build by yourself to make it be able to run on XP. See below</sub>

### build
the steps of build is listed in [.appveyor.yml](https://github.com/TitanSnow/ts-xmake-gui/blob/newnt/.appveyor.yml)

## little note
there is a cross-platform pseudo terminal (pty) solution in this repo to capture console app's output if you're interested in it
