import argparse

from .lox import Lox


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("file", default=None)

    args = parser.parse_args()

    lox = Lox()
    if args.file:
        lox.run_file(args.file)
    else:
        lox.run_prompt()


if __name__ == "__main__":
    main()
