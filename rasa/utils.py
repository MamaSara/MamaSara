import json

def word_to_digits(number_word, number_words={}):
    if not number_words:
        units = [
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen",
        ]

        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
        scales = ["hundred", "thousand", "million", "billion", "trillion"]

        number_words["and"] = (1, 0)
        for idx, word in enumerate(units):
            number_words[word] = (1, idx)
        for idx, word in enumerate(tens):
            number_words[word] = (1, idx * 10)
        for idx, word in enumerate(scales):
            number_words[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in number_word.split():
        if word not in number_words:
            raise Exception("Illegal word: " + word)

        scale, increment = number_words[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current

def read_responses():
    with open("responses/responses.json", 'r') as f:
        responses = json.load(f)
    return responses