# Sonification_Project
## Table of contents
* [General info](#general-info)
* [Setup](#setup)

## General info
This project's goal is to make genome data into music.
* We are developing a tool that parses genome data into a music file, where individual genes represents a different note and its length the duration of that note. 
* We will experiment to see if this tool improves the experience and efficiency of people who works with genome analysis.

## Setup
* **clean_gff3.py**: Takes in a gff3 file[-f] and three numbers(chromosome number[-n], start position[-s], end position[-e]). Returns a file that contains only gene data that belongs to the specified chro number and within the specified range. The start and end position arguemments are optional. Run by terminal command similar to the one below:

```
python3 clean_gff3.py -f human_cleaned.gff3 -n 1 -s 0 -e 157724180
```
* **gff2music_cvs.py**: Takes in a gff3 file and converts it into a csv format that is convertible to midi via the [***csvmidi***](https://www.fourmilab.ch/webtools/midicsv/) command. Run by terminal command similar to the one below:

```
python3 gff2music_cvs.py -f file.gff3
```
* To play music of the newly built Midi file, use ***timidity***. 
  * To download the library on mac: ```brew install timidity```
  * To run: ```timidity file.midi```
