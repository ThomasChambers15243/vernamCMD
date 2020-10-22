
import secrets
import argparse
from random import randint
parser  = argparse.ArgumentParser()
parser.add_argument("plainText", help="The plain text that is desired to be encrypted")
parser.add_argument("-k","--key", help="The key to be used to decrp, if one is not given then one will be generated",type=int)
args = parser.parse_args()



def generateKey(len):
  hexKey = secrets.token_hex(len+1)
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
    temp = str(bin(asciiChars[i]))
    temp = temp[2:]
    asciiChars[i] = temp
  binString = "".join(asciiChars)
  return binString

def binToText(bin):
  ##TODO##

  n = 7
  chunks = [bin[i:i+n] for i in range(0,len(bin),n)]
  print(chunks)
  for i in range(0,len(chunks)):
    temp = int(chunks[i],2)
    chunks[i] = chr(temp)
  text = "".join(chunks)
  return text




if args.key == None:
  key = generateKey(len(args.plainText))
  print(key)



