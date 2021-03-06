# DJVu to ps (gray) 
# djvups -color=no -orient=landscape <djvu_file>  <djvu_file>.ps

# Convert to pnm
pstopnm -pgm -xborder 0 -yborder 0 -landscape -nocrop -dpi=200 <name_of_file>.ps

# Split pages
unpaper -v --layout double -op 2 --no-blackfilter --no-noisefilter --no-blurfilter --no-grayfilter --no-border  <name_of_file>%03d.pgm unpaper_<name_of_file>%03d.pgm

for i in unpaper*.pgm; do pamtotiff $i > $i.tiff; done

tiffcp -c lzw *.tiff <file_name>.tiff

tiff2pdf -o <file_name>.pdf <file_name>.tiff

rm *.ps *.pgm *.tiff
