import uvicorn
from blaxel import env

port = env["BL_SERVER_PORT"] or 1338
host = env["BL_SERVER_HOST"] or "0.0.0.0"

if __name__ == "__main__":
    uvicorn.run("src.main:app", host=host, port=int(port), reload=False)
