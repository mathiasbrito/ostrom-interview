import os
import sys
import uvicorn
from fastapi import FastAPI
from ostrom.routers import tariff_router


port = int(os.environ.get('PORT', '8001'))

api = FastAPI()
api.include_router(tariff_router)


def main():
  sys.exit(
    uvicorn.run(
      'ostrom.app:api', host='0.0.0.0', port=port
    )
  )


if __name__ == '__main__':
  main()
