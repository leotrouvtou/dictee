#!/bin/sh
if [ -z "$2" ]
	then echo please use this script as follow "./tts number text"
else
    pico2wave -l fr-FR -w statics/son/$1.wav "$2";
    # ffmpeg -i statics/son/$1.wav -vn -ar 44100 -ac 2 -b:a 192k statics/son/$1.mp3
    # rm statics/son/$1.wav
fi
