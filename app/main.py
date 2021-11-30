
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2 as pg
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import false
from . import models
from .database import engine, get_db, SessionLocal



models.Base.metadata.create_all(bind=engine)



app = FastAPI()

# Dependency



#my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favourite food", "content": "I love pizza", "id": 2}]


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    #rating: Optional[int] = None

while True:
    try:
        conn = pg.connect(host = 'localhost', database = 'fastapi', user = 'postgres',
                        password = "amiya9800", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull")
        """cursor.execute("SELECT * FROM posts;")
        print(cursor.fetchall())"""
        break
    except Exception as error:
        print("Conneting failed to database")
        print(f"The error was {error}") 
        time.sleep(3)    





@app.get("/")
def welcome():
    return "Hello user welcome to the Api world"

# Testing the orm
'''@app.get("/sqlalchemy") 
def test_session(db: Session = Depends(get_db)):
    post = db.query(models.Post).
    return {"message":post}'''


#Getting all posts
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    '''cursor.execute("""SELECT * FROM posts""") # Regular sql query
    posts = cursor.fetchall()'''
    posts = db.query(models.Post).all()
    return {"data": posts}


'''def find_post(id):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return post'''



#Getting one post by id
@app.get("/posts/{id}")
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    #post = find_post(id)
    #cursor.execute(""" SELECT * FROM posts WHERE ID = %s""", (str(id)))
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:                                                              # Regular sql query
        """response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"{id} was not found"}""" # with response
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"post with {id} was not found")


    return {"post_details": post}



#creating a post
@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post:Post, db: Session = Depends(get_db)):
    #post_dict = post.dict()
    #post_dict["id"] = randrange(0, 10000000)
    #my_posts.append(post_dict) 
    #print(my_posts) 
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()  
    # conn.commit()
    #print(**post.dict())  #** is unpacking dict
    new_post = models.Post(**post.dict())  
    db.add(new_post)
    db.commit()
    db.refresh(new_post)          
    return {"data": new_post}
# anurag

'''def find_index_post(id):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index'''


#Delete a post
@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    #index = find_index_post(id)
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"{id} was not found")
    #my_posts.pop(index) 

    post.delete(synchronize_session=False)    
    db.commit()                   
    return Response(status_code=status.HTTP_204_NO_CONTENT)     



#Update a post
@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
    # #index = find_index_post(id)
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
    #                          (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"{id} was not found")

    post_query.update(updated_post.dict(), synchronize_session=False)                        
    db.commit()
    '''post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict'''
    return {"message":post_query.first()}


