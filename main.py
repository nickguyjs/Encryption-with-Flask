import random, string
from flask import Flask, render_template, request
from CaesarCipher import encryptCaesar, decryptCaesar
from RailFence import encryptRail, decryptRail
from RFCheckerHelper import getPhrases, holdPhrase, getMyPhrase, setMatrix

processed_text = ""

app = Flask(  # Create a flask app
	__name__,
	template_folder='templates',  # Name of html file folder
	static_folder='static'  # Name of directory for static files
)

class Variables:
  numRails = 0
  showNumRails = False
  showDecMes = False
  showUserEncFence = False
  processed_text = ""
  processed_text_dec = ""
  rf_user_rows = 0
  rf_user_cols = 0
  phrase = ["", "", 0]
  rf_user_cols_dec = 0
  working_on_problem = False
  user_plain_text = ""
  checkerMatrix = None
  actualMatrix = None
  is_good = "WRONG"
  
  def resetRailFence():
    Variables.numRails = 0
    Variables.showNumRails = False
    Variables.showDecMes = False
    Variables.showUserEncFence = False
    Variables.processed_text = ""
    Variables.processed_text_dec = ""
    Variables.rf_user_rows = 0
    Variables.rf_user_cols = 0
    Variables.phrase = ["", "", 0]
    Variables.rf_user_cols_dec = 0
    Variables.working_on_problem = False
    Variables.user_plain_text = "";
    Variables.checkerMatrix = None
    Variables.actualMatrix = None
    Variables.is_good = "WRONG"

def encryptCR(text):
  val = encryptCaesar(text)
  temp = None
  val, Variables.numRails, temp = encryptRail(val, None)
  setMatrix(temp)
  return val

def decryptCR(text):
  val = decryptRail(text, Variables.numRails)
  val = decryptCaesar(val)
  return val

@app.route('/')  # Original path for the site
def base_page():

	return render_template(
		'base.html',  # Template file path
	)

@app.route('/caesar', methods=['POST'])
def ceasar_post():
  text = request.form['text']
  processed_text = encryptCaesar(text) # encrypts the text
  processed_text_dec = decryptCaesar(processed_text) # decrypts the text
  return render_template(
		'caesar.html',
		enc_text = processed_text,  # Sets the variable enc_text in the template
                                # to the encrypted text
    dec_text = processed_text_dec # sets dec_text to decrypted text 
	)

@app.route('/caesar') # for the caesar cipher
def caesar_page():

	return render_template(
		'caesar.html',  # Template file path
	)

@app.route('/railfence', methods=['GET', 'POST'])
def rail_encrypt_any():
  if request.form.get("resetPage"):
    Variables.resetRailFence()
  if Variables.working_on_problem == False:
    Variables.phrase = getPhrases()
    holdPhrase(Variables.phrase);
  else:
    Variables.phrase = getMyPhrase()
  if request.form.get("btnstart"):
    print('btnstart clicked')
    Variables.showUserEncFence = True
    Variables.showNumRails = True
    Variables.showDecMes = False
  if request.form.get("btn2"):
    Variables.showNumRails = True
  if request.form.get("btndecm"):
    Variables.showDecMes = True
  if request.method == 'POST':      
    #Part 1
    if 'plaintext' in request.form:
      try:
        text = request.form['plaintext']
        temp = None
        Variables.processed_text, Variables.numRails, temp = encryptRail(text, None) # encrypts the text
        setMatrix(temp)
        Variables.processed_text_dec = decryptRail(Variables.processed_text, Variables.numRails) # decrypts the text
        Variables.showNumRails = False
        Variables.showDecMes = False
      except:
        print("ERROR: error occured while retrieving plaintext from request.form in function rail_encrypt_any")
        pass  

    #Part 2
    if 'userplaintext' in request.form:
      try:
        Variables.user_plain_text = request.form['userplaintext']
        print(Variables.user_plain_text)
      except:
        print("ERROR: error occured while retrieving userplaintext from request.form in rail_dec_prev_enc")
        pass
    
    #Part 3
    if'usercols' or 'userrows' in request.form:
      try:
        Variables.rf_user_cols = request.form['usercols']
        print(Variables.rf_user_cols)
      except:
        print("ERROR: error occured while retrieving usercols from request.form in user_enc_rail_fence")
        pass
      try:
        Variables.rf_user_rows = request.form['userrows']
        print(Variables.rf_user_rows)
      except:
        print("ERROR: error occured while retrieving userrows from request.form in user_enc_rail_fence")
        pass
    
    #Part 4
    if 'usercolsdec' in request.form:
      try:
        Variables.rf_user_cols_dec = int(request.form['usercolsdec'])
        holdPhrase(Variables.phrase)
        Variables.working_on_problem = True
        print(Variables.rf_user_cols_dec)
      except:
        print("ERROR: error occured while retrieving usercolsdec from request.form in user_dec_rand_rail_fence")
        pass
    

  return render_template(
    'rail.html',
    enc_text = Variables.processed_text,
    dec_text = Variables.processed_text_dec if Variables.showDecMes == True else "Click button",
    num_rails = Variables.numRails if Variables.showNumRails else "Click button",
    show_user_rows_cols = "You have " + str(Variables.rf_user_rows) + " rails and " + str(Variables.rf_user_cols) + " columns." if (Variables.rf_user_cols != 0) else "",
    user_rows = int(Variables.rf_user_rows) if Variables.rf_user_rows != '' else 0,
    user_cols = int(Variables.rf_user_cols) if Variables.rf_user_cols != '' else 0,
    user_pt = Variables.user_plain_text, 
      
    user_enc_rails = Variables.numRails if Variables.showUserEncFence else 0,
    user_enc_cols = len(Variables.processed_text) if Variables.showUserEncFence else 0,
    showAnswerBox = True if Variables.showUserEncFence else False,

    random_cipher = getMyPhrase()[1],
    user_cols_for_rand = Variables.rf_user_cols_dec if Variables.working_on_problem else 0,
    user_rails_for_rand = getMyPhrase()[2] if Variables.working_on_problem else 0
  )

