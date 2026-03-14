# DONALD HAVERY

**AI Systems Builder | Full-Stack Developer | Enterprise SaaS Architect**

Remote, US | dbhavery@gmail.com | github.com/dbhavery

---

## PROFESSIONAL SUMMARY

AI systems builder and full-stack developer with 37 GitHub repositories, 1,372+ commits, and 888K+ lines of production code across enterprise SaaS, real-time AI voice assistants, multi-agent orchestration platforms, and AI-powered business tools. Designed and shipped Dispatch — an enterprise SaaS platform for mobile fuel delivery with 6 role-based portals, 9 access tiers, real-time fleet tracking, AI route optimization, and cloud deployment across Railway and Neon PostgreSQL. Independently architected Aether — a production AI voice assistant with 7-agent orchestration, 5-model LLM routing, real-time avatar animation, and 2,000+ automated tests. Built Citadel (AI operations platform), Cortex (autonomous media cataloger), Herald (customer operations), Sentinel (compliance automation), and Vaultwise (knowledge management) — each a production-grade FastAPI application with full test suites. Was building custom AI agents, persistent memory systems, and autonomous development workflows before these became industry features. Brings 30 years and 3.5M+ miles in transportation operations — from CDL training and regional dispatch supervision to line haul freight — the rare combination of enterprise domain expertise and hands-on AI engineering that organizations cannot find in traditional candidates.

---

## TECHNICAL SKILLS

**AI & Machine Learning**
Claude (Sonnet/Opus), Google Gemini (Pro/Flash), Ollama, Qwen, OpenAI Whisper, HuggingFace, PyTorch, ONNX Runtime, ChromaDB, LangGraph, FLUX.1-dev, diffusers, transformers, DreamBooth LoRA, QLoRA fine-tuning

**AI Agent Architecture**
Multi-agent orchestration, intelligent intent routing & classification, LLM function calling & tool use, RAG (Retrieval-Augmented Generation), vector search (BM25 + dense), prompt engineering, context window management, skill/tool registries, autonomous development loops

**Frontend**
React 18, TypeScript, JavaScript (ES6+), Vite, Recharts (data visualization), Leaflet (interactive maps), Socket.io (real-time), React Router, CSS Modules, custom design systems, responsive design

**Backend**
Python (asyncio, FastAPI), Node.js, Express.js, Prisma ORM, REST API design, WebSocket servers, JWT authentication, bcrypt, Helmet security, rate limiting, Winston logging, CORS

**Cloud & Deployment**
Vercel, Railway, Neon PostgreSQL, Docker Compose, GitHub Actions CI/CD, custom domain configuration, SSL/TLS, environment-based configuration

**Mobile & Desktop**
Kotlin (Jetpack Compose, Android), PySide6 (Qt6, Windows), WebRTC, Firebase Cloud Messaging, biometric authentication (Windows Hello, Face/Fingerprint), Tailscale VPN

**Voice & Audio AI**
Faster-Whisper STT, ElevenLabs Scribe v2 (real-time STT), Kokoro TTS, Chatterbox voice cloning, ElevenLabs TTS, Silero VAD, Picovoice Porcupine wake word, ECAPA-TDNN speaker verification, echo cancellation

**Computer Vision & Avatar**
InsightFace/ArcFace, LivePortrait, Audio2Face-3D ONNX, Unreal Engine 5 MetaHuman, Pixel Streaming, BLIP captioning, Moondream, Qwen2.5-VL

**Data & Infrastructure**
ChromaDB (vector DB), SQLite, PostgreSQL, Redis, Prisma ORM, Peewee ORM, Google APIs (Drive/Gmail/Calendar), Firebase, Git (1,372+ commits)

**Hardware & IoT**
Raspberry Pi, Arduino, sensor integration, embedded systems prototyping, hardware-software interface development

---

## PROJECTS PORTFOLIO

