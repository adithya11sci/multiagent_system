import { useState } from 'react'
import { BellIcon } from '@heroicons/react/24/outline'
import apiService from '../services/api'
import toast from 'react-hot-toast'

export default function Alerts() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [formData, setFormData] = useState({
    message: '',
    recipients: '',
    channels: {
      sms: true,
      email: true,
      push: false,
    },
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setResult(null)

    const selectedChannels = Object.entries(formData.channels)
      .filter(([_, enabled]) => enabled)
      .map(([channel, _]) => channel)

    if (selectedChannels.length === 0) {
      toast.error('Please select at least one notification channel')
      setLoading(false)
      return
    }

    try {
      const data = await apiService.sendAlert({
        message: formData.message,
        recipients: formData.recipients.split(',').map(r => r.trim()).filter(Boolean),
        channels: selectedChannels,
      })

      if (data.success) {
        setResult(data.data)
        toast.success('Alert sent successfully!')
      } else {
        toast.error(data.error || 'Failed to send alert')
      }
    } catch (error) {
      toast.error('Failed to send alert')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const loadExample = () => {
    setFormData({
      message: 'Platform 3 is temporarily closed for maintenance. Passengers for Train 12627 please proceed to Platform 2.',
      recipients: 'passenger1@example.com, passenger2@example.com',
      channels: {
        sms: true,
        email: true,
        push: true,
      },
    })
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Multi-Channel Alert System</h1>
          <p className="mt-1 text-sm text-gray-500">
            Send notifications through SMS, Email, and Push channels
          </p>
        </div>
        <button onClick={loadExample} className="btn-secondary text-sm">
          Load Example
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Alert Form */}
        <div className="card">
          <div className="flex items-center mb-4">
            <BellIcon className="h-6 w-6 text-red-600 mr-2" />
            <h2 className="text-lg font-semibold text-gray-900">Alert Configuration</h2>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Message *
              </label>
              <textarea
                required
                value={formData.message}
                onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                rows={4}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Enter your alert message..."
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Recipients *
              </label>
              <input
                type="text"
                required
                value={formData.recipients}
                onChange={(e) => setFormData({ ...formData, recipients: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="email1@example.com, email2@example.com"
              />
              <p className="mt-1 text-xs text-gray-500">
                Comma-separated list of email addresses or phone numbers
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Notification Channels *
              </label>
              <div className="space-y-2">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={formData.channels.sms}
                    onChange={(e) => setFormData({
                      ...formData,
                      channels: { ...formData.channels, sms: e.target.checked }
                    })}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <span className="ml-2 text-sm text-gray-700">SMS (Twilio)</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={formData.channels.email}
                    onChange={(e) => setFormData({
                      ...formData,
                      channels: { ...formData.channels, email: e.target.checked }
                    })}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <span className="ml-2 text-sm text-gray-700">Email (SMTP)</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={formData.channels.push}
                    onChange={(e) => setFormData({
                      ...formData,
                      channels: { ...formData.channels, push: e.target.checked }
                    })}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <span className="ml-2 text-sm text-gray-700">Push Notification</span>
                </label>
              </div>
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
                  Sending...
                </span>
              ) : (
                'Send Alert'
              )}
            </button>
          </form>
        </div>

        {/* Results */}
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Alert Status</h2>
          
          {!result && !loading && (
            <div className="text-center py-12 text-gray-400">
              <BellIcon className="h-12 w-12 mx-auto mb-3" />
              <p>Configure and send alerts to see status</p>
            </div>
          )}

          {loading && (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-600 mx-auto mb-4"></div>
              <p className="text-gray-600">Sending alerts through channels...</p>
            </div>
          )}

          {result && (
            <div className="space-y-4">
              {result.final_response && (
                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <h3 className="font-semibold text-green-900 mb-2">✓ Success</h3>
                  <p className="text-sm text-green-800 whitespace-pre-wrap">
                    {result.final_response.summary || JSON.stringify(result.final_response, null, 2)}
                  </p>
                </div>
              )}

              {result.alert_result && result.alert_result.length > 0 && (
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <h3 className="font-semibold text-blue-900 mb-2">Delivery Status</h3>
                  <div className="text-sm text-blue-800 space-y-2">
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

      {/* Alert Examples */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Common Alert Scenarios</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {[
            {
              title: 'Train Delay',
              message: 'Train 12627 is delayed by 30 minutes. Expected arrival: 10:45 AM',
              icon: '⏱️'
            },
            {
              title: 'Platform Change',
              message: 'Platform change: Train 22644 will arrive at Platform 5 instead of Platform 3',
              icon: '🚉'
            },
            {
              title: 'Cancellation',
              message: 'Train 16340 has been cancelled due to technical issues. Refunds available.',
              icon: '⚠️'
            },
            {
              title: 'Emergency',
              message: 'Emergency situation on Platform 2. All passengers please evacuate immediately.',
              icon: '🚨'
            },
          ].map((example, idx) => (
            <button
              key={idx}
              onClick={() => setFormData({
                ...formData,
                message: example.message
              })}
              className="text-left p-4 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <div className="flex items-start">
                <span className="text-2xl mr-3">{example.icon}</span>
                <div>
                  <h3 className="font-medium text-gray-900">{example.title}</h3>
                  <p className="text-sm text-gray-600 mt-1">{example.message}</p>
                </div>
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
