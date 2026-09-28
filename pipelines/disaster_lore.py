"""国土地理院 自然災害伝承碑データのダウンロード。

全国分を1ファイルにまとめた CSV（UTF-8 BOM 付き）が ZIP で配布されている。
ZIP のファイル名は版ごとに変わるので、ダウンロードページのリンクから URL を取る。

データソース: 自然災害伝承碑
https://www.gsi.go.jp/bousaichiri/denshouhi_datainfo.html
"""

import io
import logging
import re
import ssl
import zipfile
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen

logger = logging.getLogger("pipelines")

PAGE_URL = "https://www.gsi.go.jp/bousaichiri/denshouhi_download.html"

OUTPUT = "disaster_lore.csv"

# www.gsi.go.jp は安全な再ネゴシエーション（RFC 5746）に対応しておらず、OpenSSL 3 の既定では
# 接続を拒否される。証明書の検証は既定のまま残し、この取得に限って旧方式の接続を許す
SSL_CONTEXT = ssl.create_default_context()
SSL_CONTEXT.options |= ssl.OP_LEGACY_SERVER_CONNECT

LINK_RE = re.compile(r'<a href="([^"]+\.zip)">\s*自然災害伝承碑データ（CSV形式）')


def fetch(url: str) -> bytes:
    req = Request(url, headers={"User-Agent": "dataset-gsi"})
    with urlopen(req, context=SSL_CONTEXT) as resp:
        return resp.read()


def download_disaster_lore_data(dest_dir: str) -> None:
    """自然災害伝承碑の全国 CSV を取得して disaster_lore.csv に置く。

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
        raise RuntimeError(f"CSV の ZIP へのリンクが見つからない: {PAGE_URL}")
    zip_url = urljoin(PAGE_URL, m.group(1))

    logger.info(f"  downloading {zip_url}...")
    with zipfile.ZipFile(io.BytesIO(fetch(zip_url))) as zf:
        csv_names = [n for n in zf.namelist() if n.endswith(".csv")]
        if len(csv_names) != 1:
            raise RuntimeError(f"ZIP 内の CSV が1つではない: {csv_names}")
        data = zf.read(csv_names[0])

    tmp_path = out_path.with_suffix(".tmp")
    tmp_path.write_bytes(data)
    tmp_path.rename(out_path)
    logger.info(f"  {OUTPUT} ready in {dest} ({csv_names[0]})")
