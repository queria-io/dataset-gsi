"""国土地理院 全国都道府県市区町村別面積調のダウンロード。

面積調の CSV（Shift_JIS）は時点ごとに「面積」「備考」の2列が横に並ぶ。
ファイルは期間で3つに分かれていて、時点の列の並びがそれぞれ違うので、
ここで縦持ち（1行 = 1地域 × 1時点）の UTF-8 CSV にまとめてから dbt に渡す。

データソース: 全国都道府県市区町村別面積調
https://www.gsi.go.jp/KOKUJYOHO/OLD-MENCHO-title.htm#csv
"""

import csv
import io
import logging
import re
import ssl
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen

logger = logging.getLogger("pipelines")

BASE_URL = "https://www.gsi.go.jp/KOKUJYOHO/MENCHO/backnumber"

FILES = [
    # 令和6年1月1日時点以降（四半期ごと）
    "R8_04_mencho.csv",
    # 令和元年7月1日時点〜令和5年10月1日時点（四半期ごと）
    "R1_R5_mencho.csv",
    # 平成26年〜平成30年（年1回・10月1日時点）
    "H26_H30_mencho.csv",
]

OUTPUT = "municipality_area.csv"

# www.gsi.go.jp は安全な再ネゴシエーション（RFC 5746）に対応しておらず、OpenSSL 3 の既定では
# 接続を拒否される。証明書の検証は既定のまま残し、この取得に限って旧方式の接続を許す
SSL_CONTEXT = ssl.create_default_context()
SSL_CONTEXT.options |= ssl.OP_LEGACY_SERVER_CONNECT

HEADER_ROW = 4

ERA_START = {"平成": 1988, "令和": 2018}

# 時点の見出し。例: 令和8年4月1日(k㎡) / 令和元年10月1日面積(k㎡) / 令和元年7月面積(k㎡) / 平成30年面積(k㎡)
LABEL_RE = re.compile(r"^(平成|令和)(元|\d+)年(?:(\d+)月(?:(\d+)日)?)?(?:面積)?\(k㎡\)$")


def parse_survey_date(label: str) -> date:
    """見出しから時点の日付を返す。月日が無い見出しは年1回実施の10月1日時点、日が無いものは1日。"""
    m = LABEL_RE.match(label)
    if not m:
        raise ValueError(f"unexpected column label: {label!r}")
    era, year, month, day = m.groups()
    y = ERA_START[era] + (1 if year == "元" else int(year))
    if month is None:
        return date(y, 10, 1)
    return date(y, int(month), int(day or 1))


def melt(text: str, source_file: str) -> list[list[str]]:
    rows = list(csv.reader(io.StringIO(text)))
    header = rows[HEADER_ROW]
    out = []
    for row in rows[HEADER_ROW + 1 :]:
        if not any(row):
            continue
        code, prefecture, county, municipality = row[:4]
        for i in range(4, len(header), 2):
            label = header[i]
            out.append(
                [
                    source_file,
                    re.sub(r"(?:面積)?\(k㎡\)$", "", label),
                    parse_survey_date(label).isoformat(),
                    code,
                    prefecture,
                    county,
                    municipality,
                    row[i],
                    row[i + 1] if i + 1 < len(row) else "",
                ]
            )
    return out


def download_area_data(dest_dir: str) -> None:
    """面積調 CSV 3ファイルを取得し、縦持ちの municipality_area.csv を作る。

    既に作成済みの場合はスキップする。
    """
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    out_path = dest / OUTPUT
    if out_path.exists():
        logger.info(f"  skip (already exists: {out_path})")
        return

    rows = []
    for filename in FILES:
        logger.info(f"  downloading {filename}...")
        req = Request(f"{BASE_URL}/{filename}", headers={"User-Agent": "dataset-gsi"})
        with urlopen(req, context=SSL_CONTEXT) as resp:
            text = resp.read().decode("cp932")
        rows.extend(melt(text, filename))

    tmp_path = out_path.with_suffix(".tmp")
    with open(tmp_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "source_file",
                "survey_label",
                "survey_date",
                "area_code",
                "prefecture",
                "county",
                "municipality",
                "area_km2",
                "remark",
            ]
        )
        writer.writerows(rows)
    tmp_path.rename(out_path)
    logger.info(f"  {OUTPUT} ready in {dest} ({len(rows)} rows)")
