import argparse
import sys
import time
from random import choice
from random import randint

from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple

if sys.version_info >= (3, 7):
    from importlib.resources import read_text
else:
    from importlib_resources import read_text

LOWER_LETTERS = [x for x in "abcdefghijklmnopqrstuvwxyz"]
UPPER_LETTERS = [x for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
DIGITS = [str(x) for x in range(10)]
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


def build_random_letter_phrase(size: str) -> str:
    random_phrase = ""
    if size == "short":
        count = 50
    elif size == "medium":
        count = 75
    elif size == "long":
        count = 100
    else:
        count = 50

    group_count = 0
    max_group_count = randint(1, 7)
    for x in range(count):
        if group_count == max_group_count:
            random_phrase += " "
            max_group_count = randint(1, 7)
            group_count = 0
        else:
            if group_count == 0 and choice([True, False]):
                random_phrase += choice(UPPER_LETTERS)
            else:
                random_phrase += choice(LOWER_LETTERS)
            group_count += 1
    return random_phrase


def build_nine_key_phrase(size: str) -> str:
    nine_key_phrase = ""
    if size == "short":
        count = 42
    elif size == "medium":
        count = 65
    elif size == "long":
        count = 90
    else:
        count = 50
    for x in range(count):
        nine_key_phrase += choice(DIGITS)
    return nine_key_phrase


def check_for_mistakes(practice_phrase: str, typed_phrase: str) -> int:
    # todo need more work
    if typed_phrase == practice_phrase:
        return 0
    practice_len = len(practice_phrase)
    typed_len = len(typed_phrase)
    error_count = 0
    for p, t in zip(practice_phrase, typed_phrase):
        if p != t:
            error_count += 1
    if typed_len < practice_len:
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
    parser.add_argument("--random_letters", action="store_true",
                        help="Random upper and lower letters and spaces")
    parser.add_argument("--nine_key", action="store_true",
                        help="Nine key practice with numbers")
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
        if argv.random_letters:
            practice_phrase = build_random_letter_phrase(argv.size)
        elif argv.nine_key:
            practice_phrase = build_nine_key_phrase(argv.size)
        else:
            practice_phrase = choice(phrase)
        practice(practice_phrase, argv.show_wps)
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