@app.route('/railfence') # for rail fence cipher
def rail_page():

	return render_template(
		'rail.html',  # Template file path
	)

@app.route('/rfdec', methods=['GET', 'POST'])
def RFDecrypt():
  if request.form.get('getstr'):
    Variables.phrase = getPhrases()
    holdPhrase(Variables.phrase)
  if request.method == 'POST':    
    if 'txtName-0-0' in request.form:
      Variables.checkerMatrix = [[chr(1000)] * Variables.rf_user_cols_dec for i in range(getMyPhrase()[2])]
      for i in range(getMyPhrase()[2]):
        for j in range(Variables.rf_user_cols_dec):
          if ('txtName-' + str(i) + "-" + str(j)) in request.form:
            val = request.form['txtName-' + str(i) + "-" + str(j)]
            Variables.checkerMatrix[i][j] = val if val != "" else chr(1000)
            print("ADD: " + val)
      x, y, z = encryptRail(getMyPhrase()[0], getMyPhrase()[2])
      for row in Variables.checkerMatrix:
        print(*row)
      if z == Variables.checkerMatrix:
        print("ALL GOOD")
        Variables.is_good = "ALL GOOD"
      else:
        Variables.is_good = "WRONG"
    if 'usercolsdec' in request.form:
      try:
        Variables.rf_user_cols_dec = int(request.form['usercolsdec'])
        holdPhrase(Variables.phrase)
        print(Variables.rf_user_cols_dec)
      except:
        print("ERROR: error occured while retrieving usercolsdec from request.form in RFDecrypt")
        pass
  return render_template(
    'RFDecrypt.html',
    random_cipher = getMyPhrase()[1] if len(getMyPhrase()[1]) > 0 else "",
    user_rails_for_rand = getMyPhrase()[2] if getMyPhrase()[2] > 0 else 0,
    user_cols_for_rand = Variables.rf_user_cols_dec if Variables.rf_user_cols_dec > 0 else 0,
    correctness = Variables.is_good
  )

@app.route('/CaesarRail', methods=['POST'])
def cr_post():
  text = request.form['text']
  processed_text = encryptCR(text) # encrypts the text
  processed_text_dec = decryptCR(processed_text) # decrypts the text
  return render_template(
		'caesarRail.html',
		enc_text = processed_text,  # Sets the variable enc_text in the template
                                # to the encrypted text
    dec_text = processed_text_dec # sets dec_text to decrypted text 
	)
@app.route('/CaesarRail') # for rail fence cipher
def cr_page():

	return render_template(
		'caesarRail.html',  # Template file path
	)

if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
		host='0.0.0.0',  # Establishes the host, required for repl to detect the site
		port=random.randint(2000, 9000)  # Randomly select the port the machine hosts on.
	)


