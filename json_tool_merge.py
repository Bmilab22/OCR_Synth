
#---------------file_namc --------------
import os
import json


# import os
# import json
# def update_file_paths(base_dir):
#     # 遍历主文件夹下的所有子文件夹
#     for subdir in os.listdir(base_dir):
#         subdir_path = os.path.join(base_dir, subdir)
#         if os.path.isdir(subdir_path):
#             metadata_file = os.path.join(subdir_path, 'metadata.jsonl')
#             print(f"Processed{metadata_file}")
#             if os.path.exists(metadata_file):
#                 updated_lines = []
#                 entry_count = 0
#                 total_entries = 0  # 记录总条目数
#                 with open(metadata_file, 'r', encoding='utf-8') as f:
#                     for line in f:
#                         total_entries += 1  # 每读取一行就增加总条目数
#                         data = json.loads(line.strip())
#                         file_name = data.get('file_name')
#                         if file_name:
#                             # 构造新的文件路径
#                             new_file_path = os.path.join('./outputs_en', subdir, file_name).replace('\\', '/')
#                             # 更新字典
#                             del data['file_name']
#                             data['image_filepath'] = new_file_path
#                             entry_count += 1
#                         updated_lines.append(json.dumps(data, ensure_ascii=False))
#                 # 将更新后的内容写回文件
#                 with open(metadata_file, 'w', encoding='utf-8') as f:
#                     for updated_line in updated_lines:
#                         f.write(updated_line + '\n')
                        
#                 # 输出每个jsonl文件中的条目数量
#                 print(f"Processed {entry_count} entries in {metadata_file}")
#                 print(f"Processed {total_entries} entries in {metadata_file}")

# # 指定主文件夹路径
# base_dir = '/mnt/petrelfs/zhujiawei/Projects/donut-master/synthdog/1M'

# # 调用函数进行处理
# update_file_paths(base_dir)


#---------------image_path -> s3 ceph --------------


# def update_file_paths(base_dir, s3_prefix):
#     for subdir in os.listdir(base_dir):
#         subdir_path = os.path.join(base_dir, subdir)
#         if os.path.isdir(subdir_path):
#             metadata_file = os.path.join(subdir_path, 'metadata_page.jsonl')
#             output_file = os.path.join(subdir_path, 'synthdog_subresult.jsonl')

#             if os.path.exists(metadata_file):
#                 updated_lines = []
#                 entry_count = 0
#                 with open(metadata_file, 'r', encoding='utf-8') as f:
#                     for line in f:
#                         try:
#                             data = json.loads(line.strip())
#                             image_filepath = data.get('image_filepath')
#                             if image_filepath and image_filepath.startswith('./outputs_cn_en_paper/'):
#                                 # 构造新的S3文件路径
#                                 new_file_path = os.path.join(s3_prefix, os.path.relpath(image_filepath, './outputs_cn_en_paper/')).replace('\\', '/')
#                                 # 更新字典中的image_filepath
#                                 data['image_filepath'] = new_file_path
#                                 entry_count += 1
#                             updated_lines.append(json.dumps(data, ensure_ascii=False))
#                         except json.JSONDecodeError as e:
#                             print(f"Failed to decode JSON object in {subdir}: {e}")
#                             continue
                
#                 # 将更新后的内容写入新文件
#                 with open(output_file, 'w', encoding='utf-8') as f:
#                     for updated_line in updated_lines:
#                         f.write(updated_line + '\n')
                
#                 # 输出每个jsonl文件中的条目数量
#                 print(f"Processed {entry_count} entries in {metadata_file} and saved to {output_file}")

# # 指定主文件夹路径和S3前缀
# base_dir = '/mnt/petrelfs/zhujiawei/Projects/donut-master/synthdog/outputs_cn_en_paper'
# s3_prefix = 's3://doc-parse-huawei/mineru2/synthdog/outputs_cn_en_paper'

