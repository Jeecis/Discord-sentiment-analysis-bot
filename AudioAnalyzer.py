import os
import pathlib
import shutil
import discord

import requests
from openai import OpenAI
from Analyzer import Analyzer


class AudioAnalyzer(Analyzer):
    """"Class that controls the audio/video processing in sentiment analysis"""

    def __init__(self, client):
        """"Initializes the OpenAI client, Analyzer class, voice call connections and discord bot client"""
        super().__init__()
        self.client = OpenAI(
            api_key=os.environ["OPENAI_API_KEY"]
        )
        self.connections = {}
        self.bot = client

    def transcript(self, attachment):
        """"Transcripts the provided audio/video file"""
        url = attachment.url
        print(url)
        audioName = attachment.filename
        try:
            # Fetch the CSV file content
            r = requests.get(url, stream=True)
        except:
            print("Invalid url from attachment")
            return None

        if not (audioName[-4:].lower() in [ ".mp3", ".mp4", ".m4a", ".ogg", ".wav"] or audioName[-5:].lower() in [".flac", ".mpeg", ".mpga",".webm"]):
            print("Invalid file type")
            return None


        with open(audioName, 'wb') as out_file:
            shutil.copyfileobj(r.raw, out_file)

        audio_file = open(audioName, "rb")
        transcription = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
        audio_file.close()
        file_to_delete = pathlib.Path(audioName)
        file_to_delete.unlink()
        print(transcription)

        return transcription

    async def startRec(self, ctx):
        """"Joins the voice call and starts recording each person"""
        voice = ctx.author.voice
        print(self.bot.guilds)


        if not voice:
            await ctx.respond("You aren't in a voice channel!")

        vc = await voice.channel.connect()  # Connect to the voice channel the author is in.
        self.connections.update({ctx.guild.id: vc})  # Updating the cache with the guild and channel.

        vc.start_recording(
            discord.sinks.MP3Sink(),  # The sink type to use.
            self.once_done,  # What to do once done.
            ctx.channel  # The channel to disconnect from.
        )

    async def once_done(self, sink: discord.sinks.WaveSink(), channel: discord.TextChannel, *args):
        """"Executes once the bot leaves the voice call and sends the recordings in the chat"""
        print(sink.audio_data.items())
        recorded_users = [f"{self.bot.get_user(user_id).name}" for user_id, audio in sink.audio_data.items()]
        await sink.vc.disconnect()  # Disconnect from the voice channel.
        files = [discord.File(audio.file, f"{self.bot.get_user(user_id).name}_{user_id}.{sink.encoding}") for
                 user_id, audio in
                 sink.audio_data.items()]  # List down the files.
        message = await channel.send(f"Audio file for: {', '.join(recorded_users)}.",
                                     files=files)  # Send a message with the accumulated files.

        # Transcribe each recorded audio file
        for i in range(len(message.attachments)):
            trnscrpt = self.transcript(message.attachments[i])
            await channel.send(f"{message.attachments[i].filename} transcript:\n"+trnscrpt)
            sentiment=self.sentimentanalysis(trnscrpt)
            emotions=self.emotionanalysis(trnscrpt)
            embed = discord.Embed(title="Sentiment", color=0x3498db)

            # Sentiment Analysis
            sentiment = (f"Sentiment: {sentiment[2]} \n"
                         f"Positiveness rating: {round(sentiment[0], 3)} \n"
                         f"Negativeness rating: {round(sentiment[1], 3)} \n")

            emotional = (f"Top 5 emotions present in your text:\n "
                         f"{emotions[0]['label']}, score - {round(emotions[0]['score'], 3)} \n"
                         f"{emotions[1]['label']}, score - {round(emotions[1]['score'], 3)} \n"
                         f"{emotions[2]['label']}, score - {round(emotions[2]['score'], 3)} \n"
                         f"{emotions[3]['label']}, score - {round(emotions[3]['score'], 3)} \n"
                         f"{emotions[4]['label']}, score - {round(emotions[4]['score'], 3)} \n")

            embed.add_field(name="Sentiment", value=sentiment, inline=True)
            embed.add_field(name="Emotions", value=emotional, inline=True)

            await channel.send(embed=embed)

    async def stopRec(self, ctx):
        """"Executes once the bot leaves the voice call and removes the connection id from connection dictionary"""
        if ctx.guild.id in self.connections:
            vc = self.connections[ctx.guild.id]
            vc.stop_recording()
            del self.connections[ctx.guild.id]
        else:
            await ctx.send("I am currently not recording here.")

