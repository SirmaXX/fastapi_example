

from pydantic import BaseModel
class User(BaseModel):
    username: str
    email: str = None
    group: str = None

class UserInDB(User):
    hashed_password: str

fake_users_db = {
    "johndoe": {
        "id": 891,
        "username": "johndoe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "group": "group1",
        "visitcount": 0
    },
    "alice": {
        "id": 451,
        "username": "alice",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "group": "group2",
        "visitcount": 0
    },
    "charlie": {
        "id": 233,
        "username": "charlie",
        "email": "charlie@example.com",
        "hashed_password": "fakehashedsecret3",
        "group": "group1",
        "visitcount": 0
    }
}
