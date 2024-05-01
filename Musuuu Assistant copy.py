import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
from youtubesearchpython import VideosSearch
import requests
from bs4 import BeautifulSoup
import getpass  # Import for password input
import smtplib

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your assistant. How may I help you today?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again, please...")
        return "None"
    return query

def voice_lock(user):
    while True:
        speak(f"Please say your name, {user}, to unlock the assistant.")
        name = user.lower()
        user_input = takeCommand().lower()
        
        if user_input == name:
            speak(f"Voice match successful. Assistant unlocked for {user}.")
            break
        else:
            speak(f"Voice doesn't match, {user}. Please try again.")

def sendEmail(to, subject, message):
    try:
        # Replace 'your_email@gmail.com' and 'your_password' with your email credentials
        from_email = 'your_email@gmail.com'
        password = 'your_password'

        # Create a connection to the SMTP server (in this case, Gmail's SMTP server)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # Log in to your email account
        server.login(from_email, password)

        # Create the email message
        email_message = f"Subject: {subject}\n\n{message}"

        # Send the email
        server.sendmail(from_email, to, email_message)

        # Close the connection
        server.quit()

        print("Email sent successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Email was not sent.")

if __name__ == "__main__":
    user = "Mustafa"
    voice_lock(user)
    
    wishMe()
    while True:
        query = takeCommand().lower()

        if 'open YouTube and search for' in query:
            query = query.replace("open YouTube and search for", "")
            videos_search = VideosSearch(query, limit=1)
            results = videos_search.result()
            
            if results and len(results) > 0 and 'link' in results[0]:
                video_link = results[0]['link']
                speak(f"Here's a video related to {query}. Opening YouTube.")
                webbrowser.open(video_link)
            else:
                speak(f"Sorry, I couldn't find a video related to {query} on YouTube.")

        # Include other commands for your assistant as needed

        elif 'fetch code from website' in query:
            speak("Please provide the URL of the website you want to fetch code from.")
            website_url = takeCommand().lower()
            if 'stackoverflow' in website_url:
                stack_overflow_url = 'https://stackoverflow.com'
                response = requests.get(stack_overflow_url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    code_snippets = soup.find_all('code')
                    if code_snippets:
                        speak("Here's some code from Stack Overflow:")
                        for snippet in code_snippets:
                            speak(snippet.get_text())
                    else:
                        speak("No code snippets found on Stack Overflow.")
                else:
                    speak("Failed to fetch code from Stack Overflow. Please check the URL.")
            else:
                speak("Sorry, I don't know how to fetch code from this website.")
        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com")
        elif 'open google' in query:
            webbrowser.open("https://www.google.com")
        elif 'open stackoverflow' in query:
            webbrowser.open("https://stackoverflow.com")
        elif 'open chatgpt' in query:
            webbrowser.open("https://openai.com")
        elif 'play music' in query:
            music_dir = 'D:\\Non Critical\\songs\\Favorite Songs2'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
        elif 'open code' in query:
            codePath = ""#Replace with your code editor's path
            os.startfile(codePath)
        elif 'email to friend' in query:
            try:
                speak("What should the subject be?")
                subject = takeCommand()
                speak("What should I say in the email?")
                content = takeCommand()
                to = "reciver_mail@gmail.com"
                sendEmail(to, subject, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry, I am not able to send this email")
