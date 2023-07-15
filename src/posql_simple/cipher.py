class keyTooLongError( Exception ):
    pass

# Create a 5x5 matrix using a secret key
# instead of having 25 char, we're gonna have 32-126
# symmetric algo
# dropped this idea, since, it only works with the 25 letters of the alphabet
class PlayFairCypherExtended: # with all the ascii code ? ( those who are readable )
    def __create_matrix(key):
        key = key.upper()
        matrix = [[0 for i in range (5)] for j in range(5)]
        letters_added = []
        row = 0
        col = 0
        # add the key to the matrix
        for letter in key:
            if letter not in letters_added:
                matrix[row][col] = letter
                letters_added.append(letter)
            else:
                continue
            if (col==4):
                col = 0
                row += 1
            else:
                col += 1
        #Add the rest of the alphabet to the matrix
        # A=65 ... Z=90
        for letter in range(65,91):
            if letter==74: # I/J are in the same position
                    continue
            if chr(letter) not in letters_added: # Do not add repeated letters
                letters_added.append(chr(letter))
                
        #print (len(letters_added), letters_added)
        index = 0
        for i in range(5):
            for j in range(5):
                matrix[i][j] = letters_added[index]
                index+=1

        return matrix

    #Add fillers if the same letter is in a pair
    def __separate_same_letters(message):
        index = 0
        while (index<len(message)):
            l1 = message[index]
            l2 = message[index+1]
            if index == len(message)-1:
                message = message + 'X'
                index += 2
            else:
                if l1==l2:
                    message = message[:index+1] + "X" + message[index+1:]
                index +=2   
        return message

    #Return the index of a letter in the matrix
    #This will be used to know what rule (1-4) to apply
    def __indexOf(letter,matrix):
        # linear scan for getting the actual value
        # since matrix is always 5x5 ; no opt needed
        print ( letter )
        for i in range (5):
            try:
                index = matrix[i].index(letter) # the matrix[i] returns a list, and the index method return the idx of the element
                return (i,index)                # return a tuple of the control var ( loop ) and the index or the position of the letter in the matrix
            except:
                continue 

    #Implementation of the playfair cipher
    #If is_encrypt=True the method will encrypt the message
    # otherwise the method will decrypt
    # error if the key strictly bigger than 25
    @staticmethod
    def playfair(key, message, is_encrypt=True):
        if not ( len ( key ) > 25 ):
            inc = 1
            if not is_encrypt:
                inc = -1
            matrix = PlayFairCypher.__create_matrix(key)
            print ( "the matrix: ", matrix )
            message = message.upper()
            message = message.replace(' ','') # removing any space ? 
            print ( message )
            message = PlayFairCypher.__separate_same_letters(message)
            print ( message )

            # print ("message : ", message)

            cipher_text=''
            for (l1, l2) in zip(message[0::2], message[1::2]):  # object deconstruction
                print ( l1, l2 )
                row1,col1 = PlayFairCypher.__indexOf(l1,matrix) # the matrix will contain all the letters of the alphabet
                row2,col2 = PlayFairCypher.__indexOf(l2,matrix)
                if row1==row2: #Rule 2, the letters are in the same row
                    cipher_text += matrix[row1][(col1+inc)%5] + matrix[row2][(col2+inc)%5]
                elif col1==col2:# Rule 3, the letters are in the same column
                    cipher_text += matrix[(row1+inc)%5][col1] + matrix[(row2+inc)%5][col2]
                else: #Rule 4, the letters are in a different row and column
                    cipher_text += matrix[row1][col2] + matrix[row2][col1]
            
            return cipher_text

        raise keyTooLongError


# advanced Encryption Standard
# NOTES ; symmetric-key algo, meaning we're using the same key for encrypting and decrypting.
    # assymetric-key algo, meaning encrypting with a public and decrypting with a secret key.
    # symmetric algo.
    # 3 parts ; generate a key; generate a cipher ( the algo ) ; encrypt and decrypt the data with the cipher
    # 256 bit keys take up to 32 character instead of 44 char in base64
# need a dependency for that ...
import hashlib
class AESCypher( object ):
    def __init__( self, key ): # key of any lenght ( prefered to be 256 bit )
        self.block_size = 128  # block sizes for the ciphering
        self.key = hashlib.sha256(key.encode()).digest() # will generate a hash

    def __pad( self, plain_text : str ) -> str :
        number_of_bytes_to_pad = self.block_size - len(plain_text) % self.block_size
        ascii_string = chr(number_of_bytes_to_pad) # no unicode ( padding the str with random char )
        padding_str = number_of_bytes_to_pad * ascii_string # interesting
        padded_plain_text = plain_text + padding_str
        return padded_plain_text # now the length of the string is a multiple of 128
    
    @staticmethod
    def __unpad( content : str ) -> str :
        last_character = content[len(content) - 1:] # getting only the last char 
        bytes_to_remove = ord(last_character)       # makes sense when you see the __pad func
        return content[:-bytes_to_remove]

    def encrypt(self, content : str ):
        plain_text = self.__pad(content)
        iv = Random.new().read(self.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted_text = cipher.encrypt(plain_text.encode())
        return b64encode(iv + encrypted_text).decode("utf-8")

# tell me ...

if __name__=='__main__':
    print ( "hello world"[: len ( name ) - 1])