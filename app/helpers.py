from os import getenv


def text_analytics_client():
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics.aio import TextAnalyticsClient

    key = getenv("SUBSCRIPTION_KEY")
    endpoint = getenv("ENDPOINT")
    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    return text_analytics_client


def valid_sentiment(sentiment: str):
    valid = ("positive", "neutral", "negative")
    if sentiment in valid:
        return sentiment
