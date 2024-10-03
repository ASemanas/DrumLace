#!/bin/bash

ly="./lilypond-2.24.2/bin/lilypond "
target='out/Bootsandcats.ly'
fs="fluidsynth -F"
sf="soundfonts/Real_Drum_s__GM.sf2"

#;fluidsynth -F out/out.wav out/out.midi;aplay out/out.wav
./main.py $1 $2 #> /dev/null 2>&1

exit_status=$?

#echo $2


for f in out/shell/*.sh; do
  bash "$f" > /dev/null 2>&1
done

for f in out/shell/*.sh; do
  rm "$f" > /dev/null 2>&1
done

for f in out/*; do
  chmod ugo+rwx $f > /dev/null 2>&1
done

for f in in/* ; do > /dev/null 2>&1
  chmod ugo+rwx $f > /dev/null 2>&1
done

for f in out/*.pdf; do
  cp $f ./html/images > /dev/null 2>&1
  rm $f > /dev/null 2>&1
done

for f in out/*.wav;do
  cp $f ./html/wav > /dev/null 2>&1
  rm $f > /dev/null 2>&1
done

for f in out/*.midi;do
  cp $f ./html/midi > /dev/null 2>&1
  rm $f > /dev/null 2>&1
done


for f in in/*;do
  cp $f ./html/in > /dev/null 2>&1
  rm $f > /dev/null 2>&1
done

echo $exit_status
exit $exit_status