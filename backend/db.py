#  pip install pymysql

import pymysql
from fastapi import FastAPI
from pydantic import BaseModel
from model_classes import ApiData, CreateUserApiData

app = FastAPI()


def get_db_connection():
    return pymysql.connect( host="localhost", user="root", password="15081947", database="amazon_db", port=3307, cursorclass=pymysql.cursors.DictCursor )


@app.post("/users")
def get_users( req : ApiData ):
    connection = get_db_connection()
    # print(connection)

    # select or get data
    select_query = "select * from users where user_id = %s; "

    cursor =connection.cursor()
    cursor.execute( select_query, (req.user_id) )
    users = cursor.fetchall()

    # print( users )

    connection.close()

    return { "users": users, "id": req.user_id }






@app.post("/create-user")
def create_user( req : CreateUserApiData ):
    connection = get_db_connection()
    cursor = connection.cursor()
    insert_query = " insert into users(name, email, password) values(%s, %s, %s); "
    cursor.execute( insert_query, ( req.name, req.email, req.password   ) )

    connection.commit()
    connection.close()

    return { "data": req }



