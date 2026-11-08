"""Acceptance tests for the Credit exercise.

Each test runs your program as a whole, exactly as a user would: it types
some answers to the "Number: " question, then checks what your program
prints and tries to explain what is wrong.

Run the tests from the exercise folder with:

    python test_credit.py
"""

import os
import subprocess
import sys
from pathlib import Path

EXERCISE_DIR = Path(__file__).resolve().parent
SCRIPT = "credit.py"
PROMPT = "Number: "
TIMEOUT = 5  # seconds
CARD_TYPES = ["AMEX", "MASTERCARD", "VISA", "INVALID"]
AMEX_STARTS = ["34", "37"]
MASTERCARD_STARTS = ["51", "52", "53", "54", "55"]
VISA_STARTS = ["4"]

# Each test case: (what is checked, answers typed by the user).
# Convention: only the LAST answer is made of digits, all the others
# must be rejected by the program (which then asks again).
CASES = [
    ("4003600000000014 (example of the instructions)",
     ["4003600000000014"]),
    ("VISA with 13 digits", ["4222222222222"]),
    ("MASTERCARD starting with 51", ["5110201050803030"]),
    ("MASTERCARD starting with 55", ["5555555555554444"]),
    ("AMEX starting with 34", ["340706080907000"]),
    ("AMEX starting with 37", ["378282246310005"]),
    ("wrong checksum", ["347067893866178"]),
    ("wrong checksum (the digits of the products must be added)",
     ["4678698198463464"]),
    ("right checksum, starts with 4, but 15 digits", ["400360000000012"]),
    ("right checksum, starts with 34, but 16 digits", ["3407060809070003"]),
    ("right checksum, 16 digits, but starts with 56", ["5610591081018250"]),
    ("6176292929 (example of the instructions)", ["6176292929"]),
    ("hyphens and a word are rejected",
     ["4003-6000-0000-0014", "foo", "4003600000000014"]),
    ("an empty answer and spaces are rejected",
     ["", "5555 5555 5555 4444", "5555555555554444"]),
]


# ---------------------------------------------------------------------------
# Running the student's program
# ---------------------------------------------------------------------------

