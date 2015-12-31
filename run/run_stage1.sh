#!/bin/bash

# arguments

# XML dump file (uncompressed)
xml_dump=$1

# Output directory: XML files divided by page
output_dir=$2

# Directory where the wiki-error-corpus github files are located
code_root=$3

rm -rf ${output_dir}
mkdir -p ${output_dir}

nohup python ${code_root}/reader/divide_xml_revisions.py ${xml_dump} ${output_dir} > stage1.log &
