# Avatar Interview — Speech & Content UX Test

**Tester:** _______________
**Date:** _______________
**Device/Browser:** _______________
**Volume level:** _______________

## Instructions

Play each video (q1–q13) and the idle loop. For each, evaluate using the checklist below. Mark PASS/FAIL and note issues. Compare spoken audio against the transcript provided.

---

## IDLE VIDEO (idle.webm)

| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 1 | Natural blinking at normal rate (every 3–5 seconds) | | | |
| 2 | Subtle head/body movement (not frozen) | | | |
| 3 | No mouth movement during idle | | | |
| 4 | Looping is seamless (no visible jump at loop point) | | | |
| 5 | No audio artifacts or hum | | | |

---

## Q1: "What do you build?"

**Transcript:**
> So, I build AI systems — like, full production systems, not just demos. My main project is Isabelle, she's a voice assistant I built from scratch. Seven sub-agents, routes across five different LLMs, handles real-time voice... the whole pipeline. I also built an enterprise SaaS platform called StaFull with six different role-based portals. But yeah, the short answer is — I take AI from a concept all the way to something you can actually ship and use.

### Speech Accuracy
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 1 | Every sentence spoken completely (no cut-offs) | | | |
| 2 | No added words not in the transcript | | | |
| 3 | No missing/skipped words from the transcript | | | |
| 4 | Proper nouns pronounced correctly (Isabelle, StaFull, LLMs) | | | |
| 5 | Numbers spoken correctly (seven, five, six) | | | |

### Comprehension & Naturalness
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 6 | Speech speed feels conversational (not rushed, not sluggish) | | | |
| 7 | Answer directly addresses the question asked | | | |
| 8 | A non-technical recruiter could understand the gist | | | |
| 9 | Tone sounds natural and human (not robotic or rehearsed) | | | |
| 10 | Appropriate pauses at commas and em-dashes | | | |

### Content Review
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 11 | Not too wordy — could a shorter answer work? | | | |
| 12 | Jargon is explained or obvious from context | | | |
| 13 | Key message lands: "I build full production AI systems" | | | |

**Flagged issues:**
_____________________________________________

---

## Q2: "How does your LLM routing work?"

**Transcript:**
> Yeah so the routing is — it's actually one of my favorite parts. I've got five models set up. There's a local Qwen model for anything that needs to be fast, like sub-400 millisecond responses. Then Claude Sonnet and Opus handle the heavier reasoning stuff, and Gemini Pro and Flash for multimodal — images, that kind of thing. And there's an eight-point intent classifier that looks at each request and decides which model handles it based on complexity, context, cost... it's not just random load balancing, it's intelligent routing with fallback chains if something goes down.

### Speech Accuracy
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 1 | Every sentence spoken completely (no cut-offs) | | | |
| 2 | No added words not in the transcript | | | |
| 3 | No missing/skipped words from the transcript | | | |
| 4 | Proper nouns correct (Qwen, Claude Sonnet, Opus, Gemini Pro, Flash) | | | |
| 5 | Numbers spoken correctly (five, 400, eight-point) | | | |

### Comprehension & Naturalness
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 6 | Speech speed feels conversational | | | |
| 7 | Answer directly addresses the question asked | | | |
| 8 | A non-technical recruiter could understand the gist | | | |
| 9 | Tone sounds natural and human | | | |
| 10 | Appropriate pauses at commas and em-dashes | | | |

### Content Review
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 11 | Not too wordy — could a shorter answer work? | | | |
| 12 | Jargon is explained or obvious from context | | | |
| 13 | Key message lands: "intelligent model routing, not random" | | | |

**Content flag:** "sub-400 millisecond", "eight-point intent classifier", "BM25", "fallback chains" — heavy jargon. Would a hiring manager understand this? Consider simplifying for a general audience.

**Flagged issues:**
_____________________________________________

---

## Q3: "What's your background?"

**Transcript:**
> Honestly? I spent thirty years in transportation operations — managing distributed teams, logistics, making time-critical decisions with, you know, incomplete information. And then I just... got obsessed with AI. Like, fully obsessed. Built a serious portfolio in under two years. Every concept I studied, I immediately turned into working code. I don't have a CS degree — I'll be upfront about that — but I've got {{repos}} repos, over {{commits}} commits, and {{loc}}K lines of production code. The work speaks for itself.