### Aether — Production AI Voice Assistant (2 Generations)
**github.com/dbhavery/aether** | Python | 1,372+ commits | v1: 152K+ LOC, v2: 9.5K LOC | 2,000+ automated tests

Built a complete real-time AI voice assistant from scratch across two generations — original architecture, multi-agent orchestration, real-time voice processing, photorealistic avatar animation, and cross-platform deployment to desktop, Android, Telegram, and WebSocket.

**Multi-Agent Orchestration**
- Designed **OrchestratorAgent + 7 sub-agent architecture** (ConversationNode, GeminiNode, ClaudeNode, ToolNode, AgentNode, VisionNode, MemoryNode) — each agent specialized for its domain, coordinated by a central orchestrator with timing, filler generation, and barge-in detection
- Built **5-model intelligent LLM routing** with multi-layer intent classification: instant regex match, user override detection, keyword patterns (77 phrases), real-time context, LLM classification fallback (local Qwen, 50-100ms), and automatic tier downgrade on failure — routing across local Qwen (91-380ms), Claude Sonnet/Opus, and Gemini Pro/Flash
- Implemented **32 core tools and 509 skills** with dynamic Gemini function declarations, fuzzy matching, agentic tool-calling loops (max 5 rounds with result injection), and usage analytics
- Built v2 clean rewrite in **1,372+ commits over 3 days** — modular EventBus architecture with backpressure, 16 modules (12 core + 4 extensions), typed event system, and security-first design with 2 completed audit waves

**Real-Time Voice Pipeline**
- Engineered **449ms p50 latency** (microphone to first audio output): Silero VAD, Faster-Whisper STT (82ms) with ElevenLabs Scribe v2 real-time fallback (30-80ms), intent routing, LLM streaming, sentence-by-sentence TTS synthesis via Chatterbox Turbo voice cloning — competitive with commercial voice assistants
- Implemented **Picovoice Porcupine wake word** detection (92.5% accuracy), speaker verification with dynamic enrollment (ECAPA-TDNN, tiered confidence, EMA updates, 500-sample LRU), and process watchdog with auto-restart on health check failures

**Memory & Intelligence**
- Built **tiered memory system**: 5GB LRU hot cache (v1) / 512MB (v2), gzip-compressed cold storage, ChromaDB RAG with hybrid search (BM25 + dense vector via nomic-embed-text-v2-moe), SQLite knowledge base with SHA-256 dedup, and AdaptiveLearner tracking user preferences, corrections, and barge-ins for continuous routing improvement
- Created **LangGraph agent orchestration** (v2) with research and writing sub-agents, daily persona interview system, memory correction detection, and busy-state detection

**Real-Time Avatar Animation**
- Created **Audio2Face-3D ONNX pipeline** (98 FPS on CPU) generating 52 ARKit blendshapes via diffusion model, streamed through custom TCP binary protocol to UE5 MetaHuman with Pixel Streaming video delivery
- Built **Ditto motion pipeline**: HuBERT audio encoding (1024-dim @ 25fps) feeding LMDM conditional diffusion transformer for 265-dim motion synthesis, rendered through LivePortrait warping network — 20-23 FPS at 3.3GB VRAM, 98-100% lip sync detection
- Implemented **LivePortrait integration** with precomputed keypoint ring buffer achieving 23+ FPS at 512x512 on RTX 3090 Ti, MJPEG stream relay to desktop client

**Cross-Platform Deployment**
- **Windows Desktop**: PySide6 neumorphic UI with 3 views (text chat, voice call, full-screen video), Windows Hello biometric auth, settings panel with YAML round-trip config sync, system tray integration, always-on-top mode
- **Android**: Kotlin/Jetpack Compose with WebRTC video, biometric auth, FCM push notifications, Tailscale network-aware auto-switching (WiFi/cellular), real-time conversation sync
- **Telegram Bot** and **WebSocket Server** with binary protocol (14 message types), token authentication, rate limiting, 10-client connection limit

