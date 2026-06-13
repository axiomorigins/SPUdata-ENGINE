# SPUdata Agentic SDK (spu_agent.py)

A lightweight Python wrapper designed for the **Genesis Cohort**. This SDK allows you to connect any LLM (OpenAI, Anthropic, LangChain) directly to the **SPUdata Sovereign Memory Layer**.

## What it does
1. **Fetches Deterministic Logic:** Pulls verified, sterile logic blocks (SPUs) from the TallySticks ledger.
2. **Validates Cryptographic Hashes:** Automatically verifies the X-SPU-Governance-Hash for true Inherent Auditability.
3. **Injects Context:** Violently forces the LLM to obey the rulebook by building a heavily constrained, token-efficient prompt payload.
4. **Prevents Contamination:** Drops requests that fail the EAVEcore security shield natively in the wrapper.

## Quickstart

\\\python
from spu_agent import SovereignAgent

# 1. Initialize the agent (requires a £1 or £3 Tier SPUdata Key)
agent = SovereignAgent(api_key="spudata_YOUR_API_KEY")

# 2. Wrap your prompt with a deterministic rulebook (e.g. SPU-650c4309: Nolan Principles)
safe_prompt = agent.build_governed_prompt(
    spu_id="SPU-650c4309", 
    user_query="Draft an internal memo regarding the new procurement contract."
)

# 3. Pass safe_prompt directly to your LLM of choice!
\\\

## Architecture Validation
By using this wrapper, your AI agent's execution is mathematically recorded to the **TallySticks Witness Ledger**. You can cryptographically verify every single prompt you ever generate by downloading your audit CSV at spudata.com and verifying the hash at 	allysticks.uk.
