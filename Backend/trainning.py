import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import json
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD
import random

# Download NLTK resources if not already done
try:
    nltk.download("punkt")
    nltk.download("wordnet")
except Exception as e:
    print(f"Error downloading NLTK data: {e}")
    exit()

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# Initialize data structures
words = []
classes = []
documents = []
ignore_words = ['?', '!']

# Load intents JSON file with error handling
try:
    with open('data.json') as data_file:
        intents = json.load(data_file)
except FileNotFoundError:
    print("Error: 'data.json' file not found.")
    exit()
except json.JSONDecodeError:
    print("Error: 'data.json' is not a valid JSON file.")
    exit()

# Process intents data
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # Tokenize each word
        w = word_tokenize(pattern)
        words.extend(w)
        # Add documents in the corpus
        documents.append((w, intent['tag']))

        # Add to our classes list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Lemmatize, lower each word, and remove duplicates
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(set(words))

# Sort classes
classes = sorted(set(classes))

# Print dataset stats
print(f"{len(documents)} documents")
print(f"{len(classes)} classes: {classes}")
print(f"{len(words)} unique lemmatized words: {words}")

# Save words and classes
with open('texts.pkl', 'wb') as file:
    pickle.dump(words, file)

with open('labels.pkl', 'wb') as file:
    pickle.dump(classes, file)

# Prepare training data
training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1 if word in word_patterns else 0)

    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append(bag + output_row)

# Shuffle training data and convert to numpy array
random.shuffle(training)
try:
    training = np.array(training)
except ValueError as e:
    print(f"Error converting training data to numpy array: {e}")
    exit()

train_x = training[:, :len(words)]
train_y = training[:, len(words):]

# Build the model
model = Sequential([
    Dense(128, input_shape=(len(train_x[0]),), activation='relu'),
    Dropout(0.5),
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(len(train_y[0]), activation='softmax')
])

# Compile the model
sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Train the model
model.fit(train_x, train_y, epochs=200, batch_size=5, verbose=1)

# Save the model
model.save('model.h5')

print("Model created successfully.")
