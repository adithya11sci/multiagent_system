import axios, { AxiosInstance, AxiosRequestConfig } from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

class ApiService {
  private api: AxiosInstance

  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Request interceptor
    this.api.interceptors.request.use(
      (config) => {
        console.log('API Request:', config.method?.toUpperCase(), config.url)
        return config
      },
      (error) => {
        return Promise.reject(error)
      }
    )

    // Response interceptor
    this.api.interceptors.response.use(
      (response) => {
        console.log('API Response:', response.status, response.data)
        return response
      },
      (error) => {
        console.error('API Error:', error.response?.data || error.message)
        return Promise.reject(error)
      }
    )
  }

  // Health check
  async healthCheck() {
    const response = await this.api.get('/api/health')
    return response.data
  }

  // Main orchestration
  async orchestrate(request: string, context?: any) {
    const response = await this.api.post('/api/orchestrate', {
      request,
      context: context || {},
    })
    return response.data
  }

  // Train delay
  async handleTrainDelay(data: {
    train_number: string
    delay_minutes: number
    current_location: string
    affected_passengers?: number
  }) {
    const response = await this.api.post('/api/train-delay', data)
    return response.data
  }

  // Passenger query
  async passengerQuery(query: string, passenger_id?: string) {
    const response = await this.api.post('/api/passenger-query', {
      query,
      passenger_id,
    })
    return response.data
  }

  // Crowd prediction
  async predictCrowd(data: {
    train_number: string
    route: string
    time?: string
  }) {
    const response = await this.api.post('/api/crowd-prediction', data)
    return response.data
  }

  // Send alert
  async sendAlert(data: {
    message: string
    recipients: string[]
    channels: string[]
  }) {
    const response = await this.api.post('/api/send-alert', data)
    return response.data
  }

  // Get agents status
  async getAgentsStatus() {
    const response = await this.api.get('/api/agents/status')
    return response.data
  }

  // Query RAG
  async queryRAG(query: string) {
    const response = await this.api.get('/api/rag/query', {
      params: { query },
    })
    return response.data
  }

  // Get demo scenarios
  async getDemoScenarios() {
    const response = await this.api.get('/api/demo/scenarios')
    return response.data
  }

  // WebSocket connection
  createWebSocket(): WebSocket {
    const wsUrl = API_BASE_URL.replace('http', 'ws') + '/ws'
    return new WebSocket(wsUrl)
  }
}

export default new ApiService()
