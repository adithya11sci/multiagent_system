# Setup Guide - Multi-Agent WhatsApp System

Complete setup instructions for the Multi-Agent WhatsApp System.

## 📋 Prerequisites

- Python 3.9 or higher
- OpenAI API key
- Twilio account (for WhatsApp)
- Google Cloud account (for Gmail API)
- Git

## 🚀 Quick Start

### 1. Clone/Setup Project

```bash
cd d:\multiagent
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

**Activate virtual environment:**

Windows:
```bash
.\venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Copy the example environment file:

```bash
copy .env.example .env
```

Edit `.env` with your credentials:

```env
# OpenAI
OPENAI_API_KEY=sk-your-key-here

# Twilio WhatsApp
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Security
SECRET_KEY=your-random-secret-key
ENCRYPTION_KEY=your-encryption-key

# Database (optional for now)
DATABASE_URL=sqlite:///./data/multiagent.db
```

### 5. Setup Gmail OAuth (Optional but Recommended)

Create Google Cloud Project and enable Gmail API:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download credentials as `credentials.json`
6. Save to `./credentials/credentials.json`

Run setup script:

```bash
python scripts/setup_gmail_auth.py --user-id default --test
```

This will:
- Open browser for Google authentication
- Save OAuth token
- Test Gmail access

### 6. Setup Twilio WhatsApp

1. Sign up at [Twilio](https://www.twilio.com/)
2. Enable WhatsApp in Twilio Console
3. Get your WhatsApp sandbox number
4. Configure webhook URL (see below)

## 🧪 Testing

### Test Locally Without WhatsApp

Run the test suite:

```bash
python scripts/test_system.py
```

This tests:
- ✅ Planner Agent
- ✅ Extraction Agent
- ✅ Validator Agent
- ✅ Basic conversation flow

### Test with Manual API Call

Start the server:

```bash
python main.py
```

In another terminal, test with curl:

```bash
curl -X POST http://localhost:8000/test ^
  -H "Content-Type: application/json" ^
  -d "{\"from\": \"+1234567890\", \"message\": \"Hello, can you help me?\"}"
```

## 🌐 Deploy for Production

### Option 1: Local with ngrok (Development)

1. Install ngrok: https://ngrok.com/
2. Start server: `python main.py`
3. In another terminal: `ngrok http 8000`
4. Copy the ngrok URL (e.g., `https://abc123.ngrok.io`)
5. Set Twilio webhook to: `https://abc123.ngrok.io/webhook/whatsapp`

### Option 2: Cloud Deployment

#### Deploy to Heroku

```bash
# Install Heroku CLI
# Login
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set OPENAI_API_KEY=your-key
heroku config:set TWILIO_ACCOUNT_SID=your-sid
# ... set all other env vars

# Deploy
git push heroku main

# Set webhook
# URL: https://your-app-name.herokuapp.com/webhook/whatsapp
```

#### Deploy to AWS/Azure/GCP

- Use Docker container
- Set up environment variables
- Configure webhook URL
- Ensure HTTPS enabled

## 📞 Configure Twilio Webhook

1. Go to [Twilio Console](https://console.twilio.com/)
2. Navigate to Messaging → Settings → WhatsApp Sandbox
3. Set "When a message comes in" webhook to:
   - `https://your-domain.com/webhook/whatsapp`
   - Method: POST
4. Set "Status Callback URL" (optional):
   - `https://your-domain.com/webhook/status`
   - Method: POST

## 🔧 Configuration Options

### Agent Configuration

In `.env`:

```env
# Agent settings
MAX_ITERATIONS=5          # Max replanning attempts
AGENT_TIMEOUT=30          # Timeout in seconds
ENABLE_MEMORY=True        # Enable conversation memory
ENABLE_VALIDATION=True    # Enable data validation
```

### Memory Settings

```env
# Vector store
CHROMA_PERSIST_DIR=./data/chroma
VECTOR_DIMENSION=1536
```

### Logging

```env
LOG_LEVEL=INFO           # DEBUG, INFO, WARNING, ERROR
LOG_FILE=./logs/multiagent.log
```

## 🎯 Usage Examples

### Example 1: Check Email for Bill

**User:** "What is my last electricity bill amount? Check my email."

**System:**
1. Planner creates plan to search email
2. Email agent searches for "electricity bill"
3. Extraction agent extracts amount
4. Validator verifies data
5. Responds with bill amount

### Example 2: General Query

**User:** "Hello, how are you?"

**System:**
1. Planner recognizes as general conversation
2. Responds conversationally
3. No tool execution needed

### Example 3: Complex Multi-Step

**User:** "Find my last 3 bills and calculate the average"

**System:**
1. Planner creates multi-step plan
2. Email agent searches emails
3. Extraction agent extracts amounts
4. Validator verifies each
5. Calculates average
6. Responds with result

## 🐛 Troubleshooting

### Gmail Authentication Issues

```bash
# Delete old token and re-authenticate
rm ./credentials/token_*.json
python scripts/setup_gmail_auth.py --user-id default
```

### Twilio Connection Issues

- Verify credentials in `.env`
- Check Twilio account status
- Ensure webhook URL is accessible (use ngrok for testing)

### Memory/Vector Store Issues

```bash
# Clear ChromaDB data
rm -rf ./data/chroma
# Restart system
python main.py
```

### OpenAI API Errors

- Check API key is valid
- Verify account has credits
- Check rate limits

## 📊 Monitoring

### Check Logs

```bash
# View real-time logs
tail -f ./logs/multiagent.log

# Search for errors
grep ERROR ./logs/multiagent.log
```

### Health Check

```bash
curl http://localhost:8000/health
```

## 🔐 Security Best Practices

1. **Never commit `.env` file** - Use `.env.example` as template
2. **Rotate keys regularly** - Especially OAuth tokens
3. **Use HTTPS in production** - Never HTTP for webhooks
4. **Limit permissions** - Only grant necessary scopes
5. **Monitor access logs** - Check for unauthorized access
6. **Encrypt sensitive data** - Use encryption for tokens

## 📚 Next Steps

1. ✅ Complete basic setup
2. ✅ Test locally
3. ✅ Deploy to cloud
4. ✅ Configure Twilio webhook
5. ✅ Test with real WhatsApp messages
6. 📈 Add custom agents/tools
7. 📈 Implement database storage
8. 📈 Add analytics/monitoring

## 🤝 Support

For issues or questions:
- Check logs: `./logs/multiagent.log`
- Review configuration: `.env`
- Test components: `python scripts/test_system.py`

## 📖 Architecture Documentation

See [README.md](README.md) for detailed architecture information.

---

**Ready to go!** 🚀

Start the system:
```bash
python main.py
```
