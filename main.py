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

app = FastAPI()

# Models
class UsersBase(BaseModel):
    """ Informacion basica del usuario cuando esta por registrarse"""
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)
    
class UserLogin(UsersBase):
    password:str = Field(...,min_length=8,max_length=64)

class User(UsersBase):
    first_name: str = Field(...,min_length=1,max_length=50)
    last_name: str = Field(...,min_length=1,max_length=50)
    birth_date: Optional[date] = Field(default=None)

class UserRegister(User, UserLogin):
    pass

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

### create user
@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Regiter a User",
    tags=["Users"]
    )
def signup(user:UserRegister = Body(...)):
    """
    Signup

    This is path operation register a user in the app.

    ---
    parameters:
    - in: Request Body parameter:
        - **user: UserRegister** -> A UserRegister object with user_id, email, first_name, last_name, birth_date, password

    - Return a json with the basci user information:
        - user_id: UUID
        - email: str
        - first_name: str
        - last_name: str
        - birth_date: datetime
    """
    with open("users.json","r+",encoding='utf-8') as f:
        # leyendo el json que esta en archivo users.json
        results = json.loads(f.read()) # convierte el archivo leido a una lista de dicionario json
        
        # creo un diccionario apartir del request Body que envia el usuario
        user_dict = user.dict()
        
        # casting de las variables user_id: UUID y birth_date: datetime para convertirlas a json
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        
        # agrego al json result el user_dict
        results.append(user_dict)

        # movernos al principio del archivo
        f.seek(0)
        f.write(json.dumps(results))
        return user


### login a user
@app.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"]
    )
def Login():
    pass

### Get all users
@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"]
    )
def show_all_users():
    """
    This path operation shows all users in the app
    
    ---
    Parameters:
    - None 
    
    Returns a json list with all users in the app, with the following keys:
    - user_id: UUID
    - email: str
    - first_name: str
    - last_name: str
    - birth_date: datetime
        
    """
    with open("users.json","r",encoding='utf-8') as f:
        results = json.loads(f.read()) # como esto es simil a json, fastApi lo puede convertir a un json
        return results

### Get a user
@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a user",
    tags=["Users"]
    )
def show_a_user(
    user_id:str = Path(
        ...,
        min_length=1,
        title='user id',
        description="This is the person id, It's required"
    )
):
    """
    Show a User

    This path operation show if a person exist in the app

    Parameters:
        - user_id: UUID

    Returns a json with user data:
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: datetime
    """
    with open("users.json","r",encoding='utf-8') as f:
        results = json.loads(f.read())

    id=str(user_id)
        
    for data in results:
        if data["user_id"]  == id:
            return data
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail= "¡This person doesn't exist!"
        )
    

### Delete a user
@app.delete(
    path="/users/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a user",
    tags=["Users"]
    )
def delete_a_user(
    user_id:str = Path(
        ...,
        min_length=1,
        title='user id',
        description="This is the person id, It's required"
    )
):
    """
    Delete a User

    This path operation delete if a person exist in the app

    Parameters:
        - user_id: UUID

    Returns a json with user data:
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: datetime
    """
    with open("users.json","r+",encoding='utf-8') as f:
        results = json.loads(f.read())
    user_id=str(user_id)

    for data in results:
        if data["user_id"]  == user_id:
            results.remove(data)
            with open("users.json", "w", encoding="utf-8") as z:
                z.seek(0)
                z.write(json.dumps(results))
            return data
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail= "¡This person doesn't exist!"
        )
   

### Update a user
@app.put(
    path="/users/{user_id}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a user",
    tags=["Users"]
    )
def update_a_user():
    pass

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
