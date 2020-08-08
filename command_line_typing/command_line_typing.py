import argparse
import sys
import time
from random import choice

from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple

if sys.version_info >= (3, 7):
    from importlib.resources import read_text
else:
    from importlib_resources import read_text

FILE_NAME = "phrases.txt"


def load_practice_phrases() -> Tuple[List[str], List[str], List[str]]:
    """ Loads phrases from file and returns 3 lists (short, medium, long)"""
    short = []
    medium = []
    long = []
    size = ""
    data = read_text("command_line_typing", FILE_NAME)

    for line in data.splitlines():
        if line == "[SHORT]":
            size = "short"
        elif line == "[MEDIUM]":
            size = "medium"
        elif line == "[LONG]":
            size = "long"
        elif size == "short":
            short.append(line)
        elif size == "medium":
            medium.append(line)
        elif size == "long":
            long.append(line)

    return short, medium, long


def check_for_mistakes(practice_phrase: str, typed_phrase: str) -> int:
    # todo make this better
    practice_len = len(practice_phrase)
    typed_len = len(typed_phrase)
    error_count = 0
    for p, t in zip(practice_phrase, typed_phrase):
        if p != t:
            error_count += 1
    error_count += abs(practice_len - typed_len)
    return error_count


def practice(practice_phrase: str, show_wps: bool) -> bool:
    print()
    print(practice_phrase)
    print()
    start_time = time.time()
    data = input()
    elapse_time = time.time() - start_time
    if data.lower() in ["quit", "exit"]:
        return False
    error_count = check_for_mistakes(practice_phrase, data)

    # calculate wpm
    adjusted_len = len(data) / 5
    gross_wpm = adjusted_len / (elapse_time / 60.0)
    gross_wps = adjusted_len / elapse_time
    net_wpm = (adjusted_len - error_count) / (elapse_time / 60.0)
    net_wps = (adjusted_len - error_count) / elapse_time

    print()
    print("STATS:")
    print(f"Gross WPM: {gross_wpm:.1f}")
    print(f"Errors: {error_count}")
    print(f"Net WPM: {net_wpm:.1f}")
    print(f"Time: {elapse_time:.1f} seconds")
    if show_wps:
        print(f"Gross WPS: {gross_wps:.1f}")
        print(f"Net WPS: {net_wps:.1f}")

    return True


def argument_parsing(args: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", dest="size", type=str,
                        choices=["short", "medium", "long"],
                        help="Size of the practice typing phrase.")
    parser.add_argument("-c", dest="continues", action="store_true",
                        help="Continues practice until exit or quit is entered.")
    parser.add_argument("-p", dest="pause", action="store_true",
                        help="Pause before starting practice.")
    parser.add_argument("--wps", dest="show_wps", action="store_true",
                        help="Show words per second.")
    return parser.parse_args(args)


def main(args: Optional[Sequence[str]] = None) -> int:
    argv = argument_parsing(args)
    short_phrases, medium_phrases, long_phrases = load_practice_phrases()
    if argv.size == "short":
        phrase = short_phrases
    elif argv.size == "medium":
        phrase = medium_phrases
    elif argv.size == "long":
        phrase = long_phrases
    else:
        phrase = short_phrases + medium_phrases + long_phrases

    while True:
        if argv.pause:
            input("Press enter to start: ")
        practice(choice(phrase), argv.show_wps)
        if argv.continues:
            user_input = input("Another practice random practice phrase? ").lower()
            if user_input in ["y", "yes"]:
                continue
            else:
                break
        else:
            break
    return 0


if __name__ == "__main__":
    exit(main())
