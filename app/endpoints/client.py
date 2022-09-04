from fastapi import APIRouter, status, Request
from sqlalchemy import insert, literal_column

from models.client import Client
from schemas import *

router = APIRouter(
    prefix='/client',
    tags=['Client'],
)


@router.post(
    '/create_client/',
    response_model=CreateUserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create(
        request: Request,
        model: CreateUser,
):
    user_query = insert(Client).values(model.dict()["user"]).returning(literal_column('*'))
    async with request.app.state.db.get_session() as session:
        result = await session.execute(user_query)
        result_data = result.fetchone()
    print("~" * 100)
    print(result_data.id)
    print("~" * 100)

    return CreateUserResponse(user_id=result_data.id)
