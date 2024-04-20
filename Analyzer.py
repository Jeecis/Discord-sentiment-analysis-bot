import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch.nn.functional as F
from transformers import pipeline


class Analyzer:
    """"Class that controls the emotion and sentiment analysis for each of the ML models"""

    def __init__(self):
        """"Initializes both models (model and classifier) and tokenizer that uses NLP to tokenize the text"""
        self.tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
        self.model = DistilBertForSequenceClassification.from_pretrained(
            "distilbert-base-uncased-finetuned-sst-2-english")

        # Initialize the text classification model for emotion analysis
        self.classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)

    def sentimentanalysis(self, text):
        """"Function that calculates sentiment.
        It returns an array consisting of 3 entries [float, float, String]: 1st is the positive sentiment portion,
        2nd Negative sentiment portion and 3rd is the classification (Negative or positive) """

        # Tokenize the input text
        inputs = self.tokenizer(str(text), return_tensors="pt")

        # Perform inference using the sentiment analysis model
        with torch.no_grad():
            logits = self.model(**inputs).logits

        probs = F.softmax(logits, dim=1)

        # Extract the positive and negative probabilities
        positive_prob = probs[0, 1].item()
        negative_prob = probs[0, 0].item()

        print(f"Positive probability: {positive_prob:.4f}")
        print(f"Negative probability: {negative_prob:.4f}")

        predicted_class_id = logits.argmax().item()

        return [positive_prob, negative_prob, self.model.config.id2label[predicted_class_id]]

    def emotionanalysis(self, text):
        """"Function that calculates emotional sentiment.
        It returns an array consisting of top 5 emotion sentiments in the provided text
        (as dictionaries, {"label": String, "score": float})."""

        # Perform emotion analysis using the classifier
        model_outputs = self.classifier(str(text))
        top5 = []
        for i in range(0, 5):
            top5.append(model_outputs[0][i])
            top5[i]["score"] = float(f"{top5[i]['score']:.4f}")

        return top5

    def emotionanalysisFull(self, text):
        """"Function that calculates emotional sentiment.
        It returns an array consisting of all the emotion sentiments in the provided text
        (as dictionaries, {"label": String, "score": float})."""

        # Perform emotion analysis using the classifier
        model_outputs = self.classifier(str(text))

        return model_outputs[0]








