runId=`date +%Y%m%d%H%M%S`
interval_min=60
file_input_dir="/tmp"
file_output_dir="/tmp"

find $file_input_dir -type f -name '*.out' -mmin ${interval_min} -exec stat  --printf="runId=$runId fname=%n fsize=%s atime=%X mtime=%Y ctime=%Z \n" {} \;
