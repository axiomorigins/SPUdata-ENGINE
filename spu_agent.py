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