# # 调用函数进行处理
# update_file_paths(base_dir, s3_prefix)





import os
import json

def merge_jsonl_files(base_dir, output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        total_entries = 0
        for subdir in os.listdir(base_dir):
            subdir_path = os.path.join(base_dir, subdir)
            if os.path.isdir(subdir_path):
                input_file = os.path.join(subdir_path, 'synthdog_subresult.jsonl')
                if os.path.exists(input_file):
                    entry_count = 0
                    with open(input_file, 'r', encoding='utf-8') as infile:
                        for line in infile:
                            # 确保每行是有效的JSON对象并写入输出文件
                            try:
                                json_object = json.loads(line.strip())
                                outfile.write(json.dumps(json_object, ensure_ascii=False) + '\n')
                                entry_count += 1
                                total_entries += 1
                            except json.JSONDecodeError as e:
                                print(f"Failed to decode JSON object in {input_file}: {e}")
                                continue
                    
                    # 输出每个jsonl文件中的条目数量
                    print(f"Merged {entry_count} entries from {input_file}")

        # 输出总条目数量
        print(f"All entries ({total_entries}) have been merged into {output_file}.")

# 指定主文件夹路径和输出文件路径
base_dir = '/mnt/petrelfs/zhujiawei/Projects/donut-master/synthdog/outputs_cn_en_paper/'
output_file = '/mnt/petrelfs/zhujiawei/Projects/donut-master/synthdog/outputs_cn_en_paper/synthdog_result_cnen_1M.jsonl'

# 调用函数进行处理
merge_jsonl_files(base_dir, output_file)

# import os
# import json

# def update_file_paths(base_dir):
#     # 用于存储所有已处理的 image_id，防止重复处理
#     processed_image_ids = set()
    
#     for subdir in os.listdir(base_dir):
#         subdir_path = os.path.join(base_dir, subdir)
#         if os.path.isdir(subdir_path):
#             metadata_file = os.path.join(subdir_path, 'metadata.jsonl')
#             if os.path.exists(metadata_file):
#                 updated_lines = []
#                 entry_count = 0
#                 with open(metadata_file, 'r', encoding='utf-8') as f:
#                     for line in f:
#                         try:
#                             data = json.loads(line.strip())
#                             file_name = data.get('file_name')
#                             image_id = data.get('ground_truth', {}).get('gt_parse', {}).get('text_sequence', {}).get('ocr', [{}])[0].get('text', None)  # 尝试获取image_id
                            
#                             if file_name and image_id not in processed_image_ids:
#                                 # 构造新的文件路径
#                                 new_file_path = os.path.join('./outputs_en', subdir, file_name).replace('\\', '/')
#                                 # 更新字典
#                                 del data['file_name']
#                                 data['image_filepath'] = new_file_path
                                
#                                 # 添加到已处理的image_id集合中
#                                 processed_image_ids.add(image_id)
#                                 entry_count += 1
#                             elif file_name:  # 如果file_name存在但image_id已经在集合中，则跳过该条目
#                                 entry_count += 1
#                                 continue
#                             else:
#                                 updated_lines.append(json.dumps(data, ensure_ascii=False))
#                                 continue
                            
#                             updated_lines.append(json.dumps(data, ensure_ascii=False))
#                         except json.JSONDecodeError as e:
#                             print(f"Failed to decode JSON object in {subdir}: {e}")
#                             continue
                
#                 # 将更新后的内容写回文件
#                 with open(metadata_file, 'w', encoding='utf-8') as f:
#                     for updated_line in updated_lines:
#                         f.write(updated_line + '\n')
                
#                 # 输出每个jsonl文件中的条目数量
#                 print(f"Processed {entry_count} entries in {metadata_file}")

# # 指定主文件夹路径
# base_dir = '/mnt/petrelfs/zhujiawei/Projects/donut-master/synthdog/outputs_en'

# # 调用函数进行处理
# update_file_paths(base_dir)