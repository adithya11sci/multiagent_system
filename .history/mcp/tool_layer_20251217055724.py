"""
MCP (Model Context Protocol) Tool Layer
Standardizes tool access with security and scope enforcement
"""
from typing import Dict, Any, List, Optional, Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import json

from context.context_protocol import UserContext


class ToolCapability(str, Enum):
    """Tool capabilities"""
    READ = "read"
    WRITE = "write"
    SEARCH = "search"
    EXECUTE = "execute"
    DELETE = "delete"


class ToolScope(str, Enum):
    """Tool access scopes"""
    EMAIL_READ = "email.read"
    EMAIL_SEND = "email.send"
    DB_READ = "db.read"
    DB_WRITE = "db.write"
    API_CALL = "api.call"
    FILE_READ = "file.read"
    FILE_WRITE = "file.write"


@dataclass
class ToolDefinition:
    """MCP Tool Definition"""
    name: str
    description: str
    capabilities: List[ToolCapability]
    scopes: List[ToolScope]
    parameters: Dict[str, Any]
    version: str = "1.0.0"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "capabilities": [c.value for c in self.capabilities],
            "scopes": [s.value for s in self.scopes],
            "parameters": self.parameters,
            "version": self.version
        }


class MCPTool(ABC):
    """
    Base class for MCP-compliant tools
    All tools must implement this interface
    """
    
    def __init__(self, definition: ToolDefinition):
        self.definition = definition
    
    @abstractmethod
    async def execute(
        self,
        context: UserContext,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute the tool with given parameters
        Must check context permissions before execution
        """
        pass
    
    def validate_context(self, context: UserContext) -> bool:
        """Validate if context has required permissions"""
        for scope in self.definition.scopes:
            if not context.has_permission(scope.value):
                return False
        return True
    
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """Validate if all required parameters are provided"""
        required_params = self.definition.parameters.get("required", [])
        for param in required_params:
            if param not in parameters:
                return False
        return True
    
    def get_definition(self) -> Dict[str, Any]:
        """Get tool definition"""
        return self.definition.to_dict()


class MCPToolRegistry:
    """
    Registry for MCP tools
    Manages tool discovery and access
    """
    
    def __init__(self):
        self._tools: Dict[str, MCPTool] = {}
    
    def register_tool(self, tool: MCPTool):
        """Register a new tool"""
        self._tools[tool.definition.name] = tool
    
    def unregister_tool(self, tool_name: str):
        """Unregister a tool"""
        if tool_name in self._tools:
            del self._tools[tool_name]
    
    def get_tool(self, tool_name: str) -> Optional[MCPTool]:
        """Get tool by name"""
        return self._tools.get(tool_name)
    
    def list_tools(
        self,
        context: Optional[UserContext] = None
    ) -> List[Dict[str, Any]]:
        """
        List all available tools
        If context provided, filter by permissions
        """
        tools = []
        for tool in self._tools.values():
            if context is None or tool.validate_context(context):
                tools.append(tool.get_definition())
        return tools
    
    def discover_tools(
        self,
        capability: Optional[ToolCapability] = None,
        scope: Optional[ToolScope] = None
    ) -> List[str]:
        """Discover tools by capability or scope"""
        matching_tools = []
        
        for name, tool in self._tools.items():
            if capability and capability not in tool.definition.capabilities:
                continue
            if scope and scope not in tool.definition.scopes:
                continue
            matching_tools.append(name)
        
        return matching_tools
    
    async def execute_tool(
        self,
        tool_name: str,
        context: UserContext,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a tool with security checks
        """
        tool = self.get_tool(tool_name)
        
        if not tool:
            return {
                "success": False,
                "error": f"Tool '{tool_name}' not found"
            }
        
        # Validate context permissions
        if not tool.validate_context(context):
            return {
                "success": False,
                "error": f"Insufficient permissions for tool '{tool_name}'"
            }
        
        # Validate parameters
        if not tool.validate_parameters(parameters):
            return {
                "success": False,
                "error": f"Invalid parameters for tool '{tool_name}'"
            }
        
        try:
            result = await tool.execute(context, parameters)
            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# Global tool registry
mcp_registry = MCPToolRegistry()
