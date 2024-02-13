
import fastapi
import redis
from fastapi import Depends, FastAPI, HTTPException, status,Request,Query
from typing import Optional
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from Lib.models import UserInDB,fake_users_db,User
import time


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(db, username: str):
    user_dict = db.get(username)
    if user_dict:
        return UserInDB(**user_dict)  
    
    
    
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = get_user(fake_users_db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user:
       return current_user
    else:
         raise HTTPException(status_code=400, detail="Inactive user")




myHostname = "demorediss.redis.cache.windows.net"
myPassword = "Lss3FXIzW6h1D5P6TqljrI8KRja3yGNtYAzCaHVMZrI="

# Connect to Redis
r = redis.StrictRedis(host=myHostname, port=6380, password=myPassword, ssl=True)


limiter = Limiter(key_func=get_remote_address )
app = fastapi.FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)





@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = user_dict.get("hashed_password")
    if not hashed_password == form_data.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}



@app.get("/users/me", description="kullanıcıyı gösterir")
@limiter.limit("5/minute")
async def read_users_me(request: fastapi.Request,current_user: User = Depends(get_current_active_user), stream: Optional[bool] = Query(False)):   
    if current_user.visitcount > 10:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    
    if stream:
        stream_responses = []
        for i in range(5):
            response_data ={ "welcome to ": current_user.username + " group " + current_user.group + " saddsa " + str(current_user.visitcount)   }
            stream_responses.append(response_data.copy())
            time.sleep(1)  # Delay by 1 second
        return stream_responses
    else:
      return {"welcome to ": current_user.username + " group " + current_user.group + " saddsa " + str(current_user.visitcount) } 
     
    
    
    
@app.get("/", description="redis için test fonksiyonu")
async def index():
    return {
        "info": "/docs endpointi ile swagger arayüzüne ulaşabilirsiniz.",
    }



@app.get("/v1/redis_test" , description="redis için test fonksiyonu")
async def redis_get():
    try:
        # Set a key-value pair
        r.set("my_key", "my_value")

        # Get the value associated with a key
        value = r.get("my_key")
        return {"message": f"Value retrieved from Redis: {value}"}
    except redis.RedisError as e:
        return {"error": f"Error connecting to Redis: {e}"}



@app.get("/v1/ratelimit_test", description="rate için test fonksiyonu (dakikada 1 request)")
@limiter.limit("1/minute")
async def rate_limit(request: fastapi.Request):
    return {"message": "Not rate limited"}