**Security & Quality**
- Built **three-layer security**: command injection blocking (11 regex bypass patterns), PurePosixPath path traversal protection, permission framework, WebSocket token auth (32-byte hex, constant-time verify), PC control allowlists, prompt injection defense ([EXTERNAL_CONTENT] trust boundaries)
- Managed **GPU coordination** across 7+ models within 24GB VRAM: priority-based loading, lazy initialization, tensor offloading, automatic idle unloading
- Wrote **2,000+ automated tests**: unit, integration, performance benchmarking, chaos/failure injection, end-to-end — with pytest, Ruff linting, Pyright type checking, Bandit security scanning, and GitHub Actions CI/CD

---

### Citadel — AI Operations Platform
**github.com/dbhavery/citadel** | Python | 6 packages | 10K+ LOC | 100% test coverage

- Built modular monorepo for production AI infrastructure with **zero-dependency HNSW vector search** — eliminates $70+/mo managed vector DB costs with pure Python implementation
- Designed **multi-provider LLM routing** with automatic failover across Claude, Gemini, and Ollama with semantic caching that saves $0.01-0.10 per cached hit
- Implemented **ReAct agent framework** with tool execution, thought chains, and multi-step reasoning across 6 independently deployable packages

---

### FuelFleet — Enterprise SaaS Platform for Mobile Fuel Delivery
**github.com/dbhavery/fuelfleet-platform** | 12 repositories | 1,372+ commits | 19K+ LOC | 19K+ lines CSS
React 18, TypeScript, Node.js, Express, Prisma, PostgreSQL, Socket.io, Leaflet, Recharts | Deployed on Railway + Vercel

Designed, architected, and built a complete enterprise SaaS platform for a mobile fuel delivery business from concept to cloud deployment — 6 portals, 9 user roles, real-time fleet tracking, AI route optimization, and a 255-input simulation engine. This is not a tutorial project; it is a production-ready startup platform with custom domains, role-based access control, and cloud infrastructure.

**Platform Architecture**
- Architected **microservices ecosystem** with 12 repositories: 6 independent portals, shared design system, core API engine, simulation engine, and deployment infrastructure — each service independently deployable with shared authentication and design tokens
- Built **Core Engine API** (Express.js + Prisma ORM + Neon PostgreSQL) with JWT authentication, bcrypt password hashing, Helmet security headers, rate limiting, file uploads (multer), structured logging (Winston), CORS management, and real-time event streaming (Socket.io)
- Deployed **full cloud infrastructure** on Railway with custom domain routing, auto-generated SSL certificates, and PostgreSQL via Neon connection pooling

**6 Role-Based Portals**
- **HQ Command Center** (Holdings Admin) — 18-page admin dashboard with financial analytics, franchise monitoring, marketing campaign management, legal/compliance tracking, SBA lending metrics, live website content editor, and real-time fleet maps (React-Leaflet) with KPI dashboards (Recharts). Secondary authentication gates on sensitive areas
- **Franchise Portal** — Dual-mode interface: P&L Cockpit for franchise owners and Mission Control for managers (daily operations, delivery scheduling, driver/vehicle management, fuel inventory)
- **Driver Co-Pilot** — 4-mode operational interface (Parked, Driving, Delivery, Resupply) with real-time route optimization, customer eligibility checks, fuel tank monitoring, safety alerts
- **Customer Portal** — 5 sub-portals: Residential, B2B Employer, B2C Employee, Investor, SBA Lender
- **Unified Auth Gateway** — Centralized authentication across all portals

**Simulation & Testing Engine**
- Engineered **255-input Simulation Engine** (TypeScript) generating realistic data across 20 categories — vehicle GPS/telemetry, fuel dispensing, AI safety camera feeds, driver performance, payment processing, environmental conditions, equipment maintenance, and anomaly detection
- Built 9 scenario presets with time control (pause/resume/1x-100x speed), per-vehicle WebSocket subscriptions, manual sensor override injection

---

