# Shifting Cipher

## Shifting Cipher is a simple file encryption and decryption program written in Python. It uses a character shifting algorithm where each character is shifted by a corresponding character which comes from a user-provided key. This is a symmetric cipher, meaning the same key is used for both encryption and decryption.

## How it Works
* Each character in the input text is converted to its corresponding Unicode value
* Each character in the key is also converted to its corresponding Unicode value
* The key repeats as much as necessary to match the length of the text
* Encryption adds the keys value to the text character value
* Decryption subtracts the keys value from the encrypted character value

## Features
* Encrypts text files using a shifting cipher
* Decrypts encrypted file
* Key repeats until it matches length of text
* Preserves all characters (" ", and " ' ")

## Requirements
* Python 3.9+

## How to Run

* First you must create a text file which you want to encrypt in the downloaded ShiftingCipher folder

* Run program in terminal: python shiftingcipher.py

Printed menu: 
== Shifting Cipher ==
1. Encrypt a file
2. Decrypt a file
3. Quit

Encrypting file steps:
1. Choose option 1
2. Enter the text file name you created
3. Enter a name for the output file that will store the encrypted message
4. Enter encryption key

The encrypted text will now be stored in the output file

Decrypting file steps:
1. Choose option 2
2. Enter the encrypted file's name
3. Enter a name for the output file that will store the decrypted message
4. Enter the same exact encryption key

The decrypted text will now be stored in the output file


