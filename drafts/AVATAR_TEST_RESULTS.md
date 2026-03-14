# Avatar Interview — Automated Speech + Animation Test Results

**Generated:** 2026-03-13 23:13
**Speech Model:** faster-whisper base.en (CUDA float16)
**Animation Model:** MediaPipe FaceMesh (468 landmarks)
**Method:** Whisper transcription + frame-by-frame face analysis

---

## Executive Summary

| Q | Question | Duration | WPM | Accuracy | Added | Missing | Complete | Status |
|---|---------|----------|-----|----------|-------|---------|----------|--------|
| q1 | What do you build? | 31.4s | 180 (fast) | 96.2% | 17 | 3 | NO | **REVIEW** |
| q2 | How does your LLM routing work? | 32.5s | 159 | 100.0% | 0 | 0 | Yes | **PASS** |
| q3 | What's your background? | 29.1s | 169 | 100.0% | 0 | 0 | Yes | **PASS** |
| q4 | Explain your agent architecture. | 31.5s | 172 (fast) | 95.1% | 13 | 4 | Yes | **PASS** |
| q5 | What was your hardest technical challenge? | 33.6s | 191 (fast) | 100.0% | 0 | 0 | Yes | **PASS** |
| q6 | How do you approach testing? | 31.1s | 162 | 100.0% | 0 | 0 | Yes | **PASS** |
| q7 | How does your RAG system work? | 33.9s | 173 (fast) | 100.0% | 0 | 0 | Yes | **PASS** |
| q8 | Where do you see yourself next? | 27.5s | 150 | 100.0% | 0 | 0 | Yes | **PASS** |
| q9 | How do you handle a project that's failing? | 33.4s | 192 (fast) | 100.0% | 0 | 0 | Yes | **PASS** |
| q10 | How do you learn new technology? | 36.9s | 171 (fast) | 99.0% | 1 | 1 | Yes | **PASS** |
| q11 | How do you make architecture decisions? | 37.7s | 164 | 99.0% | 0 | 1 | Yes | **PASS** |
| q12 | What would you build in your first 90 days? | 35.5s | 184 (fast) | 99.1% | 1 | 1 | Yes | **PASS** |
| q13 | Why you over a traditional CS background? | 40.0s | 129 | 81.1% | 0 | 20 | NO | **REVIEW** |

**Average WPM:** 169 (target: 130–160 for conversational)
**WPM range:** 129–192

---

## Q1: "What do you build?"

**Duration:** 31.4s | **Words:** 94 | **WPM:** 180 | **Accuracy:** 96.2%

### Missing Words (3)
`routes and use`

### Added Words (17)
`roots i take ai from a concept all the way to something you can act when used`

### Completion Issue
**WARNING:** Answer may be cut off — final words don't match expected ending.

**Speed:** Too fast (180 WPM). May be hard to follow.

### Actual Transcription
> So I build AI systems, like full production systems, not just demos. My main project is Isabelle, she's a voice assistant I built from scratch. Seven specialized agents working together, roots across five different language models, handles real-time voice, the whole pipeline. I also built an enterprise SaaS platform called Stafel, with six different role-based portals. But yeah, the short answer is, I take AI from a concept all the way to something you can actually ship. I take AI from a concept all the way to something you can act when used.

---

## Q2: "How does your LLM routing work?"

**Duration:** 32.5s | **Words:** 86 | **WPM:** 159 | **Accuracy:** 100.0%

**Speed:** Good (159 WPM).

### Actual Transcription
> Yeah, so the routing is, it's actually one of my favorite parts. I've got five models set up. There's a fast local model for quick responses under 400 milliseconds. Then Claude handles the deeper reasoning, and Gemini handles anything visual, like images. And there's a classifier that looks at each request and decides which model should handle it, based on how complex it is, what context is needed, and what it costs. So it's not random. It's intelligent routing with automatic fallbacks if something goes down.

---

## Q3: "What's your background?"

**Duration:** 29.1s | **Words:** 82 | **WPM:** 169 | **Accuracy:** 100.0%

**Speed:** Good (169 WPM).

