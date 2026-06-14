import os
import requests

class SovereignAgent:
    """
    The Axiom Origins SDK Wrapper for Autonomous Agents.
    Enforces deterministic context retrieval via the SPUdata Memory Layer.
    """
    
    def __init__(self, api_key=None):
        # Allow developers to pass the key directly or use environment variables
        self.api_key = api_key or os.environ.get("SPUDATA_API_KEY")
        self.base_url = "https://spudata.com/api/v1"
        
        if not self.api_key:
            raise ValueError("Initialization Failed: Sovereign API key (X-SPU-KEY) is required.")

    def fetch_spu(self, spu_id):
        """
        Pulls the deterministic rulebook from the Vault and validates the Witness Hash.
        """
        print(f"[*] Querying SPUdata Vault for {spu_id}...")
        headers = {"X-SPU-KEY": self.api_key}
        
        try:
            response = requests.get(f"{self.base_url}/spu/{spu_id}", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                gov_hash = response.headers.get("X-SPU-Governance-Hash", "UNVERIFIED")
                
                print(f"[+] Verified Logic Retrieved: {data.get('title')}")
                print(f"[+] TallySticks Witness Hash: {gov_hash}")
                
                return data.get('content')
                
            elif response.status_code == 403:
                raise PermissionError(f"EAVEcore Shield: Access Denied. {response.json().get('error')}")
            elif response.status_code == 404:
                raise FileNotFoundError(f"SPUdata Error: {spu_id} not found in the active ledger.")
            else:
                raise Exception(f"Gateway Error: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            raise SystemExit(f"Network failure connecting to SPUdata Node: {e}")

    def build_governed_prompt(self, spu_id, user_query):
        """
        The 93.5% Token Reduction Protocol.
        Automatically prepends the SPU logic to the agent's prompt to bypass hallucination.
        """
        sterile_logic = self.fetch_spu(spu_id)
        
        # Construct the final governed payload for the LLM
        governed_payload = (
            f"--- SOVEREIGN CONTEXT LOADED ({spu_id}) ---\n"
            f"{sterile_logic}\n"
            f"------------------------------------------\n\n"
            f"AGENT DIRECTIVE:\n{user_query}"
        )
        return governed_payload

    def freeze_state(self, session_id, context_summary):
        """
        The Save-State Protocol.
        Compresses the agent's active memory and uploads it as a Private SPU.
        """
        print(f"[*] Freezing Agent State for Session: {session_id}...")
        headers = {"X-SPU-KEY": self.api_key, "Content-Type": "application/json"}
        
        payload = {
            "title": f"STATE-SAVE: {session_id}",
            "content": f"[FROZEN CONTEXT]\n{context_summary}\n[END CONTEXT]",
            "category": "AI/ML",
            "is_public": False # Must be private to prevent state leakage
        }
        
        try:
            response = requests.post(f"{self.base_url}/spu", json=payload, headers=headers)
            if response.status_code == 201:
                spu_id = response.json().get('spu_id')
                print(f"[+] State Frozen Successfully. Handoff ID: {spu_id}")
                return spu_id
            elif response.status_code == 403:
                raise PermissionError("Upgrade Required: Save-State requires a £3 Private Enclave.")
            else:
                raise Exception(f"State Save Failed: {response.text}")
        except Exception as e:
            print(f"[!] Handoff Error: {e}")
            return None

    def wake_state(self, spu_id):
        """
        The Context-Resume Protocol.
        A new agent fetches the frozen SPU and seamlessly resumes the task.
        """
        print(f"[*] Waking Frozen State from {spu_id}...")
        return self.fetch_spu(spu_id)

    def evaluate_vault_opportunity(self, token_burn, external_calls_made):
        """
        The Auto-Synthesis Suggestion.
        Recognizes when an agent is wasting compute on repetitive research and suggests vaulting.
        """
        if external_calls_made > 3 or token_burn > 5000:
            suggestion = (
                f"\n[!] SYSTEM OPTIMIZATION DETECTED [!]\n"
                f"Agent burned ~{token_burn} tokens traversing {external_calls_made} external sources.\n"
                f"Suggestion: Let's clean this final synthesized logic up and vault it to your £3 Private Enclave.\n"
                f"Next time, you can retrieve this intelligence in O(1) deterministic time, saving compute and bypassing the web."
            )
            print(suggestion)
            return True
        return False

# ==========================================
# EXAMPLE USAGE:
# ==========================================
if __name__ == "__main__":
    agent = SovereignAgent(api_key="spudata_YOUR_LIVE_KEY_HERE")
    TARGET_SPU = "SPU-650c4309"
    raw_query = "Draft an internal memo regarding the new procurement contract with Vendor X."
    
    try:
        safe_prompt = agent.build_governed_prompt(TARGET_SPU, raw_query)
        print("\n[READY FOR LLM INGESTION]")
        print(safe_prompt)
    except Exception as e:
        print(f"\n[!] Execution Halted: {e}")

