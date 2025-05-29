import numpy as np
import tensorflow as tf
from transformers import (
    DistilBertTokenizer,
    TFDistilBertModel,
    AdamWeightDecay
)

# Load tokenizer
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")

# Load the model
model_path = "C:/Users/USER/Desktop/jarvis/models/text_sentiment_model.h5"
sentiment_model = tf.keras.models.load_model(
    model_path,
    custom_objects={
        'TFDistilBertModel': TFDistilBertModel,
        'AdamWeightDecay': AdamWeightDecay
    }
)

# Define sentiment labels
sentiment_labels = ["negative", "neutral", "positive"]

def predict_sentiment(text):
    tokens = tokenizer([text], max_length=128, padding='max_length', truncation=True, return_tensors="tf")
    prediction = sentiment_model.predict({
        'input_ids': tokens['input_ids'],
        'attention_mask': tokens['attention_mask']
    })
    sentiment_class = np.argmax(prediction, axis=1)[0]
    return sentiment_labels[sentiment_class]
