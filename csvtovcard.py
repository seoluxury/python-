import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import os

def csv_to_vcard(csv_file, vcard_file):
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        # Đọc một đoạn đầu để tự phát hiện delimiter
        sample = csvfile.read(2048)
        csvfile.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=";,|\t")
        except Exception:
            dialect = csv.excel  # Mặc định là dấu phẩy
        reader = csv.DictReader(csvfile, dialect=dialect)
        count = 0
        for row in reader:
            name = ''
            phone = ''
            for k, v in row.items():
                if k and k.strip().lower() == 'name':
                    name = v.strip() if v else ''
                if k and k.strip().lower() == 'phone':
                    phone = v.strip() if v else ''
            if not name and not phone:
                continue
            with open(vcard_file, 'a', encoding='utf-8') as vcardfile:
                vcardfile.write('BEGIN:VCARD\n')
                vcardfile.write('VERSION:3.0\n')
                vcardfile.write(f'FN:{name}\n')
                vcardfile.write(f'TEL;TYPE=CELL:{phone}\n')
                vcardfile.write('END:VCARD\n\n')
                count += 1
    return count

def select_file():
    file_path = filedialog.askopenfilename(
        title="Chọn file CSV",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    if file_path:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, file_path)

def convert():
    csv_file = entry_file.get()
    if not csv_file or not os.path.isfile(csv_file):
        messagebox.showerror("Lỗi", "Vui lòng chọn file CSV hợp lệ!")
        return
    vcf_file = os.path.splitext(csv_file)[0] + ".vcf"
    # Xóa file vcf cũ nếu có
    if os.path.exists(vcf_file):
        os.remove(vcf_file)
    try:
        count = csv_to_vcard(csv_file, vcf_file)
        messagebox.showinfo("Thành công", f"Đã chuyển {count} liên hệ sang file:\n{vcf_file}")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể chuyển file:\n{e}")

# Giao diện
root = tk.Tk()
root.title("Chuyển CSV sang vCard (.vcf)")
root.geometry("430x120")
root.resizable(False, False)

lbl = tk.Label(root, text="Chọn file CSV (cột name/Name, phone/Phone):")
lbl.pack(pady=(10,2))

frame = tk.Frame(root)
frame.pack(pady=2)

entry_file = tk.Entry(frame, width=40)
entry_file.pack(side=tk.LEFT, padx=5)
btn_browse = tk.Button(frame, text="Chọn file...", command=select_file)
btn_browse.pack(side=tk.LEFT)

btn_convert = tk.Button(root, text="Chuyển qua vCard", width=20, command=convert, bg="#28a745", fg="white")
btn_convert.pack(pady=15)

root.mainloop()
