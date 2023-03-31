
# source: https://www.youtube.com/watch?v=GN6ICac3OXY&ab_channel=Amigoscode
from fastapi import FastAPI, HTTPException
from typing import List
from models import User, Gender, Role, UserUpdate
from uuid import UUID

app = FastAPI()

db: List[User] = [
	User(
		id=UUID("744f76aa-1ccf-47df-a43f-63fb75c1f3fb"),
		first_name="Rachel",
		last_name="Romee",
		gender=Gender.female,
		roles=[Role.admin]
	),
		User(
		id=UUID("c18369ab-4fce-492b-9912-b9ff66b6d0e5"),
		first_name="Camille",
		last_name="Sebastien",
		gender=Gender.male,
		roles=[Role.student, Role.user]
	)
]

@app.get("/")
async def root():
	return {"Hello": "World"}

@app.get("/api/v1/users")
async def fetch_users():
	return db

@app.post("/api/v1/users")
async def register_user(user: User):
	db.append(user)
	return {"id": user.id}

@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdate, user_id: UUID):
	for user in db:
		if user.id == user_id:
			if user_update.first_name is not None:
				user.first_name = user_update.first_name
			if user_update.last_name is not None:
				user.last_name = user_update.last_name
			if user_update.middle_name is not None:
				user.middle_name = user_update.middle_name
			if user_update.roles is not None:
				user.roles = user_update.roles
			return
	raise HTTPException(
		status_code=404,
		detail=f"user with id: {user_id} does not exist"
	)

@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
	for user in db:
		if user.id == user_id:
			db.remove(user)
			return
	# if the loop condition is not met, send error
	raise HTTPException(
		status_code=404,
		detail=f"user with id: {user_id} does not exist"
	)
