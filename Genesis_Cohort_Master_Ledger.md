# Genesis Cohort Master Ledger & Telemetry Matrix
**Document Ref: #AXM-GCL-2026**
**Objective:** A systematic, institutional-grade tracking ledger designed to capture raw telemetry, security validations, and qualitative developer experience across the 50 developers participating in the Genesis Cohort.

---

## 📋 The 7-Point Telemetry Matrix

### 1. 👤 Tester Identity & Provisioning (The Meta Data)
Tracks developer onboarding and validates the Stripe provisioning pipeline.
* **Coupon Code Used:** (Assigned via Email during engagement)
* **Tester Name / GitHub Username:**
* **Tester Email:**
* **Tester Tier:** `[Public / Private]` (Certain enclave stress tests require £3 keys)
* **Stripe Onboarding Status:** `[Pass / Fail]` (Did the code work and mint a key?)
* **SDK Initialization:** `[Pass / Fail]` (Did they successfully run `test_agent.py`?)

### 2. 🛡️ EAVEcore Interception (The Shield Tests)
Tracks whether testers successfully triggered the deterministic blast doors, logging `rejection_time_ms`.
* **Standard PII Drop:** `[Pass / Fail]` (Did they try to vault an email, UK NINO, or phone number?)
* **Financial Data Drop:** `[Pass / Fail]` (Did they attempt PAN/Credit Cards or Sort Code/Account Numbers?)
* **Infrastructure / Secrets Drop:** `[Pass / Fail]` (Did they try API keys, `sk_live_`, or hardcoded secrets?)
* **Deep-Infra / Network Drop:** `[Pass / Fail]` (Did they test DB URIs like `postgres://` or internal IPs like `192.168.x.x`?)
* **Crypto Wallet Drop:** `[Pass / Fail]` (Did they test BSV, BTC, or ETH raw wallets?)
* **Evasion Attempt:** `[Pass / Fail]` (Did they try whitespace injection, zero-width characters, or mixed capitalization?)
* **Average Rejection Time (ms):** (The raw speed metric reported by the SDK).

### 3. 🧠 The "Check First" Protocol (Retrieval & Token Savings)
Tracks the core commercial value proposition of the SPUdata network.
* **Public SPU Retrieval:** `[Pass / Fail]` (Did they successfully fetch `SPU-0d992c39` or others via the SDK?)
* **Governed Prompt Built:** `[Pass / Fail]` (Did the SDK successfully wrap their query in the SPU rulebook?)
* **Raw Token Savings Reported:** `[Integer]` (How many compute tokens do they estimate SPUdata saved their agent?)

### 4. 🧊 Sovereign Enclave (The Save-State Protocol)
Tests the £3 Private Tier boundaries, O(1) memory fidelity, and stack exhaustion limits.
* **Public Key Block:** `[Pass / Fail]` (Did the system return `403 Upgrade Required` when attempting `freeze_state` with a public key?)
* **Private Freeze Success:** `[Pass / Fail]` (Did their Tier-3 key successfully execute a `freeze_state` upload?)
* **Wake State Fidelity:** `[Pass / Fail]` (Did they execute a `wake_state` and confirm a 100% data match with zero degradation?)
* **Nested JSON Exhaustion Test:** `[Pass / Fail]` (Did they try to bury a secret 500 levels deep, and did the system survive?)

### 5. 🛑 The Sovereign Kill Switch & Fair Usage (FUP)
Verifies the mechanical guardrails that protect the server's compute.
* **Rate Limit Trigger:** `[Pass / Fail]` (Did they hit the 1,000 requests / 60 seconds wall and receive HTTP `429`?)
* **Malicious Binary Block:** `[Pass / Fail]` (Did they attempt to upload an executable or media file and receive HTTP `415` or `400`?)

### 6. 🏛️ TallySticks Audit (The Witness Layer)
Verifies the immutable proof of the entire session.
* **Audit Ledger Export:** `[Pass / Fail]` (Did they successfully use `GET /api/v1/audit/export` to download their session CSV?)
* **Decoupled Verification:** `[Pass / Fail]` (Did they take an `X-SPU-Governance-Hash` and successfully verify it on `tallysticks.uk`?)

### 7. 📝 Feedback & Developer Experience
Captures subjective data required to polish the commercial offering.
* **Bug Reports / Bypasses Found:** `[Text]` (Crucial: Did any of them figure out a way to break or bypass the engine?)
* **UX/UI Friction Points:** `[Text]` (Was the SDK hard to use? Was error parsing clear?)
* **Feature Requests:** `[Text]` (What tools or capabilities do they wish the agent had?)

---

## 📥 Direct CSV Import Template (Copy & Paste to Excel / Google Sheets)

Below is the exact CSV header structure formatted for instant import into your master spreadsheet. 

```csv
Coupon Code Used,Tester Name / GitHub Username,Tester Email,Tester Tier,Stripe Onboarding Status,SDK Initialization,Standard PII Drop,Financial Data Drop,Infrastructure / Secrets Drop,Deep-Infra / Network Drop,Crypto Wallet Drop,Evasion Attempt,Average Rejection Time (ms),Public SPU Retrieval,Governed Prompt Built,Raw Token Savings Reported,Public Key Block,Private Freeze Success,Wake State Fidelity,Nested JSON Exhaustion Test,Rate Limit Trigger,Malicious Binary Block,Audit Ledger Export,Decoupled Verification,Bug Reports / Bypasses Found,UX/UI Friction Points,Feature Requests
GENESIS-TEST-01,dev_pioneer1,pioneer1@example.com,Private,Pass,Pass,Pass,Pass,Pass,Pass,Pass,Pass,1.42,Pass,Pass,12500,Pass,Pass,Pass,Pass,Pass,Pass,Pass,Pass,None,Clean SDK setup,Add more Next.js SPUs
GENESIS-TEST-02,ai_architect,architect@example.com,Public,Pass,Pass,Pass,Pass,Pass,Pass,Pass,Pass,1.38,Pass,Pass,18000,Pass,Pass,Pass,Pass,Pass,Pass,Pass,Pass,None,Clear error parsing,GraphQL support
```

---

## 🛡️ Telemetry Evaluation Protocol

When reviewing incoming logs from the 50 developers:
1. **Immediate Shield Audits:** If any tester logs a `Fail` on a drop test (meaning a malicious payload bypassed EAVEcore), immediately inspect their exact string geometry. Update `app.py` regex dictionaries and re-run `docker compose build` to seal the vector.
2. **Speed Benchmarks:** Ensure `Average Rejection Time (ms)` remains strictly under **5.00ms** for regex evaluation to maintain the mathematical proof of Liability Zero.
3. **Fidelity Verification:** Confirm 100% pass rates on `Wake State Fidelity`. Any degradation in O(1) memory retrieval requires an immediate review of SQLite blob encoding parameters.
