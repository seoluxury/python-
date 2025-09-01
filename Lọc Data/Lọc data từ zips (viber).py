import os
import zipfile



def extract_and_normalize_phones(zip_folder, output_file):
    phone_set = set()
    zip_files = [f for f in os.listdir(zip_folder) if f.endswith('.zip')]
    for zip_file in zip_files:
        zip_path = os.path.join(zip_folder, zip_file)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file in zip_ref.namelist():
                if file.endswith('.txt'):
                    with zip_ref.open(file) as f:
                        for line in f:
                            try:
                                line = line.decode('utf-8')
                            except:
                                continue
                            digits = ''.join(filter(str.isdigit, line))
                            if not digits:
                                continue
                            if digits.startswith('0') and len(digits) == 10:
                                digits = '84' + digits[1:]
                            elif digits.startswith('84') and len(digits) == 11:
                                pass
                            elif len(digits) == 9:
                                digits = '84' + digits
                            else:
                                continue
                            phone_set.add(digits)
    with open(output_file, 'w', encoding='utf-8') as fout:
        for phone in sorted(phone_set):
            fout.write(phone + '\n')

if __name__ == "__main__":
 
    zip_folder = 'zips'
    final_output = 'minh seo đã xuất.txt'
    extract_and_normalize_phones(zip_folder, final_output)

    # Thông báo popup khi hoàn thành
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Hoàn thành", f"Đã xuất file: {final_output}")
    root.destroy()
