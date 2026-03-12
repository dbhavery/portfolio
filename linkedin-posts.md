# LinkedIn Posts — Ready to Copy-Paste

Post 1-2x per week. Each post should feel natural, not promotional.
These are written in Don's voice based on real project experiences.

---

## Post 1: The Zombie Process War Story

I built a voice assistant that ran 24/7. It died silently.

Not crashed — died. The process was alive, consuming resources, responding to health checks. But it hadn't processed a voice command in 5 days. An STT buffer overflow flooded 14,490 warnings, and the pipeline froze while the process kept running.

The fix wasn't a restart script. It was 4 layers of defense:

1. Circuit breaker on the STT buffer (trips after 10 overflows in 30s)
2. Pipeline health watchdog (checks every 15s, resets after 3 consecutive trips)
3. EventBus backpressure (drops events when subscribers can't keep up)
4. Process supervisor (kills true zombies after 3 failed health probes)

The lesson: "Is the process running?" is the wrong question. "Is the process doing useful work?" is what matters.

Reliability isn't about preventing failures. It's about detecting them faster than your users do.

#AIEngineering #Reliability #VoicePipeline #LessonsLearned

---

## Post 2: Why I Built Vector Search From Scratch

Pinecone: $70/month. FAISS: compiled C++ binaries that break on Windows. pgvector: requires PostgreSQL.

I needed a vector search index that was:
- Pure Python (pip install, done)
- Zero external dependencies
- Embeddable in any application

So I implemented HNSW from the original 2018 Malkov & Yashunin paper.

The algorithm itself isn't complicated — it's a navigable small-world graph with hierarchical layers. The hard parts were:

- Tuning M and ef_construction (more art than science)
- Thread-safe insertion without global locks
- Making deletion work without corrupting the graph

Result: O(log n) search, works anywhere Python runs, zero infrastructure cost.

Sometimes the best dependency is no dependency.

GitHub: github.com/dbhavery/citadel

#VectorSearch #HNSW #AIInfrastructure #BuildDontBuy

---

## Post 3: The Real Cost of LLM API Calls

I route every query through 5 tiers of LLM:

- Tier 1 (local Ollama): Free. 50ms. Handles "what time is it?"
- Tier 2 (Gemini Flash): $0.001. 200ms. General knowledge.
- Tier 3 (Claude Sonnet): $0.01. 500ms. Complex reasoning.
- Tier 4 (Claude Opus): $0.05. 1s+. Deep analysis.
- Tier 5 (Gemini Pro): $0.02. 800ms. Long context.

The insight: 70%+ of queries don't need a frontier model. A local 7B model handles greetings, time checks, simple lookups, and status queries perfectly.

By routing intelligently instead of defaulting to the most expensive model, I cut API costs by roughly 70% with zero perceived quality loss for the user.

The hard part isn't calling an LLM. It's knowing which LLM to call.

#LLM #CostOptimization #AIArchitecture #MLOps

---

## Post 4: 30 Years of Trucking Taught Me Systems Architecture

Before I wrote a line of code, I spent 30 years coordinating freight across the Pacific Northwest. 3.5 million miles. Dispatch, scheduling, compliance, real-time route optimization.

Turns out, a freight network IS a distributed system:

- Trucks are worker nodes
- Dispatch is the orchestrator
- Load manifests are message queues
- DOT compliance is the type system
- Weather and traffic are external API failures

When I started building AI infrastructure, the patterns were already there. Circuit breakers? That's what you do when a route is blocked. Load balancing? That's dispatch 101. Graceful degradation? Every trucker knows the backup route.

The best software engineers I know didn't start with code. They started with problems complex enough to demand systems thinking.

If your background isn't traditional CS — that might be your advantage, not your weakness.

#CareerChange #SystemsThinking #AIEngineering #NonTraditionalPath

---

## Post 5: What 2,000+ Tests Actually Test

"We have 90% code coverage" means nothing.

Here's what I actually test across my projects:

- **Contract tests**: Does the API return the shape clients expect?
- **Boundary tests**: What happens at 0, 1, MAX_INT, empty string, None?
- **Regression tests**: Every bug fix gets a test that reproduces the original bug
- **Integration tests**: Do the modules actually work together?
- **Smoke tests**: Does the system start and handle one real request?

What I don't test:
- Implementation details (private methods, internal state)
- Third-party library behavior
- Things that can't fail (type-checked function signatures)

2,000+ tests across 37 repositories. Not because I love writing tests — because I hate debugging the same issue twice.

The test isn't the goal. The confidence to ship is.

#Testing #SoftwareEngineering #QualityAssurance #DevPractices

---

## Post 6: Building a Compliance Scanner Without an LLM

Hot take: Not every AI tool needs an LLM.

I built Sentinel — a compliance scanner that checks systems against 62 real SOC 2, GDPR, and HIPAA requirements. The first version used keyword trigram matching, not GPT-4.

Why?

Compliance needs **reproducibility**. If you run the same scan twice, you need the same result. LLMs are stochastic — they might flag different things each time.

The keyword scanner is:
- Deterministic (same input = same output, always)
- Auditable (you can see exactly why something was flagged)
- Fast (scans in seconds, not minutes)
- Free (no API calls)

The LLM layer comes second — it interprets the findings, generates policy documents, and explains gaps in plain English. But the core analysis is old-school information retrieval.

Use the right tool for the job. Sometimes that tool is a regex.

#Compliance #AIEngineering #GDPR #SOC2 #PracticalAI
