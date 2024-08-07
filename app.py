from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from fastapi import FastAPI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import json
import jsonify

from flask import Flask , request


Port = 5000
# Loading environment variables
load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

def translation(language1,language2,text):
    # creating prompt_template
    system_template = "translate the given text from {language1} into {language2}"
    prompt_template = ChatPromptTemplate.from_messages([
        ("system",system_template),("user","{text}")
    ])

    # creating the chat model
    model = ChatGroq(model="llama3-8b-8192")

    # creating thr output parser
    parser = StrOutputParser()

    # create the last chain model 
    chain = prompt_template | model | parser
    response = chain.invoke({"language1":language1,
                  "language2":language2,
                  "text":text
                  })
    return response
app = Flask(__name__)

@app.route("/",methods=['GET'])
def homepage():
    return 'hello there'

@app.route("/process",methods=['POST'])  
def process_data():
    # Here you can implement any processing logic
    # processed_text = f"Translating '{data.text}' from {data.from_language} to {data.to_language}."
    language1= request.json.get("from_language")
    language2 = request.json.get("to_language")
    text = request.json.get("text")
    response = translation(language1,language2,text)
    return {"result": response}
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Port)