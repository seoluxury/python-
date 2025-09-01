def loc_trung(file_tong, file_kiemtra, file_ketqua):
    # Đọc dữ liệu từ file tổng
    with open(file_tong, "r", encoding="utf-8") as f:
        tong_set = set(line.strip() for line in f if line.strip())

    # Đọc file cần kiểm tra
    with open(file_kiemtra, "r", encoding="utf-8") as f:
        kiemtra_list = [line.strip() for line in f if line.strip()]

    # Lọc bỏ những dòng trùng
    ketqua = [line for line in kiemtra_list if line not in tong_set]

    # Ghi ra file kết quả
    with open(file_ketqua, "w", encoding="utf-8") as f:
        for line in ketqua:
            f.write(line + "\n")

    print(f"Đã lọc xong. Kết quả được lưu tại: {file_ketqua}")


# Ví dụ chạy
if __name__ == "__main__":
    loc_trung("tong.txt", "kiemtra.txt", "ketqua.txt")
