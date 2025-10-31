import pickle
import uvicorn

from fastapi import FastAPI
from typing import Dict, Any, Literal, Optional
from pydantic import BaseModel, Field, ConfigDict

# Referred to ChatGPT to structure the class. Commented out features not relevant to the assignment.
class Client(BaseModel):
    lead_source: Literal[
        "paid_ads",
        "social_media",
        "events",
        "referral",
        "organic_search",
        "NA"
    ]

    # industry: Literal[
    #     "retail",
    #     "healthcare",
    #     "education",
    #     "manufacturing",
    #     "technology",
    #     "finance",
    #     "other",
    #     "NA"
    # ]

    # employment_status: Literal[
    #     "unemployed",
    #     "employed",
    #     "self_employed",
    #     "student",
    #     "NA"
    # ]

    # location: Literal[
    #     "south_america",
    #     "australia",
    #     "europe",
    #     "africa",
    #     "middle_east",
    #     "north_america",
    #     "asia",
    #     "NA"
    # ]

    number_of_courses_viewed: int = Field(..., ge=0)
    annual_income: float = Field(..., ge=0.0)
    # interaction_count: int = Field(..., ge=0)
    # lead_score: float = Field(..., ge=0.0, le=1.0)


class PredictResponse(BaseModel):
    convert_probability: float
    converted: bool


# Response
app = FastAPI(title="client-conversion-prediction")


with open('pipeline_v2.bin', 'rb') as f_in:
    pipeline = pickle.load(f_in)


def predict_single(client):
    result = pipeline.predict_proba(client)[0, 1]
    return float(result)


@app.post("/predict")
def predict(client: Client) -> PredictResponse:
    prob = predict_single(client.model_dump())

    return PredictResponse(
        convert_probability=prob,
        converted=prob >= 0.5
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9696)