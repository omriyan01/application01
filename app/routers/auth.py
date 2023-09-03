from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from . import oauth2

router = APIRouter(tags=['authentication'])


@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid credentials")
    
    if not utils.verfiy(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid credentials")
    
    acess_token = oauth2.create_access_token(data= {"user_id": user.id})
    
    return {"token": acess_token, "token_type": "bearer"}