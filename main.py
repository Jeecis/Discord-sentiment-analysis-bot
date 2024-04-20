import os
import discord
from discord.ext import commands
from Analyzer import Analyzer
from AudioAnalyzer import AudioAnalyzer
from DataPlot import DataPlot
from DatasetAnalyzer import DatasetAnalyzer

BOT_TOKEN = os.environ["DISCORD_API_KEY"]

bot=discord.Bot(intents=discord.Intents.all())
analyze=Analyzer()
audio=AudioAnalyzer(bot)
datasets=DatasetAnalyzer()
plotter=DataPlot()


@bot.command(description="Provide an MP4 or MP3 file to get a sentiment analysis")
async def attachments(ctx: commands.Context, attachment: discord.Attachment):
    """"Discord command that, needs to be provided with an MP4 or MP3 file and this function will
    transcript the audio and send the sentiment of the text in Discord"""
    await ctx.respond("Resluts:")
    strg= audio.transcript(attachment)
    if strg is None:
        await ctx.send("Invalid file or file url")
        return None
    sentiment=analyze.sentimentanalysis(strg)
    emotions = analyze.emotionanalysis(strg)
    embed1 = discord.Embed(title="Text", color=0x3498db)
    embed1.add_field(name="", value=strg, inline=True)

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

    await ctx.send(embed=embed)

@bot.command(description="Gives emotional and optimism sentiment analysis")
async def sentiment(ctx: commands.Context, text):
    """"Discord command, that needs to be provided with
     a text and this function will send the sentiment of the text in Discord"""
    await ctx.respond("Resluts:")
    sentiment=analyze.sentimentanalysis(text)
    emotions=analyze.emotionanalysis(text)
    print(sentiment)
    print(emotions)
    await ctx.send(text)

    embed = discord.Embed(title="Sentiment", color=0x3498db)

    # Sentiment Analysis
    sentiment = (f"Sentiment: {sentiment[2]} \n"
        f"Positiveness rating: {round(sentiment[0],3)} \n"
            f"Negativeness rating: {round(sentiment[1],3)} \n")

    emotional = (f"Top 5 emotions present in your text:\n "
                 f"{emotions[0]['label']}, score - {round(emotions[0]['score'],3)} \n"
                 f"{emotions[1]['label']}, score - {round(emotions[1]['score'],3)} \n"
                 f"{emotions[2]['label']}, score - {round(emotions[2]['score'],3)} \n"
                 f"{emotions[3]['label']}, score - {round(emotions[3]['score'],3)} \n"
                 f"{emotions[4]['label']}, score - {round(emotions[4]['score'],3)} \n")

    embed.add_field(name="Sentiment", value=sentiment, inline=True)
    embed.add_field(name="Emotions", value=emotional, inline=True)

    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    """"Indicates when the bot is ready to work"""
    print("Is ready!")


@bot.command(description="Joins the bot in the voice call and records audio")
async def record(ctx):
    """"Discord command, that makes the bot join Voice call and record each members speech"""
    await audio.startRec(ctx)
    await ctx.respond("Started recording!")

@bot.command(description="Makes the bot leave the voice call and send recordings")
async def stop(ctx):
    """"Discord command, that makes the bot leave the
    voice call and send the recording in the chat, with a sentiment analysis"""
    await audio.stopRec(ctx)
    await ctx.respond("Finished recording!")

@bot.command(description="Add csv file and a column name containing the texts you want to get analyzed")
async def csv(ctx, column, attachment: discord.Attachment):
    """"Discord command, that returns an analyzed csv file when provided with a new csv file"""
    await ctx.respond("Resluts:")
    await datasets.sentimentDataset(ctx,attachment,column)


@bot.command(description="Add analyzed csv file from /csv method, add the minimal percent amount for feature to be considered")
async def plotall(ctx, percent, attachment: discord.Attachment):
    """"Plot the analyzed csv file from /csv method, the sentiment
    coefficient will be plotted in Scatter plot, bar chart, pie chart and mean scatter plot"""
    await plotter.analyzeCSV(ctx,attachment,percent,"ALL")
    await ctx.send("Your CSV was analyzed")

@bot.command(description="Add analyzed csv file from /csv method, add the minimal percent amount for feature to be considered")
async def plotscatter(ctx, attachment: discord.Attachment):
    """"Plot the analyzed csv file from /csv method, the sentiment
    coefficient will be plotted in Scatter plot"""
    await plotter.analyzeCSV(ctx,attachment,0, "SCATTER")

@bot.command(description="Add analyzed csv file from /csv method, add the minimal percent amount for feature to be considered")
async def plotbar(ctx, percent, attachment: discord.Attachment):
    """"Plot the analyzed csv file from /csv method, the sentiment
    coefficient will be plotted in bar chart"""
    await plotter.analyzeCSV(ctx,attachment,percent,"BAR")
    await ctx.send("Your CSV was analyzed")

@bot.command(description="Add analyzed csv file from /csv method, add the minimal percent amount for feature to be considered")
async def plotpie(ctx, percent, attachment: discord.Attachment):
    """"Plot the analyzed csv file from /csv method, the sentiment
    coefficient will be plotted in pie chart"""
    await plotter.analyzeCSV(ctx,attachment,percent,"PIE")
    await ctx.send("Your CSV was analyzed")

@bot.command(description="Add analyzed csv file from /csv method, add the minimal percent amount for feature to be considered")
async def plotmean(ctx, attachment: discord.Attachment):
    """"Plot the analyzed csv file from /csv method, the sentiment
    coefficient will be plotted in a mean scatter plot"""
    await plotter.analyzeCSV(ctx,attachment,0,"MEAN")
    await ctx.send("Your CSV was analyzed")

@bot.command(description="Shows the information about all the available commands")
async def info(ctx):
    """Discord command that Shows the information about all the available commands"""

    # Discord Embed
    embed = discord.Embed(title="Info", color=0x3498db)

    # Sentiment Analysis
    info = ("Here is the full list of available commands\n "
            "/attachments - does audio sentiment analysis (MP4, MP3 formats)\n"
            "/sentiment - gives sentiment to your provided text\n"
            "/record - joins voice call and starts recording every members voice\n"
            "/stop - leaves voice call and sends the analyzed audio files\n"
            "/csv - provides a sentiment analysis to a full column in a csv file\n"
            "/plotall - plots csv data in bar chart, pie chart, scatter plot and mean scatter plot\n"
            "/plotscatter - plots csv data in a scatter plot\n"
            "/plotbar - plots csv data in a bar chart\n"
            "/plotpie - plots csv data in a pie chart\n"
            "/plotmean - plots csv data in a pie chart\n")

    info2 = (
            "/plotall - plots csv data in bar chart, pie chart, scatter plot and mean scatter plot\n"
            "/plotscatter - plots csv data in a scatter plot\n"
            "/plotbar - plots csv data in a bar chart\n"
            "/plotpie - plots csv data in a pie chart\n"
            "/plotmean - plots csv data in a pie chart\n")

    embed.add_field(name="Commands", value=info, inline=True)
    embed.add_field(name="BEFORE YOU USE ANY OF THE PLOT METHODS RUN THE CSV THROUGH /csv COMMAND", value=info2, inline=True)

    # Display Embed
    print(bot.commands)
    await ctx.send(embed=embed)

def main():
    bot.run(BOT_TOKEN)

if __name__ == "__main__":
    main()




