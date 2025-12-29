import { useState } from 'react'
import { ClockIcon } from '@heroicons/react/24/outline'
import apiService from '../services/api'
import toast from 'react-hot-toast'

export default function TrainDelay() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [formData, setFormData] = useState({
    train_number: '',
    delay_minutes: '',
    current_location: '',
    affected_passengers: '',
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setResult(null)

    try {
      const data = await apiService.handleTrainDelay({
        train_number: formData.train_number,
        delay_minutes: parseInt(formData.delay_minutes),
        current_location: formData.current_location,
        affected_passengers: formData.affected_passengers 
          ? parseInt(formData.affected_passengers) 
          : undefined,
      })

      if (data.success) {
        setResult(data.data)
        toast.success('Train delay processed successfully!')
      } else {
        toast.error(data.error || 'Failed to process delay')
      }
    } catch (error) {
      toast.error('Failed to process train delay')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const loadExample = () => {
    setFormData({
      train_number: '12627',
      delay_minutes: '45',
      current_location: 'Katpadi Junction',
      affected_passengers: '850',
    })
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Train Delay Management</h1>
          <p className="mt-1 text-sm text-gray-500">
            Handle train delays with automated AI-powered responses
          </p>
        </div>
        <button
          onClick={loadExample}
          className="btn-secondary text-sm"
        >
          Load Example
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Form */}
        <div className="card">
          <div className="flex items-center mb-4">
            <ClockIcon className="h-6 w-6 text-orange-600 mr-2" />
            <h2 className="text-lg font-semibold text-gray-900">Delay Information</h2>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Train Number *
              </label>
              <input
                type="text"
                required
                value={formData.train_number}
                onChange={(e) => setFormData({ ...formData, train_number: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="e.g., 12627"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Delay (minutes) *
              </label>
              <input
                type="number"
                required
                value={formData.delay_minutes}
                onChange={(e) => setFormData({ ...formData, delay_minutes: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="e.g., 45"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Current Location *
              </label>
              <input
                type="text"
                required
                value={formData.current_location}
                onChange={(e) => setFormData({ ...formData, current_location: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="e.g., Katpadi Junction"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Affected Passengers (optional)
              </label>
              <input
                type="number"
                value={formData.affected_passengers}
                onChange={(e) => setFormData({ ...formData, affected_passengers: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="e.g., 850"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Processing...
                </span>
              ) : (
                'Process Delay'
              )}
            </button>
          </form>
        </div>

        {/* Results */}
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">AI Response</h2>
          
          {!result && !loading && (
            <div className="text-center py-12 text-gray-400">
              <ClockIcon className="h-12 w-12 mx-auto mb-3" />
              <p>Submit delay information to see AI response</p>
            </div>
          )}

          {loading && (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <p className="text-gray-600">AI agents are processing...</p>
            </div>
          )}

          {result && (
            <div className="space-y-4">
              {result.final_response && (
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <h3 className="font-semibold text-blue-900 mb-2">Summary</h3>
                  <p className="text-sm text-blue-800 whitespace-pre-wrap">
                    {result.final_response.summary || JSON.stringify(result.final_response, null, 2)}
                  </p>
                </div>
              )}

              {result.operations_result && result.operations_result.length > 0 && (
                <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
                  <h3 className="font-semibold text-orange-900 mb-2">Operations Analysis</h3>
                  <div className="text-sm text-orange-800 space-y-2">
                    {result.operations_result.map((op: any, idx: number) => (
                      <div key={idx} className="whitespace-pre-wrap">
                        {typeof op === 'string' ? op : JSON.stringify(op, null, 2)}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {result.alert_result && result.alert_result.length > 0 && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                  <h3 className="font-semibold text-red-900 mb-2">Alerts Sent</h3>
                  <div className="text-sm text-red-800 space-y-2">
                    {result.alert_result.map((alert: any, idx: number) => (
                      <div key={idx} className="whitespace-pre-wrap">
                        {typeof alert === 'string' ? alert : JSON.stringify(alert, null, 2)}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
