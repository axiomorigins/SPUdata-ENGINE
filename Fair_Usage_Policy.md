# SPUdata Fair Usage Policy (FUP)
**Document Ref: #AXM-FUP-2026**

## 1. Context and Purpose
The SPUdata network is designed to be the foundational "Memory Layer" for Autonomous AI Agents. Because autonomous systems can execute loops at machine speed, it is strictly necessary to establish legal and mechanical guardrails to ensure the stability, security, and economic viability of the Sovereign Engine.

By provisioning a Sovereign API Key (£1 Global Commons or £3 Private Enclave), developers in the Genesis Cohort explicitly agree to the following operational constraints.

---

## 2. Mechanical Guardrails & Rate Limits
To protect the core 2GB VPS infrastructure and the TallySticks Witness nodes from unintended DDoS vectors (e.g., an LLM caught in an infinite `while True:` loop), the following rate limits are strictly enforced at the routing layer:

*   **Fair Use Allotment:** 50,000 API calls per 30-day rolling window per API key.
*   **Loop Protection:** Any key exceeding 1,000 requests within a 60-second window will trigger a localized cooldown and temporarily return HTTP `429 Too Many Requests`.
*   **Enforcement:** Exceeding the 50,000 monthly limit will trigger an automatic `403 Upgrade Required` response. Your key will be paused until the next billing cycle or until a High-Volume Enterprise tier is provisioned.

---

## 3. The EAVEcore Code of Conduct
The EAVEcore Active Interceptor is designed to shield the database from Personally Identifiable Information (PII) and hardcoded secrets. 

> [!CAUTION]
> **Prohibited Actions against the Shield:**
> 1. Do not use the SPUdata network to intentionally filter or launder mass datasets of PII.
> 2. Do not attempt to bypass or obfuscate payloads to defeat the EAVEcore Regular Expression sweep.
> 3. Do not run automated "stress tests" against the `POST /api/v1/spu` endpoint to map the EAVEcore detection logic.

Any key repeatedly triggering EAVEcore interception blocks in a short time frame will be automatically flagged for review.

---

## 4. The Global Commons (Anti-Harvesting Clause)
The £1 Public Vault tier grants read/write access to the Global Commons—a shared library of deterministic logic (e.g., The Nolan Principles, API Governance Standards).

*   **Prohibited Action:** You may not execute automated scripts to recursively scrape, harvest, or download the entirety of the Public Vault.
*   **Commercial Resale:** You may not repackage, resell, or distribute the contents of the Global Commons as a proprietary dataset.

---

## 5. The Sovereign Kill Switch
Axiom Origins Ltd. reserves the right to exercise the **Sovereign Kill Switch** (`is_active = False`) at any time, without prior notice or refund, if a developer's autonomous agent threatens the stability of the SPUdata Engine or violates the Social Value Contract.

> [!WARNING]
> Termination is deterministic. A deactivated key permanently loses access to all vaulted logic, and the associated TallySticks cryptographic receipts will be locked. 

---

## 6. Liability Zero
Axiom Origins provides the infrastructure to decouple logic from the LLM context window. However, the ultimate execution of any retrieved SPU rests entirely with the developer's agentic pipeline. Axiom Origins assumes **Zero Liability** for the real-world consequences of decisions made by autonomous systems utilizing the SPUdata network.
