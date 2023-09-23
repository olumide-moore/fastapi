from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body

from pydantic import BaseModel #pydantic is a library that allows us to create classes that are used to define the data that we receive in our API#

from random import randrange
import psycopg2
from time import sleep
app = FastAPI() # Create an instance of the FastAPI class
#run uvicorn app.main:app --reload to run the server
test_posts= [{"title":"First Post", "content":"This is the content of the first post", "published":True, "rating":4, "id":1},
             {"title":"Second Post", "content":"This is the content of the second post", "published":True, "rating":5, "id":2}]

while True:
    try: 
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Aston2021')
        cursor=conn.cursor()
        print("Connected to the database")
        break
    except Exception as e:
        print("Error connecting to the database")
        print(e)
        sleep(3)
    
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

@app.get("/posts/latest") 
def get_latest_post():
    return {"post": test_posts[-1]} #returns the last element in the list

def find_post_index(id):
    for i in range(len(test_posts)):
        if test_posts[i]["id"]==id:
            return i
    return None
@app.get("/posts/{id}") #note: /latest route is similar to this but it is executed first, so this runs if the parameter is not latest
def get_post(id: int, response: Response):
    index=find_post_index(id)
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} not found")
    return {"post": test_posts[index]}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(mydata: Post):
    # print(mydata.title)
    mydata_dict=mydata.model_dump() #returns a dictionary of the data
    mydata_dict["id"]=randrange(0,1000000)
    test_posts.append(mydata_dict)
    return mydata_dict

@app.put("/posts/{id}")
def update_post(id: int, newdata: Post):
    #find the post
    index=find_post_index(id)
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} not found")
    newdata_dict=newdata.model_dump()
    newdata_dict["id"]=id
    test_posts[index]=newdata_dict
    return {"post": newdata_dict}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #find the post
    index=find_post_index(id)
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} not found")
    test_posts.remove(test_posts[index])
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#Note: Finding a route in fastapi follows methods order
#The first route that matches the request will be the one that is executed
