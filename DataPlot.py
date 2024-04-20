import pandas as pd
import requests
import matplotlib.pyplot as plt
import discord

class DataPlot:
    """"Class devoted specifically for analyzing CSV
    datasets that have been run through my projects sentiment analysis"""
    def __init__(self):
        """"Initializes the column constant and introduces
        Dataframes df and unchanged, which are used for an easier accessibility for """
        self.df=None
        self.unchanged=None
        self.columns=['Neutral', 'Approval', 'Annoyance', 'Admiration', 'Realization',
                     'Anger', 'Excitement', 'Disappointment', 'Disgust', 'Disapproval', 'Joy', 'Sadness', 'Amusement', 'Love', 'Fear',
                     'Confusion', 'Optimism', 'Curiosity', 'Desire', 'Surprise', 'Caring',
                     'Gratitude', 'Embarrassment', 'Grief', 'Pride', 'Relief', 'Nervousness', 'Remorse']

    async def analyzeCSV(self,ctx, attachment, percent,type):
        """"Function that specifically reads the provided csv and passes the dataset
        further for the appropriate plotting command"""

        # Retrieve the URL of the attached CSV file
        url=attachment.url

        try:
            # Fetch the CSV file content
            r = requests.get(url, stream=True)
        except:
            print("Invalid url from attachment")
            await ctx.send("Invalid url from attachment")
            return None

        # Read the CSV content into a pandas DataFrame
        try:
            self.df = pd.read_csv(r.raw)
        except:
            print("Invalid file type")
            await ctx.send("Invalid file type")
            return None

        # Select specific columns from the DataFrame based on self.columns attribute
        try:
            self.df = self.df[self.columns]
        except:
            print("Invalid file, run it through /csv first")
            await ctx.send("Invalid file, run it through /csv first")
            return None

        # Create a copy of the DataFrame for reference
        self.unchanged = self.df.copy()

        # Perform different plotting actions based on the provided type
        match type:
            case "ALL":
                # Plot pie chart, bar chart, mean plot, and scatter plot
                await self.plotPie(ctx, attachment, percent)
                await self.plotBar(ctx, attachment, percent)
                await self.plotMean(ctx, attachment)
                await self.plotScatter(ctx, attachment)
            case "BAR":
                # Plot only a bar chart
                await self.plotBar(ctx, attachment, percent)
            case "SCATTER":
                # Plot only a scatter plot
                await self.plotScatter(ctx, attachment)
            case "MEAN":
                # Plot only a mean plot
                await self.plotMean(ctx, attachment)
            case "PIE":
                # Plot only a pie chart
                await self.plotPie(ctx, attachment, percent)

        await ctx.send("Your CSV was analyzed")

    async def plotScatter(self, ctx, attachment):
        """"Function that plots the provided dataset into Scatter plot
        format and sends the resulting image straight to the discord chat"""

        x_values = []
        y_values = []

        # Extract x and y values for the scatter plot
        for emotion in self.columns:
            x_values.extend(self.unchanged[emotion])
            y_values.extend([emotion] * len(self.unchanged))

        # Plot scatter plot
        plt.figure(figsize=(10, 6))
        plt.scatter(x_values, y_values, color='skyblue', alpha=0.8)
        plt.title('Mean Percentage of Emotions')
        plt.title('Mean Percentage of Emotions')  # Duplicate title, potentially erroneous
        plt.xlabel('Percentage')
        plt.ylabel('Emotion')
        plt.grid(True)
        plt.tight_layout()

        # Save the scatter plot image
        plt.savefig('scatterplot.png')
        plt.close()

        # Prepare scatter plot image for sending via Discord
        image = discord.File("scatterplot.png")
        embed = discord.Embed(title=f"Scatterplot of {attachment.filename}")
        embed.set_image(url="attachment://scatterplot.png")

        # Send scatter plot image to Discord chat
        await ctx.send(embed=embed, file=image)

    async def plotMean(self, ctx, attachment):
        """"Function that plots the provided dataset into scatter plot
        format with calculated mean for the total entries and sends the resulting image straight to the discord chat"""

        # Calculate mean percentages for each emotion
        mean_percentages = self.unchanged[self.columns].mean()

        # Plot mean percentages as a scatter plot
        plt.figure(figsize=(10, 6))
        plt.scatter(mean_percentages, mean_percentages.index, color='skyblue', alpha=0.8)
        plt.xlabel('Percentage')
        plt.ylabel('Emotion')
        plt.grid(True)
        plt.tight_layout()

        # Save the mean scatter plot image
        plt.savefig('mean.png')
        plt.close()

        # Prepare mean scatter plot image for sending via Discord
        image = discord.File("mean.png")
        embed = discord.Embed(title=f"Mean percentage of {attachment.filename}")
        embed.set_image(url="attachment://mean.png")

        # Send mean scatter plot image to Discord chat
        await ctx.send(embed=embed, file=image)

    async def plotBar(self, ctx, attachment,percent):
        """"Function that plots the provided dataset into bar chart
        format and sends the rsulting image straight to the discord chat"""

        for col in self.columns:
            # Threshold the DataFrame based on the provided percentage
            self.df.loc[self.df[col.capitalize()] > (int(percent) / 100), col] = 1

        # Filter the DataFrame to include only columns with at least one value equal to 1
        filtered_df = self.df.loc[:, (self.df == 1).any()]

        # Count occurrences of each emotion
        emotion_counts = filtered_df.eq(1).sum()

        # Plot the emotion count as a bar chart
        plt.figure(figsize=(14, 6))
        emotion_counts.plot(kind='bar', color='skyblue')
        plt.xlabel('Emotion')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.title('Emotion counts')

        # Save the bar chart image
        plt.savefig('barchart.png')
        plt.close()

        # Prepare bar chart image for sending via Discord
        image = discord.File("barchart.png")
        embed = discord.Embed(title=f"Bar Chart of {attachment.filename}")
        embed.set_image(url="attachment://barchart.png")

        # Send bar chart image to Discord chat
        await ctx.send(embed=embed, file=image)

    async def plotPie(self, ctx, attachment, percent):
        """"Function that plots the provided dataset into pie chart
        format and sends the resulting image straight to the discord chat"""

        # Threshold the DataFrame based on the provided percentage
        for col in self.columns:
            self.df.loc[self.df[col.capitalize()] > (int(percent) / 100), col] = 1

        # Filter the DataFrame to include only columns with at least one value equal to 1
        filtered_df = self.df.loc[:, (self.df == 1).any()]

        # Count occurrences of each emotion
        emotion_counts = filtered_df.eq(1).sum()

        # Plot the emotion counts as a pie chart
        plt.figure(figsize=(10, 10))
        plt.pie(emotion_counts, labels=emotion_counts.index, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title('Emotion counts')

        # Save the pie chart image
        plt.savefig('piechart.png')
        plt.close()

        # Prepare pie chart image for sending via Discord
        image = discord.File("piechart.png")
        embed = discord.Embed(title=f"Pie Chart of {attachment.filename}")
        embed.set_image(url="attachment://piechart.png")

        # Send pie chart image to Discord chat
        await ctx.send(embed=embed, file=image)


