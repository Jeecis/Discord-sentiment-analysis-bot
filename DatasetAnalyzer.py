import io
import requests
import pandas as pd
import discord

from Analyzer import Analyzer


class DatasetAnalyzer(Analyzer):
    """"Class that controls the audio/video processing in sentiment analysis"""

    def __init__(self):
        super().__init__()
        self.df = None

    async def sentimentDataset(self, ctx, attachment, column):
        """"Calculates sentiment for each of the dataset entries in the specified column.
        Sends a csv file containing sentiment and emotion analysis. Each emotion gets a devoted column"""
        res=self.manageCSV(attachment,column)
        if res==-1:
            await ctx.send("Invalid url from attachment")
        elif res==-2:
            await ctx.send("Invalid file type")
        elif res==-3:
            await ctx.send("Invalid column name")

        sentiments=res[0]
        emotions=res[1]
        self.df=res[2]


        for entry in self.df[column]:
            sentiment = self.sentimentanalysis(str(entry))[2]
            emotions_result = self.emotionanalysisFull(str(entry))

            sentiments.append(sentiment)
            for emon in emotions_result:
                emotions[emon["label"]].append(emon["score"])

        # Add sentiment and emotion columns to the DataFrame
        print(sentiments)
        print(len(self.df))
        self.df['Sentiment'] = sentiments
        for emotion in emotions:
            self.df[emotion.capitalize()] = emotions[emotion]

        # Convert DataFrame to CSV format
        csv_string = self.df.to_csv(index=False)
        csv_bytes = io.BytesIO(csv_string.encode())

        # Create a Discord file and send it
        csv_file = discord.File(csv_bytes, filename=attachment.filename)
        await ctx.send("Here is your csv file")
        await ctx.send(file=csv_file)


    def manageCSV(self, attachment, column):
        """"Manages proper CSV file modifications"""
        url = attachment.url
        try:
            # Fetch the CSV file content
            r = requests.get(url, stream=True)
        except:
            print("Invalid url from attachment")
            return -1

        # Read the CSV file
        try:
            self.df = pd.read_csv(r.raw)
        except:
            print("Invalid file type")
            return -2

        sentiments = []
        emotions = {emotion: [] for emotion in
                    ['neutral', 'approval', 'annoyance', 'admiration', 'realization',
                     'anger', 'excitement', 'disappointment', 'disgust', 'disapproval', 'joy', 'sadness', 'amusement',
                     'love', 'fear',
                     'confusion', 'optimism', 'curiosity', 'desire', 'surprise', 'caring',
                     'gratitude', 'embarrassment', 'grief', 'pride', 'relief', 'nervousness', 'remorse']}

        # Calculate sentiment and emotion analysis for each entry in the specified column
        try:
            col=self.df[column]
        except:
            print("Invalid column name")
            return -3

        return [sentiments, emotions, self.df]
