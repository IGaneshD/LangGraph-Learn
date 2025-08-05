from langchain_openai import AzureChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import getpass
from dotenv import load_dotenv

load_dotenv()


# to create rich command line you can use following python libraries
# 1.questionary
# 2.InquirerPy

class AzureModel:

    def __init__(self):

        if "AZURE_OPENAI_API_KEY" not in os.environ:
            os.environ["AZURE_OPENAI_API_KEY"] = getpass.getpass("Enter api key of azure deployment")

        if "AZURE_OPENAI_ENDPOINT" not in os.environ:
            os.environ["AZURE_OPENAI_ENDPOINT"] = input("Enter azure deployment endpoint")
        
        if "AZURE_OPENAI_VERSION" not in os.environ:
            os.environ["AZURE_OPENAI_VERSION"] = input("Enter azure deployment api version")
        
        if "AZURE_OPENAI_DEPLOYMENT" not in os.environ:
            os.environ["AZURE_OPENAI_DEPLOYMENT"] = input("Enter azure deployment name")

        self.llm = AzureChatOpenAI(api_version=os.getenv("AZURE_OPENAI_VERSION"), 
                                   azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"))
    
    def __call__(self):
        return self.llm
    

class GoogleModel:

    def __init__(self):

        if "GOOGLE_API_KEY" not in os.environ:
            os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API Key: ")

        
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

    
    def __call__(self):
        return self.llm
    




def get_llm_by_user(get_default=True):
    if get_default:
        return GoogleModel()()
    
    prompt = """Choose One of the Following Model\n
            1.Gemini-2.5.flash-lite(public)(default)
            2.GPT-4o-mini(protected)
            
            Entering anything else will consider option 1
    """
    try:
        model_choice = int(input(prompt))
    except ValueError:
        print("Using Default Model - Gemini-2.5.flash-lite...")
        return GoogleModel()
    
    if model_choice==1:
        print("Using Gemini-2.5.flash-lite...")
        return GoogleModel()()
    elif model_choice==2:
        print("usign GPT-4o-mini")
        print(type(AzureModel()))
        return AzureModel()()
    else:
        print("Using Default Model - Gemini-2.5.flash-lite...")
        return GoogleModel()()
