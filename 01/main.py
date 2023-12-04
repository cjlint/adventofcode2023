import marisa_trie

number_words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
reversed_number_words = [word[::-1] for word in number_words]
numbers = [(i,) for i in range(1, 10)]

number_trie = marisa_trie.RecordTrie("h", zip(number_words, numbers))
reversed_number_trie = marisa_trie.RecordTrie("h", zip(reversed_number_words, numbers))


def parse_calibration_simple_part1(line: str) -> int:
    first_num = next(c for c in line if c.isdigit())
    last_num = next(c for c in reversed(line) if c.isdigit())
    return int(first_num + last_num)


def parse_single_calibration(line: str) -> str:
    return parse_single_calibration_with_trie(line, number_trie)


def parse_single_calibration_reversed(line: str) -> str:
    return parse_single_calibration_with_trie(line[::-1], reversed_number_trie)


def chop_front(s: str):
    chopped = s[1:]
    while chopped:
        yield chopped
        chopped = chopped[1:]
    yield ""


def parse_single_calibration_with_trie(line: str, trie: marisa_trie.RecordTrie) -> str:
    current_word = ""
    for c in line:
        if c.isdigit():
            return c
        word = current_word + c
        if word in trie:
            return str(trie[word][0][0])
        if trie.keys(word):
            current_word = word
        else:
            current_word = next(
                substr for substr in chop_front(word) if trie.keys(substr)
            )
    raise Exception(f"no number found on line {line}")


def parse_and_combine(line: str) -> int:
    result = int(
        parse_single_calibration(line) + parse_single_calibration_reversed(line)
    )
    print(f"{line.strip()} ---- {result}")
    return result


def main():
    with open("input", "r") as f:
        lines = f.readlines()

    result = sum(parse_calibration_simple_part1(line) for line in lines)
    print(result)


def main2():
    with open("input", "r") as f:
        lines = f.readlines()

    result = sum(parse_and_combine(line) for line in lines)
    print(result)


if __name__ == "__main__":
    # main()
    main2()

    tests = [
        ("6798seven", "6", "7", 67),
        ("six8b32csscsdgjsevenfivedlhzhc", "6", "5", 65),
        ("fourvzgnfnhkkp2", "4", "2", 42),
        ("fourvzgnfnhkkp", "4", "4", 44),
        ("oneight", "1", "8", 18),
        ("feightwo4twofivefour", "8", "4", 84),
        ("fone", "1", "1", 11),
    ]

    for testcase, expected_normal, expected_reverse, expected_combination in tests:
        print(testcase)
        assert parse_single_calibration(testcase) == expected_normal
        assert parse_single_calibration_reversed(testcase) == expected_reverse
        assert parse_and_combine(testcase) == expected_combination
