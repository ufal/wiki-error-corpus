#!/bin/bash 

# Input filename (relative)
input_file=$1

# Directory where the stage1 files are located
input_dir=$2

# Ouput directory
output_dir=$3

# Directory where the wiki-error-corpus github files are located
code_root=$4

input_file_path=${input_dir}/${input_file}

python ${code_root}/lib/WikiExtractor.py --no-templates -a  ${input_file_path} > ${output_dir}/${input_file}
