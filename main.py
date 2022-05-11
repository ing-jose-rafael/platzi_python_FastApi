# Python
import json
from uuid import UUID
from datetime import date, datetime
from typing import List, Optional

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

# FastAPI
from fastapi import Body, FastAPI, HTTPException, Path
from fastapi import status

from schemas.user import User
from routes.user import user


app = FastAPI()

# Models

class Tweet(BaseModel):
    tweet_uid: UUID = Field(...)
    content:str = Field(
        ...,
        min_length = 1,
        max_length = 256
    )
    # fecha y hora en que se crea el tweet
    created_at:datetime = Field(default=datetime.now())
    # fecha y hora en que se actualiza el tweet, será opcional por que cuando se crea el tweet no tendrá valor
    updated_at: Optional[datetime] = Field(default=None)
    by: User = Field(...)

# Path Operations

## Users

app.include_router(user)

## Tweets

### Show all tweets
@app.get(
    path="/",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
    tags=["Tweets"]
    )
def home():
    """
    This path operation shows all tweets in the app
    
    ---
    Parameters:
    - None 
    
    Returns a json list with all tweets in the app, with the following keys:
    -  tweet_uid: UUID
    -  content:str
    -  created_at:datetime
    -  updated_at: Optional[datetime]
    -  by: User
        
    """
    with open("tweets.json","r",encoding='utf-8') as f:
        results = json.loads(f.read()) # como esto es simil a json, fastApi lo puede convertir a un json
        return results

### Post a tweet
@app.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweets"]
    )
def post_a_tweet(tweet:Tweet = Body(...)):
    """
    Post a Tweet

    This is the endpoint to create a new tweet and save it in the app.

    ---
    parameters:
    - Request Body parameter:
        - **tweet: Tweet** -> A tweet object with tweet_uid, content, create_at, update_at, by

    Return a json with the basic tweet information
    - tweet_uid: UUID 
    - content: str 
    - created_at: datetime 
    - updated_at: Optional[datetime] 
    - by: User

    """
    with open("tweets.json","r+",encoding='utf-8') as f:
        results = json.loads(f.read())
         
        # creo un diccionario apartir del request Body que envia el usuario
        tweet_dict = tweet.dict()
        
        # casting de las variables tweet_id: UUID y birth_date: datetime para convertirlas a json
        tweet_dict["tweet_uid"] = str(tweet_dict["tweet_uid"])
        tweet_dict["created_at"] = str(tweet_dict["created_at"])
        
        tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
        tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"])
        tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"])
        # agrego al json result el tweet_dict
        results.append(tweet_dict)

        # movernos al principio del archivo
        f.seek(0)
        f.write(json.dumps(results))

        return tweet

### Show a tweet
@app.get(
    path="/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweets"]
    )
def show_a_tweet():
    """
    Show a Tweet

    This is the endpoint to search a tweet in the datebase and show a tweet.

    ---
    parameters:
    - in: Request Body parameter:
        - **tweet: Tweet** -> A tweet object with tweet_uid, content, create_at, update_at, by

    Return a tweet object with tweet_uid, content, create_at, update_at, by

    """
    pass

### Delete a tweet
@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"]
    )
def show_a_tweet():
    """
    Delete a Tweet

    This is the endpoint to delete a tweet in the datebase.

    ---
    parameters:
    - in: Request Body parameter:
        - **tweet: Tweet** -> A tweet object with tweet_uid, content, create_at, update_at, by

    Return a tweet object with tweet_uid, content, create_at, update_at, by

    """
    pass

### Update a tweet
@app.put(
    path="/tweets/{tweet_id}/update",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"]
    )
def show_a_tweet():
    """
    Update a Tweet

    This is the endpoint to Update a tweet in the datebase.

    ---
    parameters:
    - in: Request Body parameter:
        - **tweet: Tweet** -> A tweet object with tweet_uid, content, create_at, update_at, by

    Return a tweet object with tweet_uid, content, create_at, update_at, by

    """
    pass
