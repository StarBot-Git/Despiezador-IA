from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

class FileResult(BaseModel):
    name: str
    detected_views: list[str]
    has_text: bool
    comments: list[str]

class Conclusions(BaseModel):
    estado: str
    razones: list[str]

class ReportAIResult(BaseModel):
    files: list[FileResult]
    general_description: str
    conclusions: Conclusions

def send_request(model, input, response_format):
    return client.responses.parse(model=model, input=input, text_format=ReportAIResult)

def upload_file(path:str = None, purpose:str="input_file"):
    if path:
        return client.files.create(file=open(file=path, mode="rb"), purpose=purpose)