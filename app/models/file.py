from pydantic import BaseModel, validator


class File(BaseModel):
    path: str
    # name: str

file = File(path="c/users", name='file')
# print(file)
