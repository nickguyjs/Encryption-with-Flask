import random, string
from flask import Flask, render_template, request
from CaesarCipher import encryptCaesar, decryptCaesar
from RailFence import encryptRail, decryptRail

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

def encryptCR(text):
  val = encryptCaesar(text)
  val, Variables.numRails = encryptRail(val)
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
def rail_post():
  if request.form.get("btn2"):
    Variables.showNumRails = True
  if request.form.get("btndecm"):
    Variables.showDecMes = True
  if request.form.get("btnstart"):
    Variables.showUserEncFence = True
    Variables.showNumRails = True
    Variables.showDecMes = False
  if request.method == 'POST':      
    if 'plaintext' or 'usercols' or 'userrows' in request.form:
      try:
        Variables.rf_user_cols = request.form['usercols']
        print(Variables.rf_user_cols)
      except:
        pass
      try:
        Variables.rf_user_rows = request.form['userrows']
        print(Variables.rf_user_rows)
      except:
        pass
      try:
        text = request.form['plaintext']
        Variables.processed_text, Variables.numRails = encryptRail(text) # encrypts the text
        Variables.processed_text_dec = decryptRail(Variables.processed_text, Variables.numRails) # decrypts the text
        Variables.showNumRails = False
        Variables.showDecMes = False
      except:
        pass    

  return render_template(
      'rail.html',
      enc_text = Variables.processed_text,
      dec_text = Variables.processed_text_dec if Variables.showDecMes == True else "Click button",
      num_rails = Variables.numRails if Variables.showNumRails else "Click button",
      show_user_rows_cols = "You have " + str(Variables.rf_user_rows) + " rails and " + str(Variables.rf_user_cols) + " columns." if (Variables.rf_user_cols != 0) else "",
      user_rows = int(Variables.rf_user_rows) if Variables.rf_user_rows != '' else 0,
      user_cols = int(Variables.rf_user_cols) if Variables.rf_user_cols != '' else 0,
      user_enc_rails = Variables.numRails if Variables.showUserEncFence else 0,
      user_enc_cols = len(Variables.processed_text) if Variables.showUserEncFence else 0,
      showAnswerBox = True if Variables.showUserEncFence else False
  )



@app.route('/railfence') # for rail fence cipher
def rail_page():

	return render_template(
		'rail.html',  # Template file path
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