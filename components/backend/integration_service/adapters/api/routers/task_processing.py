from fastapi import APIRouter, Depends, status

from integration_service.application import dtos, use_cases
from ..dependencies import get_task_handler

router = APIRouter()


@router.post("/tasks",
             response_model=dtos.TaskInfo,
             status_code=status.HTTP_200_OK,
             tags=["Tasks"]
             )
async def process_task(
    task: dtos.Task,
    task_handler: use_cases.TaskHandler = Depends(get_task_handler)
) -> dtos.TaskInfo:
    return await task_handler.execute(**task.dict())
