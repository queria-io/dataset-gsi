"""国土地理院 日本の主な山岳標高のダウンロード。

CSV（Shift_JIS）が版ごとに日付の入ったファイル名で配布されている。
ダウンロードページのリンクから URL を取り、UTF-8 にして置く。

データソース: 日本の主な山岳標高
https://www.gsi.go.jp/kihonjohochousa/kihonjohochousa41139.html
"""

import csv
import io
import logging
import re
from pathlib import Path
from urllib.parse import urljoin

from pipelines.disaster_lore import fetch
from shared.fetch import write_atomic

logger = logging.getLogger("pipelines")

PAGE_URL = "https://www.gsi.go.jp/kihonjohochousa/kihonjohochousa41139.html"

OUTPUT = "mountain.csv"

LINK_RE = re.compile(r'<a href="([^"]+\.csv)"[^>]*>\s*(?:<span[^>]*>)?\s*日本の主な山岳標高一覧')


def download_mountain_data(dest_dir: str) -> None:
    """日本の主な山岳標高の CSV を取得して mountain.csv（UTF-8）に置く。

    既に作成済みの場合はスキップする。
    """
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    out_path = dest / OUTPUT
    if out_path.exists():
        logger.info(f"  skip (already exists: {out_path})")
        return

    page = fetch(PAGE_URL).decode("utf-8")
    m = LINK_RE.search(page)
    if not m:
        raise RuntimeError(f"CSV へのリンクが見つからない: {PAGE_URL}")
    csv_url = urljoin(PAGE_URL, m.group(1))

    logger.info(f"  downloading {csv_url}...")
    text = fetch(csv_url).decode("cp932")
    rows = list(csv.reader(io.StringIO(text)))
    if len(rows) < 2:
        raise RuntimeError(f"CSV に行が無い: {csv_url}")
    write_atomic(out_path, text)
    logger.info(f"  {OUTPUT} ready in {dest} ({len(rows) - 1} rows)")