### Speech Accuracy
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 1 | Every sentence spoken completely (no cut-offs) | | | |
| 2 | No added words not in the transcript | | | |
| 3 | No missing/skipped words from the transcript | | | |
| 4 | Template vars spoken as real numbers (not "repos" literally) | | | |
| 5 | Natural handling of ellipsis pauses ("just... got obsessed") | | | |

### Comprehension & Naturalness
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 6 | Speech speed feels conversational | | | |
| 7 | Answer directly addresses the question asked | | | |
| 8 | A non-technical recruiter could understand the gist | | | |
| 9 | Tone sounds natural and human | | | |
| 10 | Emotional beats land (honesty about no CS degree, pride in work) | | | |

### Content Review
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 11 | Not too wordy — could a shorter answer work? | | | |
| 12 | Jargon-free — accessible to any audience | | | |
| 13 | Key message lands: "career changer, self-taught, proven by output" | | | |

**Content flag:** `{{repos}}`, `{{commits}}`, `{{loc}}` are template variables. Are these being replaced with actual numbers at runtime, or is the TTS reading them literally? **CRITICAL — verify audio.**

**Flagged issues:**
_____________________________________________

---

## Q4: "Explain your agent architecture."

**Transcript:**
> Okay so Isabelle has this orchestrator that manages seven specialized sub-agents. Think of it like... the orchestrator is the manager, and each agent has its own job. ConversationNode handles the chatting, Claude and Gemini nodes do the complex reasoning, ToolNode can execute thirty-two different tools, AgentNode runs longer autonomous workflows, VisionNode deals with images and screenshots, and MemoryNode handles this tiered memory system with ChromaDB for retrieval. They all coordinate through a shared state bus and can run in parallel — which is actually the part that took the most engineering to get right.

### Speech Accuracy
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 1 | Every sentence spoken completely (no cut-offs) | | | |
| 2 | No added words not in the transcript | | | |
| 3 | No missing/skipped words from the transcript | | | |
| 4 | Proper nouns correct (ConversationNode, ToolNode, AgentNode, VisionNode, MemoryNode, ChromaDB) | | | |
| 5 | Numbers spoken correctly (seven, thirty-two) | | | |

### Comprehension & Naturalness
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 6 | Speech speed feels conversational | | | |
| 7 | Answer directly addresses the question asked | | | |
| 8 | A non-technical recruiter could understand the gist | | | |
| 9 | Tone sounds natural and human | | | |
| 10 | The "manager" analogy is clear and lands naturally | | | |

### Content Review
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 11 | Not too wordy — could a shorter answer work? | | | |
| 12 | Jargon is explained or obvious from context | | | |
| 13 | Key message lands: "orchestrator + 7 specialized agents in parallel" | | | |

**Content flag:** Very heavy on internal class names (ConversationNode, ToolNode, etc.). A recruiter won't know what these are. The "manager" analogy helps, but the list of node names may lose people. Consider: "one for conversation, one for reasoning, one for tools..." instead of class names.

**Flagged issues:**
_____________________________________________

---

## Q5: "What was your hardest technical challenge?"

**Transcript:**
> Oh man, real-time voice. Hands down. Getting the end-to-end latency under five hundred milliseconds was... it was a grind. You need Silero VAD for speech detection, Faster Whisper for transcription at like eighty-two milliseconds, then streaming LLM responses, sentence-level TTS — all while doing echo cancellation and juggling seven-plus GPU models in twenty-four gigs of VRAM on a single RTX 3090 Ti. One model leaks a gig of VRAM and the whole thing falls over. But the goal was to make it feel like a real conversation, not like talking to a robot. And I think we got there.

### Speech Accuracy
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 1 | Every sentence spoken completely (no cut-offs) | | | |
| 2 | No added words not in the transcript | | | |
| 3 | No missing/skipped words from the transcript | | | |
| 4 | Proper nouns correct (Silero VAD, Faster Whisper, RTX 3090 Ti) | | | |
| 5 | Numbers correct (500, 82, 7, 24, 3090) | | | |

### Comprehension & Naturalness
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 6 | Speech speed feels conversational | | | |
| 7 | Answer directly addresses the question asked | | | |
| 8 | A non-technical recruiter could understand the gist | | | |
| 9 | Tone sounds natural — the "Oh man" opener feels real | | | |
| 10 | Appropriate pauses convey the difficulty of the challenge | | | |

