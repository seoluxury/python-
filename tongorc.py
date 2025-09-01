import os
import re
import json
from queue import Queue
from threading import Thread, Lock
from google.cloud import vision

# -----------------------
# Cấu hình
# -----------------------
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Seo\Desktop\ocr-project-470114-0be380220168.json"

# Danh sách folder muốn OCR
folder_list = [
    r"E:\New folder\1",
    r"E:\New folder\2",
    r"E:\New folder\3"
]

NUM_THREADS = 10       # số luồng OCR cùng lúc
MAX_RETRIES = 5        # retry khi lỗi
lock = Lock()          # tránh conflict giữa các thread

# Biến tổng hợp tất cả kết quả
all_results = {}

# -----------------------
# Hàm lấy số trong tên file
# -----------------------
def extract_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else 0

# -----------------------
# Khởi tạo client Google Vision
# -----------------------
client = vision.ImageAnnotatorClient()

def run_ocr_for_folder(folder_path):
    output_file = os.path.join(folder_path, "output_text.txt")
    progress_file = os.path.join(folder_path, "processed_images.json")

    # Load ảnh đã xử lý
    if os.path.exists(progress_file):
        with open(progress_file, "r", encoding="utf-8") as pf:
            processed_images = json.load(pf)
    else:
        processed_images = []

    # Lấy danh sách file ảnh
    all_files = [
        f for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]
    all_files.sort(key=extract_number)

    # Queue ảnh cần OCR
    queue = Queue()
    for f in all_files:
        if f not in processed_images:
            queue.put(f)

    # Kết quả OCR tạm (filename -> text)
    results = {}

    # -----------------------
    # Hàm OCR 1 ảnh
    # -----------------------
    def ocr_worker():
        nonlocal results, processed_images
        while not queue.empty():
            filename = queue.get()
            image_path = os.path.join(folder_path, filename)

            for attempt in range(MAX_RETRIES + 1):
                try:
                    with open(image_path, "rb") as f:
                        content = f.read()
                    image = vision.Image(content=content)
                    response = client.text_detection(image=image)
                    texts = response.text_annotations
                    text = texts[0].description if texts else ""
                    break
                except Exception as e:
                    if attempt < MAX_RETRIES:
                        print(f"Lỗi {filename}, thử lại ({attempt+1}/{MAX_RETRIES})…: {e}")
                    else:
                        text = f"Thất bại sau {MAX_RETRIES+1} lần: {e}"

            # Lưu vào dict kết quả
            with lock:
                results[filename] = text
                processed_images.append(filename)
            print(f"Xong {filename}")
            queue.task_done()

    # -----------------------
    # Chạy multi-thread
    # -----------------------
    threads = []
    for _ in range(NUM_THREADS):
        t = Thread(target=ocr_worker)
        t.start()
        threads.append(t)

    queue.join()
    for t in threads:
        t.join()

    # -----------------------
    # Ghi kết quả ra file theo đúng thứ tự số
    # -----------------------
    processed_images = sorted(set(processed_images), key=extract_number)

    with open(progress_file, "w", encoding="utf-8") as pf:
        json.dump(processed_images, pf, ensure_ascii=False, indent=2)

    with open(output_file, "w", encoding="utf-8") as out_file:
        for fname in processed_images:
            text = results.get(fname, "")
            out_file.write(f"----- {fname} -----\n{text}\n\n")

            # Ghi thêm vào file tổng
            all_results[os.path.join(folder_path, fname)] = text

    print(f"Hoàn tất OCR folder: {folder_path}")


# -----------------------
# Chạy lần lượt tất cả folder
# -----------------------
for folder in folder_list:
    if os.path.exists(folder):
        run_ocr_for_folder(folder)
    else:
        print(f"Bỏ qua vì không tồn tại: {folder}")

# -----------------------
# Xuất file tổng hợp
# -----------------------
total_output = os.path.join(os.path.dirname(__file__), "output_all.txt")
with open(total_output, "w", encoding="utf-8") as f:
    for fname, text in all_results.items():
        f.write(f"----- {fname} -----\n{text}\n\n")

print(f"🎉 Hoàn tất OCR tất cả folder! File tổng: {total_output}")
