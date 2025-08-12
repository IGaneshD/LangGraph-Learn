import getpass
import os
import json

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
from pathlib import Path
from langchain_prompty import create_chat_prompt

load_dotenv()

# pip install langchain-prompty

# load prompty as langchain ChatPromptTemplate
# Important Note: Langchain only support mustache templating. Add 
#  template: mustache
# to your prompty and use mustache syntax.

folder = Path(__file__).parent.absolute().as_posix()
path_to_prompty = folder + "/basic.prompty"
prompt = create_chat_prompt(path_to_prompty)


model = AzureChatOpenAI(api_version=os.getenv("AZURE_OPENAI_VERSION"), azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"))


output_parser = StrOutputParser()

chain = prompt | model | output_parser

json_input = '''{
  "firstName": "Ganesh",
  "question": "prime number check program"
}'''
args = json.loads(json_input)
result = chain.invoke(args)
print(result)