### Content Review
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 11 | Not too wordy — could a shorter answer work? | | | |
| 12 | Jargon is explained or obvious from context | | | |
| 13 | Key message lands: "real-time voice is brutally hard, I solved it" | | | |

**Content flag:** "Silero VAD", "Faster Whisper", "sentence-level TTS", "VRAM" — a recruiter won't know these. The emotional hook is strong ("Oh man... it was a grind") but the technical middle section may lose non-engineers. The closing ("feel like a real conversation, not a robot") saves it. Consider trimming the tool names and keeping the human impact.

**Flagged issues:**
_____________________________________________

---

## Q6: "How do you approach testing?"

**Transcript:**
> I'm kind of obsessive about it, honestly. Over {{tests}} tests — unit, integration, end-to-end, even chaos injection. Every module has its own test suite. When I fix a bug, the first thing I do is write a test that reproduces it. Then I fix it, then I make sure the test passes. GitHub Actions handles the CI/CD so tests run on every push automatically. My philosophy is basically — if it doesn't have tests, it doesn't work. You just don't know it's broken yet.

### Speech Accuracy
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 1 | Every sentence spoken completely (no cut-offs) | | | |
| 2 | No added words not in the transcript | | | |
| 3 | No missing/skipped words from the transcript | | | |
| 4 | Template var `{{tests}}` spoken as actual number | | | |
| 5 | "CI/CD" pronounced correctly (see-eye-see-dee) | | | |

### Comprehension & Naturalness
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 6 | Speech speed feels conversational | | | |
| 7 | Answer directly addresses the question asked | | | |
| 8 | A non-technical recruiter could understand the gist | | | |
| 9 | Tone sounds natural and human | | | |
| 10 | The closing line lands as a memorable quote | | | |

### Content Review
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 11 | Not too wordy — could a shorter answer work? | | | |
| 12 | Jargon is explained or obvious from context | | | |
| 13 | Key message lands: "obsessive tester, test-first philosophy" | | | |

**Content flag:** `{{tests}}` template var — verify it resolves to a number in audio. "chaos injection" may be unfamiliar but sounds impressive in context. "CI/CD" is standard enough for engineering roles. Good closing quote. Overall clean answer.

**Flagged issues:**
_____________________________________________

---

## Q7: "How does your RAG system work?"

**Transcript:**
> So the retrieval system uses ChromaDB with a hybrid approach — BM25 for keyword matching plus dense vector search. When a question comes in, documents get chunked, embedded, stored with metadata. At query time, both methods run in parallel, the results get fused and re-ranked. On top of that, there's a knowledge base with over five hundred skills using fuzzy matching. And then the memory is tiered — short-term in the session, medium-term in SQLite, long-term in ChromaDB — so the assistant actually remembers context across conversations. It's not just search, it's actual memory.

### Speech Accuracy
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 1 | Every sentence spoken completely (no cut-offs) | | | |
| 2 | No added words not in the transcript | | | |
| 3 | No missing/skipped words from the transcript | | | |
| 4 | Proper nouns correct (ChromaDB, BM25, SQLite) | | | |
| 5 | Technical terms pronounced correctly (chunked, embedded, fused) | | | |

### Comprehension & Naturalness
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 6 | Speech speed feels conversational | | | |
| 7 | Answer directly addresses the question asked | | | |
| 8 | A non-technical recruiter could understand the gist | | | |
| 9 | Tone sounds natural and human | | | |
| 10 | The closing reframe ("not just search, it's memory") lands | | | |

### Content Review
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 11 | Not too wordy — could a shorter answer work? | | | |
| 12 | Jargon is explained or obvious from context | | | |
| 13 | Key message lands: "hybrid retrieval + tiered memory" | | | |

**Content flag:** HEAVIEST jargon answer. "BM25", "dense vector search", "chunked, embedded, stored with metadata", "fused and re-ranked", "fuzzy matching", "SQLite" — this will lose any non-engineer. The question itself ("RAG system") is already technical. If this is only for technical audiences, fine. If recruiters will see it, consider a simpler version. The closing saves it somewhat.

**Flagged issues:**
_____________________________________________

---

## Q8: "Where do you see yourself next?"

**Transcript:**
> I mean, I want to be doing exactly this but at scale. Building production AI systems, shipping real products. I'm looking at roles like AI Engineer, LLM Applications Engineer, Agentic AI — anywhere I can architect multi-agent systems and build real-time pipelines. What I bring is... I'm a builder. I don't just read about this stuff, I've deployed every concept I've learned into working software. And I'm ready to bring that to a team.

