# Pepper Demonstration for BioIntelligence Lab.

Pepper demo for BioIntelligence Lab.

Developed by Jesoon Kang, Youngjae Yoo in BioIntelligence LAB (BI LAB) & Cognitive Recognition Artifical Intelligence Group (CRAIG)


## Description

This repo contains NAOqi implementation code for robot PEPPER.

This repo includes motion, TTS, HTML interworking with tablet implementation codes for Pepper to introduce the BI LAB.

Codes are implemented based on Python 2.7 and Naoqi 2.5 versions. and other dependencies are exist.

## Installation

### Requirements
* Ubuntu 16.04
* Python 2.7

The following packages are needed to execute the code.

```
NAOqi 2.5

Installation & Setup reference : https://developer.softbankrobotics.com/pepper-naoqi-25-downloads-linux
```

```
Python2.7 packages

pip install pillow requests bs4
```

## Prepares for execute

First of all, clone this repo in local device.
```
git clone https://github.com/jesn1219/pepper_demo_bilab.git
```

Before executes our codes, 

Some files need to be moved into the pepper.

```
* Copy all files in OUR_REPO: ./html/*  to  Pepper: /opt/aldebaran/www/apps/bi-html/html/

* Copy all files in OUR_REPO: ./sound/*  to  Pepper: /opt/aldebaran/www/apps/bi-sounds/
```


## Usage

```
python main.py
```


## Implementation Specification

Our demonstration program are contains following files

```
main.py 
* For execute. wrapping file
```
```
main_engversion.py
* main logic file for English demonstrations
```
```
trainsition.py 
* For specified codes for each Scene trainsition and each followed action
```
```
data_list.py 
* For specified data for universial usage, e.g. Touch area for each scene, Word list for oral command.
```
```
./html/
* Directory folder for html files & image files for tablet display
```
```
./motion/
* Directory folder for some entertain motions
```
```
./sound/
* Directory folder for some entertain & effect sounds
```
```
./camera/
* Module for dealing cameras on pepper
```




## Enviroment Variables Settings for NAOqi

```
export PYTHONPATH=${PYTHONPATH}:/Path-to-Downloaded-SDK/lib/python2.7/site-package
export DYLD_LIBRARY_PATH=${DYLD_LIBRARY_PATH}:/Path-to-Downloaded-SDK/lib
```
