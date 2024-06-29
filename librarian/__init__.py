import check50
import re


@check50.check()
def exists():
    """log.R and answers.txt exist"""
    check50.exists("log.R")
    check50.exists("answers.txt")


@check50.check(exists)
def formatting():
    """answers.txt is correctly formatted"""
    with open("answers.txt", "r") as f:
        contents = f.readlines()

    for character in [
        "The Writer",
        "The Musician",
        "The Traveler",
        "The Painter",
        "The Scientist",
        "The Teacher",
    ]:
        found = False
        for line in contents:
            if character in line:
                found = True
                break

        if not found:
            raise check50.Failure(f"Could not find {character} in answers.txt")


@check50.check(formatting)
def log_length():
    """log.R is of sufficient length"""
    with open("log.R", "r") as f:
        contents = f.read()
    
    if len(contents) < 300:
        raise check50.Failure("log.R is not at least 300 characters long")


@check50.check(log_length)
def the_writer():
    """answers.txt finds The Writer's book"""
    check_character(
        "The Writer", "6372656174696e67206d656d6f7261626c652063686172616374657273"
    )


@check50.check(log_length)
def the_musician():
    """answers.txt finds The Musician's book"""
    check_character(
        "The Musician",
        "7468652065766f6c7574696f6e206f6620656c656374726f6e696320696e737472756d656e7473",
    )


@check50.check(log_length)
def the_traveler():
    """answers.txt finds The Traveler's book"""
    check_character("The Traveler", "666f7262696464656e206d61676963")


@check50.check(log_length)
def the_painter():
    """answers.txt finds The Painter's book"""
    check_character("The Painter", "617274697374727920696e20616e6369656e742074696d6573")


@check50.check(log_length)
def the_scientist():
    """answers.txt finds The Scientist's book"""
    check_character(
        "The Scientist",
        "7175616e74756d206d656368616e69637320666f7220626567696e6e657273",
    )


@check50.check(log_length)
def the_teacher():
    """answers.txt finds The Teacher's book"""
    check_character("The Teacher", "7468652074696d656c696e65206f6620656475636174696f6e")


def check_character(character: str, hashed_book: str) -> None:
    with open("answers.txt", "r") as f:
        contents = f.readlines()

    if not check_answers(
        contents,
        character=character,
        hashed_book=hashed_book,
    ):
        raise check50.Failure(f"answers.txt does not correctly find {character}'s book")


def check_answers(contents: list[str], character: str, hashed_book: str) -> bool:
    expected_book = bytes.fromhex(hashed_book).decode("utf-8")
    for line in contents:
        if match := re.search(rf"{re.escape(character)}[^:]*:(?P<book>.*)", line):
            book = squish(match.group("book").strip().lower())
            if book == expected_book:
                return True
    return False


def squish(text: str) -> str:
    return " ".join(text.split())
