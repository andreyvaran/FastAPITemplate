from fastapi import HTTPException
from psycopg2 import errorcodes
from sqlalchemy.exc import IntegrityError
from starlette import status

def check_errors(
        exception: IntegrityError,
        foreign_key_status_code: status = status.HTTP_400_BAD_REQUEST,
        foreign_key_detail: str | None = None,
        unique_violation_status_code: status = status.HTTP_400_BAD_REQUEST,
        unique_violation_detail: str | None = None,
        check_violation_status_code: status = status.HTTP_400_BAD_REQUEST,
        check_violation_detail: str | None = None
):
    sqlstate = exception.orig.sqlstate
    match sqlstate:
        case errorcodes.UNIQUE_VIOLATION:
            raise HTTPException(
                status_code=unique_violation_status_code,
                detail=unique_violation_detail or exception.args[0],
            )
        case errorcodes.FOREIGN_KEY_VIOLATION:
            raise HTTPException(
                status_code=foreign_key_status_code,
                detail=foreign_key_detail or exception.args[0],
            )
        case errorcodes.CHECK_VIOLATION:
            raise HTTPException(
                status_code=check_violation_status_code,
                detail=check_violation_detail or exception.args[0],
            )
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=exception.args[0],
            )