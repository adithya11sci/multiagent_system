import { useEffect, useState } from 'react'
import { CpuChipIcon, CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/outline'
import apiService from '../services/api'
import toast from 'react-hot-toast'

interface AgentStatus {
  status: string
  description: string
}

export default function Agents() {
  const [agents, setAgents] = useState<Record<string, AgentStatus>>({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadAgents()
    const interval = setInterval(loadAgents, 10000) // Refresh every 10 seconds
    return () => clearInterval(interval)
  }, [])

  const loadAgents = async () => {
    try {
      const data = await apiService.getAgentsStatus()
      setAgents(data)
      setLoading(false)
    } catch (error) {
      console.error('Failed to load agents:', error)
      toast.error('Failed to load agent status')
      setLoading(false)
    }
  }

  const agentDetails = [
    {
      name: 'planner',
      title: 'Planner Agent',
      icon: '🧠',
      color: 'purple',
      capabilities: [
        'Request analysis and decomposition',
        'Task planning and coordination',
        'Agent selection and routing',
        'Execution plan generation',
      ],
    },
    {
      name: 'operations',
      title: 'Operations Agent',
      icon: '⚙️',
      color: 'orange',
      capabilities: [
        'Train delay management',
        'Schedule optimization',
        'Resource allocation',
        'Cascading impact analysis',
      ],
    },
    {
      name: 'passenger',
      title: 'Passenger Agent',
      icon: '👥',
      color: 'blue',
      capabilities: [
        'RAG-powered query answering',
        'Policy and refund information',
        'Alternative route suggestions',
        'Customer service automation',
      ],
    },
    {
      name: 'crowd',
      title: 'Crowd Agent',
      icon: '📊',
      color: 'green',
      capabilities: [
        'Overcrowding prediction',
        'Capacity optimization',
        'Historical pattern analysis',
        'Proactive recommendations',
      ],
    },
    {
      name: 'alert',
      title: 'Alert Agent',
      icon: '🔔',
      color: 'red',
      capabilities: [
        'Multi-channel notifications',
        'SMS via Twilio',
        'Email via SMTP',
        'Push notifications',
      ],
    },
  ]

  const colorClasses = {
    purple: 'bg-purple-50 border-purple-200 text-purple-900',
    orange: 'bg-orange-50 border-orange-200 text-orange-900',
    blue: 'bg-blue-50 border-blue-200 text-blue-900',
    green: 'bg-green-50 border-green-200 text-green-900',
    red: 'bg-red-50 border-red-200 text-red-900',
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading agents...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">AI Agent Status</h1>
        <p className="mt-1 text-sm text-gray-500">
          Monitor and manage specialized AI agents in the multi-agent system
        </p>
      </div>

      {/* System Overview */}
      <div className="card bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-100">
        <div className="flex items-start">
          <CpuChipIcon className="h-8 w-8 text-blue-600 mr-4" />
          <div>
            <h2 className="text-lg font-semibold text-gray-900 mb-2">Multi-Agent Architecture</h2>
            <p className="text-sm text-gray-700 mb-3">
              This system uses 5 specialized AI agents powered by Google Gemini Pro and orchestrated with LangGraph. 
              Each agent is an expert in their domain, working collaboratively to handle complex railway management tasks.
            </p>
            <div className="flex items-center space-x-4 text-sm">
              <div className="flex items-center">
                <CheckCircleIcon className="h-5 w-5 text-green-600 mr-1" />
                <span className="text-gray-700">LangGraph Orchestration</span>
              </div>
              <div className="flex items-center">
                <CheckCircleIcon className="h-5 w-5 text-green-600 mr-1" />
                <span className="text-gray-700">Gemini Pro AI</span>
              </div>
              <div className="flex items-center">
                <CheckCircleIcon className="h-5 w-5 text-green-600 mr-1" />
                <span className="text-gray-700">RAG System</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Agent Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {agentDetails.map((agent) => {
          const status = agents[agent.name]
          const isActive = status?.status === 'active'
          
          return (
            <div
              key={agent.name}
              className={`card border-2 ${colorClasses[agent.color as keyof typeof colorClasses]}`}
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center">
                  <span className="text-3xl mr-3">{agent.icon}</span>
                  <div>
                    <h3 className="text-lg font-semibold">{agent.title}</h3>
                    <p className="text-sm opacity-75">{status?.description}</p>
                  </div>
                </div>
                <div className="flex items-center">
                  {isActive ? (
                    <CheckCircleIcon className="h-6 w-6 text-green-600" />
                  ) : (
                    <XCircleIcon className="h-6 w-6 text-red-600" />
                  )}
                </div>
              </div>

              <div className="space-y-2">
                <div className="flex items-center justify-between text-sm mb-3">
                  <span className="font-medium">Status</span>
                  <span className={`badge ${isActive ? 'badge-success' : 'badge-error'}`}>
                    {status?.status || 'unknown'}
                  </span>
                </div>

                <div>
                  <h4 className="text-sm font-medium mb-2">Capabilities</h4>
                  <ul className="space-y-1">
                    {agent.capabilities.map((capability, idx) => (
                      <li key={idx} className="text-xs flex items-start">
                        <span className="mr-2">•</span>
                        <span>{capability}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {/* Agent Workflow */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Agent Workflow</h2>
        <div className="space-y-4">
          <div className="flex items-center">
            <div className="flex-shrink-0 w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center text-purple-600 font-semibold">
              1
            </div>
            <div className="ml-4">
              <h3 className="font-medium text-gray-900">Planner Agent</h3>
              <p className="text-sm text-gray-600">Analyzes request and creates execution plan</p>
            </div>
          </div>
          
          <div className="ml-4 border-l-2 border-gray-200 h-8"></div>
          
          <div className="flex items-center">
            <div className="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 font-semibold">
              2
            </div>
            <div className="ml-4">
              <h3 className="font-medium text-gray-900">LangGraph Orchestrator</h3>
              <p className="text-sm text-gray-600">Routes tasks to appropriate specialized agents</p>
            </div>
          </div>
          
          <div className="ml-4 border-l-2 border-gray-200 h-8"></div>
          
          <div className="flex items-center">
            <div className="flex-shrink-0 w-8 h-8 bg-green-100 rounded-full flex items-center justify-center text-green-600 font-semibold">
              3
            </div>
            <div className="ml-4">
              <h3 className="font-medium text-gray-900">Specialized Agents</h3>
              <p className="text-sm text-gray-600">Execute tasks in parallel or sequence based on plan</p>
            </div>
          </div>
          
          <div className="ml-4 border-l-2 border-gray-200 h-8"></div>
          
          <div className="flex items-center">
            <div className="flex-shrink-0 w-8 h-8 bg-orange-100 rounded-full flex items-center justify-center text-orange-600 font-semibold">
              4
            </div>
            <div className="ml-4">
              <h3 className="font-medium text-gray-900">Result Synthesis</h3>
              <p className="text-sm text-gray-600">Combines results and provides final response</p>
            </div>
          </div>
        </div>
      </div>

      {/* Technical Details */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="font-semibold text-gray-900 mb-3">🎯 Key Features</h3>
          <ul className="space-y-2 text-sm text-gray-700">
            <li className="flex items-start">
              <span className="text-green-500 mr-2">✓</span>
              <span>Autonomous decision making</span>
            </li>
            <li className="flex items-start">
              <span className="text-green-500 mr-2">✓</span>
              <span>Parallel task execution</span>
            </li>
            <li className="flex items-start">
              <span className="text-green-500 mr-2">✓</span>
              <span>RAG-powered knowledge retrieval</span>
            </li>
            <li className="flex items-start">
              <span className="text-green-500 mr-2">✓</span>
              <span>Real-time coordination</span>
            </li>
          </ul>
        </div>

        <div className="card">
          <h3 className="font-semibold text-gray-900 mb-3">🔧 Technology Stack</h3>
          <ul className="space-y-2 text-sm text-gray-700">
            <li className="flex items-start">
              <span className="text-blue-500 mr-2">•</span>
              <span>Google Gemini Pro for AI reasoning</span>
            </li>
            <li className="flex items-start">
              <span className="text-blue-500 mr-2">•</span>
              <span>LangGraph for orchestration</span>
            </li>
            <li className="flex items-start">
              <span className="text-blue-500 mr-2">•</span>
              <span>ChromaDB for vector storage</span>
            </li>
            <li className="flex items-start">
              <span className="text-blue-500 mr-2">•</span>
              <span>Python FastAPI backend</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  )
}
