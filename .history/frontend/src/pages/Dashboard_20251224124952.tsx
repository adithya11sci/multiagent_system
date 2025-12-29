import { useEffect, useState } from 'react'
import { 
  ClockIcon, 
  UserGroupIcon, 
  UsersIcon, 
  BellIcon,
  ChartBarIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline'
import { Link } from 'react-router-dom'
import apiService from '../services/api'
import toast from 'react-hot-toast'

interface AgentStatus {
  status: string
  description: string
}

interface SystemHealth {
  status: string
  orchestrator: boolean
  rag_system: boolean
  agents: {
    [key: string]: boolean
  }
}

export default function Dashboard() {
  const [health, setHealth] = useState<SystemHealth | null>(null)
  const [loading, setLoading] = useState(true)
  const [agentStats, setAgentStats] = useState<Record<string, AgentStatus>>({})

  useEffect(() => {
    loadDashboardData()
    // Refresh every 30 seconds
    const interval = setInterval(loadDashboardData, 30000)
    return () => clearInterval(interval)
  }, [])

  const loadDashboardData = async () => {
    try {
      const [healthData, agentsData] = await Promise.all([
        apiService.healthCheck(),
        apiService.getAgentsStatus(),
      ])
      setHealth(healthData)
      setAgentStats(agentsData)
      setLoading(false)
    } catch (error) {
      console.error('Failed to load dashboard data:', error)
      toast.error('Failed to connect to backend. Make sure the API server is running.')
      setLoading(false)
    }
  }

  const quickActions = [
    {
      name: 'Report Train Delay',
      description: 'Handle train delays with automated responses',
      icon: ClockIcon,
      href: '/train-delay',
      color: 'bg-orange-500',
    },
    {
      name: 'Passenger Query',
      description: 'Answer customer questions using AI',
      icon: UserGroupIcon,
      href: '/passenger-query',
      color: 'bg-blue-500',
    },
    {
      name: 'Crowd Prediction',
      description: 'Predict overcrowding and optimize capacity',
      icon: UsersIcon,
      href: '/crowd-prediction',
      color: 'bg-purple-500',
    },
    {
      name: 'Send Alert',
      description: 'Multi-channel notifications',
      icon: BellIcon,
      href: '/alerts',
      color: 'bg-red-500',
    },
  ]

  const stats = [
    {
      name: 'Active Agents',
      value: health ? Object.values(health.agents).filter(Boolean).length : 0,
      total: 5,
      icon: ChartBarIcon,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
    },
    {
      name: 'System Status',
      value: health?.status === 'healthy' ? 'Healthy' : 'Offline',
      icon: CheckCircleIcon,
      color: health?.status === 'healthy' ? 'text-green-600' : 'text-red-600',
      bgColor: health?.status === 'healthy' ? 'bg-green-100' : 'bg-red-100',
    },
    {
      name: 'RAG System',
      value: health?.rag_system ? 'Active' : 'Inactive',
      icon: ChartBarIcon,
      color: health?.rag_system ? 'text-green-600' : 'text-orange-600',
      bgColor: health?.rag_system ? 'bg-green-100' : 'bg-orange-100',
    },
  ]

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 rounded-lg shadow-lg p-8 text-white">
        <h1 className="text-3xl font-bold mb-2">Welcome to Railway Intelligence System</h1>
        <p className="text-blue-100">
          AI-powered multi-agent system for autonomous railway management
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {stats.map((stat) => (
          <div key={stat.name} className="card">
            <div className="flex items-center">
              <div className={`flex-shrink-0 rounded-md p-3 ${stat.bgColor}`}>
                <stat.icon className={`h-6 w-6 ${stat.color}`} />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    {stat.name}
                  </dt>
                  <dd className="flex items-baseline">
                    <div className={`text-2xl font-semibold ${stat.color}`}>
                      {stat.value}
                      {stat.total && (
                        <span className="text-sm text-gray-500 ml-1">/ {stat.total}</span>
                      )}
                    </div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
          {quickActions.map((action) => (
            <Link
              key={action.name}
              to={action.href}
              className="card hover:shadow-lg transition-shadow duration-200"
            >
              <div className="flex items-center space-x-3">
                <div className={`flex-shrink-0 rounded-lg ${action.color} p-3`}>
                  <action.icon className="h-6 w-6 text-white" />
                </div>
                <div>
                  <h3 className="text-sm font-medium text-gray-900">{action.name}</h3>
                  <p className="text-xs text-gray-500 mt-1">{action.description}</p>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>

      {/* Agent Status */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Agent Status</h2>
        <div className="space-y-3">
          {Object.entries(agentStats).map(([name, agent]) => (
            <div key={name} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div>
                <h3 className="text-sm font-medium text-gray-900 capitalize">{name} Agent</h3>
                <p className="text-xs text-gray-500">{agent.description}</p>
              </div>
              <span className={`badge ${
                agent.status === 'active' ? 'badge-success' : 'badge-error'
              }`}>
                {agent.status}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* System Info */}
      <div className="card bg-blue-50 border border-blue-100">
        <div className="flex items-start">
          <div className="flex-shrink-0">
            <svg className="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-blue-900">About This System</h3>
            <p className="mt-2 text-sm text-blue-700">
              This multi-agent AI system uses 5 specialized agents powered by Google Gemini Pro and orchestrated with LangGraph. 
              Each agent is an expert in their domain, working together to provide intelligent railway management solutions.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
