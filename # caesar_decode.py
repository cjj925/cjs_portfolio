def atbash_decrypt(ciphertext):
    decrypted = ""
    for char in ciphertext:
        if char.isalpha():
            if char.isupper():
                decrypted += chr( ord('Z') - (ord(char) - ord('A')) )
            else:
                decrypted += chr( ord('z') - (ord(char) - ord('a')) )
        else:
            decrypted += char
    return decrypted

ciphertext = "zorxv dzh yvtrmmrmt gl tvg evib grivw lu hrggrmt yb svi hrhgvi lm gsv yzmp zmw lu szermt mlgsrmt gl wl lmxv li gdrxv hsv szw kvvkvw rmgl gsv yllp svi hrhgvi dzh ivzwrmt yfg rg szw ml krxgfivh li xlmevihzgrlmh rm rg zmw dszg rh gsv fhv lu z yllp gslftsg zorxv drgslfg krxgfivh li xlmevihzgrlm hl hsv dzh xlmhrwvirmt rm svi ldm nrmw zh dvoo zh hsv xlfow uli gsv slg wzb nzwv svi uvvo evib hovvkb zmw hgfkrw dsvgsvi gsv kovzhfiv lu nzprmt z wzrhb xszrm dlfow yv dligs gsv gilfyov lu tvggrmt fk zmw krxprmt gsv wzrhrvh dsvm hfwwvmob z dsrgv Izyyrg drgs krmp vbvh izm xolhv yb svi"

plaintext = atbash_decrypt(ciphertext)
print(plaintext)

