# 🌦️ SkynixIQ — Smart Telegram Weather Bot

[![Deploy to Render](https://img.shields.io/badge/Deploy%20to-Render-blue?logo=render&style=for-the-badge)](https://render.com/docs/deploy-fast)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)
![OpenWeatherMap](https://img.shields.io/badge/API-OpenWeatherMap-orange?style=for-the-badge&logo=openweathermap)
![Google Gemini](https://img.shields.io/badge/Gemini%20AI-Google-red?style=for-the-badge&logo=google)

---

**SkynixIQ** is a smart Telegram bot built with Python that gives you **real-time weather forecasts** — and now supports **voice queries** and **AI-enhanced responses** using **Google Gemini**. Just type or speak something like `weather in Accra` or say a city name like `Nairobi` — and get instant, natural weather summaries directly in Telegram!

---

## 📸 Preview

> **You:** `weather in Accra`  
> **Bot:**  
> ` Right now in Accra, it's around 29°C but feels closer to 31°C. Expect some light rain — so you might want to carry an umbrella just in case🌤️`

---

## ✨ Features

- 📍 Real-time weather from OpenWeather API  
- 🧠 Gemini AI for enhanced natural responses (optional)  
- 🗣️ Supports voice messages via Telegram  
- 🤖 Smart input detection — `weather in [city]`, or just the city name  
- 🔍 Natural language filtering (`"now"`, `"please"`, `"today"` ignored)  
- ⚙️ Uses `python-telegram-bot` for Telegram integration  
- 🚀 Free deployment on [Render.com](https://render.com)

---

## 📂 Project Structure

```
skynixiq-weather-bot/
│
├── bot.py              # Main bot script
├── .env                # Environment secrets (not pushed to GitHub)
├── requirements.txt    # Python dependencies
├── Procfile            # Render worker setup
├── render.yaml         # Optional: Render IaC deployment config
└── README.md           # You're reading it!

```

---

## 🚀 One-Click Deploy (Render)

1. Fork this repo  
2. Click this button:  
   [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/bartonpratt/skynixiq-weather-bot)
3. Add your 3 environment variables in the Render dashboard:
   - `BOT_TOKEN`
   - `WEATHER_API_KEY`
   - `GEMINI_API_KEY`

---

## 🛠 Manual Deployment Guide

### ✅ 1. Clone the Repo & Prepare

```bash
git clone https://github.com/bartonpratt/skynixiq-weatherbot.git
cd skynixiq-weatherbot
```

### ✅ 2. Create Required Files

#### `requirements.txt`

```txt
python-telegram-bot==20.0
python-dotenv
requests
pydub
SpeechRecognition
google-generativeai
```

#### `Procfile`

```
worker: python bot.py
```

#### `.env` (local only — don’t upload to GitHub)

```env
BOT_TOKEN=your_telegram_bot_token
WEATHER_API_KEY=your_openweather_api_key
GEMINI_API_KEY=your_google_gemini_api_key
```

---

### ✅ 3. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/skynixiq-weatherbot.git
git push -u origin main
```

---

### ✅ 4. Deploy on [Render.com](https://render.com)

- Create a **Background Worker**
- Set:

  | Setting            | Value                     |
  |--------------------|---------------------------|
  | Build Command      | `pip install -r requirements.txt` |
  | Start Command      | `python bot.py`           |

- Add your **Environment Variables**:

  - `BOT_TOKEN`
  - `WEATHER_API_KEY`
  - `GEMINI_API_KEY`

- Click **Deploy**

---

## 💬 Usage Instructions

1. Open Telegram and start your bot with `/start`
2. Try sending:

   - `weather in Cape Town`
   - `What's the weather in Kumasi?`
   - Just `Nairobi`
   - 🎙️ Send a voice message saying "London"

---

## 🧠 Input Examples

| User Input                    | Works? | Example Response                    |
|------------------------------|--------|-------------------------------------|
| `weather in Accra`           | ✅     | Temp, Feels like, Weather condition |
| `what’s the weather in Cairo?` | ✅   | Same as above                       |
| `Kigali`                     | ✅     | Works with just the city name       |
| 🎙️ Voice: "Weather in Paris" | ✅     | Works with voice too!               |

---

## 🔐 Environment Variables

| Variable          | Description                                                       |
|-------------------|-------------------------------------------------------------------|
| `BOT_TOKEN`       | Telegram bot token from [@BotFather](https://t.me/BotFather)      |
| `WEATHER_API_KEY` | Weather API key from [OpenWeatherMap](https://openweathermap.org) |
| `GEMINI_API_KEY`  | Gemini API key from [Google AI Studio](https://makersuite.google.com/app) |

---

## 🔧 Setup Notes

### 🗣️ Voice Message Support

To handle Telegram voice messages, `pydub` requires **FFmpeg** installed on your system.

#### ✅ Install FFmpeg:

- **Windows**: [Download here](https://ffmpeg.org/download.html) and add the `bin/` folder to your system PATH.
- **Linux**:
  ```bash
  sudo apt install ffmpeg
  ```

> Without FFmpeg, the bot will not be able to process voice messages.

---

### ⚠️ PyAudio Not Required

Even though `SpeechRecognition` supports `pyaudio`, it’s **not needed** in this project because we are processing uploaded audio files, not live microphone input.

---

## 🪪 License

MIT License — use it freely and give credit where due.

---

## 👨‍💻 Author

**Joseph Barton Pratt**  
📫 [bartonpratt@gmail.com](mailto:bartonpratt@gmail.com)  
🐙 [github.com/bartonpratt](https://github.com/bartonpratt)

