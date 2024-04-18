from fastapi import FastAPI

from agent import route as AgentRoutes
from datasource import route as DataSourceRoutes

app = FastAPI()

app.include_router(AgentRoutes)
app.include_router(DataSourceRoutes)


