from flask import Flask, render_template, request, Blueprint
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch

textDetector_app = Blueprint("textDetector", __name__)

# Load pre-trained DistilBERT model and tokenizer
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased')

def check_text(text):
    try:
        # Tokenize and convert to model input format
        inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)

        # Make a prediction
        outputs = model(**inputs)

        # Get predicted label
        prediction = torch.argmax(outputs.logits).item()

        # Analyze the prediction and classify as AI-generated or human-written
        if prediction == 0:  # You may need to adjust this based on your model
            return "This text is likely human-written."
        else:
            return "This text appears to be AI-generated."
    except Exception as e:
        return f"An error occurred: {str(e)}"

@textDetector_app.route('/')
def index():
    return render_template('textDetector.html')

@textDetector_app.route('/', methods=['POST'])
def process_text():
    user_input = request.form['user_input']

    if user_input:
        result = check_text(user_input)
        return render_template('textDetector.html', result=result, user_input=user_input)
    else:
        return render_template('textDetector.html', warning="Please enter some text.")
