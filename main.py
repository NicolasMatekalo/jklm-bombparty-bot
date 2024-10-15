import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import DATA_PATH, LANGUAGE, GAME_URL, TIMEOUT, USERNAME, PRIVATE, CREATE, ROOM_CODE

ALPHABET = "abcdefghijlmnopqrstuv"

def get_word_score(word: str, remaining_letters: set) -> int:
    score = 0
    for letter in remaining_letters:
        if letter in word:
            score += 1

    return score

def consume_word(word: str, remaining_words: set, remaining_letters: set):
    # Remove used word
    remaining_words.remove(word)
    
    # Remove used letters
    for letter in word:
        if letter in remaining_letters:
            remaining_letters.remove(letter)

def get_word(syllable: str, remaining_words: set, remaining_letters: set) -> str:
    result = ""
    best_score = -1
    for w in remaining_words:
        if syllable in w:
            w_score = get_word_score(w, remaining_letters)
            if w_score > best_score:
                result = w
                best_score = w_score
    
    return result

def get_clickable_element(driver, xpath):
    return WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, xpath)))

def create_lobby(driver):
    # Open web page
    driver.get(GAME_URL)
    
    # Wait for page to load
    time.sleep(2)
    
    # Set nickname
    name_button = get_clickable_element(driver, "//button[@class='auth']")
    name_button.click()
    name_input = get_clickable_element(driver, "//input[@class='styled nickname']")
    name_input.clear()
    name_input.send_keys(USERNAME)
    
    # Confirm nickname
    ok_button = get_clickable_element(driver, "//button[@data-text='ok']")
    ok_button.click()
    
    # Set privacy
    if PRIVATE:
        privacy_button = get_clickable_element(driver, "//label[@for='roomPrivacyPrivate']")
    else:
        privacy_button = get_clickable_element(driver, "//label[@for='roomPrivacyPublic']")
    privacy_button.click()
    
    # Select BombParty
    bombparty_button = get_clickable_element(driver, "//label[@for='gameRadio-bombparty']")
    bombparty_button.click()
    
    # Create lobby
    play_button = get_clickable_element(driver, "//button[@data-text='play']")
    play_button.click()

def join_lobby(driver, code: str):
    # Open web page
    url = GAME_URL + code
    driver.get(url)
    
    # Choose nickname
    name_input = get_clickable_element(driver, "//input[@class='styled nickname']")
    name_input.clear()
    name_input.send_keys(USERNAME)
    
    # Confirm nickname
    ok_button = get_clickable_element(driver, "//button[@class='styled']")
    ok_button.click()
    
        
# Load dictionnary
with open(DATA_PATH / f"{LANGUAGE}_words.txt", encoding="utf-8") as f:
    words = set(f.read().splitlines())
    
# Create driver
driver = webdriver.Firefox()
driver.implicitly_wait(TIMEOUT)

if CREATE:
    create_lobby(driver)
else:
    join_lobby(driver, ROOM_CODE)

# Switch to the correct iframe
iframe = driver.find_element(By.XPATH, "//iframe[@src='https://phoenix.jklm.fun/games/bombparty']")
driver.switch_to.frame(iframe)

# Join game
join_button = get_clickable_element(driver, "//button[@class='styled joinRound']")
join_button.click()

remaining_words = words.copy()
remaining_letters = set(ALPHABET)

while True:
    # Wait until it is the bot's turn
    try:
        text_input = get_clickable_element(driver, "//input[@type='text']")
    except TimeoutException:
        continue
    
    # Get the current syllable
    syllable = driver.find_element(By.XPATH, "//div[@class='syllable']")
    
    # Get new current word
    current_word = get_word(syllable.text.lower(), remaining_words, remaining_letters)
    
    # Input current word
    for letter in current_word:
        text_input.send_keys(letter)
        # Sleep between letters to make it more human
        time.sleep(0.1)
    text_input.send_keys(webdriver.Keys.RETURN)
    
    # Update remaining words and letters     
    consume_word(current_word, remaining_words, remaining_letters)
    
    # Reset set of letters if empty
    if len(remaining_letters) == 0:
        remaining_letters = set(ALPHABET)
        
    # Sleep a bit to not play twice for the same turn
    time.sleep(0.5)
