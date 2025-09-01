def process_vn_phone_numbers(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as fin, \
         open(output_file, 'w', encoding='utf-8') as fout:
        for line in fin:
            digits = ''.join(filter(str.isdigit, line))
            if not digits:
                continue
            if digits.startswith('0') and len(digits) == 10:
                digits = '+84' + digits[1:]
            elif digits.startswith('84') and len(digits) == 11:
                digits = '+84' + digits[2:]
            elif len(digits) == 9:
                digits = '+84' + digits
            else:
                continue
            fout.write(digits + '\n')

# Gọi hàm
process_vn_phone_numbers('input.txt', 'output.txt')
print("Đã xuất file output.txt!")
