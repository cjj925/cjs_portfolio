# Atbash Cipher Decryptor

## Overview
This project is an Atbash Cipher Decryptor made with Python. An Atbash Cipher is a simple substitution cipher where each letter of the alphabet corresponds to the reverse letter (A -> Z, B -> Y, C -> X). This program decrypts the given ciphertext while keeping upper and lower case letters and leaving non-alphabetic characters unchanged.

## How It Works
* Runs through each character in the ciphertext
* Checks if character is an alphabetic letter
* Applies Atbash substitution using ASCII values
* Uppercase letters, lowercase letters, spaces, and punctuation all unchanged
* Outputs decrypted plaintext

## Concepts
* classlical cryptography
* Character encoding using chr() and ord()
* string iteration
* text formatting

## Requirements
* Python 3.9+
