from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from src import text_extraction as te
from src import intelligent_parsing as ip

# Initialize Flask app
app = Flask(__name__)

# Set upload folder and allowed extensions
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'jpeg', 'jpg', 'png', 'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Utility function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to handle text extraction based on file type
def extract_text_from_file(filepath, file_extension):
    extractor = te.FileTextExtractor()

    if file_extension == 'pdf':
        # Extract text from PDF
        return extractor.extract_text(filepath)
    elif file_extension == 'txt':
        # Read text directly from txt file
        with open(filepath, 'r') as file:
            return file.read()
    elif file_extension in ['jpeg', 'jpg', 'png']:
        # Call your OCR process for image files
        return extractor.extract_text_from_image(filepath)  # Ensure your module handles this
    else:
        return None

# Main route to render the upload page
@app.route('/')
def index():
    return render_template('upload.html')

# Route to handle file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save the file
        file.save(filepath)

        # Extract the file extension
        file_extension = filename.rsplit('.', 1)[1].lower()

        # Extract text for all file types
        extracted_text = extract_text_from_file(filepath, file_extension)

        # Parse the extracted text
        output_record = None
        if extracted_text:
            intelligent_parser = ip.IntelligentDocumentParser()
            output_record = intelligent_parser.parse(extracted_text)

        # Pass the extracted raw text and the filename along with the parsed data
        return render_template('result.html', output_record=output_record, extracted_text=extracted_text, filename=filename)

    return redirect(request.url)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