### Cortex — AI Media Cataloger
**github.com/dbhavery/cortex** | Python (FastAPI) | 164 tests | 28 file types

- Built autonomous media indexing system with **BLIP captioning**, **InsightFace face recognition** (512-dim ArcFace embeddings with DBSCAN clustering), and Google Photos/Drive sync — processes 5,700+ files with zero manual intervention
- Designed continuous processing pipeline — drop a file in, it's captioned, face-detected, categorized, and searchable within 60 seconds
- Content-hash deduplication (SHA-256) handles renames, copies, and cross-source duplicates across local and cloud storage

---

### Herald — Customer Operations Platform
**github.com/dbhavery/herald** | Python (FastAPI) | 95 tests | 34 endpoints

- Built AI-powered customer ops platform reducing support response time from minutes to seconds with **citation-backed AI responses** and pluggable LLM backend
- Implemented **TF-IDF weighted lexicon sentiment scoring** with IDF corpus weighting, 6-category auto-categorization, and 5-factor customer health scoring (activity, sentiment, tickets, plan, tenure)
- Designed churn prediction and SLA analytics with real-time dashboards

---

### Sentinel — Compliance Autopilot
**github.com/dbhavery/sentinel** | Python (FastAPI) | 50 tests | 62 requirements | 14 templates

- Built automated compliance platform for **SOC 2, GDPR, HIPAA** — gap analysis in seconds vs weeks of manual audit
- Implemented AI policy generation, document scanning, drift monitoring, and audit-ready report generation with configurable framework templates

---

### Vaultwise — Knowledge Management Platform
**github.com/dbhavery/vaultwise** | Python (FastAPI) | 133 tests | 20 endpoints

- Built **TF-IDF search engine from scratch** — zero ML dependencies, pure Python tokenization, stop word removal, TF/IDF calculation, L2 normalization, and cosine similarity
- Designed document ingestion with word-based chunking, AI-powered Q&A with source citations, and auto-generated training articles and quizzes

---

### Custom Image Generator & Editor (CIGE)
**github.com/dbhavery/Custom-Image-Generator-and-Editor** | Python/PyTorch | 127 tests

- Built local AI image generation — **$0 per image** vs $0.02-0.10 on cloud APIs. FLUX.1-dev for quality, RealVisXL Lightning for speed
- Implemented VRAM-aware model management with neumorphic desktop UI (PySide6), 3 generation modes, and CUDA-optimized inference on RTX 3090 Ti

---

### Autoloop — Autonomous Development Loop
**github.com/dbhavery/autoloop** | Bash | 573 BATS tests

- Built hands-free task execution wrapper for Claude Code with **dual-condition exit gate** — requires both heuristic completion indicators AND explicit exit signal to prevent premature stops
- Implemented **circuit breaker pattern** detecting stagnation (3 loops no changes), repeated errors (5 loops same error), and output decline (>70% drop) with automatic recovery
- Three-layer API limit detection (timeout guard, structural JSON, filtered text fallback) — zero dependencies beyond Bash 4.0+ and jq

---

### AI Developer Tools
**github.com/dbhavery** | Python | 5 tools | 196 tests

- **fineforge** — Fine-tune LLMs on consumer GPUs at $0 cloud cost (48 tests)
- **promptlab** — Test prompts across 3+ LLM providers with assertion framework (55 tests)
- **ragtest** — RAG pipeline evaluation and benchmarking (54 tests)
- **mcplex** — MCP server for local AI models (24 tests)
- **coderev** — AI-powered code review GitHub App using Claude (15 tests)

---

### Additional Projects

**Aether Avatar** (github.com/dbhavery/aether-avatar) — 8-module offline pipeline for photorealistic avatar generation. Face identity: DreamBooth LoRA on FLUX.1-dev with 90-image dataset, 0.71-0.79 cosine similarity.

**OpenClaw** — Production Telegram AI agent with QMD memory backend (BM25 + vector semantic search + LLM re-ranking), local Qwen 8B inference.

