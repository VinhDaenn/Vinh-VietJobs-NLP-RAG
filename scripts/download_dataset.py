#!/usr/bin/env python3
"""Lấy dataset VietJobs gốc từ HF (không API key) hoặc CSV có sẵn, tạo data/VietJobs.csv.gz cho Git.

Chạy:
  python scripts/download_dataset.py
  python scripts/download_dataset.py --input ~/Downloads/VietJobs.csv
"""
import argparse
import gzip
import hashlib
import shutil
import sys
import tempfile
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

SOURCE = "https://huggingface.co/datasets/dinhieufam/VietJobs/resolve/main/VietJobs.csv?download=true"
EXPECTED_SHA256 = "85862b06fda4e814fe0c1d8622f173d189c92758345f77df16d1232d0c49d477"
BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data"
MIN_SIZE = 100_000_000


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as src:
        for block in iter(lambda: src.read(2 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def download(dest):
    request = Request(SOURCE, headers={"User-Agent": "VietJobsResearch/1.0", "Accept": "application/octet-stream"})
    try:
        with urlopen(request, timeout=120) as response, dest.open('wb') as target:
            shutil.copyfileobj(response, target, 2 * 1024 * 1024)
    except (URLError, HTTPError, TimeoutError) as exc:
        raise RuntimeError("Không tải được dataset. Tải CSV bằng trình duyệt rồi chạy --input <đường_dẫn>. URL: " + SOURCE) from exc


def main():
    ap = argparse.ArgumentParser(description='Tải và nén VietJobs.csv để đưa lên Git')
    ap.add_argument('--input', type=Path, help='Đường dẫn VietJobs.csv đã tải sẵn')
    ap.add_argument('--force', action='store_true', help='Ghi đè data/VietJobs.csv.gz')
    args = ap.parse_args()
    DATA.mkdir(parents=True, exist_ok=True)
    target = DATA / 'VietJobs.csv.gz'
    if target.exists() and not args.force:
        print('Đã có:', target, f'({target.stat().st_size/1024**2:.1f} MiB)')
        print('Nếu muốn tạo lại, dùng --force')
        return 0

    with tempfile.TemporaryDirectory(prefix='vietjobs_') as tempdir:
        temp = Path(tempdir)
        csvfile = args.input.expanduser().resolve() if args.input else temp / 'VietJobs.csv'
        if args.input:
            if not csvfile.is_file():
                raise FileNotFoundError(f'Không tìm thấy CSV: {csvfile}')
            print('Đọc file đã tải:', csvfile)
        else:
            print('Tải dữ liệu VietJobs (103 MB) từ:', SOURCE)
            download(csvfile)
        if csvfile.stat().st_size < MIN_SIZE:
            raise RuntimeError(f'CSV chỉ có {csvfile.stat().st_size} bytes, không phải dataset đầy đủ. Hãy kiểm tra file.')
        digest = sha256(csvfile)
        if digest != EXPECTED_SHA256:
            raise RuntimeError(
                'SHA-256 của file khác file VietJobs.csv gốc.\n'
                f'Thực tế: {digest}\nMong đợi: {EXPECTED_SHA256}\n'
                'Bạn có thể đã tải nhầm hoặc file từ phiên bản khác.'
            )
        print('Đã xác thực SHA-256:', digest)
        temp_gz = DATA / 'VietJobs.csv.gz.partial'
        try:
            with csvfile.open('rb') as source, gzip.open(temp_gz, 'wb', compresslevel=9) as packed:
                shutil.copyfileobj(source, packed, 2 * 1024 * 1024)
            temp_gz.replace(target)
        finally:
            temp_gz.unlink(missing_ok=True)

    mb = target.stat().st_size / 1024**2
    print(f'Đã tạo {target} ({mb:.1f} MiB).')
    if target.stat().st_size > 100 * 1024**2:
        print('CẢNH BÁO: >100 MiB; cần Git LFS hoặc không commit file dataset.')
    else:
        print('Có thể dùng git add data/VietJobs.csv.gz nếu quyền phân phối lại cho phép.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
