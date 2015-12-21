#!/bin/bash


# Input directory: Location of the stage2 directory 
input_dir=$1

# Output directory: stage2 output 
output_dir=$2

# Directory where the wiki-error-corpus github files are located
code_root=$3


# username 
usern=`id -u -n`


max_jobs=1000

rm -rf ${output_dir}
mkdir ${output_dir}

pushd ${input_dir}
for i in $(ls); do
  echo "Processing file: ${i}"
  num_jobs=`qstat -u '*' | grep -P '^\d' | tr -s ' ' | cut -f4 -d' ' | grep ${usern} | wc -l`
  while [ $num_jobs -ge $max_jobs ]
  do
    echo -e "Number of jobs limit reached: \e[91m1000 (waiting)\e[0m"
    sleep 1
    num_jobs=`qstat -u '*' | grep -P '^\d' | tr -s ' ' | cut -f4 -d' ' | grep ${usern} | wc -l`      
    if [ $num_jobs -lt $max_jobs ]
    then 
      echo -e "\e[92mSubmitting again...\e[0m"
    fi
  done
  qsub -S /bin/bash -wd ${output_dir} -p -200 -e /dev/null -o /dev/null  ${code_root}/run/stage2a.sh ${i} ${input_dir} ${output_dir} ${code_root}
done
popd
