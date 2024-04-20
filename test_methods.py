import time

from Analyzer import Analyzer
from DatasetAnalyzer import DatasetAnalyzer
from AudioAnalyzer import AudioAnalyzer
import pytest

pytest_plugins = ('pytest_asyncio',)


#PYTEST
def test_sentiment_analysis_positive():
    sentiment_analyzer=Analyzer()
    text = "I love this product! It's amazing!"
    result = sentiment_analyzer.sentimentanalysis(text)
    assert result[0] > result[1]
    assert result[2] == "POSITIVE"

def test_sentiment_analysis_negative():
    sentiment_analyzer = Analyzer()
    text = "This product is terrible. I hate it."
    result = sentiment_analyzer.sentimentanalysis(text)
    assert result[0] < result[1]
    assert result[2] == "NEGATIVE"


def test_emotion_analysis():
    emotion_analyzer = Analyzer()
    text = "I am feeling happy and excited today!"
    result = emotion_analyzer.emotionanalysis(text)

    assert isinstance(result, list)
    assert len(result) == 5

    for emotion in result:
        assert isinstance(emotion, dict)
        assert 'label' in emotion
        assert 'score' in emotion
        assert isinstance(emotion['label'], str)
        assert isinstance(emotion['score'], float)

    scores = [emotion['score'] for emotion in result]
    assert scores == sorted(scores, reverse=True)


class Attachment:
    def __init__(self, url, filename):
        self.url = url
        self.filename = filename

## Performance test
@pytest.mark.asyncio
async def test_manageCSV_performance():

    attachment=Attachment("https://cdn.discordapp.com/attachments/1223008492953272330/1225577355712397392/testing.csv?ex=6621a2db&is=660f2ddb&hm=935826c80adaebc36bb9f9731990d0156411657d0e214c440b6302e8ce76dd62&",
                         "testing.csv")

    analyzer=DatasetAnalyzer()

    start_time = time.time()
    analyzer.manageCSV(attachment,column="text")
    end_time = time.time()

    elapsed_time = end_time - start_time

    print(f"Manage csv performence: elapsed time {elapsed_time:.2f} seconds")
    assert elapsed_time < 30, "Function takes too long to load"

#Integration test
@pytest.mark.asyncio
async def test_trancript_sentiment_intgr():

    attachment=Attachment("https://cdn.discordapp.com/attachments/1223008492953272330/1225563548105703504/bigbicepbigga_771786002153996309.mp3?ex=662195ff&is=660f20ff&hm=6d69a614852d09b403148ca43a8568309678d37f40334892757e3f3bcdc49c90&",
                         "bigbicepbigga_771786002153996309.mp3")

    analyzer=AudioAnalyzer(None)
    strg=analyzer.transcript(attachment)
    result = Analyzer().sentimentanalysis(strg)
    assert result[0] > result[1]
    assert result[2] == "POSITIVE"

@pytest.mark.asyncio
async def test_trancript_emotion_intgr():

    attachment=Attachment("https://cdn.discordapp.com/attachments/1223008492953272330/1225563548105703504/bigbicepbigga_771786002153996309.mp3?ex=662195ff&is=660f20ff&hm=6d69a614852d09b403148ca43a8568309678d37f40334892757e3f3bcdc49c90&",
                         "bigbicepbigga_771786002153996309.mp3")

    analyzer=AudioAnalyzer(None)
    strg=analyzer.transcript(attachment)
    result = Analyzer().emotionanalysis(strg)
    assert result[0]["label"] == "gratitude"
    assert result[0]["score"] >0.9