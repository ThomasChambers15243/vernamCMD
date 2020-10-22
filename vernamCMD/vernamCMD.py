
import secrets
import argparse

parser  = argparse.ArgumentParser(description="A program to simulate the vernam cypher")
plainText_cypherText = parser.add_mutually_exclusive_group(required=True)
encrypt_decrypt = parser.add_mutually_exclusive_group(required=True)


plainText_cypherText.add_argument("-pt","--plainText", help="The plain text that is desired to be encrypted")
plainText_cypherText.add_argument("-ct","--cypherText", help="The cyhperText that is desired to be decrypted")

plainText_cypherText.add_argument("-k","--key", help="The key to be used to decrp, if one is not given then one will be generated",type=int)

encrypt_decrypt.add_argument("-en","--encrypt", help="True if you wish to decrypt plaintext, defualt is False. Providing a key is optional. en cannot be used with dc", action="store_true")
encrypt_decrypt.add_argument("-dc","--decrypt", help="True if you wish to decrypt, defualt is False, key must be provided, dc cannot be used with dc.", action="store_true")
args = parser.parse_args()



def generateKey(len):
  hexKey = secrets.token_hex(len+(1+secrets.randbelow(1000)))
  intKey = int(hexKey,16)
  binKey = str(bin(intKey))
  key = binKey[2:]
  return key

#returns the binary representatoin of a plain text
def textToBin(text):
  asciiChars = []
  for i in text:
    asciiChars.append(ord(i))
  for i in range(0,len(asciiChars)):
    temp = (format(asciiChars[i],'08b'))#08b to keep leading 0's
    asciiChars[i] = temp
  binString = "".join(asciiChars)
  return binString

#returns the text from a binary string
def binToText(binary):
  n = 8
  chunks = [binary[i:i+n] for i in range(0,len(binary),n)]
  for i in range(0,len(chunks)):
    temp = int(chunks[i],2)
    chunks[i] = chr(temp)
  text = "".join(chunks)
  return text

#Performs bitwise XOR on the key and the binary rep of the text
def logicalXOR(key,binText):
  result=[]
  for i in range(0,len(key)):
    #try catch here as once the entire plain text has been xor'ed
    #the rest of the key is appended
    try:
      if str(key[i]) != str(binText[i]):
        result.append("1")
      else:
        result.append("0")
    except:
      result.append(str(key[i]))
  return "".join(result)

#Encrypts plain text from agrs
#If no key is given then by default one is generated using the legth of the plaintext.
def encryptText(key=generateKey(len(args.plainText))):
  binaryText = textToBin(args.plainText)
  cypherText = logicalXOR(key,binaryText)

  return cypherText, key

#Takes in origional key that was used to encrypt and
#decrypts the cypher text with it
def decryptCypher(key,cypherText):
  decypherText = logicalXOR(key,cypherText)
  plain = binToText(decypherText)

  return plain

def main():
  #CTK = CyhperText and Key where CTK[0] = cyphertext and CTK[1] = key
  if args.encrypt == True:
    if args.key == None:
      CTK = encryptText()
      cypherText = CTK[0]
    else:
      CTK = encryptText(args.key)
      cypherText = CTK[0]
    KEY = CTK[1]
  #'elif args.decrypt == True:

#print(decryptCypher(CTK[1],cypherText))

if __name__ == "__main__":
    main()
