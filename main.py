from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import DATA_PATH, LANGUAGE, GAME_URL, TIMEOUT, USERNAME, PRIVATE

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

def create_lobby() -> str:
    # Open web page
    driver = webdriver.Firefox()
    driver.implicitly_wait(TIMEOUT)
    driver.get(GAME_URL)
    
    # Set nickname
    name_button = WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='auth']")))
    name_button.click()
    name_input = WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, "//input[@class='styled nickname']")))
    name_input.clear()
    name_input.send_keys(USERNAME)
    
    # Confirm nickname
    ok_button = driver.find_element(By.XPATH, "//button[@class='styled']")
    ok_button.click()
    
    # Set privacy
    if PRIVATE:
        privacy_button = WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, "//label[@for='roomPrivacyPrivate']")))
    else:
        privacy_button = WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, "//label[@for='roomPrivacyPublic']")))
    privacy_button.click()
    
    # Select BombParty
    bombparty_button = WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, "//label[@for='gameRadio-bombparty']")))
    bombparty_button.click()
    
    # Create lobby
    play_button = WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-text='play']")))
    play_button.click()

def join_lobby(code: str):
    # Open web page
    url = GAME_URL + code
    driver = webdriver.Firefox()
    driver.implicitly_wait(TIMEOUT)
    driver.get(url)
    
    # Choose nickname
    name_input = WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, "//input[@class='styled nickname']")))
    name_input.clear()
    name_input.send_keys(USERNAME)
    
    # Confirm nickname
    ok_button = driver.find_element(By.XPATH, "//button[@class='styled']")
    ok_button.click()
    
create_lobby()
