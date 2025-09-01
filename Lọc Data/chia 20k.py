# Script chia file input.txt thành nhiều file nhỏ, mỗi file tối đa 50 000 dòng

input_file = "input.txt"
lines_per_file = 20000

with open(input_file, "r", encoding="utf-8") as infile:
    file_count = 1
    while True:
        # Đọc tối đa lines_per_file dòng mỗi lượt
        lines = []
        for _ in range(lines_per_file):
            line = infile.readline()
            if not line:
                break
            lines.append(line)
        if not lines:
            break  # Đã đọc hết file gốc

        output_file = f"output_{file_count}.txt"
        with open(output_file, "w", encoding="utf-8") as outfile:
            outfile.writelines(lines)
        print(f"Đã tạo {output_file} ({len(lines)} dòng)")
        file_count += 1
