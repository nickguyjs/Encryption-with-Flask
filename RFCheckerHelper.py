import random

phrases = [["ILOVEPIZZA", "IEZLVPZAOI", 3], ["THEBRITISHARECOMING", "TERTSAEOIGHBIIHRCMN", 2], ["WEAREDISCOVEREDFLEEATONCE", "WDEEFARLREEEVEEDOACICTNSO", 8], ["WORKHARDER", "WHEOKADRRR", 3], ["THISISEASY", "TEHSAIISSY", 4]];

class HoldMyPhrase:
  heldPhrase = ["", "", 0]
  heldMatrix = None

def getPhrases():
  choice = random.randint(0,4)
  return phrases[choice]

def holdPhrase(hf):
  HoldMyPhrase.heldPhrase = hf

def getMyPhrase():
  print(HoldMyPhrase.heldPhrase[2])
  return HoldMyPhrase.heldPhrase

def setMatrix(mat):
  HoldMyPhrase.heldMatrix = mat