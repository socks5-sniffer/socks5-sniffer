# Hi there, 👋

I build **AI-Accelerated, Security-First Applications** using Python and cloud-native tools.

My focus is simple:
- ⚡ Ship quick using **AI-assisted development**
- 🔐 Build with **security in mind from day one**
- ☁️ Deploy and run in **real cloud environments (GCP)**

I’m currently focused on becoming a **strong Python engineer with real-world cloud deployment experience**.

---
## 🧠 Research Project: ARM-Protocol (release coming soon)

**ARM (Agent Reasoning Markup)** is a multi-agent reasoning transparency protocol. Instead of passing raw outputs between agents, ARM propagates full reasoning traces — assumptions, confidence levels, discarded paths, and decision basis — so downstream agents can audit and challenge logic rather than blindly inherit conclusions.

**Description:**
ARM runs questions through a structured four-agent cognitive mesh across two deliberation rounds. Round 1 agents reason in isolation; Round 2 agents receive compressed peer traces and must declare what specifically changed their position. A permanently-isolated γ-Silent agent provides a calibration anchor to detect **memetic drift** — when peer pressure inflates confidence without improving logic. 30+ experimental runs show ~85% of agent-rounds produce epistemic tightening (reduced confidence), not drift.

**Stack:**

| Category | Tools |
| :--- | :--- |
| **Frontend** | React (JSX), Vite |
| **AI** | Claude (Anthropic), GPT-4o-mini, Gemini 2.5 Flash |
| **Protocol** | Custom multi-agent JSON trace schema |
| **Infra** | `.env` key management, JSON telemetry export |

**Key Signals:**
- 📉 Epistemic tightening dominant in ~85% of agent-rounds  
- ⚠️ Memetic drift detected and flagged in ~10% of agent-rounds  
- 🔁 γ-Silent baseline reproduces identical confidence scores across repeated runs  
- 🔬 RLHF bias audit built into every reconciliation round  

> ARM makes multi-agent reasoning auditable and measurable — replacing unearned consensus with verifiable epistemic signals.

---

## 🍽️ 🏃 Lead Project: Scrumptious

**SCRUMtious** is my Scrum team — the engine that drives how **PicklePi** gets built. It's where planning, sprints, and iteration strategy live, keeping development organized and moving forward with intention.

**Description:**
Scrumptious formalizes the agile workflow behind PicklePi: sprint planning, backlog grooming, and continuous delivery. It exists to make sure AI-accelerated development doesn't become chaotic — structure meets speed.

**Stack:**

| Category | Tools |
| :--- | :--- |
| **Project Mgmt** | GitHub Projects, Issues, Milestones |
| **Process** | Scrum (sprints, backlog, retrospectives) |
| **Automation** | GitHub Actions (CI/CD pipelines) |
| **Docs** | Markdown, GitHub Wiki |

**Pipelines:**
- ✅ Sprint-gated CI checks on every PR  
- 🔁 Automated issue tracking tied to commits  
- 📋 Milestone-driven release workflow  

> Scrumptious keeps PicklePi honest — every feature ships through a sprint, every sprint ships through a pipeline.

---

## 🥒 🚀 Favorite Project: PicklePi

**PicklePi** is my primary build — the product Scrumptious plans and ships. It reflects how I actually develop: rapid iteration with AI, backend-first thinking, and real cloud deployments.

**Description:**
picklePI is a full-stack, TypeScript educational platform designed to teach foundational Python through hardware-centric logic. Hosted on Google Cloud and managed via the SCRUMtious framework, it features a containerized execution environment that allows students to interact with Python code safely. The project serves as a live demonstration of "Secure by Design" principles, incorporating automated CI/CD security gates and rigorous input sanitization.
**Stack:**

| Category | Tools |
| :--- | :--- |
| **Language** | TypeScript, Python |
| **Backend** | Flask / FastAPI |
| **Cloud** | Google Cloud Platform (Cloud Run, Firebase) |
| **Database** | Firestore |
| **Infra** | Docker, Cloud Run, `.env` secrets management |

