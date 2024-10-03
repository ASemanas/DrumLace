#!/bin/bash
git pull https://github.com/ASemanas/DrumLace.git -r master

git add .

git commit -m $1

git push -u origin master