#!/bin/bash
# NOTE : Quote it else use array to avoid problems #
# FILES="/mnt/mailabs/es_ES/by_book/mix/don_quijote/wavs/*.wav"
FILES="/mnt/commonvoice/cv-corpus-8.0-2022-01-19/es/mp3.8000/*.mp3"
#DEST="/mnt/mailabs/es_ES/by_book/mix/don_quijote/wavs.8000"
DEST="/mnt/commonvoice/cv-corpus-8.0-2022-01-19/es/wavs"

for f in $FILES
do
  base_name=$(basename -s .mp3 $f)
  dest_name="$DEST/$base_name"
  echo "Processing $base_name file..."
  #sudo sox $f -r 8000 $dest_name
  sox -t mp3 $f "$dest_name.wav"  
  # take action on each file. $f store current file name
  #cat "$f"
done


