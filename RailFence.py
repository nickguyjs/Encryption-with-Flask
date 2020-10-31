from random import randint

def encryptRail(plaintext, numberRails):
  """Encrypts the plaintext using a Rail Fence cipher."""
  if numberRails == None:
    numRails = 2 if len(plaintext) < 10 else (randint(3,5) if len(plaintext) < 20 else randint(5, 10))
  else:
    numRails = numberRails
    # sets numRails to random number based on length of plaintext
  rf = [[chr(1000)] * len(plaintext) for i in range(numRails)] # creates a matrix length of the text and height based on numRails

  down = False # starts the direction
  row = 0; # sets the starting row
  col = 0; # sets the starting column
  for i in range(len(plaintext)): # runs for the length of plaintext
    if row == 0 or row == numRails - 1: # if at the top or the bottom
      down = not down # flip the direction, allows for zig-zag pattern
  
    rf[row][col] = plaintext[i]; # set the element for given column in correct row
    col += 1 # increment column

    row = row + 1 if down else row - 1 # increments or decrements row
  
  enc = "" 
  for row in rf:
    for x in row:
      if ord(x) != 1000: 
        enc += "" + x # adds element to encrypted text if not a placeholder

  for row in rf:
    print(*row) # prints out the RF array to console

  
  return enc, numRails, rf # returns the ciphertext and key

def decryptRail(ciphertext, numRails):
  """Decrypts the ciphertext using a Rail Fence cipher."""
  rf = [[chr(1000)] * len(ciphertext) for i in range(numRails)] # creates matrix
    
  txt = 0; # used to keep track of loc. on ciphertext
  for i in range(numRails): # loop for # of rails
    down = False # sets the direction
    row = 0; # sets the row
    col = 0; # sets the column
    for j in range(len(ciphertext)): # loop for length of ciphertext
      if row == 0 or row == numRails - 1: 
        down = not down # direction flips if at top or bottom
           
      if row == i:
        rf[row][col] = ciphertext[txt]; # adds element at ciphertext location to RF matrix 
        txt += 1 # increments txt
      
      col += 1
      row = row + 1 if down else row - 1 # increments or decrements row

  dec = ""

  down = False # sets the direction
  row = 0
  col = 0
  for j in range(len(ciphertext)): # loop forward through ciphertext again
    if row == 0 or row == numRails - 1: 
      down = not down # flip direction

    dec += rf[row][col]; # adds element to decrypted text
    col += 1
    row = row + 1 if down else row - 1 
  
  return dec # returns decrypted text