"""国土地理院 指定緊急避難場所・指定避難所データのダウンロード。

国土地理院「指定緊急避難場所データ」サイト (hinanmap.gsi.go.jp) から
市区町村提供データを統合した全国版 CSV (UTF-8 BOM 付き) をダウンロードする。

データソース: 指定緊急避難場所データ
https://www.gsi.go.jp/bousaichiri/hinanbasho.html
"""

import logging
from pathlib import Path
from urllib.request import Request, urlopen

logger = logging.getLogger("pipelines")

BASE_URL = "https://hinanmap.gsi.go.jp/hinanjocp/defaultFtpData/csv"

FILES = [
    # 指定避難所（災害対策基本法第49条の7）
    "mergeFromCity_1.csv",
    # 指定緊急避難場所（災害対策基本法第49条の4）
    "mergeFromCity_2.csv",
]


def download_evacuation_data(dest_dir: str) -> None:
    """全国統合版の指定緊急避難場所・指定避難所 CSV をダウンロードする。

    既にダウンロード済みの場合はスキップする。
    """
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)

    for filename in FILES:
        csv_path = dest / filename
        if csv_path.exists():
            logger.info(f"  skip (already exists: {csv_path})")
            continue

        logger.info(f"  downloading {filename}...")
        req = Request(f"{BASE_URL}/{filename}", headers={"User-Agent": "dataset-gsi"})
        tmp_path = csv_path.with_suffix(".tmp")
        with urlopen(req) as resp, open(tmp_path, "wb") as f:
            f.write(resp.read())
        tmp_path.rename(csv_path)
        logger.info(f"  {filename} ready in {dest}")
