import os, re
import requests
import google.generativeai as genai
import asyncio
from functools import partial
from dotenv import load_dotenv
from telegram import Update, Message
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)

from pydub import AudioSegment
import speech_recognition as sr

# === Load secrets from .env file ===
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
# Initialize Google Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# === Ensure audio directory exists for saving temporary files ===
AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

# === /start command handler ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Sends a welcome message and basic usage instructions
    await update.message.reply_text(
        "👋 Hey! I'm SkynixIQ, your smart weather assistant.\n"
        "Need the forecast? Just ask me something like:\n\n"
        "• `weather in Accra`\n"
        "• `what's the weather in Cape Town?`\n"
        "• or simply type the city name!\n\n"
        "I'll get you the latest weather in seconds. ☁️🌤️🌧️"
    )

# === Fetch weather from OpenWeather API ===
def get_weather(city: str):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric"  # Return results in Celsius
    }

    try:
        # Send GET request to OpenWeather API
        response = requests.get(base_url, params=params)
        data = response.json()

        if data["cod"] != 200:
            return f"⚠️ City not found: {city}"

        # Extract weather information
        weather = data["weather"][0]["description"].title()
        temp = data["main"]["temp"]
        feels = data["main"]["feels_like"]

        return f"🌤️ Weather in {city.title()}:\nTemperature: {temp}°C\nFeels like: {feels}°C\nCondition: {weather}"
    except Exception as e:
        return f"⚠️ Error: {e}"

async def process_weather_request(message_text: str, update: Update):
    message = message_text.strip().lower()

    # Simple greeting only
    if re.fullmatch(r"(hi+|hello+|hey+|howdy+|heya+|hola+)[\s!,.]*", message):
        await update.message.chat.send_action(action="typing")
        await update.message.reply_text(
            "👋 Hi there! I'm SkynixIQ, your weather assistant. "
            "Just type `weather in [city]` or simply the city name to get the latest forecast!"
        )
        return

    # Case 1: Sentence contains "weather in"
    if "weather in" in message:
        match = re.search(r"weather in\s+([a-z\s]+)", message)
        if match:
            city = match.group(1).strip()
            city = re.sub(r"\b(today|now|please|tomorrow|like|looking)\b", "", city).strip()
            if city:
                await update.message.chat.send_action(action="typing")
                report = get_weather(city)
                friendly_report = await enhance_with_gemini_async(report)
                await update.message.reply_text(friendly_report)
                return
        await update.message.reply_text("⚠️ I couldn't detect the city. Try: `weather in Cape Town`")
        return

    # Case 2: Treat message as city (removing noise words)
    city = re.sub(r"\b(today|now|please|weather|in|for|is|tell|me|the|like|looking)\b", "", message).strip()
    if city:
        await update.message.chat.send_action(action="typing")
        report = get_weather(city)
        friendly_report = await enhance_with_gemini_async(report)
        await update.message.reply_text(friendly_report)
    else:
        await update.message.reply_text(
            "❓ Try one of the following:\n• `weather in Nairobi`\n• or just type the city name like `Accra`"
        )

# === Text message handler ===
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Calls the shared logic to process text messages
    await process_weather_request(update.message.text, update)

# === Voice message handler ===
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    voice = update.message.voice

    ogg_path = f"{AUDIO_DIR}/{user.id}_voice.ogg"
    wav_path = f"{AUDIO_DIR}/{user.id}_voice.wav"

    try:
        # Step 1: Download the voice message (OGG format)
        file = await context.bot.get_file(voice.file_id)
        await file.download_to_drive(ogg_path)

        # Step 2: Convert the OGG file to WAV format using pydub
        audio = AudioSegment.from_ogg(ogg_path)
        audio.export(wav_path, format="wav")

        # Step 3: Transcribe the WAV file using Google Speech Recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            transcribed_text = recognizer.recognize_google(audio_data)

        # Step 4: Inform the user what was heard (optional)
        await update.message.reply_text(f"🗣️ You said: {transcribed_text}") #you can comment this line out

        # Step 5: Process the transcribed text like normal user input
        await process_weather_request(transcribed_text, update)

    except sr.UnknownValueError:
        # If speech couldn't be recognized
        await update.message.reply_text("😶 I couldn't understand that voice message.")
    except Exception as e:
        # Catch any other errors (e.g. download, conversion)
        await update.message.reply_text(f"❌ Error processing voice: {e}")
    finally:
        # Always clean up the audio files
        for path in (ogg_path, wav_path):
            if os.path.exists(path):
                os.remove(path)

# === Enhances a weather report using Gemini (synchronously) ===
def enhance_with_gemini(weather_report: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-2.5-pro")
        prompt = (
            f"Turn the following weather update into a single friendly, natural-sounding sentence, "
            f"as if spoken by a helpful AI assistant. Mention the city, temperature, what it feels like, "
            f"and include a useful suggestion based on the condition (like carrying an umbrella or staying hydrated). "
            f"End with a single appropriate weather emoji — no headers or extra formatting.\n\n"
            f"Weather update: {weather_report}"
        )

        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"{weather_report}\n\n(⚠️ Gemini enhancement failed: {e})"
    
# === Async-safe wrapper around the Gemini function ===
async def enhance_with_gemini_async(weather_report: str) -> str:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, partial(enhance_with_gemini, weather_report))
    




# === Main entry point ===
def main():
    # Create the Telegram app with bot token
    app = ApplicationBuilder().token(TOKEN).build()

    # Register command and message handlers
    app.add_handler(CommandHandler("start", start))  # /start command
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))  # Text messages
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))  # Voice messages

    print("🌦️ Weather Bot is running...")
    app.run_polling()

# Run the bot
if __name__ == "__main__":
    main()
