# 🛡️ SPUdata-ENGINE: The Context CDN, MCP Server & PII Shield for Agentic AI

[![EAVEcore Governance](https://img.shields.io/badge/Governance-EAVEcore%209--Vector%20Shield-10b981)](https://spudata.com)
[![MCP Compatible](https://img.shields.io/badge/MCP-Claude%20%7C%20Cursor%20%7C%20Windsurf%20%7C%20Gemini-667eea)](https://spudata.com/api/v1/download/mcp-server)
[![GCP Cloud Run Ready](https://img.shields.io/badge/Google%20Cloud-Vertex%20AI%20%26%20Cloud%20Run-4285F4)](https://spudata.com/#enterprise)

**Live Platform:** [https://spudata.com](https://spudata.com)  
**Developed by:** Axiom Origins Ltd & SPUdata Ltd (Company No. 16943167, England & Wales)

---

## ⚡ Why SPUdata Exists

Autonomous AI agents and IDE assistants (Claude Desktop, Cursor, Windsurf, Gemini Code Assist, Vertex AI) suffer from three compounding bottlenecks:
1. **Exploding Token & Energy Overhead ("Context Rot"):** Scraping raw HTML documentation or carrying 80,000-token chat histories degrades model accuracy and burns expensive compute allowances.
2. **Context Bleed Across Projects:** Mixing architecture patterns across repositories or organizational departments causes hallucinations.
3. **Identity Bleed & PII Contamination:** Developers or autonomous workflows accidentally leaking live API keys, database connection strings, UK National Insurance Numbers, or customer PII into LLM memory stores.

**SPUdata + EAVEcore** solves all three via a stateless **Context CDN** and **Zero-Dependency MCP Server**:

| Empirical Benchmark | Raw Web / Unfiltered RAG | SPUdata Deterministic Vault | Verified Improvement |
| :--- | :---: | :---: | :---: |
| **Context Payload Size** | ~47,956 tokens | **391 tokens** | **93.5% – 99.2% Token Reduction** |
| **Retrieval Latency** | ~1,050 ms | **465 ms** | **56% Faster (O(1) Pull)** |
| **Inference Energy per Call** | ~0.003 kWh | **~0.00001 kWh** | **300x Energy Reduction (Net-Zero Core)** |
| **PII & Secret Exposure** | Unfiltered | **< 2 ms 9-Vector EAVEcore Block** | **Liability Zero (SHA-256 Witnessed)** |

---

## 🔌 1. Quick Start: Plug into Claude Desktop, Cursor, Windsurf, or Gemini CLI (MCP)

`spudata_mcp_server.py` is a **zero-dependency Python stdlib MCP Server** (JSON-RPC 2.0 over stdio). No `pip install` is required.

### Step 1: Download `spudata_mcp_server.py` & Get Your Key
* Provision an API Key at **[https://spudata.com/register.html](https://spudata.com/register.html)** (Starts at **£1** for Global Commons, **£3** for a Single-Project Enclave, **£29/yr** for Pro Developer Suite, or **£99/yr** for a 10-Seat Agency Compliance Vault).
* Download `spudata_mcp_server.py` from this repository or directly from **[https://spudata.com/api/v1/download/mcp-server](https://spudata.com/api/v1/download/mcp-server)**.

### Step 2: Add to `claude_desktop_config.json` or `.cursor/mcp.json`
```json
{
  "mcpServers": {
    "spudata": {
      "command": "python",
      "args": ["/absolute/path/to/spudata_mcp_server.py"],
      "env": {
        "SPUDATA_API_KEY": "spudata_YOUR_VAULT_KEY"
      }
    }
  }
}
```

### 7 Native MCP Tools Available to Your AI Agent
| Tool Name | Description |
| :--- | :--- |
| `spudata_search` | Search the Global Commons & Core Registry for verified rulebooks (`fastapi`, `stripe`, `react`, `pii`, `nolan`, etc.). |
| `spudata_get_rulebook` | Retrieve a deterministic SPU rulebook by ID (supports `preferred_tag` for intelligent fork routing) + `X-SPU-Governance-Hash`. |
| `spudata_list_my_vault` | List all private and public SPU rulebooks and frozen state checkpoints in your authenticated Vault. |
| `spudata_save_memory` | Vault a verified architecture pattern or resolved use-case (`SPU-OPS`). Automatically runs the 9-vector EAVEcore PII shield. |
| `spudata_freeze_state` | Execute the **O(1) Save-State Protocol**: checkpoint current task state into your Private Enclave so you can clear context windows without losing progress. |
| `spudata_wake_state` | Restore a frozen agent checkpoint by its SPU ID in O(1) time. |
| `spudata_pii_scan` | Scan any prompt, config, or code snippet against the 9-vector EAVEcore Governance Cartridge before sending it to an LLM. |

---

## 🐍 2. Quick Start: Python Agentic SDK (`spu_agent.py`)

For custom autonomous agents, LangChain/CrewAI pipelines, or Google Cloud Run microservices, use `SovereignAgent` from `spu_agent.py`:

```python
from spu_agent import SovereignAgent

# Initialize with your X-SPU-KEY (or set SPUDATA_API_KEY in environment)
agent = SovereignAgent(api_key="spudata_YOUR_VAULT_KEY")

# 1. Build a governed, zero-hallucination prompt from a canonical SPU
safe_prompt = agent.build_governed_prompt(
    spu_id="SPU-650c4309",  # The Nolan Principles Framework
    query="Draft an internal procurement compliance review."
)

# 2. O(1) Save-State Checkpointing (Prevents Context Rot at 80k tokens)
checkpoint_id = agent.freeze_state(
    session_id="MIGRATION-TASK-01",
    context_summary="Completed DB schema v2; next step is Stripe webhook verification."
)

# 3. Wake State in a fresh agent process with zero token bloat
restored_context = agent.wake_state(checkpoint_id)
```

---

## 🛡️ 3. The EAVEcore 9-Vector PII & Secret Blast Door

Every write (`POST /api/v1/spu`) and validation call (`POST /api/v1/validate`) passes through the **EAVEcore Active Runtime Interception Cartridge** in `< 2 ms`, blocking:
1. **Hardcoded API Keys & Secrets** (`sk_live_`, AWS, GCP, generic tokens/passwords)
2. **Plaintext Email Addresses**
3. **UK National Insurance Numbers (NINO)**
4. **UK & International Telephone / Mobile Numbers**
5. **Banking Details (UK Sort Codes & Account Numbers)**
6. **Financial PAN / Credit Card Numbers (FCA Compliance Block)**
7. **Database & Cache Credential URIs (`postgres://`, `mongodb://`, `redis://`)**
8. **Internal IPv4 Network Topologies (SSRF Prevention)**
9. **Raw Cryptographic Wallet Addresses (BTC / BSV / Bech32 / ETH)**

Every transaction is cryptographically hashed (`X-SPU-Governance-Hash`) and exportable via **`GET /api/v1/audit/export`** as an immutable **TallySticks Witness Ledger CSV**.

---

## ☁️ 4. Google Cloud Run & Vertex AI Enterprise Architecture

Operating natively on **Google Cloud Run**, SPUdata acts as an upstream pre-processor for **Google Vertex AI** and enterprise LLM workloads—eliminating jurisdictional data bleed under **ISO-42001**, the **EU AI Act**, **UK GDPR**, and **G-Cloud 15 / CDDO Net-Zero** frameworks.

* **Web Dashboard & Vault Provisioning:** [https://spudata.com](https://spudata.com)
* **Sovereign Documentation & GQTM Standard:** [https://spudata.com/docs.html](https://spudata.com/docs.html)
* **Enterprise & Public Sector Inquiries:** `governance@axiomorigins.com`
