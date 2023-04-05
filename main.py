from config import DATA_PATH, LANGUAGE

ALPHABET = "abcdefghijlmnopqrstuv"
remaining_letters = set(ALPHABET)

with open(DATA_PATH / f"{LANGUAGE}_words.txt", encoding="utf-8") as f:
    words = set(f.read().splitlines())

def get_word_score(word: str) -> int:
    score = 0
    for letter in remaining_letters:
        if letter in word:
            score += 1

    return score

def consume_letters(word: str):
    for letter in word:
        if letter in remaining_letters:
            remaining_letters.remove(letter)
            
    if len(remaining_letters) == 0:
        remaining_letters = set(ALPHABET)

def get_word(syllable: str) -> str:
    result = ""
    best_score = -1
    for w in words:
        if syllable in w:
            w_score = get_word_score(w)
            if w_score > best_score:
                result = w
                best_score = w_score
                
    words.remove(result)
    return result

print(get_word("ync"))
