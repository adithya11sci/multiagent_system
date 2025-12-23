# Railway Intelligence Multi-Agent System - Setup Guide

## 📋 Prerequisites

### Required
- Python 3.9 or higher
- pip (Python package manager)
- Gemini API Key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Optional (for full functionality)
- Twilio Account (for SMS alerts)
- Gmail Account with App Password (for email alerts)
- Telegram Bot Token (for push notifications)

## 🔧 Step-by-Step Setup

### 1. Environment Setup

#### Windows
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Verify activation (should show (venv) prefix)
```

#### Linux/Mac
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify activation (should show (venv) prefix)
```

### 2. Install Dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

Expected installation time: 2-5 minutes depending on internet speed.

### 3. Get Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

### 4. Configure Environment Variables

#### Create .env file
```bash
# Copy example file
copy .env.example .env    # Windows
cp .env.example .env      # Linux/Mac
```

#### Edit .env file
Open `.env` in your text editor and add:

```env
# Required - Get from Google AI Studio
GEMINI_API_KEY=AIzaSyD...your_key_here...

# Optional - For SMS alerts via Twilio
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=+1234567890

# Optional - For email alerts
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_gmail_app_password

# Optional - For Telegram notifications
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

### 5. Setup Optional Services

#### A. Twilio (SMS Alerts)
1. Sign up at [Twilio](https://www.twilio.com/)
2. Get your Account SID and Auth Token from Console
3. Get a Twilio phone number
4. Add credentials to `.env`

#### B. Gmail (Email Alerts)
1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account → Security
   - Search "App passwords"
   - Create password for "Mail"
3. Add email and app password to `.env`

#### C. Telegram Bot (Optional)
1. Message @BotFather on Telegram
2. Create new bot with /newbot command
3. Copy the bot token
4. Add to `.env`

### 6. Initialize RAG Data

The system comes with sample data in `data/rag/`. For production:

1. **Update timetables.json** with real train schedules
2. **Edit policies.txt** with actual railway policies
3. **Modify refund_rules.txt** with current refund rules
4. **Update route_maps.json** with route information

### 7. Verify Installation

Run verification script:
```bash
python -c "import google.generativeai; import langchain; import chromadb; print('✅ All imports successful')"
```

If successful, you should see: `✅ All imports successful`

### 8. Test Run

Start the system:
```bash
python main.py
```

You should see:
```
🚂 Initializing Railway Intelligence System...
📚 Loading RAG knowledge base...
✅ RAG system initialized
🧠 Initializing Multi-Agent Orchestrator...
✅ Orchestrator ready
```

## 🎮 First Usage

### Try Demo Scenarios

1. Select option `1` for Train Delay demo
2. Watch the agents work together
3. Review the JSON output

### Interactive Mode

1. Select option `5` for Interactive Mode
2. Enter a request like:
   ```
   Train 12627 delayed by 30 minutes
   ```
3. See the AI agents analyze and respond

## 🔍 Troubleshooting

### Common Issues

#### 1. Import Error: No module named 'google.generativeai'
**Solution:**
```bash
pip install google-generativeai
```

#### 2. Gemini API Error: Invalid API Key
**Solution:**
- Verify your API key in `.env`
- Check key is active in Google AI Studio
- Ensure no extra spaces in the key

#### 3. ChromaDB Error
**Solution:**
```bash
pip install --upgrade chromadb
```

#### 4. LangGraph Import Error
**Solution:**
```bash
pip install --upgrade langgraph langchain
```

#### 5. Twilio/Email not working
**Solution:**
- System will work without these (warnings only)
- Alerts will be simulated
- Configure credentials if needed

### Getting Help

1. Check error messages carefully
2. Verify all dependencies installed: `pip list`
3. Ensure Python version: `python --version` (should be 3.9+)
4. Check `.env` file exists and has correct values

## 🚀 Production Deployment

### Database Setup
Replace mock data with real database:
```python
# In tools/train_schedule_tool.py
from sqlalchemy import create_engine

engine = create_engine(DATABASE_URL)
# Query real data
```

### Scale Considerations
- Use Redis for caching
- Deploy on cloud (AWS/Azure/GCP)
- Set up monitoring and logging
- Configure rate limiting

### Security
- Keep API keys secure
- Use environment variables
- Enable authentication for API endpoints
- Regular security audits

## 📊 System Architecture

```
┌─────────────────────────────────────────────┐
│           User Interface Layer              │
│  (CLI / API / Web Dashboard - to be added)  │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│         Planner Agent (Master)              │
│              Gemini Pro                     │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│       LangGraph Orchestrator                │
│    (State Management & Routing)             │
└────┬────────┬───────────┬────────┬──────────┘
     │        │           │        │
┌────▼───┐ ┌──▼──┐ ┌─────▼──┐ ┌───▼────┐
│Operations│ │Pass.│ │ Crowd  │ │ Alert  │
│  Agent   │ │Agent│ │ Agent  │ │ Agent  │
└────┬─────┘ └──┬──┘ └────┬───┘ └───┬────┘
     │          │         │         │
     └──────────┴─────────┴─────────┘
                  │
     ┌────────────┴────────────┐
     │                         │
┌────▼─────┐          ┌───────▼────┐
│   RAG    │          │   Tools    │
│ System   │          │  External  │
│(ChromaDB)│          │  APIs      │
└──────────┘          └────────────┘
```

## 🎓 Next Steps

1. **Explore the Code**
   - Start with `main.py`
   - Review agent implementations
   - Understand orchestrator flow

2. **Customize**
   - Add your own data to RAG
   - Modify agent prompts
   - Add new tools

3. **Extend**
   - Create new agent types
   - Build web dashboard
   - Integrate real-time data

4. **Deploy**
   - Containerize with Docker
   - Set up CI/CD
   - Monitor performance

## 📚 Additional Resources

- [Gemini API Documentation](https://ai.google.dev/docs)
- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [ChromaDB Documentation](https://docs.trychroma.com/)

---

**Need help?** Open an issue or check the README.md for more details.

**Ready to start?** Run `python main.py` and explore! 🚂
