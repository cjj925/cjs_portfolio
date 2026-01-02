# shiftingcipher.py
# CJ Rinaldi
# Shifting Cipher

def encrypt(text, key):
    result = "" # stores encrypted message
    key = [ord(k) for k in key] # This converts the key to a list of numbers
    
    for i, ch in enumerate(text): # loop through each character
        currchar = ord(ch) # stores unicode number for current char
    
        shift = key[i % len(key)] # loops through the message
        
        shiftchar = (currchar + shift) # encrypts
        
        result += chr(shiftchar) # converts unicode number to char and adds to result
        
    return result # returns encrypted message

def decrypt(text, key):
    result = "" # stores the decrypted message
    key = [ord(k) for k in key] # This converts the key to their unicode number
    for i, ch in enumerate(text): # loop through each encrypted char
        currchar = ord(ch) # stores unicode number for current char
    
        shift = key[i % len(key)] # loops through the message
        
        shiftchar = (currchar - shift) # reverse encryption
        
        result += chr(shiftchar) # converts unicode number into a char and adds to char
        
    return result # returns decrypted message

def encrypt_file(input_file, output_file, key):
    try:
        with open(input_file, 'r', encoding='utf-8') as f: # open and read input file
            text = f.read()
    except FileNotFoundError:
        print(f"Error: {input_file}' not found.") # handle exception
        return
    encrypted = encrypt(text, key) # encrypt file with provided key
    
    with open(output_file, 'w', encoding='utf-8') as f: # create and write encrypted contents to outputfile 
        f.write(encrypted)
        
        print(f"Encrypted file saved as '{output_file}'")
        
def decrypted_file(input_file, output_file, key):
    try:
        with open(input_file, 'r', encoding='utf-8') as f: # open and read encrypted file
            text = f.read()
    except FileNotFoundError:
        print(f"Error: '{input_file}' not found.") # handle exception
        return
    decrypted = decrypt(text, key) # decrypt file with provided key
    
    with open(output_file, 'w', encoding='utf-8') as f: # create and write decrypted contents to outputfile
        f.write(decrypted)
        
        print(f"Decrypted file saved as '{output_file}'")
    
def main():
        
    print("== Shifting Cipher ==")
    print("1. Encrypt a file")
    print("2. Decrypt a file")
    print("3. Quit")
        
    try:
        choice = int(input("Enter your choice (1-3): ")) # main menu
    except ValueError:
        print("Invalid input. Please enter a number.") # handle valueError exception
        return
        
    if choice == 3: # Exit program
        print("Goodbye!")
        return
    
    input_file = input("Enter input file name: ") # file names and encryption key
    output_file = input("Enter output file name: ")
    key = input("Enter encryption key: ")
        
    if choice == 1:
        encrypt_file(input_file, output_file, key)
    elif choice == 2:
        decrypted_file(input_file, output_file, key)
    else:
        print("Invalid choice. Please select 1, 2, or 3.")
            
if __name__ == "__main__":
    main()

        
        
