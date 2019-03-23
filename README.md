# OldNotInNew-and-NewNotInOld
Coding exercise see this [pdf](OldNotInNew&#32;and&#32;NewNotInOld.pdf) for more details


### Setup:
````
> pip install requirements.txt
````
### Usage:
````
> py .\main.py -h
usage: main.py [-h] [-v] [-s] [-d]
               [inputOld] [inputNew] [outputOld] [outputNew]

find old files not in new, and new files not in old

positional arguments:
  inputOld       input file of old file names (default: Old.sha1.txt)
  inputNew       input file of new file names (default: New.sha1.txt)
  outputOld      output file of old file names (default: OldNotInNew.txt)
  outputNew      output file of new file names (default: NewNotInOld.txt)

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  shows all logging
  -s, --silent   hides all logging
  -d, --debug    shows debugging logging
````
