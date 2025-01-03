def read_first_n_lines(file_path, n=500):
    """
    Read the first `n` lines from a file and return them as a list of strings.
    
    :param file_path: Path to the text file to read.
    :param n: Number of lines to read. Default is 500.
    :return: List containing the first `n` lines of the file.
    """
    lines = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for idx, line in enumerate(file):
            if idx == n:
                break
            lines.append(line.strip())
    return lines

def write_lines_to_file(lines, output_file_path):
    """
    Write lines to an output file.
    
    :param lines: List of strings to write to the file.
    :param output_file_path: Path to the output file.
    """
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for line in lines:
            file.write(line + '\n')

def main(input_file_path, output_file_path, num_lines=500):
    """
    Main function to read the first `num_lines` from `input_file_path` and save them to `output_file_path`.
    
    :param input_file_path: The path to the large text file.
    :param output_file_path: The path where to save the first `num_lines`.
    :param num_lines: The number of lines to read and save.
    """
    # Read the first `num_lines` from the input file
    first_n_lines = read_first_n_lines(input_file_path, num_lines)
    
    # Optionally print the lines to console (uncomment the next line if you want to print to console)
    # for line in first_n_lines: print(line)
    
    # Write the first `num_lines` to the output file
    write_lines_to_file(first_n_lines, output_file_path)

if __name__ == "__main__":
    # Define your input and output file paths here
    input_file_path = '/mnt/petrelfs/zhujiawei/Projects/donut-master/synthdog/list_cn_en/part_cn_en_01.txt'
    output_file_path = '/mnt/petrelfs/zhujiawei/Projects/donut-master/synthdog/list_cn_en/part_cn_en_500.txt'
    
    # Call the main function to process the files
    main(input_file_path, output_file_path, num_lines=500)