from pydantic import BaseModel


# To be deprecated with auth_router's authenticate() function
class Credentials(BaseModel):
    username: str
    password: str
