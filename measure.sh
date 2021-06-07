#!/bin/bash

# Padronizar o vídeo
res=2880x1920
fps=24
frames=1440

for pattern in 1x1 3x2 6x4 9x6 12x8;do
for qp in 16 19 22 25 28; do
    reference1="yuv/nyc_drive_${res}_${fps}.yuv"
    reference2="yuv/sunset_${res}_${fps}.yuv"
    
    name1=nyc_drive_${res}_${fps}_${pattern}_${qp}
    name2=sunset_${res}_${fps}_${pattern}_${qp}
    encoded1="encoded/${name1}.yuv"
    encoded2="encoded/${name2}.yuv"
    
    projections/TApp360ConvertStatic -c measure_metrics.cfg -f ${frames} -i ${encoded1} -r ${reference1}|tee ${name1}.txt
    projections/TApp360ConvertStatic -c measure_metrics.cfg -f ${frames} -i ${encoded2} -r ${reference2}|tee ${name2}.txt
        
done
done
