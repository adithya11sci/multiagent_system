# Multi-Agent WhatsApp System

A production-ready multi-agent system that processes WhatsApp messages using LangChain orchestration, MCP tool standardization, and context-aware reasoning.

## 🎯 What This System Does

- ✅ Receives and processes WhatsApp messages
- ✅ Understands user intent using AI
- ✅ Uses multiple specialized agents (Planner, Email, Extraction, Validator)
- ✅ Accesses tools securely via MCP (Model Context Protocol)
- ✅ Maintains conversation memory and context
- ✅ Returns grounded, verified answers
- ✅ Reads emails, databases, and APIs as needed

## 🏗️ Architecture

```
WhatsApp User
     │
     ▼
WhatsApp Business API / Twilio
     │
     ▼
Message Ingestion Service
     │
     ▼
LangChain Orchestrator (Brain)
     │
 ┌───┴───────────────┐
 │                   │
 ▼                   ▼
Planner Agent     Memory Manager
 │                   │
 ▼                   ▼
Tool Agents       Context Store
 │
 ▼
MCP Tool Layer
 │
 ▼
Email / DB / APIs / Search
```

## 🔧 Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your credentials
```

### 3. Set Up Google OAuth for Email

```bash
python scripts/setup_gmail_auth.py
```

### 4. Run the System

```bash
python main.py
```

## 📁 Project Structure

```
multiagent/
├── agents/              # Individual agent implementations
├── context/            # Context Protocol implementation
├── memory/             # Memory management
├── mcp/                # MCP tool layer
├── services/           # WhatsApp, Email services
├── orchestrator/       # LangChain orchestration
├── security/           # Authentication & authorization
├── utils/              # Utilities
└── main.py            # Entry point
```

## 🧠 Agent Roles

| Agent | Responsibility |
|-------|---------------|
| **Planner Agent** | Task breakdown, intent understanding |
| **Email Agent** | Email access and search |
| **Extraction Agent** | Data parsing from emails/documents |
| **Validator Agent** | Truth checking, anti-hallucination |
| **Memory Agent** | Context retention across conversations |

## 🛡️ Security Features

- ✅ OAuth 2.0 for email access
- ✅ MCP scope enforcement
- ✅ Per-user context isolation
- ✅ No cross-user memory leakage
- ✅ Encrypted token storage

## 📊 Example Flow

**User:** "What is my last electricity bill amount? Check my email."

1. **Planner Agent** understands intent → needs email search
2. **Email Agent** searches Gmail for "electricity bill"
3. **Extraction Agent** extracts bill amount from email
4. **Validator Agent** verifies data authenticity
5. **Memory Agent** stores the interaction
6. **Response:** "Your latest electricity bill from TNEB for June 2025 is ₹1,245."

## 🚀 Features

- **Multi-Agent Orchestration**: LangChain-powered reasoning
- **Tool Standardization**: MCP for secure, vendor-neutral tool access
- **Context Management**: Persistent conversation context
- **Memory System**: Vector DB + summary memory
- **Validation Layer**: Anti-hallucination checks
- **WhatsApp Integration**: Twilio-based messaging

## 📝 License

MIT License
