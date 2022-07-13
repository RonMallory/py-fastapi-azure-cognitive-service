from typing import Union
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from models import SentimentAnalysis, SentenceAnalysis, Documents
from helpers import text_analytics_client


app = FastAPI()


async def analyze_sentiment(data):

    client = text_analytics_client()
    documents = data["documents"]
    async with client:
        result = await client.analyze_sentiment(documents)

    docs = [doc for doc in result if not doc.is_error]
    document_list = []
    for idx, doc in enumerate(docs):
        document = SentimentAnalysis(
            id=idx,
            document=documents[idx],
            sentiment=doc.sentiment,
            confidence_scores=doc.confidence_scores,
        )
        sentence_count = 0
        for sentence in doc.sentences:
            sentence_obj = SentenceAnalysis(
                sid=sentence_count,
                text=(sentence.text).strip(),
                sentiment=sentence.sentiment,
                confidence_score=sentence.confidence_scores,
            )
            sentence_count += 1

            document.add_sentences(sentence_analysis=sentence_obj)
        document_list.append(document)
    return document_list


async def filter_analyze_sentiment(data, filter: str):

    client = text_analytics_client()
    documents = data["documents"]
    async with client:
        result = await client.analyze_sentiment(documents)

    docs = [doc for doc in result if not doc.is_error]
    filtered_docs = [doc for doc in docs if doc.sentiment == filter]

    if filter == "positive":
        scored_docs = [
            sentiment
            for sentiment in filtered_docs
            if sentiment.confidence_scores.positive >= 0.9
        ]
    if filter == "neutral":
        scored_docs = [
            sentiment
            for sentiment in filtered_docs
            if sentiment.confidence_scores.neutral >= 0.9
        ]
    if filter == "negative":
        scored_docs = [
            sentiment
            for sentiment in filtered_docs
            if sentiment.confidence_scores.negative >= 0.9
        ]
    document_list = []
    for idx, doc in enumerate(scored_docs):
        document = SentimentAnalysis(
            id=idx,
            document=documents[idx],
            sentiment=doc.sentiment,
            confidence_scores=doc.confidence_scores,
        )
        sentence_count = 0
        for sentence in doc.sentences:
            sentence_obj = SentenceAnalysis(
                sid=sentence_count,
                text=(sentence.text).strip(),
                sentiment=sentence.sentiment,
                confidence_score=sentence.confidence_scores,
            )
            sentence_count += 1

            document.add_sentences(sentence_analysis=sentence_obj)
        document_list.append(document)
    return document_list


@app.post("/sentiment/", response_model=list[SentimentAnalysis])
async def text_sentiment(text: Documents):
    json_encode = jsonable_encoder(text)
    response = await analyze_sentiment(json_encode)
    return response


@app.post("/sentiment/positive", response_model=list[SentimentAnalysis])
async def sort_positive_sentiment(text: Documents):
    json_encode = jsonable_encoder(text)
    response = await filter_analyze_sentiment(
        data=json_encode, filter="positive"
    )
    return response


@app.post("/sentiment/neutral", response_model=list[SentimentAnalysis])
async def sort_neutral_sentiment(text: Documents):
    json_encode = jsonable_encoder(text)
    response = await filter_analyze_sentiment(
        data=json_encode, filter="neutral"
    )
    return response


@app.post("/sentiment/negative", response_model=list[SentimentAnalysis])
async def sort_negative_sentiment(text: Documents):
    json_encode = jsonable_encoder(text)
    response = await filter_analyze_sentiment(
        data=json_encode, filter="negative"
    )
    return response
