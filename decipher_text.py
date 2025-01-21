import random
import nltk
from collections import Counter
from nltk.util import bigrams, trigrams

# Ensure the NLTK words corpus is downloaded
nltk.download('words')
nltk.download('reuters')
nltk_words = set(nltk.corpus.words.words())

# Bigram model from NLTK
nltk_bigram_model = Counter(bigrams(nltk.corpus.reuters.words()))

# Define valid ciphertext characters
VALID_CIPHERTEXT_CHARS = "1234567890@#$zyxwvutsrqpon"

COMMON_TWO_LETTER_WORDS = {"to", "it", "is", "in", "of", "on", "by", "at", "we", "he", "me", "if", "so", "up"}

# Objective function: Calculate the bigram score based on NLTK's bigram corpus
def bigram_score(deciphered_text):
    words = deciphered_text.split()
    bigram_count = sum(1 for bigram in bigrams(words) if bigram in nltk_bigram_model)
    return bigram_count / len(words) if words else 0

# Objective function: Calculate the percentage of valid words
def nltk_score(deciphered_text):
    words = deciphered_text.split()
    valid_words = sum(1 for word in words if word.lower() in nltk_words)
    
    # Count how many common two-letter words are in the deciphered text
    two_letter_word_count = sum(1 for word in words if word.lower() in COMMON_TWO_LETTER_WORDS)
    
    # Add a bonus for each two-letter word found
    bonus = two_letter_word_count * 2  # This bonus weight can be adjusted
    
    return (valid_words / len(words)) * 100 + bonus if words else 0

def combined_score(deciphered_text, word_weight=0.3, bigram_weight=0.7):
    word_score = nltk_score(deciphered_text)
    bigram_score_value = bigram_score(deciphered_text)
    
    combined = (word_weight * word_score) + (bigram_weight * bigram_score_value)
    return combined

# Frequency analysis-based substitution key
def frequency_analysis(ciphertext):
    char_freq = Counter(char for char in ciphertext if char in VALID_CIPHERTEXT_CHARS)
    sorted_chars = [char for char, _ in char_freq.most_common()]
    english_freq = "etaoinshrdlcumwfgypbvkjxqz"
    return {sorted_chars[i]: english_freq[i] for i in range(len(sorted_chars))}

# Single-letter substitution adjustment
def adjust_for_single_letters(ciphertext, key, replace_with):
    single_letters = [word for word in ciphertext.split() if len(word) == 1]
    if single_letters:
        most_frequent = Counter(single_letters).most_common(1)[0][0]
        for k, v in key.items():
            if v == replace_with:
                key[k], key[most_frequent] = key[most_frequent], replace_with
    return key

# Improved substitution decryption
def decipher_text(ciphertext, key):
    # Include common punctuation marks in the valid characters
    VALID_EXTRA_CHARS = ",.!?;:"
    return ''.join(key.get(char, char) for char in ciphertext if char in VALID_CIPHERTEXT_CHARS or char in " \n" or char in VALID_EXTRA_CHARS)

# Simulated Annealing for local search optimization
def simulated_annealing(ciphertext, initial_key):
    max_iterations=14000
    temperature=1.0
    cooling_rate=0.99
    reverse_initial_key = {v: k for k, v in initial_key.items()}  # Reverse mapping of the initial key
    a_char = reverse_initial_key.get('a', None)
    i_char = reverse_initial_key.get('i', None)
    
    # Detect if there are single-character words in the ciphertext
    single_char_words = {word for word in ciphertext.split() if len(word) == 1}
    
    # Lock the substitutions for 'a' and 'i' if the corresponding characters are found as single-character words
    locked_chars = []
    if a_char in single_char_words and i_char in single_char_words:
        locked_chars = [a_char, i_char]
    elif a_char in single_char_words:
        locked_chars = [a_char]
    elif i_char in single_char_words:
        locked_chars = [i_char]
    else:
        locked_chars = []

    best_key = initial_key.copy()
    best_score = combined_score(decipher_text(ciphertext, best_key))
    current_key = best_key.copy()
    current_score = best_score

    for _ in range(max_iterations):
        # Generate a neighboring key by swapping two random substitutions
        neighbor_key = current_key.copy()
        # Randomly sample two characters to swap, but exclude locked characters
        swap_candidates = [key for key in neighbor_key.keys() if key not in locked_chars]

        if len(swap_candidates) < 2:
            break  # If there aren't enough characters to swap, break the loop
        char1, char2 = random.sample(swap_candidates, 2)
        neighbor_key[char1], neighbor_key[char2] = neighbor_key[char2], neighbor_key[char1]

        # Calculate the new score
        deciphering_text = decipher_text(ciphertext, neighbor_key)
        neighbor_score = combined_score(deciphering_text)

        # Check for two-letter word matches
        two_letter_word_count = sum(1 for word in deciphering_text.split() if word.lower() in COMMON_TWO_LETTER_WORDS)
        # Add a bonus for each two-letter word found in the new decryption
        two_letter_bonus = two_letter_word_count * 1  # Adjust the weight here
        
        # Adjust the score based on two-letter word matches
        neighbor_score += two_letter_bonus

        # Accept the new key with probability based on temperature
        if neighbor_score > current_score or random.random() < temperature:
            current_key = neighbor_key
            current_score = neighbor_score

        # Update the best key if the new one is better
        if current_score > best_score:
            best_key = current_key
            best_score = current_score

        # Cool down the temperature
        temperature *= cooling_rate

    return best_key, best_score

def simulated_annealing_multiple_runs(ciphertext, initial_key, num_runs):
    best_overall_key = None
    best_overall_score = float('-inf')
    best_overall_deciphered_text = ""

    for _ in range(num_runs):
        best_key, best_score = simulated_annealing(
            ciphertext, 
            initial_key
        )
        # Decipher the text using the best key from this run
        deciphered_text = decipher_text(ciphertext, best_key)

        # Update the overall best result if this run's score is better
        if best_score > best_overall_score:
            best_overall_key = best_key
            best_overall_score = best_score
            best_overall_deciphered_text = deciphered_text

    # print(f"\nBest score after {num_runs} runs: {best_overall_score}")
    return best_overall_deciphered_text, best_overall_key, best_overall_score


# Main decipher function
class DecipherText(object):  # Do not change this
    def decipher(self, ciphertext):  # Do not change this
        """Decipher the given ciphertext"""
        num_runs = 100

        # Frequency analysis for initial key
        initial_key = frequency_analysis(ciphertext)

        # Create two variants based on single-letter substitution
        key_a = adjust_for_single_letters(ciphertext, initial_key.copy(), 'a')
        key_i = adjust_for_single_letters(ciphertext, initial_key.copy(), 'i')
        
        # Perform simulated annealing multiple times for both keys
        best_deciphered_text, best_key, best_score = None, None, float('-inf')
        for key in [key_a, key_i]:
            deciphered_text, key, score = simulated_annealing_multiple_runs(ciphertext, key, num_runs)
            if score > best_score:
                best_deciphered_text, best_key, best_score = deciphered_text, key, score
        
        
        # Print the results as required by the template
        print("Ciphertext: " + ciphertext)  # Do not change this
        print("Deciphered Plaintext: " + best_deciphered_text)  # Do not change this
        print("Deciphered Key: " + str(best_key))  # Do not change this

        return deciphered_text, best_key  # Do not change this

if __name__ == '__main__':  # Do not change this
    DecipherText()  # Do not change this
