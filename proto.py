import argparse
import sys
from protolib import errors
from pathlib import Path
from protolib.creator import Creator


def create_argument_parser():
    parser = argparse.ArgumentParser(
        description="A library for serializing and deserializing protobuf"
                    "protocol by Google")

    parser.add_argument(
        "input_file",
        type=argparse.FileType(),
        help="Input file in extension .proto for representing in .py code"
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        help="The output file where the result of the work will be recorded"
    )
    return parser.parse_args(sys.argv[1:])


def main():
    parser = create_argument_parser()

    # Checking that the uploaded file is correct
    input_filename = parser.input_file.name
    extension = Path(input_filename).suffix
    # Todo logging inputfile
    match extension:
        case '.proto':
            # Todo logging deserialize
            creator = Creator(input_filename, parser.output)
            creator.proto2python()
        case _:
            raise errors.BadExtension


if __name__ == "__main__":
    main()