### Actual Transcription
> Honestly, I spent 30 years in transportation operations, managing distributed teams, logistics, making time-critical decisions with incomplete information, and then I just got obsessed with AI like fully obsessed, built a real portfolio in under two years. Every concept I studied I immediately turned into working code. I don't have a CS degree, I'll be upfront about that. But I've got almost 40 repos, over a thousand commits, and almost a million lines of production code. The work speaks for itself.

---

## Q4: "Explain your agent architecture."

**Duration:** 31.5s | **Words:** 90 | **WPM:** 172 | **Accuracy:** 95.1%

### Missing Words (4)
`isabelle claude 30 2`

### Added Words (13)
`isabel cloud 32 assistant and can run in parallel which was h1stly the`

**Speed:** Too fast (172 WPM). May be hard to follow.

### Actual Transcription
> Okay, so Isabel has this orchestrator, think of it like a manager, and it coordinates seven specialized agents, each with its own job. One handles conversation, one does complex reasoning with Cloud or Gemini, one can run 32 different tools, another handles longer workflows autonomously, one processes images and screenshots, and one manages memory, so the assistant actually remembers things across conversations. They all share state and can run in parallel, which was honestly the assistant and can run in parallel, which was honestly the hardest part to get right.

---

## Q5: "What was your hardest technical challenge?"

**Duration:** 33.6s | **Words:** 107 | **WPM:** 191 | **Accuracy:** 100.0%

**Speed:** Too fast (191 WPM). May be hard to follow.

### Actual Transcription
> Oh man, real time voice, hands down, getting the full round trip latency. From when you stop talking to when the assistant starts responding, under 500 milliseconds it was a grind. You've got speech detection, transcription, the language model thinking, then generating the voice response all while doing echo cancellation so it doesn't hear itself. And all of this is running on a single GPU with 7 plus models loaded at once. One model uses too much memory and the whole thing falls over. But the goal was to make it feel like a real conversation, not like talking to a robot. And I think we got there.

---

## Q6: "How do you approach testing?"

**Duration:** 31.1s | **Words:** 84 | **WPM:** 162 | **Accuracy:** 100.0%

**Speed:** Good (162 WPM).

### Actual Transcription
> I'm kind of obsessive about it honestly. Over 700 tests, unit, integration, end-to-end, even chaos testing where I break things on purpose. Every module has its own test suite. When I fix a bug, the first thing I do is write a test that reproduces it, then I fix it, then I make sure the test passes. GitHub Actions runs everything automatically on every push. My philosophy is basically, if it doesn't have tests, it doesn't work. You just don't know it's broken yet.

---

## Q7: "How does your RAG system work?"

**Duration:** 33.9s | **Words:** 98 | **WPM:** 173 | **Accuracy:** 100.0%

**Speed:** Too fast (173 WPM). May be hard to follow.

### Actual Transcription
> So when the assistant needs to look something up, it uses two search methods at the same time. One for exact keyword matches and one that understands meaning. Both run in parallel and the results get merged and ranked. On top of that, there's a knowledge base with over 500 skills it can draw from. And then memory is layered. Recent stuff stays in the current session. Older context goes into a database and long-term knowledge lives in a dedicated search engine. So the assistant genuinely remembers things across conversations. It's not just search, it's actual memory.

---

## Q8: "Where do you see yourself next?"

**Duration:** 27.5s | **Words:** 69 | **WPM:** 150 | **Accuracy:** 100.0%

**Speed:** Good (150 WPM).

### Actual Transcription
> I mean, I want to be doing exactly this, but at scale. Building production AI systems, shipping real products. I'm looking at roles like AI engineer, applications engineer, anywhere I can build multi-agent systems and real-time pipelines. What I bring is, I'm a builder. I don't just read about this stuff. I've deployed every concept I've learned into working software, and I'm ready to bring that to a team.

---

## Q9: "How do you handle a project that's failing?"

**Duration:** 33.4s | **Words:** 107 | **WPM:** 192 | **Accuracy:** 100.0%

**Speed:** Too fast (192 WPM). May be hard to follow.

