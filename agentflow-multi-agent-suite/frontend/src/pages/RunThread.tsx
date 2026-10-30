import { useParams } from 'react-router-dom'
import { Sparkles } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'

export default function RunThread() {
  const { runId } = useParams()
  const imgRef = useRef<HTMLImageElement>(null)
  const [connected, setConnected] = useState(false)

  useEffect(() => {
    if (!runId) return
    const ws = new WebSocket(`ws://localhost:8000/ws/${runId}`)
    ws.onopen = () => setConnected(true)
    ws.onmessage = (ev) => {
      try {
        const msg = JSON.parse(ev.data)
        if (msg.type === 'frame' && msg.data && imgRef.current) {
          imgRef.current.src = `data:image/jpeg;base64,${msg.data}`
        }
      } catch {}
    }
    ws.onclose = () => setConnected(false)
    return () => ws.close()
  }, [runId])

  return (
    <div className="min-h-screen bg-background text-foreground">
      <header className="sticky top-0 z-10 backdrop-blur-xl bg-background/70 border-b border-border px-6 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-violet-400 shadow-[0_0_60px_rgba(167,139,250,0.9)]" />
            <span className="text-sm font-medium">AgentFlow</span>
          </div>
          <span className="text-sm text-muted">•</span>
          <span className="text-sm text-muted">Run {runId?.slice(0, 8)}</span>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full border border-violet-400/40 bg-violet-400/10">
            <Sparkles className="w-3.5 h-3.5 text-violet-300" />
            <span className="text-violet-200">Aria • COS</span>
          </div>
        </div>
      </header>
      <main className="max-w-6xl mx-auto px-4 py-10 space-y-10">
        <div className="rounded-2xl border border-violet-400/30 bg-surface overflow-hidden shadow-glow">
          <div className="flex items-center justify-between px-6 py-3 border-b border-border">
            <div className="flex items-center gap-2 text-sm">
              <div className={`w-1.5 h-1.5 rounded-full ${connected ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'}`} />
              <span>Live Browser</span>
              <span className="text-muted">• {connected ? 'Streaming' : 'Connecting'}</span>
            </div>
            <div className="flex items-center gap-2">
              <button className="text-xs px-3 py-1.5 rounded-lg border border-border hover:bg-white/5 transition-colors">Take Control</button>
              <button className="text-xs px-3 py-1.5 rounded-lg border border-border hover:bg-white/5 transition-colors">Hand back to Aria</button>
            </div>
          </div>
          <div className="aspect-video bg-black flex items-center justify-center">
            <img ref={imgRef} alt="live browser" className="w-full h-full object-contain" />
          </div>
        </div>
        <div className="space-y-6">
          <div className="flex items-start gap-4">
            <div className="w-9 h-9 rounded-full bg-gradient-to-br from-violet-400 to-fuchsia-400 flex items-center justify-center text-xs font-medium shadow-[0_0_60px_rgba(167,139,250,0.4)]">A</div>
            <div className="flex-1 space-y-2">
              <div className="flex items-center gap-2">
                <span className="text-sm">Aria • COS</span>
                <span className="text-xs text-muted">just now</span>
              </div>
              <div className="rounded-2xl border border-border bg-surface px-6 py-4 max-w-3xl">
                <div className="text-sm leading-relaxed">Initializing swarm. Scouting target URL and mapping access requirements. I'll yield control if login or CAPTCHA is detected.</div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}


იტომfunctions.write_file
