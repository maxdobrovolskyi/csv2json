import sys
import argparse

from utils import load, extract, transform

import logging
from logging.handlers import RotatingFileHandler


log_handler = RotatingFileHandler("logs.log", backupCount=5, maxBytes=20000)
log_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
log_handler.setFormatter(log_formatter)

console_handler = logging.StreamHandler(sys.stdout)
console_formatter = logging.Formatter(fmt="%(levelname)s: %(message)s")
console_handler.setFormatter(console_formatter)

logger = logging.getLogger("logger")
logger.setLevel(logging.INFO)

logger.addHandler(log_handler)
logger.addHandler(console_handler)


def build_cli():
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", type=str, help="csv file", required=True)
    parser.add_argument("--output", type=str, help="json file")
    parser.add_argument("--map", type=str, help="yaml file")
    parser.add_argument("--where", type=str, help="condition")
    parser.add_argument("--pretty", action="store_true", help="condition")
    parser.add_argument("--date_cols", type=str, help="condition")

    return parser.parse_args()


def main():
    logger.info("app started")
    args = build_cli()
    try:
        df = load(file=args.input, where=args.where, dates=args.date_cols)
        if args.date_cols and args.date_cols in df.columns:
            df[args.date_cols] = df[args.date_cols].dt.strftime("%Y-%m-%d")
        if args.map:
            df = transform(yaml_file=args.map, df=df)
        extract(df, file_name=args.output, pretty=args.pretty)
    except OSError as e:
        logger.error(f"Error loading file: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