### Actual Transcription
> First thing I do is stop guessing. I look at the actual error, trace it back to the root cause. Not the symptom, the real origin. I've got a rule. If I can't fix it in two attempts, I stop and rethink the approach entirely. I don't do band-aid fixes. If the architecture is wrong, I fix the architecture. I've killed features, rewritten modules, thrown away days of work when the foundation wasn't right. It's painful in the moment, but six months later you're not drowning in technical debt. What matters most is being honest early. Don't hide problems, surface them fast and fix them at the source.

---

## Q10: "How do you learn new technology?"

**Duration:** 36.9s | **Words:** 105 | **WPM:** 171 | **Accuracy:** 99.0%

### Missing Words (1)
`learn`

### Added Words (1)
`learned`

**Speed:** Too fast (171 WPM). May be hard to follow.

### Actual Transcription
> Building. That's how I learned. Seriously. Every single concept I've studied, I turned into working code within days. Not tutorials, not toy examples, real systems. When I wanted to understand how multiple AI agents work together, I built a seven-agent system from scratch. When I wanted to learn how search engines work internally, I built one from the ground up instead of using a hosted service. I went from zero programming experience to almost a million lines of production code in under two years. The secret is, I don't move on until I've shipped something that actually works. Theory without implementation is just trivia.

---

## Q11: "How do you make architecture decisions?"

**Duration:** 37.7s | **Words:** 103 | **WPM:** 164 | **Accuracy:** 99.0%

### Missing Words (1)
`percent`

**Speed:** Good (164 WPM).

### Actual Transcription
> Every decision gets logged, what we chose, what we rejected, and why. It's not just gut feeling. Here's an example. For search, I could have paid 70 plus dollars a month for a hosted service. Instead, I built my own. The trade-off is, I own the maintenance, but I eliminated an outside dependency and a recurring cost. Same thinking with the model routing, why pay for one expensive model to handle everything, when a classifier can send 70% of requests to a free local model. I always start with, what's the simplest thing that solves the actual problem, and what are the real trade-offs?

---

## Q12: "What would you build in your first 90 days?"

**Duration:** 35.5s | **Words:** 109 | **WPM:** 184 | **Accuracy:** 99.1%

### Missing Words (1)
`im`

### Added Words (1)
`on`

**Speed:** Too fast (184 WPM). May be hard to follow.

### Actual Transcription
> First, 30 days on listening and reading, understanding the existing systems, the pain points, the technical debt, not proposing big changes yet. I'd pick up a few quick wins to build trust and learn the codebase through real work. Days 30 to 60, I'd start identifying where AI can have the biggest impact. Maybe it's a pipeline that's too slow. Maybe it's a manual process that could be automated. Maybe there's no visibility into what's failing. By day 90, I'd want to have shipped at least one meaningful improvement and have a concrete proposal for a bigger initiative. I'm not the guy who spends three months making slides. I ship.

---

## Q13: "Why you over a traditional CS background?"

**Duration:** 40.0s | **Words:** 86 | **WPM:** 129 | **Accuracy:** 81.1%

### Missing Words (20)
`i dont just know the theory ive built the systems and i bring a perspective that most engineers dont have`

### Completion Issue
**WARNING:** Answer may be cut off — final words don't match expected ending.

**Speed:** Good (129 WPM).

### Actual Transcription
> Honestly, hire me because of it, not despite it. 30 years of managing complex operations, distributed teams, time critical logistics, decisions with incomplete data. That's exactly the kind of systems thinking that makes good AI infrastructure. CS graduates understand algorithms. I understand what happens when your system breaks at 2 in the morning and there's real money on the line. Plus, I've proven I can learn. Almost a million lines of production code. Over 700 tests, multi-agent systems, voice pipelines. All built in under 2 years.

---


# Part 2: Animation & Visual Analysis

---

## Animation Summary

