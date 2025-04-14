import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def get_voice_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Say something to search on YouTube...")
        recognizer.adjust_for_ambient_noise(source)

        try:
            audio = recognizer.listen(source, timeout=4, phrase_time_limit=4)  
            search_query = recognizer.recognize_google(audio)
            print(f"✅ Recognized: {search_query}")
            return search_query
        except sr.WaitTimeoutError:
            print("❌ No speech detected within 4 seconds.")
            return None
        except sr.UnknownValueError:
            print("❌ Could not understand the audio.")
            return None
        except sr.RequestError:
            print("❌ Could not request results. Check your internet connection.")
            return None

def search_youtube(query):
    driver = webdriver.Chrome()
    driver.get("https://www.youtube.com")

    time.sleep(2)  

    search_box = driver.find_element(By.NAME, "search_query")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    time.sleep(3) 
    videos = driver.find_elements(By.ID, "video-title")

    for video in videos:
        if video.get_attribute("href"): 
            video.click()
            break  
    query = get_voice_command()
    if query:
        search_youtube(query)
