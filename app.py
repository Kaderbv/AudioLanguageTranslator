from flask import Flask, request, render_template 
from openai import OpenAI
from pathlib import Path
import yaml
import os
from convertor import text_to_speech

app = Flask(__name__) 


with open("keys.yaml","r") as file:
    keys=yaml.safe_load(file)
client = OpenAI(api_key=keys["api_key"])

# To render a index form 
@app.route('/', methods=["GET", "POST"])
def view_form():
    return render_template('index.html')
    
@app.route('/Save', methods=["POST"])
def index():
    if request.method == "POST": 
        f = request.files['audio_data']
        with open('audio.wav', 'wb') as audio:
            f.save(audio)
      
        return render_template('index.html/handle_submit', request="POST") 
    else:
        return render_template("index.html")

@app.route("/handle_submit", methods=["GET", "POST"]) 
def handle_submit(): 
    if request.method == "POST": 
       
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio.wav")
        print(file_path)
        #file.save(file_path)
   
        audio_file= open(file_path, "rb")
        # Converts audio to text
        translation = client.audio.translations.create(model="whisper-1", file=audio_file)   
        print(translation)
        
        # transcrips from one lang to another language in text
        response = client.audio.transcriptions.create(
            model='whisper-1',
            file=audio_file,
            language=request.form.get('toLang')
        )
        transcription_text = response.text 
        print(request.form.get('toLang') + " "+transcription_text)   
        text_to_speech(transcription_text, 'Male')
        return  render_template("index.html", translation=request.form.get('toLang'), transcription_text=transcription_text) 

    return render_template("index.html") 

if __name__ == "__main__": 
    app.run(debug=True) 
