# 🚀 Quick Reference Guide - Railway Intelligence System

## ⚡ Quick Start Commands

```bash
# Setup
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt

# Configure
copy .env.example .env
# Edit .env and add GEMINI_API_KEY

# Run
python main.py
```

## 📝 Common Tasks

### 1. Run a Demo
```python
from orchestrator import RailwayOrchestrator

orchestrator = RailwayOrchestrator()
result = orchestrator.run(
    "Train 12627 delayed by 45 minutes",
    {"train_number": "12627", "delay_minutes": 45}
)
```

### 2. Query Passenger Info
```python
result = orchestrator.run(
    "What trains go from Bangalore to Delhi?",
    {"origin": "Bangalore", "destination": "Delhi"}
)
```

### 3. Check Overcrowding
```python
result = orchestrator.run(
    "Predict overcrowding for train 12627 tomorrow",
    {"train_number": "12627", "travel_date": "2025-12-24"}
)
```

## 🔧 Configuration

### Environment Variables
```env
# Required
GEMINI_API_KEY=your_key_here

# Optional - SMS
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=+1234567890

# Optional - Email  
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

### Agent Settings (config.py)
```python
AGENT_CONFIG = {
    "planner": {
        "temperature": 0.7,    # Creativity level
        "max_tokens": 2048     # Response length
    },
    "operations": {
        "temperature": 0.3     # More deterministic
    }
}
```

## 📊 System Components

### Agents
| Agent | Purpose | Input | Output |
|-------|---------|-------|--------|
| Planner | Task decomposition | Request + Context | Execution plan |
| Operations | Delay analysis | Train + Delay | Impact analysis |
| Passenger | Query answering | Question | RAG-powered answer |
| Crowd | Capacity prediction | Train + Date | Occupancy forecast |
| Alert | Notifications | Alert spec | Delivery status |

### Tools
| Tool | Function | Used By |
|------|----------|---------|
| TrainScheduleTool | Schedule access | Operations |
| DelaySimulator | Propagation modeling | Operations |
| CrowdPredictor | Occupancy prediction | Crowd |
| BookingAnalyzer | Booking patterns | Crowd |
| NotificationService | Multi-channel alerts | Alert |

## 🎯 Use Case Templates

### Template 1: Delay Response
```python
request = "Train {train_number} delayed by {minutes} minutes"
context = {
    "train_number": "12627",
    "delay_minutes": 45,
    "current_location": "Station Name",
    "affected_passengers": 850
}
```

### Template 2: Passenger Query
```python
request = "Passenger query about {topic}"
context = {
    "query": "What is the refund policy?",
    "passenger_id": "P1234",
    "booking_reference": "PNR123456"
}
```

### Template 3: Capacity Planning
```python
request = "Analyze capacity for train {train_number}"
context = {
    "train_number": "12627",
    "travel_date": "2025-12-25",
    "is_holiday": True
}
```

## 🔍 Debugging

### Enable Verbose Logging
```python
# In config.py
LOG_LEVEL = "DEBUG"
```

### Check Agent State
```python
orchestrator = RailwayOrchestrator()
orchestrator.run(request, context)
state = orchestrator.planner.get_state()
print(state)
```

### Test Individual Agents
```python
from agents import OperationsAgent

ops = OperationsAgent()
result = ops.analyze_delay("12627", 45, "Katpadi")
print(result)
```

## 📈 Performance Tips

### 1. Optimize RAG Retrieval
```python
# In rag_system.py
result = rag.retrieve(query, top_k=3)  # Reduce results
```

### 2. Adjust Agent Temperature
```python
# Lower = more deterministic, faster
"temperature": 0.2  
```

### 3. Limit Iterations
```python
result = orchestrator.run(request, context, max_iterations=1)
```

## 🛠️ Customization

### Add New Agent
```python
# Create agents/my_agent.py
class MyAgent:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-pro")
    
    def process(self, input_data):
        # Your logic here
        return result

# Register in orchestrator.py
self.my_agent = MyAgent()
workflow.add_node("my_agent", self._my_agent_node)
```

### Add New Tool
```python
# Create tools/my_tool.py
class MyTool:
    def execute(self, params):
        # Your tool logic
        return result

# Use in agent
from tools.my_tool import MyTool
self.my_tool = MyTool()
```

### Add RAG Data
```python
# Add to data/rag/my_data.json
# Update config.py
RAG_DATA_SOURCES = {
    "my_data": "./data/rag/my_data.json"
}

# Initialize
rag.initialize_data()
```

## 📚 API Reference (Future)

### Orchestrator
```python
orchestrator.run(request, context, max_iterations)
# Returns: Dict with results from all agents
```

### Individual Agents
```python
planner.analyze_request(request, context)
operations.analyze_delay(train_number, delay_minutes)
passenger.answer_query(query, passenger_context)
crowd.predict_overcrowding(train_number, travel_date)
alert.create_alert(alert_type, target_audience, context)
```

## 🐛 Common Issues

### Issue: "No module named 'google.generativeai'"
**Fix**: `pip install google-generativeai`

### Issue: "API key not found"
**Fix**: Check `.env` file has `GEMINI_API_KEY=your_key`

### Issue: "ChromaDB error"
**Fix**: `pip install --upgrade chromadb`

### Issue: "LangGraph import error"
**Fix**: `pip install langgraph langchain`

## 📞 Quick Links

- 📖 [Full Documentation](README.md)
- 🔧 [Setup Guide](SETUP.md)
- 📊 [Project Overview](PROJECT_OVERVIEW.md)
- 🔑 [Get Gemini API Key](https://makersuite.google.com/app/apikey)
- 💬 [Report Issues](https://github.com/your-repo/issues)

## 💡 Pro Tips

1. **Start Simple**: Test with demo scenarios first
2. **Check Logs**: Enable DEBUG mode for troubleshooting
3. **Iterate Fast**: Use lower temperatures for faster responses
4. **Cache Results**: Implement Redis for production
5. **Monitor Usage**: Track API calls to manage costs
6. **Extend Gradually**: Add features one at a time
7. **Test Thoroughly**: Write tests for custom agents

## 🎓 Learning Path

1. **Beginner**: Run demos, understand flow
2. **Intermediate**: Modify prompts, add data
3. **Advanced**: Create agents, build tools
4. **Expert**: Architecture changes, optimizations

---

**Need Help?** Check docs or open an issue!
**Ready to Build?** Start with `python main.py`! 🚀
