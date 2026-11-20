"""国土地理院 データパイプライン。

1. evacuation: 指定緊急避難場所・指定避難所の全国統合 CSV 取得
2. area:       全国都道府県市区町村別面積調の CSV 取得
3. disaster_lore: 自然災害伝承碑の全国 CSV 取得
4. mountain:   日本の主な山岳標高の CSV 取得
5. dbt:        dbt ビルド
"""

import logging

from dbt.cli.main import dbtRunner

from pipelines.area import download_area_data
from pipelines.disaster_lore import download_disaster_lore_data
from pipelines.evacuation import download_evacuation_data
from pipelines.mountain import download_mountain_data

logger = logging.getLogger("pipelines")


def dbt_build():
    dbt = dbtRunner()

    result = dbt.invoke(["deps"])
    if not result.success:
        raise SystemExit("dbt deps failed")

    result = dbt.invoke(["build"])
    if not result.success:
        raise SystemExit("dbt build failed")

    result = dbt.invoke(["docs", "generate"])
    if not result.success:
        raise SystemExit("dbt docs generate failed")


def main():
    # 1. 指定緊急避難場所・指定避難所 CSV
    logger.info("1/5: evacuation (指定緊急避難場所・指定避難所)")
    download_evacuation_data("data")

    # 2. 全国都道府県市区町村別面積調 CSV
    logger.info("2/5: area (全国都道府県市区町村別面積調)")
    download_area_data("data")

    # 3. 自然災害伝承碑 CSV
    logger.info("3/5: disaster_lore (自然災害伝承碑)")
    download_disaster_lore_data("data")

    # 4. 日本の主な山岳標高 CSV
    logger.info("4/5: mountain (日本の主な山岳標高)")
    download_mountain_data("data")

    # 5. dbt ビルド
    logger.info("5/5: dbt build")
    dbt_build()


if __name__ == "__main__":
    main()
