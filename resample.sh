#!/bin/bash
# NOTE : Quote it else use array to avoid problems #
FILES="/mnt/mailabs/es_ES/by_book/mix/don_quijote/wavs/*.wav"
DEST="/mnt/mailabs/es_ES/by_book/mix/don_quijote/wavs.8000"
for f in $FILES
do
  base_name=$(basename $f)
  dest_name="$DEST/$base_name"
  echo "Processing $f file..."
  sudo sox $f -r 8000 $dest_name
  # take action on each file. $f store current file name
  #cat "$f"
done