# 🛡️ Genesis Testing Handbook & Metrics Log
**Document Ref: #AXM-GTH-2026**

Welcome to the Genesis Cohort. 

You have been selected to beta-test the Axiom Sovereign Governance Infrastructure (SPUdata). This engine is designed to act as the Deterministic Memory Layer for Autonomous AI Agents, providing zero-liability execution and inherent auditability.

Before we open the gates to Enterprise and Public Sector clients, we need you to try and break the blast doors.

## 🔑 Provisioning Your Sovereign Enclave

1. Navigate to **[SPUdata.com](https://spudata.com)** and create an account.
2. Select either the **£1 Public Vault** or the **£3 Private Enclave** tier.
3. At the Stripe checkout, use the unique 100% discount coupon assigned to your registered email address during onboarding.
4. Your deterministic API Key will be instantly generated upon checkout completion.

> [!NOTE]
> **Stripe & Coupon Support:**
> If you experience any problems or issues with your assigned coupon during the initial engagement process, please contact **contact@spudata.com** for immediate support. Ensure you include the subject line **Genesis Cohort** so your request is prioritized by our routing layer.

---

## 🎯 The 6 Bounty Targets (Engagement Rules)

Your objective is to stress-test the mechanical and legal guardrails of the Tripartite Engine. 

### 1. The EAVEcore Shield Attack (PII & Secrets)
* **Goal:** Attempt to upload an SPU containing hardcoded API keys, mock National Insurance numbers, or formatted email addresses.
* **Success Metric:** The system should sever the connection in < 600ms and return a 403 Forbidden error.

### 2. The Code-Injection Attack (Jailbreaking)
* **Goal:** Upload an SPU that appears to be a safe procedural rulebook, but contains a hidden prompt injection designed to make an LLM break its own rules or the Sovereign Agent Protocol (SAP-01).
* **Success Metric:** Test the efficacy of the EAVEcore regex sweep against malicious cognitive payloads.

### 3. The Context-Swapping Stress Test (Checkpoint Protocol)
* **Goal:** Use the Python SDK (reeze_state and wake_state) to bounce a reasoning task between two completely different LLM models (e.g., from GPT-4o-mini to Claude 3.5 Sonnet).
* **Success Metric:** The JSON payload must maintain perfectly sterile formatting across different models without context degradation.

### 4. The Loop Limit Attack (Rate Limiting)
* **Goal:** Write a rapid `while True:` loop script that repeatedly hammers the `/api/v1/search` endpoint.
* **Success Metric:** Trigger the mechanical cooldown (1,000 requests / 60 seconds). Ensure you receive a `429 Too Many Requests` error and that the main server does not degrade.

### 5. The Ingress Entropy Guard (The Payload Entropy Challenge)
* **Goal:** Attempt to bypass the payload filter by disguising an executable script as a Markdown file, or attempt a base64-encoded buffer overflow via `/api/v1/spu`.
* **Success Metric:** The server must recognize that the content is not plain text and drop the connection instantly with a `415 Unsupported Media Type` error. Please log the exact `rejection_time_ms` returned in the JSON response payload.

### 6. The TallySticks Audit Reconciliation
* **Goal:** Perform 10 actions (a mix of successful uploads, fetches, and intentional blocks). Export your cryptographic CSV from the dashboard.
* **Success Metric:** Go to the public Glass House at **[tallysticks.uk/audit.html](https://tallysticks.uk/audit.html)** and manually verify your transaction hashes. The verification must be frictionless and mathematically sound.

---

## 📊 The Telemetry Return (Metrics Log)

When you have completed the Bounty Targets, please return your telemetry data in the standardized JSON format below. This allows us to aggregate raw performance data and prove efficacy to future institutional clients.

`json
{
  "tester_id": "Dev_[YOUR_INITIALS]",
  "test_date": "YYYY-MM-DD",
  "vector_1_pii_interception": {
    "payload_type": "Plaintext Email & Secret Key",
    "eavecore_response_time_ms": 512,
    "block_successful": true
  },
  "vector_2_latency": {
    "average_retrieval_ms": 115,
    "estimated_token_savings": 4500
  },
  "vector_3_checkpoint_protocol": {
    "freeze_to_wake_fidelity": "100%",
    "models_used": ["GPT-4o", "Claude-3.5-Sonnet"]
  },
  "vector_4_rate_limiting": {
    "requests_before_block": 1000,
    "server_degradation_noticed": false
  },
  "vector_5_entropy_guard": {
    "payload_type": "Base64 Encoded Executable disguised as Markdown",
    "block_successful": true,
    "response_code": 415,
    "rejection_time_ms": "1.45 (milliseconds)"
  },
  "vector_6_tallysticks_audit": {
    "verification_frictionless": true,
    "hashes_matched": 10
  },
  "ux_feedback": "The Glass House verification felt like magic."
}
`

**Submission:** Please email your completed JSON payload to **contact@spudata.com** with the subject line `[Genesis Cohort] Telemetry Report - Dev_[YOUR_INITIALS]`.

Thank you for building the future of autonomous infrastructure with us.
**Reconciliation, Not Revolution.**
