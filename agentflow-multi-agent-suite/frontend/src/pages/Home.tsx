import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { Sparkles, ArrowRight, Settings as SettingsIcon } from 'lucide-react'

export default function Home() {
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const start = async () => {
    if (!url) return
    setLoading(true)
    try {
      const res = await fetch('http://localhost:8000/api/v1/runs/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target_url: url })
      })
      const data = await res.json()
      if (data.run_id) {
        navigate(`/run/${data.run_id}`)
      }
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col items-center justify-center px-4">
      <div className="absolute top-6 right-6">
        <Link to="/settings" className="flex items-center gap-2 text-sm text-muted hover:text-foreground transition-colors">
          <SettingsIcon className="w-4 h-4" />
          <span>Settings</span>
        </Link>
      </div>
      <div className="max-w-2xl w-full text-center space-y-8">
        <div className="flex items-center justify-center gap-2 text-accent">
          <Sparkles className="w-5 h-5" />
          <span className="text-sm uppercase tracking-[0.3em]">AgentFlow</span>
        </div>
        <div className="space-y-4">
          <h1 className="text-4xl md:text-6xl font-semibold tracking-tight">Multi-Agent Suite</h1>
          <p className="text-lg text-muted">Paste a job or form URL. Aria and the swarm take over. Watch live in the thread.</p>
        </div>
        <div className="relative w-full">
          <input
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://example.com/apply/..."
            className="w-full rounded-2xl bg-surface border border-border px-6 py-4 pr-32 text-lg focus:outline-none focus:ring-2 focus:ring-accent/40"
          />
          <button
            onClick={start}
            disabled={loading || !url}
            className="absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-2 rounded-xl bg-gradient-to-r from-violet-500 to-fuchsia-500 px-5 py-2.5 text-sm font-medium disabled:opacity-50"
          >
            {loading ? 'Starting...' : 'Start'} <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  )
}

