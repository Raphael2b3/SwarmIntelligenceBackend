from datetime import timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from Database.MongoDB import projectController
import models
import Database.Models.project
from security import Token, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, \
    get_current_active_user
from Database.Models.user import User

app = FastAPI()


@app.post("/project", response_model=Database.Models.project.Project)
async def get_project(
        current_user: Annotated[User, Depends(get_current_active_user)],
        form_data: Annotated[models.ProjectRequest, Depends()]):
    project = projectController.get_project(form_data)
    return project


@app.post("/user/create")
async def create_user(
        form_data: Annotated[models.CreateUserRequest, Depends()]):
    pass


if __name__ == '__main__':

    def liste_von_1_bis_10000000():
        liste = []
        for i in range(1, 10000000000001):
            liste.append(i)
        return liste


    def liste_von_1_bis_10000000_in_gut():
        for i in range(1, 10000000000001):
            yield i


    l = liste_von_1_bis_10000000()
    l_in_gut = liste_von_1_bis_10000000_in_gut()

    next(l_in_gut)

    print( l )