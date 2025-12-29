import { useState } from 'react'
import { ChatBubbleLeftRightIcon } from '@heroicons/react/24/outline'
import apiService from '../services/api'
import toast from 'react-hot-toast'

export default function PassengerQuery() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [query, setQuery] = useState('')

  const exampleQueries = [
    "What is the refund policy for cancelled trains?",
    "How do I book a ticket from Chennai to Bangalore?",
    "What are the train timings for route Chennai-Mumbai?",
    "How can I cancel my ticket and get a refund?",
  ]

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim()) return

    setLoading(true)
    setResult(null)

    try {
      const data = await apiService.passengerQuery(query)

      if (data.success) {
        setResult(data.data)
        toast.success('Query processed successfully!')
      } else {
        toast.error(data.error || 'Failed to process query')
      }
    } catch (error) {
      toast.error('Failed to process query')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Passenger Query Assistant</h1>
        <p className="mt-1 text-sm text-gray-500">
          AI-powered customer service with RAG-based knowledge retrieval
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Query Input */}
        <div className="lg:col-span-2 card">
          <div className="flex items-center mb-4">
            <ChatBubbleLeftRightIcon className="h-6 w-6 text-blue-600 mr-2" />
            <h2 className="text-lg font-semibold text-gray-900">Ask a Question</h2>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Your Query
              </label>
              <textarea
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                rows={4}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Type your question here..."
              />
            </div>

            <button
              type="submit"
              disabled={loading || !query.trim()}
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
                'Get Answer'
              )}
            </button>
          </form>

          {/* Result */}
          {result && (
            <div className="mt-6 space-y-4">
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <h3 className="font-semibold text-green-900 mb-2">AI Response</h3>
                <div className="text-sm text-green-800 whitespace-pre-wrap">
                  {result.final_response?.summary || result.passenger_result?.[0] || JSON.stringify(result, null, 2)}
                </div>
              </div>

              {result.passenger_result && result.passenger_result.length > 1 && (
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <h3 className="font-semibold text-blue-900 mb-2">Additional Information</h3>
                  <div className="text-sm text-blue-800 space-y-2">
                    {result.passenger_result.slice(1).map((info: any, idx: number) => (
                      <div key={idx} className="whitespace-pre-wrap">
                        {typeof info === 'string' ? info : JSON.stringify(info, null, 2)}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {loading && (
            <div className="mt-6 text-center py-8">
              <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600 mx-auto mb-3"></div>
              <p className="text-gray-600">AI is analyzing your query...</p>
            </div>
          )}
        </div>

        {/* Example Queries */}
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Example Queries</h2>
          <div className="space-y-2">
            {exampleQueries.map((example, idx) => (
              <button
                key={idx}
                onClick={() => setQuery(example)}
                className="w-full text-left p-3 bg-gray-50 hover:bg-gray-100 rounded-lg text-sm transition-colors"
              >
                {example}
              </button>
            ))}
          </div>

          <div className="mt-6 bg-blue-50 border border-blue-100 rounded-lg p-4">
            <h3 className="text-sm font-semibold text-blue-900 mb-2">💡 How it works</h3>
            <p className="text-xs text-blue-800">
              The Passenger Agent uses RAG (Retrieval Augmented Generation) to search through 
              railway policies, timetables, and refund rules to provide accurate, knowledge-based answers.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