| Video | Face % | Blinks | Blink/s | Blink OK | Head OK | Sync Ratio | Onset OK | Status |
|-------|--------|--------|---------|----------|---------|------------|----------|--------|
| idle | 100.0% | 1 | 0.09 | NO | Yes | N/A | N/A | **REVIEW (blink)** |
| q1 | 99.9% | 8 | 0.26 | Yes | Yes | 0.9x | Yes | **REVIEW (lip-sync)** |
| q2 | 99.9% | 5 | 0.15 | Yes | Yes | 1.5x | Yes | **PASS** |
| q3 | 100.0% | 10 | 0.27 | Yes | Yes | 1.2x | Yes | **PASS** |
| q4 | 99.9% | 12 | 0.3 | Yes | Yes | 1.0x | Yes | **REVIEW (lip-sync)** |
| q5 | 99.9% | 8 | 0.21 | Yes | Yes | 1.1x | Yes | **REVIEW (lip-sync)** |
| q6 | 99.9% | 9 | 0.3 | Yes | Yes | 1.4x | Yes | **PASS** |
| q7 | 99.9% | 8 | 0.23 | Yes | Yes | 0.7x | NO | **REVIEW (lip-sync, onset-lag)** |
| q8 | 99.9% | 5 | 0.17 | Yes | Yes | 1.2x | NO | **REVIEW (lip-sync, onset-lag)** |
| q9 | 99.9% | 8 | 0.24 | Yes | Yes | 1.2x | Yes | **PASS** |
| q10 | 99.9% | 7 | 0.2 | Yes | Yes | 1.2x | Yes | **PASS** |
| q11 | 99.9% | 11 | 0.27 | Yes | Yes | 1.2x | NO | **REVIEW (onset-lag)** |
| q12 | 100.0% | 12 | 0.33 | Yes | Yes | 0.8x | Yes | **REVIEW (lip-sync)** |
| q13 | 99.9% | 12 | 0.3 | Yes | Yes | 1.2x | Yes | **REVIEW (lip-sync)** |

### Thresholds
- **Blink rate:** 0.15–0.6 blinks/sec (9–36 per minute) = natural
- **Head frozen:** Near-zero variance in nose position = robotic
- **Lip sync ratio:** mouth openness during speech / during silence. >1.5 = good, 1.2–1.5 = acceptable, <1.2 = poor
- **Onset alignment:** Mouth opens within 200ms of first speech = good
- **Idle mouth:** Mean mouth openness should be low, std < 3.0 (no movement)

---

## IDLE VIDEO Analysis

- **Duration:** 10.6s (264 frames)
- **Face detected:** 100.0%
- **Blinks:** 1 (0.09/sec) — UNNATURAL
- **Head movement:** avg 0.0px/frame — Subtle movement detected
- **Mouth:** mean=0.2, std=0.1, max=1.0
- **Mouth idle:** Good — minimal/no mouth movement

---

## Q1 Animation: "What do you build?"

- **Face detected:** 99.9%
- **Blinks:** 8 (0.26/sec) — Natural
- **Head:** avg movement 0.88px/frame, variance 56.9 — Natural
- **Lip sync ratio:** 0.94x (poor) (mouth during speech / during silence)
- **Onset alignment:** Yes
- **Mouth:** mean=4.0, std=4.5, max=22.1

---

## Q2 Animation: "How does your LLM routing work?"

- **Face detected:** 99.9%
- **Blinks:** 5 (0.15/sec) — Natural
- **Head:** avg movement 0.91px/frame, variance 46.6 — Natural
- **Lip sync ratio:** 1.53x (good) (mouth during speech / during silence)
- **Onset alignment:** Yes
- **Mouth:** mean=4.6, std=4.1, max=19.7

---

## Q3 Animation: "What's your background?"

- **Face detected:** 100.0%
- **Blinks:** 10 (0.27/sec) — Natural
- **Head:** avg movement 0.79px/frame, variance 31.5 — Natural
- **Lip sync ratio:** 1.21x (acceptable) (mouth during speech / during silence)
- **Onset alignment:** Yes
- **Mouth:** mean=3.8, std=3.9, max=18.6

---

## Q4 Animation: "Explain your agent architecture."

