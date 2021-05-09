from fastapi import FastAPI, HTTPException
from typing import Optional
from datetime import datetime
import json
import MySQLdb
from pydantic import BaseModel
import redis

# Run the API
app = FastAPI()
cache = redis.Redis(host='redis', port=6379)

# Data Model definition of the Actor Table
class Actor(BaseModel):
    actor_id: Optional[int] = "null"
    first_name: str
    last_name: str
    #last_update: Optional[datetime] = datetime.now()

# Response if the query didn't find any data
def emptyResultSet():
    return {"response": "No data found for given Query"}

# Connect to MySQL DB
def dbConnect():
    connection = MySQLdb.connect(
        host = "localhost",
        user = "testUser",
        passwd = "test123",
        database = "sakila"
    )

    return connection

# Commit INSERT/UPDATE/DELETE to DB and return number of rows affected
def postData(sql, type):
    conn = dbConnect()
    cursor = conn.cursor()

    try:
        cursor.execute(sql)
    except Exception as e:
        # Returns Exception in JSON format
        raise HTTPException(status_code=400, detail=e.args[1])

    conn.commit()

    return {"response": "{0} Rows have been {1}".format(cursor.rowcount, type)}

# MySQL Table (Query Response) to JSON format
def toJson(cursor):
    headers = [x[0] for x in cursor.description]
    rows = cursor.fetchall()
    jsonData = []

    for row in rows:
        jsonData.append(dict(zip(headers, row)))

    if jsonData == []:
        return emptyResultSet()

    jsonDump = json.dumps(jsonData, indent=2, sort_keys=True)
    return json.loads(jsonDump)

# Get Actor by actor_id attribute
@app.get("/actors/{actorId}")
def getActorById(actorId: int):
    """
    Get an actor by its ID
    """

    conn = dbConnect()
    cursor = conn.cursor()
    cursor.execute("select actor_id, first_name, last_name, date_format(last_update,'%Y-%m-%d %T') as last_update from actor where actor_id = " + str(actorId))

    return toJson(cursor)

# INSERT an actor in the DB
@app.post("/actors")
def addActor(actor: Actor):
    """
    Add an anctor with the information:
    - **actor_id** - Internal ID value for the Actor (Optional - Auto increments if not provided in body)
    - **first_name** - First name of the Actor (Required)
    - **last_name** - Last name of the Actor (Required)
    """

    sql = """insert into actor(actor_id, first_name, last_name, last_update)
             values({0},"{1}","{2}",now())""".format(actor.actor_id, actor.first_name, actor.last_name)

    return postData(sql, "inserted")

# DELETE an actor from the DB by actor_id
@app.delete("/actors/{actorId}")
def delActor(actorId: int):
    """
    Delete an Actor by its ID
    """

    sql = "delete from actor where actor_id = " + str(actorId)

    return postData(sql, "deleted")

# UPDATE an actor in the DB by actor_id
@app.put("/actors/{actorId}")
def updateActor(actorId: int, actor: Actor):
    """
    Update an Actor by its ID with the information:
    - **first_name** - First name of the Actor (Required)
    - **last_name** - Last name of the Actor (Required)
    """

    sql = "update actor set first_name = '{0}', last_name = '{1}' where actor_id = {2}".format(actor.first_name, actor.last_name, actorId)

    return postData(sql, "updated")