**Pipelines:**
- 🐍 Python linting + unit tests on every push  
- ☁️ Cloud Run deploy on merge to main  
- 🔐 Secret scanning and environment validation  
- 🔁 Sprint-linked CI managed through Scrumptious  

> PicklePi represents my current growth: becoming highly effective with Python while shipping real, deployed applications — one sprint at a time.

---

## 🎮 Project: Faithville

A full-stack simulation project exploring UI, state management, and secure user interactions. A different flavor from PicklePi — heavier on the frontend, testing different architectural patterns.

**Description:**
Faithville simulates game-like transactions and state with a focus on security and real-time data. It runs across two cloud providers, testing how a split frontend/backend architecture holds up in production.

**Stack:**

| Category | Tools |
| :--- | :--- |
| **Frontend** | React (TypeScript), Tailwind CSS |
| **Backend** | Python |
| **Cloud** | Hostinger (frontend) + Google Cloud Run (backend) |
| **Database** | Firestore |
| **Auth** | OAuth |

**Pipelines:**
- ⚛️ React build + type-check on every PR  
- ☁️ Backend deploy to Cloud Run on merge  
- 🔐 OAuth flow validation and CORS enforcement  
- 🌐 Frontend deploy to Hostinger on release  

**Key Features:**
  - OAuth authentication  
  - Secure transaction handling ("pessimistic UI")  
  - Real-time database interactions  

---

![GitHub Activity Graph](https://github-readme-activity-graph.vercel.app/graph?username=socks5-sniffer&bg_color=0d1117&color=5bcdec&line=5bcdec&point=ffffff&area=true&hide_border=true)

---

## 🎯 Current Focus

Right now I’m intentionally focused on **mastering fundamentals that scale**:

* 🐍 **Python Development**
  - Backend design
  - APIs and data handling
  - Writing clean, maintainable code

* ☁️ **Google Cloud Platform (GCP)**
  - Cloud Run deployments  
  - Firestore and serverless patterns  
  - Environment configuration and debugging  

* 🔐 **Security Basics (Applied)**
  - Input validation  
  - CORS and API protection  
  - Secrets management  

---

## 🧪 Exposure & Exploration

I’ve also begun exploring:

- 🐳 Containers (Docker basics)  
- ☸️ Kubernetes concepts  
- 🔴 OpenShift (deployed a working app accessible on the public internet)

> Not my focus yet—but I understand the direction and have hands-on exposure.

---

## 🛠️ Tech Stack

| Category | Tools |
| :--- | :--- |
| **Languages** | Python, JavaScript, TypeScript, HTML |
| **Frontend** | React, Next.js, Tailwind CSS |
| **Backend** | Flask / FastAPI (learning & building) |
| **Cloud** | Google Cloud Platform (Cloud Run, Firebase) OpenShift | 
| **Database** | Firestore, PostgreSQL |
| **Tools** | Git, Docker (basics), Cloudflare, VSCode, Virtual Machines |

---

## 🛡️ Security Mindset

Even while learning, I build with intent:

- Never trust client input  
- Keep secrets out of code (`.env`)  
- Validate everything server-side  
- Prefer simple, secure patterns over clever ones  

---

## 🌱 About Me

- 🔭 **Currently working on:**
  - Growing **PicklePi** into a solid Python-based platform  
  - Improving backend structure and API design  
  - Getting more consistent with cloud deployments  

- 🎓 **Currently learning:**
  - Python (deeper fundamentals + best practices)  
  - GCP services and architecture  
  - Practical security  

- 🤝 **Looking to collaborate on:**
  - Beginner-friendly Python or backend projects  
  - Open source where I can contribute and learn  

- ⚡ **Fun fact:** I share my home with **17 animals** 🐾  

- 💬 **The Real Talk:**
  I’m a career switcher using AI to accelerate learning—but I focus on actually understanding what I build.

  I’d rather be **solid at Python + cloud** than spread thin across everything.

---

![GitHub Activity Graph](https://github-readme-activity-graph.vercel.app/graph?username=socks5-sniffer&bg_color=0d1117&color=5bcdec&line=5bcdec&point=ffffff&area=true&hide_border=true)