### Speech Accuracy
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 1 | Every sentence spoken completely (no cut-offs) | | | |
| 2 | No added words not in the transcript | | | |
| 3 | No missing/skipped words from the transcript | | | |
| 4 | Role titles spoken clearly (AI Engineer, LLM Applications Engineer) | | | |
| 5 | Natural pause at "What I bring is..." | | | |

### Comprehension & Naturalness
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 6 | Speech speed feels conversational | | | |
| 7 | Answer directly addresses the question asked | | | |
| 8 | A non-technical recruiter could understand the gist | | | |
| 9 | Tone sounds natural — confident but not arrogant | | | |
| 10 | The "I'm a builder" statement lands with conviction | | | |

### Content Review
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 11 | Not too wordy — could a shorter answer work? | | | |
| 12 | Jargon-free enough for general audience | | | |
| 13 | Key message lands: "I want to build AI at scale, on a team" | | | |

**Content flag:** Clean answer. Good length. "Agentic AI" as a role title is niche but the surrounding context makes intent clear. Strong close.

**Flagged issues:**
_____________________________________________

---

## Q9: "How do you handle a project that's failing?"

**Transcript:**
> First thing I do is stop guessing. I look at the actual error, trace it back to the root cause — not the symptom, the real origin. I've got a rule: if I can't fix it in two attempts, I stop and rethink the approach entirely. I don't do band-aid fixes. If the architecture is wrong, I fix the architecture. I've killed features, rewritten modules, thrown away days of work when the foundation wasn't right. It's painful in the moment, but six months later you're not drowning in tech debt. The key is being honest early — don't hide problems, surface them fast, and fix them at the source.

### Speech Accuracy
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 1 | Every sentence spoken completely (no cut-offs) | | | |
| 2 | No added words not in the transcript | | | |
| 3 | No missing/skipped words from the transcript | | | |
| 4 | "Two attempts" rule stated clearly | | | |
| 5 | Natural emphasis on key phrases ("stop guessing", "root cause") | | | |

### Comprehension & Naturalness
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 6 | Speech speed feels conversational | | | |
| 7 | Answer directly addresses the question asked | | | |
| 8 | A non-technical recruiter could understand the gist | | | |
| 9 | Tone sounds natural — shows maturity and discipline | | | |
| 10 | Emotional honesty feels real ("painful in the moment") | | | |

### Content Review
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 11 | Not too wordy — could a shorter answer work? | | | |
| 12 | Jargon-free — accessible to any audience | | | |
| 13 | Key message lands: "root cause thinker, no band-aids, honest early" | | | |

**Content flag:** Excellent answer. Minimal jargon ("tech debt" is the only term that might need context). Strong structure, clear philosophy, memorable rules. No changes needed.

**Flagged issues:**
_____________________________________________

---

## Q10: "How do you learn new technology?"

**Transcript:**
> I learn by building. Seriously — every single concept I've studied, I turned into working code within days. Not tutorials, not toy examples — real systems. When I wanted to understand multi-agent orchestration, I built a seven-agent system from scratch. When I wanted to learn vector search, I implemented HNSW from the ground up instead of using a managed database. I went from zero programming experience to ninety-five thousand lines of production code in under two years. The secret is I don't move on until I've shipped something that actually works. Theory without implementation is just trivia.

### Speech Accuracy
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 1 | Every sentence spoken completely (no cut-offs) | | | |
| 2 | No added words not in the transcript | | | |
| 3 | No missing/skipped words from the transcript | | | |
| 4 | "HNSW" pronounced correctly (aitch-en-ess-double-u) | | | |
| 5 | "Ninety-five thousand" spoken clearly as a number | | | |

### Comprehension & Naturalness
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 6 | Speech speed feels conversational | | | |
| 7 | Answer directly addresses the question asked | | | |
| 8 | A non-technical recruiter could understand the gist | | | |
| 9 | Tone sounds natural and human | | | |
| 10 | The closing line lands as quotable ("Theory without implementation...") | | | |

### Content Review
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 11 | Not too wordy — could a shorter answer work? | | | |
| 12 | Jargon is explained or obvious from context | | | |
| 13 | Key message lands: "learn by building, not reading" | | | |

