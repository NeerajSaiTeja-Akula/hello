import streamlit as st
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
from fpdf import *


genai.configure(api_key = "AIzaSyDYfQmz7AHGbtvY4l5UJGVCa8JJgJrDjaQ")
model = genai.GenerativeModel(model_name="gemini-pro")


def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Sorry, I did not understand that."
        except sr.RequestError:
            return "Sorry, my speech service is down."

def speak_text(text):
    speaker = pyttsx3.init()
    speaker.say(text)
    speaker.runAndWait()

def generate_questions(topic):
    prompt = f"Generate two interview questions for a candidate on the topic of {topic}."
    message="""{"role": "system", "content": "You are an expert interviewer."},
            {"role": "user", "content":" """+prompt+""" "}"""
    response = model.generate_content(message).text
    questions = response.split('\n')
    return [q for q in questions if q]  # Filter out empty questions

def chat_with_gpt(prompt):
    response = model.generate_content(prompt).text
    return response
# Function to log conversation
def log_conversation(user_input, assistant_response, log):
    log.append(f"You: {user_input}\n")
    log.append(f"Assistant: {assistant_response}\n")

# Function to save conversation to PDF
def save_conversation_to_pdf(conversation_log, filename="interview_chat.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in conversation_log:
        pdf.multi_cell(0, 10, line)
    pdf.output(filename)
    st.info("The interview chat has been saved to a PDF file.")

# Function to start the interview
def start_interview():
    conversation_log = []
    log = []

    speak_text("Hello there! I'm your friendly interview bot. What's your name?")
    name = recognize_speech()
    speak_text(f"Nice to meet you, {name}! Let's get started with your interview.")

    while True:
        topic = "Data science"
        st.text(f"topic: {topic}")

        if topic.lower() == 'exit':
            speak_text("Alright, have a great day! Goodbye!")
            st.text("Alright, have a great day! Goodbye!")
            break

        speak_text(f"ok, {name}! Let's talk about {topic}.")

        questions = generate_questions(topic)

        if not questions:
            speak_text("sorry there is a small problem")
            continue


        for i, question in enumerate(questions):
            speak_text(f"Here's question for you. {question}")
            st.text(f"Question : {question}")
            response = recognize_speech()
            st.text(f"User response: {response}")

            aaa=chat_with_gpt("answer : {answer} question : {question}  what are your comments as a interviewr in single sentence and also tell weather he is correct or not in single sentence in friendly way")
            speak_text(aaa)
            st.text(aaa)

            log_conversation(question, response, conversation_log)

        speak_text("Thanks for your responses! You did a great job answering the questions.")
        st.text("Interview finished. Thank you for your responses.")

        save_conversation_to_pdf(conversation_log)
        speak_text("I've saved our conversation to a PDF file for you.")
        st.text("The interview chat has been saved to a PDF file.")
        break

# Streamlit GUI setup
st.title("Interview Bot")

if st.button("Start Interview"):
    start_interview()

if st.button("Exit"):
    st.stop()