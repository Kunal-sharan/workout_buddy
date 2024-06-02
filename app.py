import streamlit as st
from audiorecorder import audiorecorder
import speech_recognition as sr
import os
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
import pandas as pd
import time
llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=st.secrets['GOOGLE_API'])

parser = JsonOutputParser()

prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions} with 'Target Muscle','Workout','Reps per set','Sets'\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | llm | parser

# res=chain.invoke({"query": gym_query})
r = sr.Recognizer()


if "workouts" not in st.session_state:
  st.session_state.workouts=[]
text=""
st.title("Workout Tracker")
audio = audiorecorder("", "")
if len(audio) > 0:
    # # To play audio in frontend:
    # st.audio(audio.export().read())
    # To save audio to a file, use pydub export method:
    audio.export("audio_input.wav", format="wav")
    
    # To get audio properties, use pydub AudioSegment properties:
    # st.write(f"Frame rate: {audio.frame_rate}, Frame width: {audio.frame_width}, Duration: {audio.duration_seconds} seconds")
    with sr.AudioFile("audio_input.wav") as source:
      a=r.record(source)
      text=r.recognize_google(a)
    # if len(text)>0:
    #   text=llm.invoke(f"The given text is related to gym analyze the complete text and fix it if random or wrong words are written make it proper don't add any extra information {text} your ouput should be a one line sentence that only containes these things  'Target Muscle','Workout','Reps per set','Sets' and make sure the 'Sets'  is not more than 4 ")
    st.write(text)
    res=chain.invoke({"query": str(text)})
    st.session_state.workouts.append(res)
    audio_file_path="audio_input.wav"
    if os.path.exists(audio_file_path):
      os.remove(audio_file_path)
      alert=st.success(f"File '{audio_file_path}' deleted successfully.")
      time.sleep(1) # Wait for 3 seconds
      alert.empty() # Clear the alert
  
    else:
      st.error("The file does not exist")
@st.experimental_fragment
def fragment():
      Show=st.button("Show workouts")
      if Show:
        if "workouts" in st.session_state and len(st.session_state.workouts)>0:
          # st.write(st.session_state.workouts)
          df=pd.DataFrame(st.session_state.workouts)
          st.dataframe(df)
fragment()

# import streamlit as st

# # Import SessionState from the streamlit community

# # Get the session state
# import streamlit as st

# if "script_runs" not in st.session_state:
#     st.session_state.script_runs = 0
#     st.session_state.fragment_runs = 0

# @st.experimental_fragment
# def fragment():
#     st.session_state.fragment_runs += 1
#     st.button("Rerun fragment")
#     st.write(f"Fragment says it ran {st.session_state.fragment_runs} times.")

# st.session_state.script_runs += 1
# fragment()
# st.button("Rerun full script")
# st.write(f"Full script says it ran {st.session_state.script_runs} times.")
# st.write(f"Full script sees that fragment ran {st.session_state.fragment_runs} times.")
