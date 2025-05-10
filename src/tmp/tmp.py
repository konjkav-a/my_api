from fastapi import FastAPI
from fastapi import Depends


class CachedDBSession:
    def __init__(self):
        self.session = None

    def __call__(self):
        if not self.session:
            print("Creating new DB session...")
            self.session = "db_connection"

        return self.session


tmp_app = FastAPI()
db_session = CachedDBSession()

@tmp_app.get("/data")
async def get_data(db: str = Depends(db_session)):
    return {"db": db}