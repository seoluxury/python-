from collections import Counter

def filter_unique_numbers(input_file, output_file):
    # Đọc toàn bộ số (mỗi dòng 1 số, đã chuẩn hóa)
    with open(input_file, 'r', encoding='utf-8') as fin:
        numbers = [line.strip() for line in fin if line.strip()]

    # Đếm số lần xuất hiện
    counts = Counter(numbers)

    # Lọc ra các số chỉ xuất hiện đúng 1 lần
    unique_numbers = [num for num, count in counts.items() if count == 1]

    # Sắp xếp nếu muốn
    unique_numbers_sorted = sorted(unique_numbers)

    # Ghi ra file output, mỗi số 1 dòng
    with open(output_file, 'w', encoding='utf-8') as fout:
        for num in unique_numbers_sorted:
            fout.write(num + '\n')

# Ví dụ sử dụng
filter_unique_numbers('input.txt', 'output.txt')
