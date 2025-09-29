import argparse
import sys

from json_redactor.utils import hash_redactor, mask_redactor, key_matcher, redact_json, regex_key_matcher

def not_none(value):
    return not value == None


def main():
    parser = argparse.ArgumentParser(prog="json-redactor")
    parser.add_argument("--file", nargs="?", help="A path to a file that contains json to be redacted")
    parser.add_argument("--keys", nargs="?", help="A comma-separated list of keys to redact")
    parser.add_argument("--key-file", nargs="?", help="A path to a file that contains a comma-separated list of keys to redact")
    parser.add_argument("--keys-regex", nargs="?", help="Keys that match this regular expression will be redacted")
    parser.add_argument("--mask", action="store_true", help="replace each sensitive value with '***REDACTED***'")
    parser.add_argument("--hash", action="store_true", help="replace each sensitive value with a deterministic SHA-256 hash of the original value")
    args = parser.parse_args()

    if args.mask and args.hash:
        parser.error("--mask and --hash cannot be used together.")

    if sum([not_none(args.keys), not_none(args.key_file), not_none(args.keys_regex)]) > 1:
        parser.error("--keys, --key_file and --keys-regex cannot be used together.")

    if args.key_file:
        with open(args.key_file, "r") as key_file:
            possible_keys = key_file.readline()
            if possible_keys:
                keys = key_matcher(possible_keys.split(","))
    elif args.keys:
        keys = key_matcher(args.keys.split(","))
    elif args.keys_regex:
        keys = regex_key_matcher(args.keys_regex)
    else:
        parser.error("One of --keys, --key-file or --keys-regex is required")

    if args.mask:
        redactor = mask_redactor
    elif args.hash:
        redactor = hash_redactor
    else:
        parser.error("One of --mask or --hash is required")

    if not sys.stdin.isatty():
        redact_json(sys.stdin.buffer, keys, redactor)
    elif args.file:
        with open(args.file, "rb") as file:
            redact_json(file, keys, redactor)
    else:
        parser.error("No file set or piped in.")


if __name__ == "__main__":
    main()