def run_program(answers):
    """Run the program, typing the answers one per line.

    Return (stdout, stderr, return code), or None if the program
    did not stop in time.
    """
    try:
        # sys.executable is the Python running the tests,
        # so "python" vs "python3" does not matter.
        result = subprocess.run(
            [sys.executable, SCRIPT],
            input="\n".join(answers) + "\n",
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=EXERCISE_DIR,
            env=dict(os.environ, PYTHONIOENCODING="utf-8"),
            timeout=TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return None
    stdout = result.stdout.replace("\r\n", "\n")
    return stdout, result.stderr.strip(), result.returncode


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def show(lines):
    """Indent lines and make spaces visible (shown as '·')."""
    if not lines:
        return "    (nothing)"
    return "\n".join("    " + line.replace(" ", "·") for line in lines)


def last_lines(text, nb_lines=4):
    """Return the last lines of a text, indented."""
    lines = text.split("\n")[-nb_lines:]
    return "\n".join("    " + line for line in lines)


# ---------------------------------------------------------------------------
# Expected answer (and the answers given by some classic mistakes)
# ---------------------------------------------------------------------------

def luhn_total(number, mistake=None):
    """Return the total computed by Luhn's algorithm.

    With a mistake, return the total computed by a wrong version
    of the algorithm instead.
    """
    total = 0
    for position, digit in enumerate(reversed(number)):
        # position 0 is the last digit, position 1 the second-to-last...
        # (going from the left gives the same mistake when the number
        # of digits is odd, and the right answer when it is even)
        if mistake == "wrong_digits_doubled":
            is_doubled = position % 2 == 0
        else:
            is_doubled = position % 2 == 1
        if not is_doubled:
            total += int(digit)
        elif mistake == "add_products":
            total += int(digit) * 2
        else:
            product = int(digit) * 2
            total += product // 10 + product % 10
    return total


def starts_with_one_of(number, starts):
    """Return True if number starts with one of the strings in starts."""
    for start in starts:
        if number.startswith(start):
            return True
    return False


def card_type(number, mistake=None):
    """Return AMEX, MASTERCARD, VISA or INVALID.

    With a mistake, return the answer of a program making that mistake.
    """
    amex_starts = AMEX_STARTS
    mastercard_starts = MASTERCARD_STARTS
    if mistake == "first_digit_only":
        amex_starts = ["3"]
        mastercard_starts = ["5"]
    elif mistake == "55_excluded":
        mastercard_starts = MASTERCARD_STARTS[:-1]
    any_length = mistake == "no_length"
    length = len(number)

    if mistake != "no_checksum" and luhn_total(number, mistake) % 10 != 0:
        return "INVALID"
    if (any_length or length == 15) and starts_with_one_of(number,
                                                           amex_starts):
        return "AMEX"
    if (any_length or length == 16) and starts_with_one_of(number,
                                                           mastercard_starts):
        return "MASTERCARD"
    if (any_length or length in (13, 16)) and starts_with_one_of(number,
                                                                 VISA_STARTS):
        return "VISA"
    return "INVALID"


MISTAKES = {
    "add_products": "you add the products (e.g. 12) instead of their "
                    "digits (1 + 2 = 3)",
    "wrong_digits_doubled": "you double the wrong digits: start with the "
                            "second-to-last digit and go from RIGHT to left "
                            "(going from the left only works when the "
                            "number of digits is even)",
    "no_checksum": "you never check the checksum (Luhn's algorithm)",
    "no_length": "you never check the length (AMEX: 15 digits, "
                 "MASTERCARD: 16, VISA: 13 or 16)",
    "first_digit_only": "you only check the first digit, but AMEX and "
                        "MASTERCARD are recognized by their first TWO digits",
    "55_excluded": "55 is forgotten: MASTERCARD numbers start with "
                   "51 to 55 (55 included)",
}


def describe(number):
    """Return e.g. '16 digits, starts with 40, Luhn total = 20 (valid)'."""
    total = luhn_total(number)
    validity = "valid" if total % 10 == 0 else "invalid"
    return (f"{len(number)} digits, starts with {number[:2]}, "
            f"Luhn total = {total} ({validity} checksum)")


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def count_prompts(stdout):
    """Count the "Number: " questions at the start of the output.

    Return (number of questions, rest of the output).
    """
    nb_prompts = 0
    while stdout.startswith(PROMPT):
        stdout = stdout[len(PROMPT):]
        nb_prompts += 1
    return nb_prompts, stdout


def check_questions(stdout, stderr, return_code, answers):
    """Check that the program asks the question the right number of times.

    Return (error message or None, rest of the output after the questions).
    """
    nb_prompts, rest = count_prompts(stdout)
    printed = "Your program printed:\n" + show(stdout.splitlines())

    if stdout.startswith((PROMPT + "\n", PROMPT.strip() + "\n")):
        return (f"The answer must be typed on the same line as the question: "
                f"use input({PROMPT!r}) instead of print().\n{printed}"), rest
    if nb_prompts == 0:
        if stdout.startswith(PROMPT.strip()):
            message = (f"The question must be exactly {PROMPT!r}, "
                       f"with a space after the colon.")
        else:
            message = f"Your program should start by asking {PROMPT!r}."
        return f"{message}\n{printed}", rest

    if "EOFError" in stderr:
        expected = card_type(answers[-1])
        message = (f"Your program asked again after {answers[-1]!r}, "
                   f"but this answer is made of digits: your program should "
                   f"print {expected}.")
        if expected == "INVALID":
            message += (" Ask again only if the answer contains something "
                        "else than digits, not when the card is invalid.")
        return message, rest
    if return_code != 0:
        answer = answers[min(nb_prompts, len(answers)) - 1]
        message = (f"Your program crashed after reading {answer!r}:\n"
                   f"{last_lines(stderr)}")
        if "ValueError" in stderr:
            message += ("\nint() fails when the text is not a whole number: "
                        "check the text first (e.g. with str.isdigit()) "
                        "before converting it.")
        elif "IndexError" in stderr:
            message += ("\nAn index is out of range: the first digit is at "
                        "index 0 and the last one at index len(...) - 1.")
        return message, rest

    if PROMPT in rest:
        extra = rest[:rest.index(PROMPT)]
        return (f"Your program printed {extra!r} before asking again. "
                f"When an answer is invalid, it should only ask again.\n"
                f"{printed}"), rest
    if nb_prompts < len(answers):
        accepted = answers[nb_prompts - 1]
        return (f"Your program accepted {accepted!r} as a card number, but "
                f"it should ask again: a card number must contain only "
                f"digits (no spaces, no hyphens, not empty).\n"
                f"{printed}"), rest
    return None, rest


def explain_wrong_type(given, number):
    """Explain why the card type printed is wrong."""
    expected = card_type(number)
    message = (f"Your program printed {given}, but it should print "
               f"{expected}.\nDetails: {describe(number)}.")
    # Which classic mistake gives the answer printed?
    candidates = []
    for mistake, explanation in MISTAKES.items():
        if card_type(number, mistake) == given:
            candidates.append(explanation)
    if len(candidates) == 1:
        message += f"\nIt looks like {candidates[0]}."
    elif len(candidates) == 2:
        message += (f"\nIt looks like {candidates[0]};"
                    f"\nor that {candidates[1]}.")
    else:
        message += ("\nCheck the three conditions one by one: length, "
                    "first digits and checksum.")
    return message


def check_answer(rest, number):
    """Check what is printed after the questions. Return a message or None."""
    expected = card_type(number)
    lines = rest.splitlines()
    printed = "Your program printed after the questions:\n" + show(lines)

    if not lines:
        return (f"Your program printed nothing after reading {number}: "
                f"it should print {expected}.")
    if len(lines) > 1:
        message = ("Your program should print only the type of card "
                   "(or INVALID), on a single line.")
        if expected in lines:
            message += (f" The right answer ({expected}) is there: remove "
                        f"the other print() (for instance prints used to "
                        f"debug).")
        return f"{message}\n{printed}"

    line = lines[0]
    if line != line.strip():
        return (f"Nothing should be printed before or after {expected} "
                f"(not even spaces).\n{printed}")
    normalized = line.upper().replace(" ", "")
    if line not in CARD_TYPES and normalized in CARD_TYPES:
        return (f"Your program printed {line!r}: write it exactly as "
                f"{normalized!r} (in capital letters, without spaces).")
    if line in CARD_TYPES:
        return explain_wrong_type(line, number)
    if expected in line.upper().split():
        return (f"Your program should print only {expected}, without any "
                f"other text.\n{printed}")
    return (f"Your program should print one of {', '.join(CARD_TYPES)} "
            f"(here {expected}).\n{printed}")


def check_case(answers):
    """Run one test case. Return None if it passes, else an error message."""
    result = run_program(answers)
    if result is None:
        return ("Your program did not stop (infinite loop?). Check that "
                "input() is called inside your loop, and that each of your "
                "loops always ends.")
    stdout, stderr, return_code = result

    message, rest = check_questions(stdout, stderr, return_code, answers)
    if message is not None:
        return message
    number = answers[-1]
    if rest == card_type(number) + "\n":
        return None
    return check_answer(rest, number)


# ---------------------------------------------------------------------------
# Main program
# ---------------------------------------------------------------------------

def main():
    sys.stdout.reconfigure(errors="replace")
    use_colors = sys.stdout.isatty() and (
        os.name != "nt" or "WT_SESSION" in os.environ)
    green = "\033[32m" if use_colors else ""
    red = "\033[31m" if use_colors else ""
    reset = "\033[0m" if use_colors else ""

    if not (EXERCISE_DIR / SCRIPT).is_file():
        print(f"No {SCRIPT} found in {EXERCISE_DIR}")
        return 1

    nb_ok = 0
    for description, answers in CASES:
        typed = ", ".join(repr(answer) for answer in answers)
        message = check_case(answers)
        if message is None:
            nb_ok += 1
            print(f"{green}✔{reset} {description}")
        else:
            print(f"{red}✗{reset} {description}")
            print(f"    Answers typed: {typed}")
            print("    " + message.replace("\n", "\n    ") + "\n")

    color = green if nb_ok == len(CASES) else red
    print(f"Validated: {color}{nb_ok}/{len(CASES)}{reset}")
    return 0 if nb_ok == len(CASES) else 1


if __name__ == "__main__":
    sys.exit(main())
