def decrypt(ciphertext):
    decrypted = ""
    for char in ciphertext: ## Iterate through characters in ciphertext
        if char.isalpha(): ## Only if character is a alphabetic character
            if char.isupper(): ## If character is uppercase
                decrypted += chr( ord('Z') - (ord(char) - ord('A')) )
            else: ## If character is lowercase
                decrypted += chr( ord('z') - (ord(char) - ord('a')) )
        else:
            decrypted += char ## Create decrypted message
    return decrypted

ciphertext = "zorxv dzh yvtrmmrmt gl tvg evib grivw lu hrggrmt yb svi hrhgvi lm gsv yzmp zmw lu szermt mlgsrmt gl wl lmxv li gdrxv hsv szw kvvkvw rmgl gsv yllp svi hrhgvi dzh ivzwrmt yfg rg szw ml krxgfivh li xlmevihzgrlmh rm rg zmw dszg rh gsv fhv lu z yllp gslftsg zorxv drgslfg krxgfivh li xlmevihzgrlm hl hsv dzh xlmhrwvirmt rm svi ldm nrmw zh dvoo zh hsv xlfow uli gsv slg wzb nzwv svi uvvo evib hovvkb zmw hgfkrw dsvgsvi gsv kovzhfiv lu nzprmt z wzrhb xszrm dlfow yv dligs gsv gilfyov lu tvggrmt fk zmw krxprmt gsv wzrhrvh dsvm hfwwvmob z dsrgv Izyyrg drgs krmp vbvh izm xolhv yb svi"

plaintext = decrypt(ciphertext)
print(plaintext)
