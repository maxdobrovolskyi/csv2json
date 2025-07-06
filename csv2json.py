import argparse


def args_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", type=str, help="csv file", required=True)
    parser.add_argument("--output", type=str, help="json file", required=True)
    parser.add_argument("--map", type=str, help="yaml file", required=True)
    parser.add_argument("--where", type=str, help="condition")

    return parser.parse_args()


def something(input, output, map, where):
    print(input, output, map, where)


if __name__ == "__main__":
    args = args_parser()

    something(args.input, args.output, args.map, args.where)
