def remove_duplicate_lines(input_file, output_file):
    lines_seen = set()
    with open(input_file, 'r', encoding='utf-8') as fin, \
         open(output_file, 'w', encoding='utf-8') as fout:
        for line in fin:
            if line not in lines_seen:
                fout.write(line)
                lines_seen.add(line)

# Ví dụ sử dụng:
remove_duplicate_lines('input.txt', 'output.txt')
print("Đã lọc trùng và xuất ra file output.txt!")
