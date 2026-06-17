import os
import requests
import json
import time

class SovereignAgent:
    """
    The Python SDK for interacting with the SPUdata Memory Layer.
    Ensures deterministic execution and non-deterministic error recovery.
    """
    def __init__(self, api_key=None, base_url="https://spudata.com"):
        self.api_key = api_key or os.getenv("SPUDATA_API_KEY")
        # Added capability to override base_url via env var for staging environments
        self.base_url = os.getenv("SPUDATA_BASE_URL", base_url)
        
        if not self.api_key:
            raise ValueError("Genesis API Key missing. Set SPUDATA_API_KEY environment variable.")

    def _handle_response(self, response):
        """Helper to handle HTTP limits gracefully."""
        if response.status_code == 429:
            raise Exception("Rate Limit Exceeded: You have hit the Fair Usage loop protection.")
        if response.status_code == 403:
            # Need to parse JSON if possible to show exact EAVEcore error
            try:
                err_msg = response.json().get('error', 'Access Denied')
            except:
                err_msg = "Access Denied: Check API Key Tier or Contamination."
            raise PermissionError(err_msg)
        if response.status_code == 415:
            try:
                err_msg = response.json().get('reason', 'Unsupported Media Type')
            except:
                err_msg = "Ingress Rejected: File format not supported."
            raise ValueError(f"Ingress Rejected: {err_msg}")
        response.raise_for_status()
        return response

    def fetch_spu(self, spu_id):
        """Fetches deterministic logic from the SPUdata Vault."""
        headers = {"X-SPU-KEY": self.api_key}
        # FIX: Aligning with the actual app.py GET endpoint structure for user SPUs
        url = f"{self.base_url}/api/v1/spu/user/{spu_id}" 
        
        try:
            response = requests.get(url, headers=headers)
            self._handle_response(response)
            
            # FIX: Safely parsing the response, whether it's JSON or Raw Text
            content_type = response.headers.get('Content-Type', '')
            if 'application/json' in content_type:
                data = response.json()
                return data.get('content', '')
            else:
                return response.text
                
        except Exception as e:
            print(f"[!] SPU Retrieval Failed: {e}")
            return None

    def freeze_state(self, session_id, context_summary):
        """
        The Save-State Protocol.
        Requires Tier-3 Private Enclave (£3).
        """
        headers = {"X-SPU-KEY": self.api_key, "Content-Type": "application/json"}
        # FIX: Aligning with the actual app.py POST endpoint
        url = f"{self.base_url}/api/v1/spu" 
        
        payload = {
            "title": f"STATE-SAVE: {session_id}",
            "content": f"[FROZEN CONTEXT]\n{context_summary}\n[END CONTEXT]",
            "category": "AI/ML",
            "is_public": False 
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            self._handle_response(response) # Handle 429/403 globally
            
            if response.status_code == 201:
                return response.json().get('spu_id')
                
        except PermissionError as e:
             raise PermissionError(f"Upgrade Required for Save-State: {e}")
        except Exception as e:
            print(f"[!] Handoff Error: {e}")
            return None

    def wake_state(self, spu_id):
        """Resumes a frozen state."""
        return self.fetch_spu(spu_id)
        
    def evaluate_vault_opportunity(self, token_burn, sources_scraped):
        """Active coaching for token reduction."""
        if token_burn > 5000 or sources_scraped > 3:
            print(f"\n[!] SYSTEM OPTIMIZATION DETECTED [!]")
            print(f"Agent burned ~{token_burn} tokens traversing {sources_scraped} external sources.")
            print("Suggestion: Clean this final synthesized logic and vault it to your £3 Private Enclave.")
            print("Next time, retrieve this intelligence in O(1) time, saving compute and bypassing the web.\n")

    def build_governed_prompt(self, spu_id, query):
        """Constructs a deterministic prompt payload."""
        start_time = time.time()
        spu_logic = self.fetch_spu(spu_id)
        
        if not spu_logic:
            raise Exception("Cannot build prompt: SPU logic unavailable.")
            
        prompt = f"""
        [GOVERNANCE SHIELD ACTIVE]
        You must follow the rulebook below. Do not deviate.
        
        -- SPU LOGIC START --
        {spu_logic}
        -- SPU LOGIC END --
        
        User Query: {query}
        """
        
        # Simulate token tracking for the coaching module
        simulated_tokens = len(prompt) // 4
        self.evaluate_vault_opportunity(token_burn=simulated_tokens, sources_scraped=1)
        
        return prompt
