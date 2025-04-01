from flask import Flask, render_template, request, redirect, url_for
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
import time
from dotenv import load_dotenv
import os
from fpdf import FPDF
from gtts import gTTS

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']

    if file.filename == '':
        return redirect(url_for('index'))

    # Ensure the 'images' directory exists
    images_folder = 'images'
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    # Use the original filename or a timestamped version to avoid overwriting
    filename = file.filename
    input_image_path = os.path.join(images_folder, filename)
    file.save(input_image_path)

    # Pass the filename to the next route
    return redirect(url_for('display_pdf', filename=filename))

@app.route('/display_pdf')
def display_pdf():
    # Get the filename from the query string, default to 'input_image.jpeg'
    filename = request.args.get('filename', 'input_image.jpeg')
    open_dyslexic_convert(filename)
    return render_template('display_pdf.html')

@app.route('/retry', methods=['POST'])
def retry():
    return redirect(url_for('index'))

@app.route('/text_to_speech', methods=['POST'])
def text_to_speech():
    # Get the filename from the query string
    filename = request.args.get('filename', 'input_image.jpeg')
    text = main(filename)
    if text:  # Ensure text is not empty
        tts = gTTS(text)
        tts.save('static/output.mp3')
        return redirect(url_for('play_audio'))
    else:
        return "No text extracted from the image", 500

@app.route('/play_audio')
def play_audio():
    return render_template('play_audio.html')

def open_dyslexic_convert(f_name):
    pdf = FPDF(format='letter', unit='in')
    # Use a default font if the custom one isn't available
    font_path = 'OpenDyslexic-Regular.ttf'  # Adjust this to the actual path if needed
    if os.path.exists(font_path):
        pdf.add_font('new', '', font_path, uni=True)
    else:
        pdf.set_font("Arial", "", 20)  # Fallback to a built-in font
        print(f"Font file '{font_path}' not found, using Arial instead.")

    pdf.add_page()
    pdf.set_font("new" if os.path.exists(font_path) else "Arial", "", 20)
    text = main(f_name)
    if text:
        pdf.multi_cell(7, 0.4, txt=text, align='J')
    else:
        pdf.multi_cell(7, 0.4, txt="No text extracted from the image.", align='J')
    pdf.output("static/output.pdf")

def main(path):
    try:
        load_dotenv()
        endpoint = "" #Your endpoint
        key = "" #Your key 

        computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(key))
        images_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
        read_image_path = os.path.join(images_folder, path)
        result = get_text(read_image_path, computervision_client)
        return result if result else ""

    except Exception as ex:
        print(f"Error in main: {ex}")
        return ""

def get_text(image_file, computervision_client):
    result = ""
    try:
        with open(image_file, "rb") as image:
            read_response = computervision_client.read_in_stream(image, raw=True)

        read_operation_location = read_response.headers["Operation-Location"]
        operation_id = read_operation_location.split("/")[-1]

        while True:
            read_result = computervision_client.get_read_result(operation_id)
            if read_result.status.lower() not in ['notstarted', 'running']:
                break
            time.sleep(1)

        if read_result.status == OperationStatusCodes.succeeded:
            for page in read_result.analyze_result.read_results:
                for line in page.lines:
                    result += line.text + "\n"
    except Exception as ex:
        print(f"Error in get_text: {ex}")

    return result

if __name__ == "__main__":
    app.run(debug=True)