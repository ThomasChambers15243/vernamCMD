
import secrets
import argparse
import sys
import os.path
import re

parser  = argparse.ArgumentParser(description="A program to simulate the vernam cypher")
plainText_cypherText = parser.add_mutually_exclusive_group(required=True)
encrypt_decrypt = parser.add_mutually_exclusive_group(required=True)


plainText_cypherText.add_argument("-pt","--plainText", help="The plain text that is desired to be encrypted")
plainText_cypherText.add_argument("-ct","--cypherText", help="The cypherText that is desired to be decrypted")

plainText_cypherText.add_argument("-ptf", help = "Text File containing the plain text that is desired to be encrypted")
plainText_cypherText.add_argument("-ctf", help = "BinaryFile containing the cypherText that is desired to be decryted")

parser.add_argument("-k","--key", help="The key to be used to decrpt")
parser.add_argument("-kf", help="Text file containg the binary key required to decrypt")

encrypt_decrypt.add_argument("-en","--encrypt", help="True if you wish to decrypt plaintext, defualt is False. A key cannot be provided. en cannot be used with ct", action="store_true")
encrypt_decrypt.add_argument("-dc","--decrypt", help="True if you wish to decrypt, defualt is False, key must be provided, dc cannot be used with pt.", action="store_true")
args = parser.parse_args()


#Generates a key with random length and even distribution
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
    temp = (format(asciiChars[i],'08b'))#08b to keep leading 0's and to keep looping through the cypher text consistant
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
def encryptText(plainText):
  key=generateKey(len(plainText))
  binaryText = textToBin(plainText)
  cypherText = logicalXOR(key,binaryText)

  return cypherText, key

#Takes in origional key that was used to encrypt and
#decrypts the cypher text with it
def decryptCypher(key,cypherText):
  decypherText = logicalXOR(key,cypherText)
  plain = binToText(decypherText)

  return plain


#Function to create and write contents to a text file, if name is taken 
#it keeps adding numbers to the end until its a new file. 
#Returns the created filename
def crWrToTextFile(fileName, contents):
  txtCheck = re.search(".txt$",fileName)
  if txtCheck == None:
    return ".txtError"
  name = fileName[:-4]
  i = 1
  while os.path.isfile(fileName) == True:
    fileName = name
    fileName+=str(i)+".txt"
    i+=1
  f = open(fileName,"w")
  f.write(contents)
  f.close()
  return fileName


def readTxtFile(fileName):
    f = open(fileName,"r")#open file
    lines = f.readlines()#read the entire file
    plainText = "".join(lines)#joins each line together
    return plainText

def main():
  #CTK = CyhperText and Key where CTK[0] = cyphertext and CTK[1] = key
  if args.encrypt == True and (args.ptf != None or args.plainText != None):
    if args.ptf == None:
      CTK = encryptText(args.plainText)
      cypherText = CTK[0]
      KEY = CTK[1]
    else:
      #Open plaintext file
      plainText = readTxtFile(args.ptf)
      CTK = encryptText(plainText)#encrpts the text file and returns as CTK
      cypherText = CTK[0]
      KEY = CTK[1]
    
    #Get user choices for how they'd like the cypher text and key saved

    correct = False
    choices = ["b","pt","f"]
    while correct != True:
      choice = input("Would you like the key and Cypher text to be printed to the console in:\nBinary, plain text or saveds binary to a text file? (b,pt,f)")
      if choice not in choices:
        print("Invalid input:\nb = print the key and cypher text in the console as binary\npt = print the key and cyphertext as ascii chars\nf = save to a text file")
      else:
        correct = True

    #execute the users choices

    if choice.lower() == "b":#Prints to concosle as binary representation
      print("Cypher Text is: \" {} \"\n".format(cypherText))
      print("Key is: \" {} \"\n".format(KEY))
    elif choice.lower() == "pt":#Prints to console as plain text representation
      print("Cypher Text is: \" {} \"\n".format(binToText(cypherText)))
      print("Key is : \" {} \"\n".format(binToText(KEY)))
    else:
      #runs the crWrBinToTextFile() function to save the cyphertext and key in two seperate .txt files
      try:
        fileNameCypher = crWrToTextFile("CypherText.txt",cypherText)
        fileNameKey = crWrToTextFile("Key.txt",KEY)
        #Checks file is a .txt file
        if fileNameCypher == ".txtError" or fileNameKey == ".txtError":
          print("Wrong FileName")
          sys.exit(1)
        else:
          print("Binary cypher text saved to a text file named {}".format(fileNameCypher))
          print("Binary key saved to a text file name {}".format(fileNameKey))
      except:
        print("Could not save to files")

  #If the user choice to decrypt
  elif args.decrypt == True and (args.cypherText != None or args.ctf != None):
    if args.ctf == None:
      plain = decryptCypher(args.key,args.cypherText)
    else:#-kf
      key = readTxtFile(args.kf)
      cypher = readTxtFile(args.ctf)
      plain = decryptCypher(key,cypher)
    correct = False
    choices = ["b","pt","no"]
    while correct != True:
      choice = input("Save to text file in plain text or binary? No to print to console and exit.(no,pt,b)\n")
      if choice not in choices:
        print("Invalid input:\nno to quit program\npt to save to a text file\nb to save the binary to a text file\n")
      else:
        correct = True
    if choice == "b":
      #saves as a binary string to a text file name binaryText.txt
      fileName = crWrToTextFile("binaryText.txt", textToBin(plain))
      print("Plain text has been saved as a binary string to {}.".format(fileName))
    elif choice == "pt":
      fileName = crWrToTextFile("plainText.txt", plain)
      print("Plain text has been saved to {}".format(fileName))
    else:
      print("Text is:\n{}".format(plain))
      sys.exit(0)

  else:
    print("Invaldid input")
    parser.print_help(sys.stderr)


if __name__ == "__main__":
    main()

