import os

def read_lines_from_file(file_path):
    """Read lines from a file and yield one by one."""
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            stripped_line = line.strip()
            if stripped_line:  # Skip empty lines
                yield stripped_line

def write_lines_to_file(file_path, lines):
    """Write lines to a file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        for line in lines:
            file.write(line + '\n')

def get_paths_from_txt_files(directory, num_files=5):
    """Get the paths listed in the first `num_files` .txt files in the directory."""
    txt_files = sorted([os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.txt')])[:num_files]
    paths = []
    for txt_file in txt_files:
        with open(txt_file, 'r', encoding='utf-8') as file:
            for line in file:
                stripped_line = line.strip()
                if stripped_line:  # Skip empty lines
                    paths.append(stripped_line)
    return paths

def merge_content_from_paths(cn_paths, en_paths, output_dir):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process each pair of paths
    for index, (cn_path, en_path) in enumerate(zip(cn_paths, en_paths), start=1):
        try:
            cn_content_gen = read_lines_from_file(cn_path)
            en_content_gen = read_lines_from_file(en_path)

            merged_lines = []
            for cn_line, en_line in zip(cn_content_gen, en_content_gen):
                merged_lines.append(cn_line)
                merged_lines.append(en_line)

            # Write the merged lines to the output file
            output_filename = f'part_cn_en_{index:02d}.txt'
            output_file_path = os.path.join(output_dir, output_filename)
            write_lines_to_file(output_file_path, merged_lines)

            print(f"Merged file saved at: {output_file_path}")

        except Exception as e:
            print(f"Error processing files {cn_path} and {en_path}: {e}")
            continue

# Define your directories and output settings here
list_cn_directory = '/mnt/petrelfs/zhujiawei/Projects/donut-master/synthdog/list_cn/'
list_en_directory = '/mnt/petrelfs/zhujiawei/Projects/donut-master/synthdog/list_en/'
output_directory = '/mnt/petrelfs/zhujiawei/Projects/donut-master/synthdog/list_cn_en/'

# Get the paths from the first 5 .txt files in each directory
cn_paths = get_paths_from_txt_files(list_cn_directory)
en_paths = get_paths_from_txt_files(list_en_directory)

# Ensure we only process an equal number of paths from both lists
min_num_paths = min(len(cn_paths), len(en_paths))
cn_paths = cn_paths[:min_num_paths]
en_paths = en_paths[:min_num_paths]

merge_content_from_paths(cn_paths, en_paths, output_directory)