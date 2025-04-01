CyberScribe is a modern tool that converts images into PDFs and audio files with a stylish neon design. It’s quick, easy to use, and built to help everyone access content in different formats. 
We wanted to create a helpful app with a cool look, making it simple to turn images into something readable or listenable.


What It Does

Image to PDF: Turns pictures into PDFs with a font that’s easy for people with dyslexia.

Text to Audio: Pulls text from images and reads it aloud.

Fast: Gets the job done in just a few seconds.

Neon Look


How We Built It

Backend: Used Flask in Python to run it, Azure Computer Vision to read text, FPDF for PDFs, and gTTS for audio.

Frontend: Designed it with HTML and CSS, added JavaScript for previews and effects.

Tools: Saved our work with Git and got help from openAI tools for coding and fixes.


How to Set It Up

Get the Code:

git clone https://github.com/sang773/panthers.docx.git  
cd panthers.docx  

Set Up a Virtual Environment:

python -m venv venv  
.\venv\Scripts\activate  # Windows  
source venv/bin/activate  # Mac/Linux

Install the Tools:

pip install flask azure-cognitiveservices-vision-computervision msrest python-dotenv fpdf gtts  

Add Your Keys:

AZURE_ENDPOINT= # Write your End point 
AZURE_KEY= # Write your key 

How to Use It


Start the App:

python app.py  

Open It:

Go to the link that you get after running the program in your browser.

Upload an Image:

Choose a picture, see the preview, and convert it to PDF or audio.

Output Examples:

![image](https://github.com/user-attachments/assets/033c3deb-4b6b-4496-8abb-be67f2f0aa6c)

![image](https://github.com/user-attachments/assets/5bc2efe5-344a-4bb0-ab45-c98006f0417e)

![image](https://github.com/user-attachments/assets/000f1b0b-1f18-464a-a002-5912f82f92af)
![image](https://github.com/user-attachments/assets/16b03730-d05f-4cf6-87ac-f923e43e7937)

![image](https://github.com/user-attachments/assets/7e5f07b9-687f-455b-b4c7-850e2f6d9a47)


What We Learned

How to use Flask, connect to Azure, and design a nice webpage.
Learned Git basics and how to fix problems.

What’s Next

Add support for more languages and audio options.
Put it online so anyone can try it.


Made by panthers.docx © 2025
