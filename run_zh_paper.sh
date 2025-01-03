
#!/bin/bash

# 检查是否输入了一个参数
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <list_file>"
    exit 1
fi

# 获取文件列表参数（假定为相对路径）
list_file="./list_cn/$1"

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
  temp_file="config_zh_paper_new_temp_$$"

  # 复制一份原始的yaml文件
  cp config_zh_paper_new.yaml $temp_file.yaml

  # 使用sed命令替换yaml文件中的特定行
  sed -i "s|resources/corpus/zhwiki.txt|$line|g" $temp_file.yaml

  # 忽略错误并运行srun命令
  set +e
  synthtiger -o "./doc-zh/1M/$filename" -c 20000 -w 4 -v template_paper SynthDoG $temp_file.yaml \
      < /dev/null || echo "srun command failed on file $line"

  # 删除临时的yaml文件
  rm $temp_file.yaml
  

done < "$list_file"

# 计算并打印执行时间
end=$(date +%s)
duration=$((end - start))
echo "Total execution time: $duration seconds"