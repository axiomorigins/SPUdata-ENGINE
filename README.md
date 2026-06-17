# 🛡️ SPUdata Agentic SDK (Python Wrapper)
**The Memory Layer for Autonomous AI Agents.**

[![Axiom Origins Tripartite Engine](https://img.shields.io/badge/Powered%20By-Axiom%20Origins-blue)](#)
[![TallySticks Witness](https://img.shields.io/badge/Ledger-TallySticks_Verified-success)](#)
[![EAVEcore Shield](https://img.shields.io/badge/Compliance-Liability_Zero-red)](#)

> [!IMPORTANT]
> **Genesis Cohort Testers:** Please read the **[Genesis Testing Handbook & Metrics Log](Genesis_Testing_Handbook.md)** for instructions on provisioning your test keys, your 6 Bounty Targets, and how to submit your telemetry data.

> [!WARNING]
> ⚠️ **Note for Genesis Testers:** SPUdata enforces strict Fair Usage Policies (1,000 requests / 60 seconds). Do not run infinite loops against the API, or the Sovereign Kill Switch will permanently sever your test key.

## Overview
The current Agentic AI ecosystem burns millions of tokens probabilistically re-inventing basic logic loops. The **SPUdata SDK** allows developers to bypass the "thinking" phase and jump straight to the "execution" phase via **Deterministic Retrieval**. 

By dropping this lightweight Python wrapper into your OpenAI, Anthropic, or LangChain pipelines, your AI agent can instantly retrieve mathematically sterile, pre-computed Sovereign Processing Units (SPUs). 

**The Result:** 
* Up to 93.5% Token Reduction.
* Zero Hallucination on core procedural tasks.
* Inherent Auditability via the TallySticks Witness Layer.

## 🚀 Quickstart

### 1. Provision Your Enclave
Before running the agent, you must provision an API key on the SPUdata network and agree to the Social Value Contract.
👉 **[Get your Sovereign Key at SPUdata.com](https://spudata.com)**

### 2. Drop the Wrapper into your Project
Download spu_agent.py and place it in your working directory. 

### 3. Initialize the Agent
Set your API key as an environment variable or pass it directly to the wrapper:

\\\python
from spu_agent import SovereignAgent

# Initialize the SPUdata connection
agent = SovereignAgent(api_key="spudata_YOUR_LIVE_KEY_HERE")

# Target a specific procedural rulebook (e.g., The Nolan Principles)
TARGET_SPU = "SPU-650c4309"
raw_query = "Draft an internal memo regarding the new procurement contract."

# The SDK fetches the rules, verifies the cryptographic hash, and wraps the prompt
safe_prompt = agent.build_governed_prompt(TARGET_SPU, raw_query)

# Pass the safe_prompt directly to your LLM of choice
print(safe_prompt)
```

## 🧠 Save-State Context Swapping
Need to hand off work between a cheap model (GPT-4o-mini) and an advanced model (Gemini 1.5 Pro)? The SDK allows you to "freeze" an agent's context and upload it as an ephemeral, private SPU. The second agent can then fetch the ID and wake up with full memory.

```python
# Agent A (OpenAI) analyzes data
summary_data = "Analysis complete. Critical anomalies found in rows 45 and 92."

# Agent A freezes its state before shutting down (Requires £3 Private Enclave)
handoff_id = agent.freeze_state(session_id="TASK-992", context_summary=summary_data)

# ... later, on a completely different server ...

# Agent B (Gemini) wakes up, pulls the exact SPU ID, and resumes the work
resumed_context = agent.wake_state(handoff_id)
```

## 🔒 The EAVEcore Shield (Active Interception)
If your agent attempts to upload or retrieve an SPU containing Personally Identifiable Information (PII) or hardcoded secrets, the EAVEcore Runtime Guard will deterministically sever the connection in < 600ms, returning a 403 Forbidden error. This guarantees absolute state isolation.

## 📜 Inherent Auditability
Every successful retrieval and every blocked contamination event generates a deterministic ECDA hash. You can view your cryptographic receipt in your SPUdata dashboard and verify its authenticity publicly at the TallySticks Glass House.

Built by Axiom Origins Ltd. - Reconciliation, Not Revolution.
