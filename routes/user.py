# Python
import json
from uuid import uuid4 
from typing import List

# fastapi
from fastapi import APIRouter # para poder definir rutas por aparte
from fastapi import Body, Path, HTTPException
from fastapi import status

# Schemas
from schemas.user import User, UserRegister

user = APIRouter()




### create user
@user.post(
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
    with open("./data/users.json","r+",encoding='utf-8') as f:
        # leyendo el json que esta en archivo users.json
        results = json.loads(f.read()) # convierte el archivo leido a una lista de dicionario json
        
        # creo un diccionario apartir del request Body que envia el usuario
        user_dict = user.dict()

        # casting de las variables user_id: UUID y birth_date: datetime para convertirlas a json
        user_dict["user_id"] = str(uuid4())
        # user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        
        # agrego al json result el user_dict
        results.append(user_dict)

        # movernos al principio del archivo
        f.seek(0)
        f.write(json.dumps(results))
        return user

### login a user
@user.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"]
    )
def Login():
    pass

### Get all users
@user.get(
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
    with open("./data/users.json","r",encoding='utf-8') as f:
        results = json.loads(f.read()) # como esto es simil a json, fastApi lo puede convertir a un json
        return results

### Get a user
@user.get(
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
    with open("./data/users.json","r",encoding='utf-8') as f:
        results = json.loads(f.read())

    id_user=str(user_id)
        
    for user in results:
        if user["user_id"]  == id_user:
            return user
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail= "¡This user doesn't exist!"
    )
    

### Delete a user
@user.delete(
    path="/users/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a user",
    tags=["Users"],
    deprecated=True
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
    with open("./data/users.json","r+",encoding='utf-8') as f:
        results = json.loads(f.read())
    user_id=str(user_id)

    for data in results:
        if data["user_id"]  == user_id:
            results.remove(data)
            with open("./data/users.json", "w", encoding="utf-8") as z:
                z.seek(0)
                z.write(json.dumps(results))
            return data
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail= "¡This person doesn't exist!"
    )

@user.delete(
    path="/users/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a user",
    tags=["Users"],
)
def delete_user(
    idUser:str=Path(
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
    with open("./data/users.json","r+",encoding='utf-8') as f:
        data = json.loads(f.read())

        idUser=str(idUser)
        # filter_by_idUser = [user for user in data if user["user_id"]!=idUser]
        for user in data:
            if user["user_id"] == idUser:
                data.remove(user)
                # movernos al principio del archivo
                f.seek(0)
                f.write(json.dumps(data))
                f.truncate()
                return user
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail= "¡This person doesn't exist!"
        )

### Update a user
@user.put(
    path="/users/{user_id}/update",
    # response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a user",
    tags=["Users"]
    )
def update_a_user(
    user_id:str = Path(
        ...,
        min_length=1,
        title='user id',
        description="This is the person id, It's required"
    ),
    userUpdate:UserRegister = Body(...)
):
    """
    Update a User

    This path operation update if a person exist in the app

    Parameters:
        - user_id: UUID
        - user: UserRegister Request Body parameter

    Returns a json with user data:
        - user_id: UUID
        - email: Emailstr
        - password:str
        - first_name: str
        - last_name: str
        - birth_date: datetime
    """
    user_dict = userUpdate.dict() # creo un diccionario apartir del request Body que envia el usuario
    user_id = str(user_id)

    with open("./data/users.json","r+",encoding='utf-8') as f:
        data = json.loads(f.read())

        # filter_by_idUser = [user for user in data if user["user_id"]!=idUser]
        for user in data:
            if user["user_id"] == user_id:
                user["email"]       =  user_dict["email"]
                user["password"]    =  user_dict["password"]
                user["first_name"]  =  user_dict["first_name"]
                user["last_name"]   =  user_dict["last_name"]
                user["birth_date"]  =  str(user_dict["birth_date"])
                # movernos al principio del archivo
                f.seek(0)
                f.write(json.dumps(data))
                f.truncate()
                return user
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail= "¡This person doesn't exist!"
        )    
