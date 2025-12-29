import { useState } from 'react'
import { UsersIcon } from '@heroicons/react/24/outline'
import apiService from '../services/api'
import toast from 'react-hot-toast'

export default function CrowdPrediction() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [formData, setFormData] = useState({
    train_number: '',
    route: '',
    time: '',
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setResult(null)

    try {
      const data = await apiService.predictCrowd({
        train_number: formData.train_number,
        route: formData.route,
        time: formData.time || undefined,
      })

      if (data.success) {
        setResult(data.data)
        toast.success('Crowd prediction completed!')
      } else {
        toast.error(data.error || 'Failed to predict crowd')
      }
    } catch (error) {
      toast.error('Failed to predict crowd')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const loadExample = () => {
    setFormData({
      train_number: '12644',
      route: 'Chennai-Bangalore',
      time: new Date().toISOString().slice(0, 16),
    })
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Crowd Prediction & Management</h1>
          <p className="mt-1 text-sm text-gray-500">
            AI-powered crowd forecasting and capacity optimization
          </p>
        </div>
        <button onClick={loadExample} className="btn-secondary text-sm">
          Load Example
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Form */}
        <div className="card">
          <div className="flex items-center mb-4">
            <UsersIcon className="h-6 w-6 text-purple-600 mr-2" />
            <h2 className="text-lg font-semibold text-gray-900">Prediction Parameters</h2>
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
                placeholder="e.g., 12644"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Route *
              </label>
              <input
                type="text"
                required
                value={formData.route}
                onChange={(e) => setFormData({ ...formData, route: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="e.g., Chennai-Bangalore"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Time (optional)
              </label>
              <input
                type="datetime-local"
                value={formData.time}
                onChange={(e) => setFormData({ ...formData, time: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
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
                  Analyzing...
                </span>
              ) : (
                'Predict Crowd'
              )}
            </button>
          </form>
        </div>

        {/* Results */}
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Prediction Results</h2>
          
          {!result && !loading && (
            <div className="text-center py-12 text-gray-400">
              <UsersIcon className="h-12 w-12 mx-auto mb-3" />
              <p>Submit parameters to see crowd prediction</p>
            </div>
          )}

          {loading && (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto mb-4"></div>
              <p className="text-gray-600">AI is analyzing crowd patterns...</p>
            </div>
          )}

          {result && (
            <div className="space-y-4">
              {result.final_response && (
                <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
                  <h3 className="font-semibold text-purple-900 mb-2">Analysis Summary</h3>
                  <p className="text-sm text-purple-800 whitespace-pre-wrap">
                    {result.final_response.summary || JSON.stringify(result.final_response, null, 2)}
                  </p>
                </div>
              )}

              {result.crowd_result && result.crowd_result.length > 0 && (
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <h3 className="font-semibold text-blue-900 mb-2">Crowd Predictions</h3>
                  <div className="text-sm text-blue-800 space-y-2">
                    {result.crowd_result.map((prediction: any, idx: number) => (
                      <div key={idx} className="whitespace-pre-wrap">
                        {typeof prediction === 'string' ? prediction : JSON.stringify(prediction, null, 2)}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {result.operations_result && result.operations_result.length > 0 && (
                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <h3 className="font-semibold text-green-900 mb-2">Recommendations</h3>
                  <div className="text-sm text-green-800 space-y-2">
                    {result.operations_result.map((op: any, idx: number) => (
                      <div key={idx} className="whitespace-pre-wrap">
                        {typeof op === 'string' ? op : JSON.stringify(op, null, 2)}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Info Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="card bg-purple-50 border border-purple-100">
          <h3 className="font-semibold text-purple-900 mb-2">🎯 Capacity Optimization</h3>
          <p className="text-sm text-purple-800">
            AI analyzes historical data to predict overcrowding and suggest optimal capacity distribution.
          </p>
        </div>
        <div className="card bg-blue-50 border border-blue-100">
          <h3 className="font-semibold text-blue-900 mb-2">📊 Pattern Recognition</h3>
          <p className="text-sm text-blue-800">
            Machine learning identifies crowd patterns based on time, route, and historical trends.
          </p>
        </div>
        <div className="card bg-green-50 border border-green-100">
          <h3 className="font-semibold text-green-900 mb-2">🚀 Proactive Solutions</h3>
          <p className="text-sm text-green-800">
            Get recommendations for alternative trains, coaches, and timing adjustments.
          </p>
        </div>
      </div>
    </div>
  )
}
