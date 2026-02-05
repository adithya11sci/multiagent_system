"""
FastAPI Server for Railway Intelligence Multi-Agent System
Provides REST API endpoints for frontend interaction
"""
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import asyncio
import json
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import orchestrator and RAG lazily to avoid blocking startup
orchestrator_module = None
rag_module = None

def lazy_import_orchestrator():
    """Lazy import of orchestrator to avoid blocking startup"""
    global orchestrator_module
    if orchestrator_module is None:
        from orchestrator import RailwayOrchestrator
        orchestrator_module = RailwayOrchestrator
    return orchestrator_module

def lazy_import_rag():
    """Lazy import of RAG system to avoid blocking startup"""
    global rag_module
    if rag_module is None:
        try:
            from rag.rag_system import RAGSystem
            rag_module = RAGSystem
        except Exception as e:
            print(f"⚠️  Could not import RAG system: {e}")
            rag_module = None
    return rag_module

# Initialize FastAPI app
app = FastAPI(
    title="Railway Intelligence Multi-Agent System API",
    description="AI-powered railway management system with specialized agents",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
orchestrator: Optional[Any] = None
rag_system: Optional[Any] = None
active_connections: List[WebSocket] = []

# Pydantic models for request/response
class RequestModel(BaseModel):
    request: str
    context: Optional[Dict[str, Any]] = {}

class ResponseModel(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: str

class TrainDelayRequest(BaseModel):
    train_number: str
    delay_minutes: int
    current_location: str
    affected_passengers: Optional[int] = 0

class PassengerQueryRequest(BaseModel):
    query: str
    passenger_id: Optional[str] = None


class AlertRequest(BaseModel):
    message: str
    recipients: List[str]
    channels: List[str]  # sms, email, push

# Background initialization
async def initialize_components():
    """Initialize heavy components in background to not block server startup"""
    global orchestrator, rag_system
    
    try:
        # Try to initialize RAG system
        print("📚 Loading RAG system in background...")
        RAGSystem = lazy_import_rag()
        if RAGSystem:
            try:
                rag_system = RAGSystem()
                rag_system.initialize_data()
                print("✅ RAG system initialized")
            except Exception as e:
                print(f"⚠️  RAG system initialization failed: {e}")
                rag_system = None
        else:
            print("⚠️  RAG system not available")
        
        # Try to initialize orchestrator
        print("🧠 Loading orchestrator in background...")
        RailwayOrchestrator = lazy_import_orchestrator()
        if RailwayOrchestrator:
            orchestrator = RailwayOrchestrator()
            print("✅ Orchestrator initialized")
        
    except Exception as e:
        print(f"⚠️  Background initialization error: {e}")
        print("   Server running with limited features")

# Lifecycle events
@app.on_event("startup")
async def startup_event():
    """Initialize system on startup"""
    global orchestrator, rag_system
    
    print("🚂 Starting Railway Intelligence System API...")
    print("⏰ Server started successfully - AI components will initialize in background")
    print("✅ API Server ready on http://localhost:8000")
    
    # Initialize components in background (non-blocking)
    asyncio.create_task(initialize_components())

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("🛑 Shutting down Railway Intelligence System API...")
    # Close any active websocket connections
    for connection in active_connections:
        await connection.close()

# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {
        "status": "online",
        "service": "Railway Intelligence Multi-Agent System",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "orchestrator": orchestrator is not None,
        "rag_system": rag_system is not None,
        "agents": {
            "planner": True,
            "operations": True,
            "passenger": True,
            "alert": True
        },
        "timestamp": datetime.now().isoformat()
    }

# Main orchestration endpoint
@app.post("/api/orchestrate", response_model=ResponseModel)
async def orchestrate_request(request: RequestModel):
    """
    Main endpoint to process requests through the multi-agent system
    """
    try:
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not initialized")
        
        # Run orchestration
        result = orchestrator.run(request.request, request.context)
        
        return ResponseModel(
            success=True,
            data=result,
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        return ResponseModel(
            success=False,
            error=str(e),
            timestamp=datetime.now().isoformat()
        )

# Specialized endpoints
@app.post("/api/train-delay", response_model=ResponseModel)
async def handle_train_delay(delay_request: TrainDelayRequest):
    """Handle train delay scenario"""
    try:
        request = f"Train {delay_request.train_number} is delayed by {delay_request.delay_minutes} minutes at {delay_request.current_location}"
        
        context = {
            "train_number": delay_request.train_number,
            "delay_minutes": delay_request.delay_minutes,
            "current_location": delay_request.current_location,
            "affected_passengers": delay_request.affected_passengers
        }
        
        result = orchestrator.run(request, context)
        
        return ResponseModel(
            success=True,
            data=result,
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        return ResponseModel(
            success=False,
            error=str(e),
            timestamp=datetime.now().isoformat()
        )

@app.post("/api/passenger-query", response_model=ResponseModel)
async def handle_passenger_query(query_request: PassengerQueryRequest):
    """Handle passenger queries using RAG"""
    try:
        request = query_request.query
        context = {}
        if query_request.passenger_id:
            context["passenger_id"] = query_request.passenger_id
        
        result = orchestrator.run(request, context)
        
        return ResponseModel(
            success=True,
            data=result,
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        return ResponseModel(
            success=False,
            error=str(e),
            timestamp=datetime.now().isoformat()
        )


@app.post("/api/send-alert", response_model=ResponseModel)
async def send_alert(alert_request: AlertRequest):
    """Send alerts through multiple channels"""
    try:
        request = f"Send alert: {alert_request.message}"
        
        context = {
            "message": alert_request.message,
            "recipients": alert_request.recipients,
            "channels": alert_request.channels
        }
        
        result = orchestrator.run(request, context)
        
        return ResponseModel(
            success=True,
            data=result,
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        return ResponseModel(
            success=False,
            error=str(e),
            timestamp=datetime.now().isoformat()
        )

# Agent status endpoints
@app.get("/api/agents/status")
async def get_agents_status():
    """Get status of all agents"""
    return {
        "planner": {"status": "active", "description": "Master coordinator"},
        "operations": {"status": "active", "description": "Train operations management"},
        "passenger": {"status": "active", "description": "Customer service with RAG"},
        "alert": {"status": "active", "description": "Multi-channel alerts"},
        "timestamp": datetime.now().isoformat()
    }

# RAG endpoints
@app.get("/api/rag/query")
async def query_rag(query: str):
    """Query RAG system directly"""
    try:
        if not rag_system:
            raise HTTPException(status_code=503, detail="RAG system not initialized")
        
        results = rag_system.query(query)
        
        return {
            "success": True,
            "query": query,
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

# WebSocket endpoint for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time updates"""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            # Keep connection alive and send periodic updates
            await websocket.send_json({
                "type": "heartbeat",
                "timestamp": datetime.now().isoformat()
            })
            await asyncio.sleep(30)
    
    except WebSocketDisconnect:
        active_connections.remove(websocket)

async def broadcast_update(data: Dict[str, Any]):
    """Broadcast updates to all connected WebSocket clients"""
    for connection in active_connections:
        try:
            await connection.send_json(data)
        except:
            active_connections.remove(connection)

# Demo scenarios
@app.get("/api/demo/scenarios")
async def get_demo_scenarios():
    """Get list of demo scenarios"""
    return {
        "scenarios": [
            {
                "id": "delay",
                "name": "Train Delay",
                "description": "Handle train delay with automated responses",
                "example": {
                    "train_number": "12627",
                    "delay_minutes": 45,
                    "current_location": "Katpadi"
                }
            },
            {
                "id": "passenger",
                "name": "Passenger Query",
                "description": "Answer passenger questions using RAG",
                "example": {
                    "query": "What is the refund policy for cancelled trains?"
                }
            },

            {
                "id": "emergency",
                "name": "Emergency Alert",
                "description": "Multi-channel emergency notifications",
                "example": {
                    "message": "Track maintenance on Platform 3",
                    "channels": ["sms", "email", "push"]
                }
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
