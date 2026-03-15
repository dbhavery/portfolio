"""TTS-optimized transcripts for Chatterbox voice generation.

These use phonetic spellings for technical terms so TTS
pronounces them correctly. The display transcripts (in HTML)
use proper spelling for human readability.

Reference voice: I:/IsabelleData/media/audio/2025/12/2025_12_24_11_36_25_1.mp3

Rewritten 2026-03-13: reduced jargon, fixed template vars, fixed cut-offs,
hardcoded stats (37 repos, 1372 commits, 888K lines, 2066 tests across all projects).
"""

TTS_TRANSCRIPTS = {
    "q1": (
        "So, I build A.I. systems — like, full production systems, not just demos. "
        "My main project is Isabelle, she's a voice assistant I built from scratch. "
        "Seven specialized agents working together, routes across five different language models, "
        "handles real-time voice... the whole pipeline. I also built an enterprise sass platform "
        "called StaFull with six different role-based portals. But yeah, the short answer is — "
        "I take A.I. from a concept all the way to something you can actually ship and use."
    ),
    "q2": (
        "Yeah so the routing is — it's actually one of my favorite parts. "
        "I've got five models set up. There's a fast local model for quick responses — "
        "under four hundred milliseconds. Then Claude handles the deeper reasoning, "
        "and Gemini handles anything visual, like images. "
        "And there's a classifier that looks at each request and decides which model should "
        "handle it — based on how complex it is, what context is needed, and what it costs. "
        "So it's not random. It's intelligent routing, with automatic fallbacks "
        "if something goes down."
    ),
    "q3": (
        "Honestly? I spent thirty years in transportation operations — managing distributed "
        "teams, logistics, making time-critical decisions with incomplete information. "
        "And then I just... got obsessed with A.I. Like, fully obsessed. Built a real portfolio "
        "in under two years. Every concept I studied, I immediately turned into working code. "
        "I don't have a C.S. degree — I'll be upfront about that — but I've got almost forty "
        "repos, over a thousand commits, and almost a million lines of production code. "
        "The work speaks for itself."
    ),
    "q4": (
        "Okay so Isabelle has this orchestrator — think of it like a manager — "
        "and it coordinates seven specialized agents, each with its own job. "
        "One handles conversation, one does complex reasoning with Claude or Gemini, "
        "one can run thirty-two different tools, another handles longer workflows autonomously, "
        "one processes images and screenshots, and one manages memory so the assistant "
        "actually remembers things across conversations. They all share state and can "
        "run in parallel — which was honestly the hardest part to get right."
    ),
    "q5": (
        "Oh man, real-time voice. Hands down. Getting the full round-trip latency — "
        "from when you stop talking to when the assistant starts responding — under "
        "five hundred milliseconds... it was a grind. You've got speech detection, "
        "transcription, the language model thinking, then generating the voice response — "
        "all while doing echo cancellation so it doesn't hear itself. And all of this is "
        "running on a single GPU with seven-plus models loaded at once. One model uses "
        "too much memory and the whole thing falls over. But the goal was to make it "
        "feel like a real conversation, not like talking to a robot. And I think we got there."
    ),
    "q6": (
        "I'm kind of obsessive about it, honestly. Over two thousand tests — unit, "
        "integration, end-to-end, even chaos testing where I break things on purpose. "
        "Every module has its own test suite. When I fix a bug, the first thing I do is "
        "write a test that reproduces it. Then I fix it, then I make sure the test passes. "
        "GitHub Actions runs everything automatically on every push. My philosophy is "
        "basically — if it doesn't have tests, it doesn't work. You just don't know "
        "it's broken yet."
    ),
    "q7": (
        "So when the assistant needs to look something up, it uses two search methods "
        "at the same time — one for exact keyword matches and one that understands meaning. "
        "Both run in parallel, and the results get merged and ranked. On top of that, "
        "there's a knowledge base with over five hundred skills it can draw from. "
        "And then memory is layered — recent stuff stays in the current session, "
        "older context goes into a database, and long-term knowledge lives in a "
        "dedicated search engine. So the assistant genuinely remembers things across "
        "conversations. It's not just search — it's actual memory."
    ),
    "q8": (
        "I mean, I want to be doing exactly this but at scale. Building production A.I. systems, "
        "shipping real products. I'm looking at roles like A.I. Engineer, "
        "Applications Engineer, anywhere I can build multi-agent systems and real-time pipelines. "
        "What I bring is... I'm a builder. I don't just read about this stuff, I've "
        "deployed every concept I've learned into working software. And I'm ready to bring that "
        "to a team."
    ),
    "q9": (
        "First thing I do is stop guessing. I look at the actual error, trace it back to the "
        "root cause — not the symptom, the real origin. I've got a rule: if I can't fix it in "
        "two attempts, I stop and rethink the approach entirely. I don't do band-aid fixes. If "
        "the architecture is wrong, I fix the architecture. I've killed features, rewritten modules, "
        "thrown away days of work when the foundation wasn't right. It's painful in the moment, "
        "but six months later you're not drowning in technical debt. What matters most is being "
        "honest early — don't hide problems, surface them fast, and fix them at the source."
    ),
    "q10": (
        "Building. That's how I learn. Seriously — every single concept I've studied, I turned into "
        "working code within days. Not tutorials, not toy examples — real systems. When I wanted "
        "to understand how multiple A.I. agents work together, I built a seven-agent system from "
        "scratch. When I wanted to learn how search engines work internally, I built one from the "
        "ground up instead of using a hosted service. I went from zero programming experience to "
        "almost a million lines of production code in under two years. The secret "
        "is I don't move on until I've shipped something that actually works. Theory without "
        "implementation is just trivia."
    ),
    "q11": (
        "Every decision gets logged — what we chose, what we rejected, and why. It's not just "
        "gut feeling. Here's an example: for search, I could have paid seventy-plus dollars a month "
        "for a hosted service. Instead, I built my own. The trade-off is I own the maintenance, "
        "but I eliminated an outside dependency and a recurring cost. Same thinking with the model "
        "routing — why pay for one expensive model to handle everything when a classifier can "
        "send seventy percent of requests to a free local model? I always start with: what's the "
        "simplest thing that solves the actual problem, and what are the real trade-offs?"
    ),
    "q12": (
        "First thirty days, I'm listening and reading. Understanding the existing systems, the "
        "pain points, the technical debt — not proposing big changes yet. I'd pick up a few "
        "quick wins to build trust and learn the codebase through real work. Days thirty to sixty, "
        "I'd start identifying where A.I. can have the biggest impact — maybe it's a pipeline "
        "that's too slow, maybe it's a manual process that could be automated, maybe there's no "
        "visibility into what's failing. By day ninety, I'd want to have shipped "
        "at least one meaningful improvement and have a concrete proposal for a bigger initiative. "
        "I'm not the guy who spends three months making slides. I ship."
    ),
    "q13": (
        "Honestly? Hire me because of it, not despite it. Thirty years of managing complex "
        "operations — distributed teams, time-critical logistics, decisions with incomplete data — "
        "that's exactly the kind of systems thinking that makes good A.I. infrastructure. "
        "C.S. graduates understand algorithms. I understand what happens when your system breaks "
        "at two in the morning and there's real money on the line. Plus, I've proven I can learn. "
        "Almost a million lines of production code, over two thousand tests, "
        "multi-agent systems, voice pipelines — all built in under two years. "
        "I don't just know the theory, I've built the systems. And I bring a perspective "
        "that most engineers don't have."
    ),
}
