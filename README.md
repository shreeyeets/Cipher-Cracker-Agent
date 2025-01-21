# Ciphertext Decoding using Frequency Analysis and Simulated Annealing

## Overview

This project is designed to decipher a given ciphertext using a combination of **frequency analysis** and **simulated annealing** optimization. The goal is to uncover the original plaintext by reversing a substitution cipher, where each character in the ciphertext has been replaced by a different character. The code implements several techniques to improve the accuracy of the decryption process, including bigram scoring and frequency-based adjustments.

## Approach

The approach is based on the assumption that the ciphertext is a result of a substitution cipher, where one character maps to another. We use **frequency analysis** to build an initial decryption key and then optimize it using **simulated annealing**. The methods used in the code cover the following steps:

1. **Frequency Analysis**: Analyzing the frequency of characters in the ciphertext and matching them to common letter frequencies in the English language (such as "ETAOINSHRDLCUMWFGYPBVKJXQZ").
   
2. **Bigram and N-gram Modeling**: Using bigram (two-letter combinations) statistics from the **Reuters corpus** in the NLTK library to score the quality of the deciphered text. This ensures that the decrypted text closely resembles natural language patterns.

3. **Simulated Annealing**: A heuristic optimization technique that starts with an initial decryption key and iteratively improves it by randomly swapping character mappings while maintaining or increasing the likelihood of a more accurate decryption.

4. **Single-letter Substitution Adjustment**: Adjusting the key to account for single-character words in the ciphertext (e.g., "I", "A") and ensuring that these are substituted correctly in the final decryption.

## Components and Methodology

### 1. **Frequency Analysis (`frequency_analysis`)**

This method counts the frequency of characters in the ciphertext and creates a mapping of the most common characters to the most frequent letters in the English alphabet. The following steps are involved:
- Count occurrences of each character in the ciphertext.
- Sort the characters based on frequency.
- Map the most frequent ciphertext characters to the most frequent letters in English using the `etaoinshrdlcumwfgypbvkjxqz` pattern.

### 2. **Bigram Score Calculation (`bigram_score`)**

This method calculates a score for the deciphered text based on how many bigrams (pairs of adjacent letters) from the text match bigrams in the **Reuters corpus**. A higher score indicates that the text follows natural language patterns. The method does the following:
- Tokenizes the deciphered text into words.
- Counts how many bigrams from the deciphered text appear in the pre-trained bigram model.
- Returns the ratio of matching bigrams to total bigrams in the text.

### 3. **Word Validity Score (`nltk_score`)**

This method checks how many words in the deciphered text are valid English words. It uses the **NLTK words corpus** to verify the validity of words. The method:
- Splits the text into words and checks each against the list of valid English words.
- Additionally, it looks for common two-letter words (e.g., "to", "it", "is") and gives a bonus for each occurrence, which can be adjusted for better results.

### 4. **Simulated Annealing (`simulated_annealing`)**

Simulated annealing is used as an optimization algorithm to improve the decryption key over time. The process starts with an initial key (from frequency analysis) and iteratively swaps two random letters in the key. The steps are as follows:
- For each iteration, randomly swap two characters in the key.
- Calculate the combined score for the new key using both the **bigram score** and **word validity score**.
- If the new score is better than the current score, or with a probability based on a "temperature" factor, accept the new key.
- Gradually reduce the temperature to prevent drastic changes and focus on refining the key.

### 5. **Single-letter Substitution Adjustment (`adjust_for_single_letters`)**

This method adjusts the substitution key to correctly handle single-character words, such as "I" or "A". Since these are common words, it's important to ensure that they map to the correct letters in the ciphertext. The method:
- Identifies the most frequent single-character word in the ciphertext.
- Ensures that the characters "a" and "i" are substituted correctly, given their significance in English.

### 6. **Decryption (`decipher_text`)**

This method takes the ciphertext and a substitution key, and uses the key to replace each character in the ciphertext with its corresponding character in the key. It also handles spaces and punctuation marks (e.g., commas, periods) as part of the valid characters. The final result is the plaintext, which is then printed in uppercase for clarity.

### 7. **Class Implementation (`DecipherText`)**

The main class, `DecipherText`, implements the decryption logic. The `decipher` method takes the ciphertext as input and applies the previously defined methods to:
- Perform frequency analysis to generate the initial key.
- Adjust the key for single-letter substitutions.
- Optimize the key using simulated annealing.
- Output the deciphered text and the decryption key.
- Tweaked it to perform in iterations for multiple annealings.
The class outputs the following:
- **Ciphertext**: The input ciphertext.
- **Deciphered Plaintext**: The resulting decrypted message.
- **Decryption Key**: The final key used for decryption.

## Features
- **Frequency Analysis**: Automatically builds a mapping of ciphertext characters to likely plaintext characters based on frequency.
- **Bigram and Word Validity Scoring**: Scores the quality of the decrypted text by comparing it to natural language bigram and word statistics.
- **Simulated Annealing**: Optimizes the decryption key iteratively to improve the quality of the decrypted text.
- **Single-letter Substitution Adjustment**: Adjusts the key to handle common single-character words like "I" or "A" accurately.
- **Uppercase Output**: All output is printed in uppercase for readability.
