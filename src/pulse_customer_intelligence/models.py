from enum import Enum
from pydantic import BaseModel, Field

class Sentiment(str, Enum):
    positive = "Positive"
    neutral  = "Neutral"
    negative = "Negative"

class Triage(BaseModel):
    sentiment: Sentiment = Field(description="Positive, Neutral, or Negative")
    category: str = Field(description="One of: Product Quality, Delivery, Pricing, Support, Freshness")
    owning_department: str = Field(description="Department name and contact email, from the lookup_department tool")
    priority: str = Field(description="High, Medium, or Low")
    summary: str = Field(description="One short sentence summarising the feedback")