**Content flag:** "HNSW" is heavy jargon — no non-engineer will know what this means. "Vector search" + "managed database" are borderline. The opening and closing are strong and universal. Consider replacing "implemented HNSW from the ground up" with "built my own search engine from scratch" for accessibility.

**Flagged issues:**
_____________________________________________

---

## Q11: "How do you make architecture decisions?"

**Transcript:**
> Every decision gets logged with the reasoning — what we chose, what we rejected, and why. It's not just gut feeling. Take the vector search decision: I could've used Pinecone or Weaviate, that's seventy-plus dollars a month for a managed service. Instead I built a zero-dependency HNSW implementation. The tradeoff is I own the maintenance, but I eliminated an external dependency and a recurring cost. Same thinking with the LLM routing — why use one expensive model for everything when an eight-point classifier can route seventy percent of queries to a free local model? I always start with: what's the simplest thing that solves the actual problem, and what are the real tradeoffs, not the theoretical ones.

### Speech Accuracy
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 1 | Every sentence spoken completely (no cut-offs) | | | |
| 2 | No added words not in the transcript | | | |
| 3 | No missing/skipped words from the transcript | | | |
| 4 | Proper nouns correct (Pinecone, Weaviate, HNSW) | | | |
| 5 | Numbers correct (seventy-plus, eight-point, seventy percent) | | | |

### Comprehension & Naturalness
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 6 | Speech speed feels conversational | | | |
| 7 | Answer directly addresses the question asked | | | |
| 8 | A non-technical recruiter could understand the gist | | | |
| 9 | Tone sounds natural and human | | | |
| 10 | Cost comparison ($70/mo vs free) is clear and impactful | | | |

### Content Review
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 11 | Not too wordy — could a shorter answer work? | | | |
| 12 | Jargon is explained or obvious from context | | | |
| 13 | Key message lands: "document decisions, weigh real tradeoffs" | | | |

**Content flag:** "Pinecone", "Weaviate", "zero-dependency HNSW implementation", "eight-point classifier" — again heavy on internal specifics. The $70/mo comparison is great and universally understood. The closing principle is strong. Consider: fewer product names, more "I evaluated paid services vs building my own" framing.

**Flagged issues:**
_____________________________________________

---

## Q12: "What would you build in your first 90 days?"

**Transcript:**
> First thirty days, I'm listening and reading. Understanding the existing systems, the pain points, the technical debt — not proposing big changes yet. I'd pick up a few quick wins to build trust and learn the codebase through real work. Days thirty to sixty, I'd start identifying where AI can have the biggest impact — maybe it's a pipeline that's too slow, maybe it's a manual process that could be automated, maybe there's no observability and things are failing silently. By day ninety, I'd want to have shipped at least one meaningful improvement and have a concrete proposal for a bigger initiative. I'm not the guy who spends three months making slides. I ship.

### Speech Accuracy
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 1 | Every sentence spoken completely (no cut-offs) | | | |
| 2 | No added words not in the transcript | | | |
| 3 | No missing/skipped words from the transcript | | | |
| 4 | Day ranges spoken clearly (thirty, thirty to sixty, ninety) | | | |
| 5 | Natural cadence through the three-phase structure | | | |

### Comprehension & Naturalness
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 6 | Speech speed feels conversational | | | |
| 7 | Answer directly addresses the question asked | | | |
| 8 | A non-technical recruiter could understand the gist | | | |
| 9 | Tone sounds natural — shows humility then confidence | | | |
| 10 | The "I ship" closing is punchy and lands | | | |

### Content Review
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 11 | Not too wordy — could a shorter answer work? | | | |
| 12 | Jargon-free — accessible to any audience | | | |
| 13 | Key message lands: "listen first, deliver fast, no theater" | | | |

**Content flag:** Excellent answer. Clear 30/60/90 structure. Minimal jargon ("observability" is the only borderline term). "I ship" is a strong closer. No changes needed.

**Flagged issues:**
_____________________________________________

---

## Q13: "Why you over a traditional CS background?"

**Transcript:**
> Honestly? Hire me because of it, not despite it. Thirty years of managing complex operations — distributed teams, time-critical logistics, decisions with incomplete data — that's exactly the kind of systems thinking that makes good AI infrastructure. CS graduates understand algorithms. I understand what happens when your system fails at two AM and there's real money on the line. Plus, I've proven I can learn. Ninety-five thousand lines of production code, seven hundred-plus tests, multi-agent systems, real-time voice pipelines — all built in under two years, all shipped, all documented. I don't just know the theory, I've built the systems. And I bring a perspective that most engineers simply don't have.

