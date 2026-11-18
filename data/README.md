# Dữ liệu VietJobs

**Nguồn chính thức:** https://huggingface.co/datasets/dinhieufam/VietJobs

**File công khai:** https://huggingface.co/datasets/dinhieufam/VietJobs/resolve/main/VietJobs.csv

Tập dữ liệu gốc khoảng 103 MB, gồm 48.092 tin tuyển dụng từ nhiều ngành nghề. Không phải tất cả các JD đều thuộc CNTT và không phải tất cả có nhãn kỹ năng dùng được.

## Thêm dữ liệu vào repo (không cần API key)

Tại thư mục gốc của repo, chạy:

```bash
python scripts/download_dataset.py
```

Script sẽ tải/kiểm tra file gốc từ Hugging Face, sau đó nén thành `data/VietJobs.csv.gz` và không giữ bản CSV 103 MB trong Git. Để dùng file CSV đã tải bằng trình duyệt:

```bash
python scripts/download_dataset.py --input "/duong-dan/VietJobs.csv"
```

Chỉ sau khi chạy thành công, folder mới **chứa bộ dữ liệu thật**. File nén không được đóng gói sẵn trong ZIP của dự án do môi trường tạo dự án không truy cập được Hugging Face.

Notebook `Vinhtrain_VietJobs.ipynb` tự tìm `data/VietJobs.csv.gz` trước khi tải mạng. CSV gốc bị `.gitignore` loại trừ. Giới hạn kích thước **một file GitHub thường** là 100 MiB; kiểm tra dung lượng file nén, dùng Git LFS nếu vượt ngưỡng.

**Trích dẫn:** Pham-Dinh et al., *VietJobs: A Vietnamese Job Advertisement Dataset*, 2026. Xem dự án https://github.com/VinNLP/VietJobs và các điều kiện cấp phép ở nguồn gốc trước khi phân phối lại toàn bộ dữ liệu.
