from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
import random
import json
import pickle
from keras.models import load_model
import os

# Download NLTK data (if not already downloaded)
nltk.download('punkt')
nltk.download('wordnet')

# Initialize FastAPI app
app = FastAPI()

# Load the trained model and data
model = load_model('chatbot_model.h5')
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
intents = json.loads(open('intents.json', encoding="utf8").read())

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Define a Pydantic model for request body
class ChatRequest(BaseModel):
    message: str

# Preprocess the input message
def preprocess_message(message):
    # Tokenize and lemmatize the message
    tokenized_message = nltk.word_tokenize(message)
    tokenized_message = [lemmatizer.lemmatize(word.lower()) for word in tokenized_message]

    # Create a bag of words
    bag = [0] * len(words)
    for word in tokenized_message:
        if word in words:
            bag[words.index(word)] = 1

    return np.array(bag)

# Predict the intent of the message
def predict_intent(message):
    bag = preprocess_message(message)
    prediction = model.predict(np.array([bag]))[0]
    threshold = 0.25  # Adjust this threshold as needed
    results = [[i, r] for i, r in enumerate(prediction) if r > threshold]

    # Sort by probability
    results.sort(key=lambda x: x[1], reverse=True)
    intent_list = []
    for r in results:
        intent_list.append({"intent": classes[r[0]], "probability": str(r[1])})

    return intent_list

# Get a response for the predicted intent
def get_response(intent_list):
    tag = intent_list[0]['intent']
    for intent in intents['intents']:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])
    return "I'm sorry, I don't understand that."

# Define the API endpoint
@app.post("/chat")
async def chat(request: ChatRequest):
    message = request.message
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # Predict intent and get response
    intent_list = predict_intent(message)
    response = get_response(intent_list)

    return {"response": response}

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)