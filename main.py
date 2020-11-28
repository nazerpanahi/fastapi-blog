from fastapi import FastAPI

from conf import ROUTERS
from db.database import SQL_Base, SQL_engine, SE_Base, SE_engine

# Make new app
app = FastAPI()


# make connection to database
@app.on_event('startup')
def startup():
    SQL_Base.metadata.create_all(bind=SQL_engine)
    SE_Base.metadata.create_all(bind=SE_engine)


# include all routers that is specified in the settings
for r in ROUTERS:
    router = r.get('router')
    prefix = r.get('prefix', '')
    tags = r.get('tags', None)
    dependencies = r.get('dependencies', None)
    responses = r.get('responses', None)
    default_response_class = r.get('default_response_class', None)

    app.include_router(router=router,
                       prefix=prefix,
                       tags=tags,
                       dependencies=dependencies,
                       responses=responses,
                       default_response_class=default_response_class)
