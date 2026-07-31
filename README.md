<div align="center">

# socks5-sniffer

**I build AI systems that have to prove they work — and I publish the results when they don't.**

Multi-agent reasoning research · agent-orchestrated delivery · hands-on STEM education

</div>

---

## 🧠 ARM-Protocol — Agent Reasoning Markup

> **Research.** Making multi-agent reasoning auditable instead of merely agreeable.

Most multi-agent systems pass **conclusions** between agents like text messages, discarding the reasoning that produced them. **ARM** propagates the full trace — assumptions, discarded alternatives, confidence, decision basis — so a downstream agent can audit and challenge the logic instead of inheriting it blind.

**How it works:** every question runs through a four-agent cognitive mesh across two rounds. Round 1 agents reason in complete isolation. Round 2 agents receive compressed peer traces and must declare *what specifically* moved them. A permanently-isolated **γ-Silent** agent — a second independent draw that peers never see — acts as consensus co-witness and calibration anchor.

The research target is the **Persuasion Duality**: sharing reasoning makes an agent auditable *and* makes it more persuasive, so a plausible-but-wrong assumption can propagate into baseless consensus — **memetic drift**.

**Stack:**

| Category | Tools |
| :--- | :--- |
| **Frontend** | React 18, Vite |
| **Models** | `claude-sonnet-4-6` · `gpt-5.5` · `gemini-3.5-flash` (any provider in any agent slot) |
| **Protocol** | Custom multi-agent JSON trace schema |
| **Deploy** | Containerfile + OpenShift manifests (deployment, service, route, PVC), devfile |
| **CI** | GitHub Actions CI + OWASP security scan |

**Where it actually stands (2026-07):**
- ❌ **The original drift detector was falsified.** A ground-truthed injection experiment (`experiments/c1vc2/`) shows confidence-magnitude drift separates contaminated from clean subjects at **chance — within-Gemini AUC ≈ 0.48**.
- ✅ **IPR (injection-propagation rate)** — did an agent *adopt* a premise authored as false? — is the surviving, falsifiable signal.
- ⚠️ The polarity gate's firm yes↔no transition class catches ~36% of inferred contaminations at 40% precision.
- 🔬 RLHF bias audit runs in every reconciliation round.

> I ran the direct test of my own central claim and it failed. That result is in the README, not buried — a metric that can't be falsified isn't a metric.

