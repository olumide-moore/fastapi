from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body

from pydantic import BaseModel #pydantic is a library that allows us to create classes that are used to define the data that we receive in our API#

from random import randrange
app = FastAPI() # Create an instance of the FastAPI class
#run unicorn main:app --reload to run the server
test_posts= [{"title":"First Post", "content":"This is the content of the first post", "published":True, "rating":4, "id":1},
             {"title":"Second Post", "content":"This is the content of the second post", "published":True, "rating":5, "id":2}]


class Post(BaseModel): #using pydantic to validate the data that we receive
    title: str 
    content: str
    published: bool = True #default value if not provided
    rating: Optional[int] = None #optional field


@app.get("/") #route decorator
def read_root():
    return {"Hello": "Hey there!"}
@app.get("/posts")
def get_posts():
    return {"data": test_posts}

def find_post(id):
    for post in test_posts:
        if post["id"]==id:
            return post
    return None
@app.get("/posts/{id}")
def get_post(id: int):
    
    return {"post": find_post(id)}

@app.post("/posts")
def create_post(mydata: Post):
    # print(mydata.title)
    mydata_dict=mydata.model_dump() #returns a dictionary of the data
    mydata_dict["id"]=randrange(0,1000000)
    test_posts.append(mydata_dict)
    return (mydata_dict)

#Note: Finding a route in fastapi follows methods order
#The first route that matches the request will be the one that is executed
