export default function Home() {
  return (
    <main style={{ padding: 40, fontFamily: 'sans-serif' }}>
      <h1>GitHub Deployment Orchestrator Assistant</h1>
      <p>Production-grade orchestration UI scaffold.</p>
      <div style={{ marginTop: 24 }}>
        <textarea
          placeholder="Ask about repository state, deployment readiness, or project planning"
          style={{ width: '100%', minHeight: 160 }}
        />
      </div>
    </main>
  )
}
