from fastapi import APIRouter, status, Request
from fastapi_pagination import Page
from fastapi_pagination.ext.async_sqlalchemy import paginate
# from fastapi_pagination.ext.sqlalchemy_future import paginate
from sqlalchemy import insert, literal_column, delete as sa_delete, select, update as sa_update
from sqlalchemy.exc import IntegrityError

from lib import check_errors
from models.client import Tag
from schemas import CreateTagResponse, CreateTag, TagFullData, TagData

router = APIRouter(
    prefix='/tag',
    tags=['Tag'],
)


@router.post(
    '/tag/',
    response_model=CreateTagResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create(
        request: Request,
        model: CreateTag,
):
    tag_query = insert(Tag).values(model.dict()).returning(literal_column('*'))
    async with request.app.state.db.get_session() as session:
        result = await session.execute(tag_query)

        result_data = result.fetchone()
        await session.commit()
    return CreateTagResponse(tag_id=result_data.id)


@router.get('',
            response_model=Page[TagFullData],
            status_code=status.HTTP_200_OK,
            )
async def get_tags(request: Request):
    async with request.app.state.db.get_session() as session:
        return await paginate(session, select(Tag))


@router.patch('/{tag_id}',
              response_model=TagFullData,
              status_code=status.HTTP_200_OK,
              )
async def update(request: Request, model: TagData, tag_id: int):
    tag_query = sa_update(Tag).where(Tag.id == tag_id).values(model.dict()).returning(literal_column("*"))

    async with request.app.state.db.get_session() as session:
        try:
            await session.execute(tag_query)
            await session.commit()
        except IntegrityError as e:
            check_errors(e.orig.sqlstate, e)


@router.delete('/{tag_id}',
               status_code=status.HTTP_204_NO_CONTENT,
               )
async def delete(request: Request, tag_id: int):
    tag_query = sa_delete(Tag).where(Tag.id == tag_id)

    async with request.app.state.db.get_session() as session:
        try:
            await session.execute(tag_query)
            await session.commit()
        except IntegrityError as e:
            check_errors(e.orig.sqlstate, e)
