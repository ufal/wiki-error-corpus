#!/bin/bash 

# Input filename (relative)
input_file=$1

# Directory where the stage3 files are located
input_dir=$2

# Ouput directory: stage4
output_dir=$3

# Directory where the wiki-error-corpus github files are located
code_root=$4


input_file_path=${input_dir}/${input_file}
output_file_path=${output_dir}/${input_file}
corpus_dir=${input_dir}

python ${code_root}/reader/extract_spelling_errors.py ${corpus_dir} ${input_file} ${output_dir}

