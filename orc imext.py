import os
import re
import requests
import time
import json
from collections import deque

# -----------------------
# Cấu hình
# -----------------------
API_KEY = "d12a803ef752aaa818ab78dc0bbeae6bc75f0ee3"  # Thay bằng API key thật
API_URL = "https://www.imagetotext.info/api/imageToText"

folder_path = r"C:\Users\Seo\Desktop\New folder\3"  # Thư mục chứa ảnh
output_file = "output_text.txt"
progress_file = "processed_images.json"

REQUESTS_PER_MIN = 30   # tối đa 30 request/phút
MAX_RETRIES = 2         # số lần thử lại khi lỗi mạng

# -----------------------
# Load ảnh đã xử lý
# -----------------------
if os.path.exists(progress_file):
    with open(progress_file, "r", encoding="utf-8") as pf:
        processed_images = json.load(pf)
else:
    processed_images = []

# -----------------------
# Lấy danh sách ảnh + sort theo số
# -----------------------
def extract_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else 0

all_files = [
    f for f in os.listdir(folder_path)
    if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith((".png", ".jpg", ".jpeg"))
]
all_files.sort(key=extract_number)

# -----------------------
# Token bucket để giới hạn 30 request/phút
# -----------------------
request_times = deque()

def wait_for_slot():
    now = time.time()
    while len(request_times) >= REQUESTS_PER_MIN:
        if now - request_times[0] > 60:
            request_times.popleft()
        else:
            sleep_time = 60 - (now - request_times[0])
            print(f"Đã gửi {REQUESTS_PER_MIN} request, chờ {sleep_time:.1f}s để sang phút mới...")
            time.sleep(sleep_time)
            now = time.time()

# -----------------------
# Xử lý ảnh
# -----------------------
with open(output_file, "a", encoding="utf-8") as out_file:
    for i, filename in enumerate(all_files):
        if filename in processed_images:
            print(f"{i+1}/{len(all_files)}: Đã xử lý {filename}, bỏ qua")
            continue

        image_path = os.path.join(folder_path, filename)

        # Giới hạn request
        wait_for_slot()

        for attempt in range(MAX_RETRIES + 1):
            try:
                with open(image_path, "rb") as f:
                    files = {"image": f}
                    headers = {"Authorization": f"Bearer {API_KEY}"}
                    response = requests.post(API_URL, headers=headers, files=files, timeout=30)

                request_times.append(time.time())  # log thời gian request

                if response.status_code == 200:
                    try:
                        result = response.json()
                        if not result.get("error", True):
                            text = result.get("result", "")
                        else:
                            text = f"API Error: {result.get('message', 'Unknown error')}"
                    except Exception:
                        text = f"Parse Error: {response.text}"
                elif response.status_code == 422:
                    text = "OCR Failed"
                else:
                    text = f"HTTP Error {response.status_code}: {response.text}"

                # Nếu request thành công, thoát vòng retry
                break

            except requests.exceptions.RequestException as e:
                if attempt < MAX_RETRIES:
                    print(f"Lỗi {filename}, thử lại ({attempt+1}/{MAX_RETRIES})…: {e}")
                    time.sleep(2)
                else:
                    text = f"Failed after {MAX_RETRIES+1} attempts: {e}"

        # Ghi kết quả
        out_file.write(f"----- {filename} -----\n{text}\n\n")
        out_file.flush()

        # Cập nhật danh sách đã xử lý
        processed_images.append(filename)
        with open(progress_file, "w", encoding="utf-8") as pf:
            json.dump(processed_images, pf, ensure_ascii=False, indent=2)

        print(f"{i+1}/{len(all_files)}: Xong {filename}")
