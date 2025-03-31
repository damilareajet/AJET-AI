import os
from flask import Flask, render_template, request, jsonify
import json
import pickle
import numpy as np
import random
from tensorflow.keras.models import load_model
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import nltk
from dotenv import load_dotenv
import openai

# Download necessary NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('wordnet', quiet=True)
except:
    pass

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# Get API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Load chatbot model and data
try:
    # Load the trained model
    model = load_model('model.h5')
    
    # Load the words and classes
    with open('texts.pkl', 'rb') as file:
        words = pickle.load(file)
    with open('labels.pkl', 'rb') as file:
        classes = pickle.load(file)
    
    # Load intents
    with open('data.json') as file:
        intents = json.load(file)
    
    model_ready = True
    print("Custom ML model loaded successfully!")
except Exception as e:
    model_ready = False
    print(f"Error loading custom ML model: {e}")
    print("Will attempt to use OpenAI API or fallback model.")

def clean_up_sentence(sentence):
    """
    Tokenize and lemmatize the sentence
    """
    sentence_words = word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words):
    """
    Create a bag of words array
    """
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    """
    Predict the class of the sentence using the model
    """
    # Get bag of words for the sentence
    p = bow(sentence, words)
    
    # Predict the intent
    res = model.predict(np.array([p]))[0]
    
    # Filter out predictions below a threshold
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    
    # Sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    
    return return_list

def get_response(ints, intents_json):
    """
    Get a response based on the predicted intent
    """
    if not ints:
        return "I'm not sure what you mean. Could you rephrase that?"
    
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    
    return result

# Original fallback chatbot implementation
def original_chatbot_response(message):
    """
    Fallback chatbot implementation when ML model and OpenAI API are not available
    """
    # Simple rule-based responses
    if "hello" in message.lower():
        return "Hello! How can I help you today?"
    elif "bye" in message.lower():
        return "Goodbye! Have a nice day!"
    elif "thank" in message.lower():
        return "You're welcome!"
    else:
        return "I'm a simple fallback chatbot. For more advanced responses, please ensure your model or API key is set correctly."

def get_openai_response(message):
    """
    Send a message to the OpenAI API and get a response
    """
    try:
        if not openai_api_key:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
        
        # Set up the OpenAI client
        client = openai.OpenAI(api_key=openai_api_key)
        
        # Make the API request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # You can use gpt-4 or other models if preferred
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        # Extract the response text
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        
        # Try using the custom ML model if available
        if model_ready:
            try:
                ints = predict_class(message)
                return get_response(ints, intents)
            except Exception as e2:
                print(f"Error using custom ML model: {e2}")
        
        # Fall back to the original model if both OpenAI and ML model fail
        return original_chatbot_response(message)

def get_custom_ml_response(message):
    """
    Get a response using the custom ML model
    """
    try:
        ints = predict_class(message)
        response = get_response(ints, intents)
        return response
    except Exception as e:
        print(f"Error using custom ML model: {e}")
        return get_openai_response(message)  # Try OpenAI as a fallback

@app.route("/chat")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    user_text = request.args.get('msg')
    
    # First try the custom ML model if available
    if model_ready:
        response = get_custom_ml_response(user_text)
    else:
        # If ML model is not available, try OpenAI API
        response = get_openai_response(user_text)
    
    return response

# Function to check if API key is valid
def test_api_key():
    if not openai_api_key:
        print("WARNING: OPENAI_API_KEY not set. Will use fallback model.")
        return False
        
    try:
        # Set up the OpenAI client
        client = openai.OpenAI(api_key=openai_api_key)
        
        # Make a simple test request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Hello"}
            ],
            max_tokens=5
        )
        
        print("OpenAI API connection successful!")
        return True
    except Exception as e:
        print(f"OpenAI API connection failed: {e}")
        print("Will use fallback model.")
        return False

if __name__ == "__main__":
    # Test API connection before starting server
    api_available = test_api_key()
    
    if model_ready:
        print("Using custom ML model as primary response method.")
    elif api_available:
        print("Using OpenAI API as primary response method.")
    else:
        print("Using simple fallback model as primary response method.")
    
    app.run(debug=True)
