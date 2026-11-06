# 運用メモ

## ビルド

```bash
uv sync
bash scripts/build.sh
```

パイプラインは避難場所の全国統合 CSV（UTF-8 BOM 付き）と面積調の CSV（Shift_JIS、時点が横に並ぶ）を `data/` にダウンロードし（既存ファイルはスキップ）、dbt で raw → stg → mart の3層を構築する。面積調は取得時に縦持ちの `data/municipality_area.csv` にまとめる。自然災害伝承碑はダウンロードページから最新の ZIP を探し、中の CSV を `data/disaster_lore.csv` に置く。
