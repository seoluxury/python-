import zipfile
import os

def read_all_txt_from_zips(zip_folder, output_file):
    zip_files = [f for f in os.listdir(zip_folder) if f.endswith('.zip')]
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for zip_file in zip_files:
            zip_path = os.path.join(zip_folder, zip_file)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                for file in zip_ref.namelist():
                    if file.endswith('.txt'):
                        with zip_ref.open(file) as f:
                            content = f.read().decode('utf-8')
                            outfile.write(content + '\n')

# Thay 'zips' bằng tên thư mục chứa các file zip, 'output.txt' là file kết quả
read_all_txt_from_zips('zips', 'output.txt')
