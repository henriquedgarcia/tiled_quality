#!/bin/bash

# Padronizar o vídeo
res=2880x1920
fps=24

ffmpeg -n -ss 12 -i original/nyc_drive.mp4 -t 60 -r ${fps} -vf "scale=${res}" yuv/nyc_drive_${res}_${fps}.yuv;
ffmpeg -n -ss 40 -i original/sunset.mp4 -t 60 -r ${fps} -vf "scale=${res}" yuv/sunset_${res}_${fps}.yuv;

for pattern in 1x1 3x2 6x4 9x6 12x8;do
for qp in 16 19 22 25 28; do
    name1=nyc_drive_${res}_${fps}_${pattern}_${qp}
    name2=sunset_${res}_${fps}_${pattern}_${qp}
    
    kvazaar -i yuv/nyc_drive_${res}_${fps}.yuv --input-res ${res} -q ${qp}  --period ${fps} --input-fps ${fps} --no-open-gop --tiles ${pattern} --slices tiles --mv-constraint frametilemargin -o encoded/${name1}.hvc
    kvazaar -i yuv/sunset_${res}_${fps}.yuv    --input-res ${res} -q ${qp}  --period ${fps} --input-fps ${fps} --no-open-gop --tiles ${pattern} --slices tiles --mv-constraint frametilemargin -o encoded/${name2}.hvc
done
done

pushd encoded/

# Encapsuling
for i in *.hvc;do
  ffmpeg -f rawvideo -framerate 24 -video_size 2880x1920 -i $i -c:v copy ${i%.hvc}.mp4;
done

# Decoding
for i in *.mp4;do 
  ffmpeg -i $i ${i%.mp4}.yuv;
done

popd
