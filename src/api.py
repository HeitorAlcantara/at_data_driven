from fastapi import FastAPI
from routers import match_summary_router, player_profile_router

app = FastAPI()
app.include_router(router=match_summary_router)
app.include_router(router=player_profile_router)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)