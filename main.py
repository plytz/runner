import ansible_runner
import argparse
import json
import sys

from ansible_runner.runner import Runner
from typing import List
from pydantic import BaseModel, ValidationError

parser = argparse.ArgumentParser()
parser.add_argument("json_input")


class JsonInput(BaseModel):
    action: str
    host: str
    ssh_user: str
    ssh_key: str


class JsonErrorResult(BaseModel):
    result: str = "error"
    message: str
    errors: List[dict] = None


class JsonSuccessResult(BaseModel):
    result: str = "success"
    events: List[dict]


def run_playbooks(playbooks: List[str]) -> List[Runner]:
    runners = []
    for playbook in playbooks:
        runner = ansible_runner.run(
            private_data_dir='/plytz',
            playbook=playbook,
            quiet=True,
            json_mode=True,
            timeout=15*60*60 #15 minutes
        )
        runners.append(runner)

    return runners


def init():
    playbooks = ["init.yml"]
    runners = run_playbooks(playbooks)
    print(JsonSuccessResult(events=runners[0].events).json())

# def main():
#     args = parser.parse_args()
#     try:
#         json_input = JsonInput(**json.loads(args.json_input))
#     except json.JSONDecodeError as error:
#         print(JsonErrorResult(message="Unable to decode JSON input").json())
#         sys.exit(1)
#     except ValidationError as error:
#         print(JsonErrorResult(
#             message="Unable to decode JSON input",
#             errors=error.errors()).json())
#         sys.exit(1)
#     except Exception as error:
#         print(JsonErrorResult(message="Something went wrong").json())
#         sys.exit(1)

#     if json_input.action == "init":
#         init()

#     sys.exit(0)



# if __name__ == "__main__":
#     main()

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
