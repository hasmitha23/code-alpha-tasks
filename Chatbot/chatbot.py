import random
import spacy
import string
import numpy as np
import tkinter as tk
from tkinter import scrolledtext
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Sample conversational dataset
responses = {
    "greetings": ["Hello! How can I assist you today?", "Hi there! What's on your mind?", "Hey! How’s your day going?"],
    "how_are_you": ["I'm just a bot, but I'm feeling great! How about you?", "I'm doing well! How’s your day?"],
    "name": ["I'm ChatBot, your friendly assistant!", "You can call me ChatBot. What's your name?"],
    "goodbye": ["Goodbye! Have a great day!", "See you later! Take care!", "Bye! Come back anytime!"],
    "jokes": ["Why don’t scientists trust atoms? Because they make up everything!", "What do you call fake spaghetti? An impasta!"],
    "fallback": ["That's interesting! Tell me more.", "I see! Can you explain a bit further?", "Hmmm, let's talk more about that."]
}

# Sample training data for matching
corpus = [
    "hi", "hello", "hey",
    "how are you", "how's it going", "how are you doing",
    "what is your name", "who are you", "what should I call you",
    "bye", "goodbye", "see you later",
    "tell me a joke", "say something funny",
]
labels = ["greetings", "greetings", "greetings",
          "how_are_you", "how_are_you", "how_are_you",
          "name", "name", "name",
          "goodbye", "goodbye", "goodbye",
          "jokes", "jokes"]

# Vectorization
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus)

def preprocess_input(user_input):
    doc = nlp(user_input)
    return " ".join([token.lemma_ for token in doc if token.text not in string.punctuation])

def get_response(user_input):
    processed_input = preprocess_input(user_input)
    user_vector = vectorizer.transform([processed_input])
    similarities = cosine_similarity(user_vector, X)
    best_match = np.argmax(similarities)
    if similarities[0][best_match] > 0.2:
        category = labels[best_match]
        return random.choice(responses[category])
    else:
        return random.choice(responses["fallback"])

def send_message():
    user_input = entry.get()
    if user_input.strip():
        chat_window.insert(tk.END, "You: " + user_input + "\n", "user")
        response = get_response(user_input)
        chat_window.insert(tk.END, "Chatbot: " + response + "\n", "bot")
        entry.delete(0, tk.END)
    if user_input.lower() == "bye":
        root.quit()

# GUI Setup
root = tk.Tk()
root.title("Chatbot")
root.geometry("400x550")
root.configure(bg="#2C3E50")

header = tk.Label(root, text="Chat with Me!", font=("Arial", 14, "bold"), bg="#1ABC9C", fg="white", pady=10)
header.pack(fill=tk.X)

chat_window = scrolledtext.ScrolledText(root, height=20, width=50, bg="#ECF0F1", fg="#2C3E50", font=("Arial", 12))
chat_window.pack(pady=10, padx=10)
chat_window.tag_config("user", foreground="#007BFF")  # Brighter blue for visibility
chat_window.tag_config("bot", foreground="#28A745")   # Brighter green for chatbot

entry = tk.Entry(root, width=40, font=("Arial", 12))
entry.pack(pady=5, padx=10, fill=tk.X)

send_button = tk.Button(root, text="Send", command=send_message, font=("Arial", 12, "bold"), bg="#1ABC9C", fg="white")  # Changed button color to orange for visibility
send_button.pack(pady=5)

root.mainloop()
