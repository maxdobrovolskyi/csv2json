import argparse
from utils import load, extract, transform


def build_cli():
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", type=str, help="csv file", required=True)
    parser.add_argument("--output", type=str, help="json file", required=True)
    parser.add_argument("--map", type=str, help="yaml file")
    parser.add_argument("--where", type=str, help="condition")

    return parser.parse_args()


if __name__ == "__main__":
    args = build_cli()

    df = load(file=args.input, where=args.where)
    if args.map:
        df = transform(yaml_file=args.map, df=df)
    extract(df, file_name=args.output)