**[→ socks5-sniffer/ARM-Protocol](https://github.com/socks5-sniffer/ARM-Protocol)** · Apache-2.0

---

## 🤖 SCRUMtious — AI-Powered Scrum Team Orchestration

> **Lead project.** One feature idea in, a full sprint cycle out.

**SCRUMtious** is a standalone web application that drives five specialised AI agents through a complete Agile sprint. Describe a feature in plain English; get back a requirements doc, user story, implementation, OWASP security audit, and sprint retrospective as a downloadable artifact bundle.

**The pipeline:** 📋 Business Analyst → 🎯 Product Owner → ⚡ Lead Developer → 🛡️ Security Auditor → 🔄 Scrum Master. Each agent builds on the last, streams live to the UI, and **pauses for you** — a human-in-the-loop approval gate after every stage lets you read, edit, and approve before the sprint continues.

**Stack:**

| Category | Tools |
| :--- | :--- |
| **Backend** | FastAPI, Python 3.11+ |
| **AI** | CrewAI, Google Gemini |
| **Realtime** | Server-Sent Events (background thread + event queue) |
| **Frontend** | Vanilla JS single-page UI — no framework |
| **Export** | Markdown bundle, PDF (xhtml2pdf) |
| **CI** | GitHub Actions CI · CodeQL · OWASP Top-10 scan |

**Key signals:**
- ⏸️ HITL approval gate between every agent — edits are re-emitted into the stream
- 🔐 Per-session tokens on protected endpoints via HttpOnly cookie
- 💾 Sessions persist to disk and reload into memory on startup
- 🛡️ Security Auditor emits an explicit `APPROVED` / `BLOCKED` verdict

> The interesting problem wasn't the agents — it was making an async event loop, a blocking crew thread, and a human who needs to read the output all cooperate.

**[→ socks5-sniffer/SCRUMtious](https://github.com/socks5-sniffer/SCRUMtious)** · MIT

---

## 🥒 picklePi — Electronics & Python, One Circuit at a Time

> **Favorite project.** Teaching the thing I had to learn myself.

**picklePi** is a gamified, project-based platform that teaches electronics and Python on the Raspberry Pi across **13 sequenced levels** — from a first LED blink to a working physical tamper-monitoring security system. No prior experience assumed.

Every level is a full lesson, not a snippet: wiring instructions with safety warnings, complete runnable code, line-by-line walkthroughs, concept deep dives, experiment challenges, and troubleshooting. Badges unlock as you go, and a Lab Notebook captures reflection on each build.

**Stack:**

| Category | Tools |
| :--- | :--- |
| **Frontend** | React 19, TypeScript 6, Vite 8, Tailwind 4, Motion |
| **Backend** | Flask + Firebase Admin (Firestore), `bleach` sanitisation |
| **Optional persistence** | Express 5 + better-sqlite3 (client-first by default) |
| **AI** | `@google/genai` — Gemini-driven curriculum level generator |
| **Deploy** | Vercel, with a full CSP + security-header policy in `vercel.json` |
| **CI** | GitHub Actions CI · CodeQL · OWASP scan · wiki sync |

**Key signals:**
- 🔒 Every `/api/progress` route requires a verified Firebase ID token — and the URL's `userId` must match the uid *inside* that token, so no user can ever read another's data
- 🧱 Strict CSP, `frame-ancestors 'none'`, and HSTS preload shipped in config
- 🎮 Client-first architecture — runs with zero backend; server-side accounts are drop-in
- 📓 Lab Notebook, badge system, and an interactive GPIO pinout reference

**[→ socks5-sniffer/picklePi](https://github.com/socks5-sniffer/picklePi)** · MIT

---

## 📊 GitHub Activity

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api?username=socks5-sniffer&show_icons=true&hide_border=true&include_all_commits=true&theme=github_dark&title_color=5bcdec&icon_color=5bcdec&bg_color=0d1117">
  <img height="165" src="https://github-readme-stats.vercel.app/api?username=socks5-sniffer&show_icons=true&hide_border=true&include_all_commits=true&title_color=1f6feb&icon_color=1f6feb" alt="GitHub stats">
</picture>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api/top-langs/?username=socks5-sniffer&layout=compact&hide_border=true&langs_count=8&theme=github_dark&title_color=5bcdec&bg_color=0d1117">
  <img height="165" src="https://github-readme-stats.vercel.app/api/top-langs/?username=socks5-sniffer&layout=compact&hide_border=true&langs_count=8&title_color=1f6feb" alt="Top languages">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-activity-graph.vercel.app/graph?username=socks5-sniffer&bg_color=0d1117&color=5bcdec&line=5bcdec&point=ffffff&area=true&hide_border=true">
  <img src="https://github-readme-activity-graph.vercel.app/graph?username=socks5-sniffer&bg_color=ffffff&color=1f6feb&line=1f6feb&point=1f6feb&area=true&hide_border=true" alt="Contribution activity graph">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/socks5-sniffer/socks5-sniffer/output/github-contribution-grid-snake-dark.svg">
  <img src="https://raw.githubusercontent.com/socks5-sniffer/socks5-sniffer/output/github-contribution-grid-snake.svg" alt="Contribution grid snake animation">
</picture>

</div>

---

## 🛠️ Tech Stack

| Category | Tools |
| :--- | :--- |
| **Languages** | Python, TypeScript, JavaScript, HTML/CSS |
| **Frontend** | React, Vite, Tailwind CSS |
| **Backend** | FastAPI, Flask, Express |
| **AI** | CrewAI, Anthropic Claude, Google Gemini, OpenAI |
| **Cloud** | Google Cloud, Firebase/Firestore, Vercel, OpenShift |
| **Data** | Firestore, SQLite, PostgreSQL |
| **Tooling** | Git, GitHub Actions, Docker/Podman, CodeQL, Cloudflare |

---

## 🎯 Current Focus

* 🧪 **Multi-agent evaluation** — designing experiments that can actually falsify a protocol's claims, not just demo it
* 🐍 **Python depth** — backend structure, API design, clean and maintainable code
* ☁️ **Deployment reality** — Cloud Run, Vercel, and OpenShift, from container to public HTTPS route
* 🔐 **Applied security** — input validation, authz that survives a hostile URL, CSP and secrets hygiene

---

## 🛡️ How I Build

- Never trust client input — validate server-side, every time
- Secrets stay out of code
- Prefer simple, secure patterns over clever ones
- Publish the negative result — a claim you can't falsify isn't a finding

---

## 🌱 About

I'm a career switcher using AI to accelerate learning, but the point is understanding what I build. I'd rather be genuinely solid at Python, cloud, and evaluation than spread thin across everything.

- 🤝 **Open to collaborating on:** multi-agent evaluation, beginner-friendly Python/backend projects, open source where I can contribute and learn
- ⚡ **Fun fact:** I share my home with **17 animals** 🐾
