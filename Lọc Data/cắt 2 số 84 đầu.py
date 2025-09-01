input_file = "input.txt"
output_file = "output.txt"

with open(input_file, "r", encoding="utf-8") as infile, \
     open(output_file, "w", encoding="utf-8") as outfile:
    for line in infile: 
        # Loại bỏ ký tự xuống dòng để kiểm tra dòng trống
        if line.strip() == "":
            continue  # Gặp dòng trống thì "cho cút đi"
        outfile.write(line[2:])
