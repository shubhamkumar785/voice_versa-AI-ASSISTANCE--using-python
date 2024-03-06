import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import wolframalpha
import openai

# Initialize Wolfram Alpha client with your app ID
WOLFRAM_ALPHA_APP_ID = "YOUR_WOLFRAM_ALPHA_APP_ID"
WOLFRAM_CLIENT = wolframalpha.Client(WOLFRAM_ALPHA_APP_ID)

# OpenAI API key
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
openai.api_key = OPENAI_API_KEY

# Initialize speech recognition and text-to-speech engines
LISTENER = sr.Recognizer()
MACHINE = pyttsx3.init()

def talk(text):
    """Function to speak out the given text."""
    MACHINE.say(text)
    MACHINE.runAndWait()

def take_input():
    """Function to take voice input from the user."""
    try:
        with sr.Microphone() as source:
            print('Listening...')
            audio = LISTENER.listen(source)
            command = LISTENER.recognize_google(audio)
            command = command.lower()
            print('Command:', command)
            if "voice_versa" in command:
                command = command.replace('voice_versa', '')
            return command
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Please try again.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

def calculate(expression):
    """Function to evaluate mathematical expressions."""
    try:
        expression = expression.replace('x', '*').replace('÷', '/')
        result = eval(expression)
        return result
    except Exception as e:
        return "Sorry, I couldn't perform the calculation."

def ai_response(query):
    """Function to generate AI response using OpenAI's GPT-3 model."""
    try:
        response = openai.Completion.create(
            engine="davinci", 
            prompt=query, 
            max_tokens=100
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"OpenAI request failed: {e}")
        return "I couldn't understand that. Could you please repeat?"

def run_voice_versa():
    """Function to handle Voice Versa commands."""
    while True:
        command = take_input()
        if command:
            if "play" in command:
                song = command.replace('play', '')
                talk("Playing " + song)
                pywhatkit.playonyt(song)

            elif 'time' in command:
                current_time = datetime.datetime.now().strftime('%I:%M %p')
                talk('The current time is ' + current_time)

            elif 'date' in command:
                current_date = datetime.datetime.now().strftime('%d/%m/%Y')
                talk("Today's date is " + current_date)

            elif 'how are you' in command:
                talk('I am fine, how about you?')

            elif 'what is your name' in command:
                talk('I am Voice Versa, what can I help you with?')

            elif 'what is the main purpose' in command:
                talk("Voice Versa is software that carries out everyday tasks via voice command. It brings AI and machine learning together to recognize our voice and perform requested tasks.")

            elif 'who is' in command:
                person = command.replace('who is', '').strip()
                try:
                    info = wikipedia.summary(person, 1)
                    talk(info)
                except wikipedia.exceptions.DisambiguationError as e:
                    talk(f"There are multiple results for {person}. Can you please specify?")
                except wikipedia.exceptions.PageError:
                    talk(f"Sorry, I couldn't find any information about {person}")

            elif 'calculate' in command:
                calculation = command.replace('calculate', '').strip()
                result = calculate(calculation)
                talk('The result is ' + str(result))

            else:
                # Query Wolfram Alpha for specific questions
                try:
                    res = WOLFRAM_CLIENT.query(command)
                    answer = next(res.results).text
                    talk(answer)
                except:
                    # Generate AI response for general questions
                    ai_resp = ai_response(command)
                    talk(ai_resp)

# Main function to run Voice Versa
if __name__ == "__main__":
    run_voice_versa()
