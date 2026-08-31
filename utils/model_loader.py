
import os
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field, ConfigDict

from utils.config_loader import load_config


class ConfigLoader:
    def __init__(self):
        print(f"Loaded Config...")
        self.config= load_config()
 
    def __getitem__(self, key):
        return self.config[key]



class ModelLoader(BaseModel):
    model_provider: Literal["groq", "google"] = "groq"
    model_name: Optional[str] = None
    config: Optional[ConfigLoader] = Field(default= None, exclude= True)

    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def load_llm(self):
        """
        Load and return the LLM Model.
        """
        print("LLM Loading...")
        print(f"Loading model from Provider: {self.model_provider}")

        if self.model_provider == 'groq':
            print("Loading LLM from GROQ......")
            groq_api_key = os.getenv("GROQ_API_KEY")
            selected_model = self.model_name or self.config["llm"]["groq"]["model_name"]
            print(f"Using Groq model: {selected_model}")
            llm = ChatGroq(model=selected_model, api_key=groq_api_key, streaming=True)

        elif self.model_provider == "google":
            print("Loading LLM from Google....")
            google_api_key = os.getenv("GOOGLE_API_KEY")
            selected_model = self.model_name or self.config["llm"]["google"]["model_name"]
            print(f"Using Google model: {selected_model}")
            llm = ChatGoogleGenerativeAI(model=selected_model, api_key=google_api_key, streaming=True)

        return llm