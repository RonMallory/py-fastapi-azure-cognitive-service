from pydantic import BaseModel


class Documents(BaseModel):
    documents: list


class SentenceAnalysis(BaseModel):
    sid: int
    text: str
    sentiment: str
    confidence_score: dict


class SentimentAnalysis(BaseModel):
    id: int
    document: str
    sentiment: str
    confidence_scores: dict
    sentences: list = None

    def add_sentences(self, sentence_analysis: SentenceAnalysis):
        if not self.sentences:
            self.sentences = []
        self.sentences.append(sentence_analysis)


class PositiveSentiment(BaseModel):
    id: int
    document: str
    sentiment: str
    confidence: dict