**Hardware & IoT** — Raspberry Pi and Arduino projects with sensor integration, custom automation — early foundation for systems-level thinking applied to AI development.

---

## PROFESSIONAL EXPERIENCE

### Old Dominion Freight Lines — Portland, OR
**Transportation Operations Specialist (Line Driver)** | 2022 – Present
- Execute line haul freight operations across the Pacific Northwest for one of the nation's largest LTL carriers, managing load integrity, DOT compliance, and on-time delivery across multi-stop routes
- Coordinate with dispatch, dock operations, and terminal teams in real-time — the same distributed systems coordination applied to multi-agent AI orchestration and WebSocket event pipelines
- Maintain CDL Class A with Hazmat, Tanker, and Doubles/Triples endorsements, operating combination vehicles under strict FMCSA safety regulations
- Apply systematic problem-solving to route disruptions, equipment issues, and weather conditions — complex, time-critical decision-making with incomplete information

### Peninsula Freight Lines — Portland, OR
**Transportation Operations Specialist (Line Driver) / Driver Trainer** | 2017 – 2021
- Performed line haul and regional freight operations, maintaining consistent safety and on-time performance records
- Selected as certified driver trainer — assessed skills, provided road instruction, and ensured safety compliance for new drivers
- Served as bridge between drivers, dispatch, and terminal operations — translating operational complexity into actionable execution

### Alpha Transport — Portland, OR
**Operator** | 2012 – 2017
- Operated commercial vehicles across Western states routes, building the foundational logistics experience that informs current AI systems architecture
- Maintained safety compliance and equipment standards across long-haul operations

### Earlier Career — Various Companies
**Supervisor, Dispatcher, Driver Trainer, Operator** | ~1996 – 2012
- Held supervisory positions managing teams of 5–6 across daily freight operations
- Dispatched regional areas coordinating dozens of employees, routes, and schedules
- Trained dozens of drivers to successfully obtain their CDL certifications
- Accumulated 3.5M+ career miles of safe commercial driving across 30 years in the transportation industry

---

## CERTIFICATIONS & LICENSES

| Transportation | AI & Technology |
|---|---|
| CDL — Class A | 37 GitHub repositories, 1,372+ commits, 888K+ LOC |
| Hazmat Endorsement (H) | Enterprise SaaS deployed to Railway + Vercel |
| Tanker Endorsement (N) | 2,000+ automated tests across projects |
| Doubles/Triples Endorsement (T) | Multi-agent AI system architecture |
| DOT Compliance & Safety Certification | Full-stack web development (React + Node.js + PostgreSQL) |
| OSHA Safety Training | Real-time systems & WebSocket engineering |
| Smith System Defensive Driving Instructor | CI/CD pipeline design (GitHub Actions) |
| Certified Transportation Manager | GPU resource management & ML inference optimization |
| Dispatch Certification | Cloud deployment & infrastructure (Railway, Vercel, Neon) |
| Freight Broker License/Authority | 1,000+ hours self-directed AI/ML education |
| ELD & Fleet Management Systems | **DeepLearning.AI — Generative AI with LLMs** (Coursera, 2026) |
| Certified Driver Trainer | *Currently pursuing:* Google Cloud Professional ML Engineer, AWS ML Engineer Associate, Databricks GenAI Engineer |
| Logistics & Supply Chain Certification | |

---

## EDUCATION

**High School Diploma**
Capital High School — Boise, ID | 1996

**Continuous Professional Development**
- 1,000+ hours self-directed AI/ML curriculum: LLM architecture, multi-agent systems, prompt engineering, Python, JavaScript/TypeScript, full-stack development, mobile development, computer vision, speech processing, model fine-tuning, cloud deployment, hardware integration
- Build-first methodology: every concept studied was immediately applied in production code — 37 repositories and 1,372+ commits of working, deployed software
- Hardware foundations: Raspberry Pi and Arduino sensor/automation projects before transitioning to AI software development
