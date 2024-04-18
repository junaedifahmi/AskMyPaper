from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from .models import Inquery
from .controller import invoke_agent, one_time_prompt

route = APIRouter(prefix='/agent', tags=['agent'])


@route.post('/ask')
def ask_agent(i: Inquery) -> str:
    # print(i)
    if resp := invoke_agent(i.text):
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={ "q": i.text, "a": resp }
        )
    else:
        return JSONResponse(status_code=500, content="Internal Error")


@route.post('/command')
def command_agent(i: Inquery):
    if resp := one_time_prompt(i.text):
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={ "q": i.text, "a": resp }
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        )