- **Face detected:** 99.9%
- **Blinks:** 12 (0.3/sec) — Natural
- **Head:** avg movement 0.60px/frame, variance 27.1 — Natural
- **Lip sync ratio:** 0.97x (poor) (mouth during speech / during silence)
- **Onset alignment:** Yes
- **Mouth:** mean=4.1, std=4.2, max=20.0

---

## Q5 Animation: "What was your hardest technical challenge?"

- **Face detected:** 99.9%
- **Blinks:** 8 (0.21/sec) — Natural
- **Head:** avg movement 0.85px/frame, variance 41.3 — Natural
- **Lip sync ratio:** 1.06x (poor) (mouth during speech / during silence)
- **Onset alignment:** Yes
- **Mouth:** mean=4.6, std=4.1, max=18.3

---

## Q6 Animation: "How do you approach testing?"

- **Face detected:** 99.9%
- **Blinks:** 9 (0.3/sec) — Natural
- **Head:** avg movement 0.70px/frame, variance 49.2 — Natural
- **Lip sync ratio:** 1.37x (acceptable) (mouth during speech / during silence)
- **Onset alignment:** Yes
- **Mouth:** mean=4.2, std=3.7, max=18.3

---

## Q7 Animation: "How does your RAG system work?"

- **Face detected:** 99.9%
- **Blinks:** 8 (0.23/sec) — Natural
- **Head:** avg movement 0.97px/frame, variance 59.1 — Natural
- **Lip sync ratio:** 0.70x (poor) (mouth during speech / during silence)
- **Onset alignment:** NO — mouth lags speech start
- **Mouth:** mean=3.9, std=3.9, max=27.5

---

## Q8 Animation: "Where do you see yourself next?"

- **Face detected:** 99.9%
- **Blinks:** 5 (0.17/sec) — Natural
- **Head:** avg movement 0.81px/frame, variance 38.5 — Natural
- **Lip sync ratio:** 1.17x (poor) (mouth during speech / during silence)
- **Onset alignment:** NO — mouth lags speech start
- **Mouth:** mean=4.5, std=4.5, max=20.9

---

## Q9 Animation: "How do you handle a project that's failing?"

- **Face detected:** 99.9%
- **Blinks:** 8 (0.24/sec) — Natural
- **Head:** avg movement 0.83px/frame, variance 36.7 — Natural
- **Lip sync ratio:** 1.25x (acceptable) (mouth during speech / during silence)
- **Onset alignment:** Yes
- **Mouth:** mean=3.7, std=3.6, max=19.5

---

## Q10 Animation: "How do you learn new technology?"

- **Face detected:** 99.9%
- **Blinks:** 7 (0.2/sec) — Natural
- **Head:** avg movement 0.88px/frame, variance 38.2 — Natural
- **Lip sync ratio:** 1.22x (acceptable) (mouth during speech / during silence)
- **Onset alignment:** Yes
- **Mouth:** mean=5.1, std=4.2, max=19.8

---

## Q11 Animation: "How do you make architecture decisions?"

- **Face detected:** 99.9%
- **Blinks:** 11 (0.27/sec) — Natural
- **Head:** avg movement 0.88px/frame, variance 35.1 — Natural
- **Lip sync ratio:** 1.23x (acceptable) (mouth during speech / during silence)
- **Onset alignment:** NO — mouth lags speech start
- **Mouth:** mean=3.7, std=3.7, max=15.6

---

## Q12 Animation: "What would you build in your first 90 days?"

- **Face detected:** 100.0%
- **Blinks:** 12 (0.33/sec) — Natural
- **Head:** avg movement 0.78px/frame, variance 40.4 — Natural
- **Lip sync ratio:** 0.75x (poor) (mouth during speech / during silence)
- **Onset alignment:** Yes
- **Mouth:** mean=4.2, std=4.1, max=17.2

---

## Q13 Animation: "Why you over a traditional CS background?"

- **Face detected:** 99.9%
- **Blinks:** 12 (0.3/sec) — Natural
- **Head:** avg movement 1.04px/frame, variance 53.1 — Natural
- **Lip sync ratio:** 1.17x (poor) (mouth during speech / during silence)
- **Onset alignment:** Yes
- **Mouth:** mean=4.6, std=4.0, max=23.0
