# #!/bin/bash

# # 检查是否输入了一个参数
# if [ "$#" -ne 1 ]; then
#     echo "Usage: $0 <list_file>"
#     exit 1
# fi

# # 获取文件列表参数
# list_file=$1

# # 检查文件是否存在
# if [ ! -f "$list_file" ]; then
#     echo "File not found!"
#     exit 1
# fi

# # 获取开始时间
# start=$(date +%s)

# # 读取list.txt中的每一行
# while read line; do
#   echo "Processing line: $line"
#   # 获取文件名（不含路径和后缀）
#   filename=$(basename -- "$line")
#   filename="${filename%.*}"

#   # 创建一个基于PID的唯一临时文件
#   temp_file="config_en_ocr_bz_temp_$$"

#   # 复制一份原始的yaml文件
#   cp config_en_ocr_bz.yaml $temp_file.yaml

#   # 使用sed命令替换yaml文件中的特定行
#   sed -i "s|resources/corpus/enwiki.txt|$line|g" $temp_file.yaml

#   # 忽略错误并运行srun命令
#   set +e
#   # (105+48) * 10W = 15M
#   # srun -p bigdata --ntasks=1 --cpus-per-task=100 --mem=1000000 synthtiger -o "./mllm-ocr/en/$filename" -c 100000 -w 64 -v template.py SynthDoG $temp_file.yaml < /dev/null || echo "srun command failed on file $line"
#   # (105+48) * 66W = 100M
#   srun -p bigdata --ntasks=1 --cpus-per-task=100 --mem=1000000 synthtiger -o "./mllm-ocr/en/$filename" -c 660000 -w 64 -v template.py SynthDoG $temp_file.yaml < /dev/null || echo "srun command failed on file $line"

#   # 删除临时的yaml文件
#   rm $temp_file.yaml

# done < "$list_file"

# # 计算并打印执行时间
# end=$(date +%s)
# duration=$((end - start))
# echo "Total execution time: $duration seconds"

#!/bin/bash

# 检查是否输入了一个参数
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <list_file>"
    exit 1
fi

# 获取文件列表参数（假定为相对路径）
list_file="./list_en/$1"

# 检查文件是否存在
if [ ! -f "$list_file" ]; then
    echo "File not found!"
    exit 1
fi

# 获取开始时间
start=$(date +%s)

# 读取list.txt中的每一行
while read line; do
  echo "Processing line: $line"
  # 获取文件名（不含路径和后缀）
  filename=$(basename -- "$line")
  filename="${filename%.*}"

  # 创建一个基于PID的唯一临时文件
  temp_file="config_en_ocr_sp_temp_$$"

  # 复制一份原始的yaml文件
  cp config_en_ocr_sp.yaml $temp_file.yaml

  # 使用sed命令替换yaml文件中的特定行
  sed -i "s|resources/corpus/enwiki.txt|$line|g" $temp_file.yaml

  # 忽略错误并运行srun命令
  set +e
  synthtiger -o "./en-noise/1M/$filename" -c 10000 -w 4 -v template_special SynthDoG $temp_file.yaml \
      < /dev/null || echo "srun command failed on file $line"

  # 删除临时的yaml文件
  rm $temp_file.yaml
  

done < "$list_file"

# 计算并打印执行时间
end=$(date +%s)
duration=$((end - start))
echo "Total execution time: $duration seconds"