import streamlit as st 
# streamlit :- web based app making 
# lite python framework

st.title("AI Resume Maker")
st.markdown("""## user can create or download AI created resume based on high ATS Score """)

#================AGENT CODE==============

import os
import time
import langchain
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
import pytesseract as pyt
from tavily import TavilyClient
from langchain.messages import SystemMessage, HumanMessage
import numpy as np
import streamlit as st
from langchain_community.document_loaders import PyMuPDFLoader

#===========API KEY LOAD================

GOOGLE_API_KEY = st.sidebar.text_input("GOOGLE_API_KEY",type ="password")
GROQ_API_KEY = st.sidebar.text_input("GROQ_API_KEY ",type ="password")
TAVILY_API_KEY = st.sidebar.text_input("TAVILY_API_KEY",type ="password")

#===========model building===============
model = ChatGoogleGenerativeAI(
    model = "gemini-3.5-flash-lite",
    google_api_key = GOOGLE_API_KEY
)
# tool 
def search_recent_news_jobs(query):
  """This function helps to search
  recent news or recent jobs
  related to given search query
  suppose user write Python Developer jobs
  It should return trending news and jobs link"""
  client = TavilyClient(
      api_key = TAVILY_API_KEY
  )
  return client.search(query)


# agent creation
from langchain.agents import create_agent

agent = create_agent(
    model = model,
    tools = [search_recent_news_jobs]
)


#==========Prompt Generator======================
def prompt_generator(agent):
  """This function helps to give detailed prompt
  followed by chain of thought and persona based prompting
  main task is to give deatiled porompt to builed resume
  for studnets and experienced person based on there personal information """

  prompt = """You are a senior HR resume analyzer,
  main task is to give
  detailed prompt to build Resume for
  Students or Experienced person
  Based on their given personal information.
  system instruction i want moel to gennerate resume in html format, include that in prompt """
  response = agent.invoke(prompt)
  file_name = 'prompt.py'
  with open(file_name, 'w') as f:
    f.write(response.content[-1]['text'])
  return "Prompt file generated Successfully, agent can read it"
prompt_generator(model)
# tool 2

def resume_maker_prompt():
  """This function just gives updated prompt for model"""
  with open('prompt.py', 'r') as f:
    prompt = f.read()
  return prompt
resume_maker_prompt()

# ===================Generator====================
prompt = """you are a helpful ai assistant
with job resume maker, your task is to give HTML format
resume with proper designing ussin recent css and js code with professional design format
user will upload data return html format rsume
always use different styling and color palate and dont add any paragraph in starting like here is a starategic type just the resume  in the resume"""

final_prompt = prompt + resume_maker_prompt()
details = input("Enter your details : ")
user_details = f"""user details : - given below :-{details}"""
query = final_prompt + user_details

if st.button("Generate resume"):
  with st.spinner("Running agent"):
    response = agent.invoke({'messages': [{'role':'user','content':query}]})
    code = response['messages'][-1].content[-1]['text']

    #st.mardown(code)
    st.html(code, width="stretch",unsafe_allow_javascript=True)