### Speech Accuracy
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 1 | Every sentence spoken completely (no cut-offs) | | | |
| 2 | No added words not in the transcript | | | |
| 3 | No missing/skipped words from the transcript | | | |
| 4 | Numbers correct (thirty, ninety-five thousand, seven hundred-plus) | | | |
| 5 | "Two AM" spoken naturally (not "two A-M") | | | |

### Comprehension & Naturalness
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 6 | Speech speed feels conversational | | | |
| 7 | Answer directly addresses the question asked | | | |
| 8 | A non-technical recruiter could understand the gist | | | |
| 9 | Tone sounds natural — confident, not defensive | | | |
| 10 | The "hire me because of it" opener lands with impact | | | |

### Content Review
| # | Criteria | Pass | Fail | Notes |
|---|---------|------|------|-------|
| 11 | Not too wordy — could a shorter answer work? | | | |
| 12 | Jargon-free enough for general audience | | | |
| 13 | Key message lands: "operations experience IS an advantage" | | | |

**Content flag:** Strong answer. The "CS graduates understand algorithms / I understand 2 AM failures" contrast is powerful and accessible. The stats (95K lines, 700+ tests) back up the claim. Good length. No changes needed.

**Flagged issues:**
_____________________________________________

---

## GLOBAL ISSUES SUMMARY

### Template Variables (CRITICAL)
The following answers contain `{{variable}}` placeholders that must resolve to actual numbers at runtime. If TTS was generated from raw transcript text, these will be spoken literally as "open curly brace curly brace repos curly brace curly brace" — **a showstopper.**

| Answer | Variables | Expected values |
|--------|----------|----------------|
| Q3 | `{{repos}}`, `{{commits}}`, `{{loc}}` | Actual GitHub stats |
| Q6 | `{{tests}}` | Actual test count |

**Action required:** Play Q3 and Q6 audio first. If template vars are spoken literally, regenerate audio with resolved values.

### Jargon Heat Map

| Answer | Jargon Level | Audience Risk |
|--------|-------------|---------------|
| Q1 | Low | Safe for all |
| Q2 | High | Engineers only |
| Q3 | Low | Safe for all |
| Q4 | High | Engineers only — class names lose recruiters |
| Q5 | High | Technical middle, good bookends |
| Q6 | Low-Med | Mostly safe |
| Q7 | Very High | Engineers only — densest jargon |
| Q8 | Low | Safe for all |
| Q9 | Low | Safe for all — best answer |
| Q10 | Medium | "HNSW" loses people, rest is good |
| Q11 | High | Product names, but cost argument is universal |
| Q12 | Low | Safe for all — second best answer |
| Q13 | Low | Safe for all — strong closer |

### Recommended Rewrites (if targeting mixed audiences)
1. **Q4:** Replace class names with plain descriptions ("one agent for conversation, one for tools, one for memory...")
2. **Q5:** Cut "Silero VAD" and "Faster Whisper" — just say "speech detection" and "transcription"
3. **Q7:** Needs full simplification pass if non-engineers will hear it
4. **Q10:** Replace "HNSW" with "search algorithm"
5. **Q11:** Fewer product names, keep the cost comparison

### Speech Speed Target
- Conversational English: 130–160 words per minute
- Interview/presentation: 120–150 wpm
- If any answer feels rushed or dragging, note the timestamp

### Lip Sync Checklist (all videos)
| # | Criteria | Pass | Fail |
|---|---------|------|------|
| 1 | Mouth opens on speech onset, not before | | |
| 2 | Mouth closes when speech stops | | |
| 3 | Visible lip movement matches vowel sounds | | |
| 4 | No lip movement during pauses | | |
| 5 | Jaw movement feels natural, not mechanical | | |

---

## TESTER SIGN-OFF

**Overall speech accuracy:** ___/10
**Overall naturalness:** ___/10
**Overall content quality:** ___/10
**Overall lip sync quality:** ___/10

**Top 3 issues to fix before launch:**
1. _____________________________________________
2. _____________________________________________
3. _____________________________________________

**Answers that need rewrites:**
_____________________________________________

**Ready to ship?** [ ] Yes  [ ] No — blocked on: _____________
