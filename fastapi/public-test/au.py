from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
import requests

app = FastAPI()

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://github.com/login/oauth/authorize",
    tokenUrl="https://github.com/login/oauth/access_token",
)

# GitHub OAuth2 配置
CLIENT_ID = "e709aff2635aeb82880b"
CLIENT_SECRET = "350ecd77f22ef351ef4109217fa82e06bdc6ab3d"

async def get_github_token(authorization_code: str):
    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': authorization_code,
    }
    headers = {'Accept': 'application/json'}
    response = requests.post("https://github.com/login/oauth/access_token", data=payload, headers=headers)
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail='GitHub authentication error'
        )
    token_payload = response.json()
    return token_payload['access_token']

@app.get("/login")
async def login(authorization_code: str = Depends(oauth2_scheme)):
    access_token = await get_github_token(authorization_code)
    # 在这里，你可以生成一个会话标识符（比如 JWT）并返回
    return {"access_token": access_token}
