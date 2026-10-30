import { Link } from 'react-router-dom'
import { ArrowLeft, Sparkles } from 'lucide-react'

export default function Settings() {
  const agents = [
    { id: 'aria', name: 'Aria • COS', color: '#a78bfa' },
    { id: 'scout', name: 'Scout', color: '#22d3ee' },
    { id: 'profiler', name: 'Profiler', color: '#60a5fa' },
    { id: 'tailor', name: 'Tailor', color: '#fb923c' },
    { id: 'navigator', name: 'Navigator', color: '#2dd4bf' },
    { id: 'verifier', name: 'Verifier', color: '#a3e635' },
    { id: 'executor', name: 'Executor', color: '#f472b6' },
  ]

  return (
    <div className="min-h-screen bg-background text-foreground">
      <header className="sticky top-0 z-10 backdrop-blur-xl bg-background/70 border-b border-border px-6 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Link to="/" className="flex items-center gap-2 text-muted hover:text-foreground transition-colors">
            <ArrowLeft className="w-4 h-4" />
            <span className="text-sm">Back</span>
          </Link>
          <span className="text-sm text-muted">•</span>
          <span className="text-sm font-medium">Settings</span>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full border border-violet-400/40 bg-violet-400/10">
            <Sparkles className="w-3.5 h-3.5 text-violet-300" />
            <span className="text-violet-200">AgentFlow</span>
          </div>
        </div>
      </header>
      <main className="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <div className="space-y-2">
          <h1 className="text-3xl font-semibold tracking-tight">Settings</h1>
          <p className="text-muted">Rename agents, configure models, and tune behavior.</p>
        </div>

        <section className="rounded-2xl border border-border bg-surface overflow-hidden">
          <div className="px-6 py-4 border-b border-border">
            <h2 className="text-lg font-medium">Agents</h2>
            <p className="text-sm text-muted">Rename each agent. Internal IDs remain fixed.</p>
          </div>
          <div className="divide-y divide-border">
            {agents.map((agent) => (
              <div key={agent.id} className="flex items-center justify-between px-6 py-4">
                <div className="flex items-center gap-3">
                  <div className="w-9 h-9 rounded-full" style={{ background: `radial-gradient(circle, ${agent.color}33, transparent), linear-gradient(135deg, ${agent.color}, ${agent.color}88)` }} />
                  <div>
                    <div className="text-sm">{agent.name}</div>
                    <div className="text-xs text-muted">{agent.id}</div>
                  </div>
                </div>
                <input
                  defaultValue={agent.name}
                  className="w-64 rounded-xl bg-background border border-border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-accent/40"
                />
              </div>
            ))}
          </div>
        </section>

        <section className="rounded-2xl border border-border bg-surface overflow-hidden">
          <div className="px-6 py-4 border-b border-border">
            <h2 className="text-lg font-medium">Model Routing (OpenRouter)</h2>
            <p className="text-sm text-muted">Use strongest free models with automatic fallbacks.</p>
          </div>
          <div className="px-6 py-6 text-sm text-muted">Routing configured per agent with sensible defaults. API key from .env.</div>
        </section>
      </main>
    </div>
  )
}
