# Introduction
Simple programm to analyze the efficient of certain keyboard layouts given in .xmodmap formate

## Funktionality
The script reads in all the keyboardlayouts in mappings 
then it assign a score to each key.
After that it reads all the characters from all the files specified in the input.
In the end it sum up all the scores of all the charactes end prints the final result.

It has also a function to print the layout of a mapping.

## Usage
`python3 main.py ~/code/**/**.java`