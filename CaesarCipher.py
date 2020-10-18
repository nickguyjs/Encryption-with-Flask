from random import randint

def decryptCaesar(text):
  """Returns the decrypted message using the key 'a'."""
  dec = ""
  for i in range(len(text)): # loops through all chars in text
    val = ord(text[i]) # sets val to current char
    val -= Key.key # removes the key from val
    dec += chr(val) # turns val to char, adds to decrypted mess.
  return dec # returns decrypted message

def encryptCaesar(text):
  """Returns an encrypted string using the key 'a'."""
  enc = ""
  Key.setKey() # gets the key
  for i in range(len(text)): # loops through all chars in text
    val = ord(text[i]) # sets val to current char
    val += Key.key # adds the key to char
    enc += chr(val) # turns val to char, adds to message.
  return enc # returns the encrypted message

class Key:
  """Used to store the key."""
  key = 0
  def setKey(): 
    """Sets the key to a number between 1 and 36."""
    Key.key = randint(1,5)