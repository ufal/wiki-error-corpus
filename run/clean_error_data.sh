#!/bin/bash

# Stage4 directory where the errors for each pages are stored
input_dir=$1

# Cleaned error data (final, easily readable)
output_dir=$2

# Directory where the wiki-error-corpus github files are located
code_root=$3


rm -rf ${output_dir}
mkdir -p ${output_dir}

cat ${input_dir}/* > ${output_dir}/error_corpus_raw_dirty.txt

cat ${output_dir}/error_corpus_raw_dirty.txt | python ${code_root}/other/clean_error_corpus.py ${output_dir}
cat ${output_dir}/orig_error_words.txt | sort | uniq -c | sort -nr > ${output_dir}/orig_error_words_sorted_counts.txt


