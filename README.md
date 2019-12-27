# Introduction

This Project consists on an real time image processing software designed to use different computer vision methods. 
This methods will be applied to images that could come from a file from a selected path or from a capture
device such a webcam. 

The software is able to apply many image filters and also perform color detection in realtime
and use it to do background replacing and color tracking. 

It is developed using the Python programming lenguaje (v2.6.6),
and it uses the libraries Python-OpenCV 2.1.0 for the image manipulation
and PyQt 4 to the User Interface Issues.

See entire documentation [here](https://docs.google.com/file/d/0B0m3f9uIC1OyYjA2NTY5YmItZGQ0NC00NmViLWE5ODAtZTRkMmQzNDE0NGYw/edit?hl=es)

## Installation
### Python, OpenCV and PyQt versions

The project was made using python 2.6.6 and OpenCv 2.1.0. It is tested on
MacOs X and Linux, and it works correctly in both operating systems with
this python and opencv versions.
4.1.2 Python, OpenCV and PyQt installation on MacOs X
To install all the required packages on OsX it’s only needed to use the following
lines on the terminal.
First you have to install a version of the repository macports http://www.macports.org/ 
because with this repository system it’s very easy to install all the dependen-
cies.

```bash
sudo port selfupdate
sudo port -v install opencv +python26
```

By default OpenCV is installed to /opt/local/ according to MacPorts conventions.
```bash
sudo port -v install py26-pyqt4
```

### Python, OpenCV and PyQt installation on Linux (Debian)
Al the dependencies of the program could be installed using the apt-get /
subversion and looking for the versions detailed before.

#### Dependences needed to run the program

All the following packages are necessary to the correct execution of the pro-
gram.

- python 2.6.6
- hurd [hurd-i386]
- libatlas3gf-base [ia64]
- libc0.1 (>= 2.3) [kfreebsd-amd64, kfreebsd-i386]
- libc0.3 (>= 2.11) [hurd-i386]
- libc6 (>= 2.11) [powerpcspe, sh4]
- libc6.1 (>= 2.2) [ia64]
- libcv1 [m68k]
- libcv2.1 [not m68k]
- libcvaux2.1 [not m68k]
- libgcc1 [powerpcspe, sh4]
- libgcc2 (>= 4.2.1) [m68k]
- libgomp1 (>= 4.2.1) [m68k]
- libhighgui1 [m68k]
- libhighgui2.1 [not m68k]
- liblapack3gf [not ia64, m68k]
- libpython2.6 (>= 2.6) [not m68k]
- libstdc++6 [powerpcspe, sh4]
- libunwind7 [ia64]
- python-support (>= 0.90.0)
- zlib1g (>= 1:1.1.4) [not m68k]

## How to use it
To run the program it’s needed to have python 2.6.6, and execute the following
order:
```bash
python main.py
```

It’s also possible to execute:
```bash
python2.6 main.py
```

