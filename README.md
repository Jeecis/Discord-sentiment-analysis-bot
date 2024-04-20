# DISCORD BOT SENTIMENT ANALYSIS
#### Video Demo:  https://youtu.be/7ZGa9OTpDH8
#### Description:

Imagine you are a businessman that needs to conduct a lot of interviews. I mean more than 100 interviews. Of course you can just simply record them and analyze the one by one. But that is a very tedious process.

That is why I created a sentiment analysis bot that can take videos, audio files, CSV files and even record and analyze your interview in REAL-TIME.
The bot displays sentiment in terms of positive or negative and additionally, provides a comprehensive look at all the emotions that are present in your text.
Here is an example of how it displays the analysis:

Sentiment: POSITIVE
Positiveness rating: 0.999
Negativeness rating: 0.001

Emotions
Top 5 emotions present in your text:
curiosity, score - 0.705
neutral, score - 0.24
desire, score - 0.072
love, score - 0.062
confusion, score - 0.031


In total this project took me around 25 hours

### Projects infastructure

main.py file contains all of the bot commands that can be called from discord

Analyzer.py is responsible for doing the sentiment analysis and emotion analysis

AudioAnalyzer.py transcripts the videos and the applies the same sentiment and emotion analysis  

DataPlot.py uses matplotlib to plot the provided csv file so it is easy to analyze

test_methods.py is a unit test file for testing some of the methods

Most importantly, a very challenging part was learning more about pythons OOP, concurrency and decorator concepts without which this whole project wouldn't be possible.

### Bot commands

Problem:
My solution:

Commands
Here is the full list of available commands
/attachments - does audio sentiment analysis (MP4, MP3 formats)
/sentiment - gives sentiment to your provided text
/record - joins voice call and starts recording every members voice
/stop - leaves voice call and sends the analyzed audio files
/csv - provides a sentiment analysis to a full column in a csv file
/plotall - plots csv data in bar chart, pie chart, scatter plot and mean scatter plot
/plotscatter - plots csv data in a scatter plot
/plotbar - plots csv data in a bar chart
/plotpie - plots csv data in a pie chart
/plotmean - plots csv data in a pie chart
BEFORE YOU USE ANY OF THE PLOT METHODS RUN THE CSV THROUGH /csv COMMAND
/plotall - plots csv data in bar chart, pie chart, scatter plot and mean scatter plot
/plotscatter - plots csv data in a scatter plot
/plotbar - plots csv data in a bar chart
/plotpie - plots csv data in a pie chart
/plotmean - plots csv data in a pie chart


### How to test it
Since hosting a discord bot with gpt integration isn't cheap the steps will be more complicated.

Download this projects file and open it in your favourite IDE (Pycharm or Vscode)

You will have to set your own API keys in environmental variables, but I will just provide the API key names mentioned in my program and to which API they are related:

For OpenAI API - OPENAI_API_KEY

For Discord bot API - DISCORD_API_KEY (for this you will have to create your own discord bot)


After setting the API keys you should be set and just run the program ;)
