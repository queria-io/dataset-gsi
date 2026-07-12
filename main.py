"""国土地理院 指定緊急避難場所データパイプライン。

1. evacuation: 指定緊急避難場所・指定避難所の全国統合 CSV 取得
2. dbt:        dbt ビルド
"""

import logging

from dbt.cli.main import dbtRunner

from pipelines.evacuation import download_evacuation_data

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
    logger.info("1/2: evacuation (指定緊急避難場所・指定避難所)")
    download_evacuation_data("data")

    # 2. dbt ビルド
    logger.info("2/2: dbt build")
    dbt_build()


if __name__ == "__main__":
    main()
