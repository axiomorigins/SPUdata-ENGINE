import os
import requests
import json
import time

class SovereignAgent:
    """
    The Python SDK for interacting with the SPUdata Memory Layer.
    Ensures deterministic execution and non-deterministic error recovery.
    """
    def __init__(self, api_key=None, base_url="https://spudata.com", cognitive_limit=80000):
        self.api_key = api_key or os.getenv("SPUDATA_API_KEY")
        # Added capability to override base_url via env var for staging environments
        self.base_url = os.getenv("SPUDATA_BASE_URL", base_url)
        
        # Cognitive Tracking
        self.cognitive_limit = int(os.getenv("SPU_COGNITIVE_LIMIT", cognitive_limit))
        self.current_token_burn = 0
        
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

    def fetch_spu(self, spu_id, preferred_tag=None):
        """Fetches deterministic logic from the SPUdata Vault with intelligent fork routing."""
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
                
                # Intelligent Fork Routing (Solves Agent Confusion)
                if preferred_tag and "available_forks" in data:
                    for fork in data["available_forks"]:
                        if preferred_tag in fork.get("fork_tags", []):
                            print(f"[INTELLIGENT ROUTING] Found specialized fork {fork['spu_id']} matching tag '{preferred_tag}'. Diverting retrieval.")
                            return self.fetch_spu(fork['spu_id']) # Recursive clean fetch of the fork
                            
                return data.get('content', '')
            else:
                return response.text
                
        except Exception as e:
            print(f"[!] SPU Retrieval Failed: {e}")
            return None

    def fork_spu(self, parent_spu_id, title, content, fork_tags="", is_public=True):
        """
        Forks an existing SPU with specialized metadata (e.g. os:linux, syntax:typescript).
        Capped at 4 public forks in the Global Commons to prevent fragmentation.
        """
        headers = {"X-SPU-KEY": self.api_key, "Content-Type": "application/json"}
        url = f"{self.base_url}/api/v1/spu/{parent_spu_id}/fork" 
        
        payload = {
            "title": title,
            "content": content,
            "fork_tags": fork_tags,
            "is_public": is_public 
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            self._handle_response(response)
            if response.status_code == 201:
                return response.json()
        except Exception as e:
            print(f"[!] Fork Failed: {e}")
            return None

    def request_superior_spu(self, target_spu_id, proposed_title, proposed_content, proposed_tags=""):
        """Submits a Wikipedia-style community proposal for SPU evolution."""
        headers = {"X-SPU-KEY": self.api_key, "Content-Type": "application/json"}
        url = f"{self.base_url}/api/v1/spu/{target_spu_id}/request-update" 
        
        payload = {
            "proposed_title": proposed_title,
            "proposed_content": proposed_content,
            "proposed_tags": proposed_tags 
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            self._handle_response(response)
            if response.status_code == 201:
                return response.json()
        except Exception as e:
            print(f"[!] Proposal Failed: {e}")
            return None

    def vote_proposal(self, proposal_id):
        """Upvotes a community fork proposal."""
        headers = {"X-SPU-KEY": self.api_key}
        url = f"{self.base_url}/api/v1/spu/proposal/{proposal_id}/vote" 
        
        try:
            response = requests.post(url, headers=headers)
            self._handle_response(response)
            return response.json()
        except Exception as e:
            print(f"[!] Vote Failed: {e}")
            return None

    def deprecate_fork(self, spu_id):
        """Deprecates an old or low-quality fork owned by the user."""
        headers = {"X-SPU-KEY": self.api_key}
        url = f"{self.base_url}/api/v1/spu/{spu_id}/deprecate" 
        
        try:
            response = requests.post(url, headers=headers)
            self._handle_response(response)
            return response.json()
        except Exception as e:
            print(f"[!] Deprecation Failed: {e}")
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

    def vault_resolved_use_case(self, title, logic_content, is_public=False):
        """
        Uploads an optimized, successful loop (Resolved Use Case) back to the vault.
        Transforms SPU-DEV (optimization phase) into SPU-OPS (standard operating procedure).
        """
        headers = {"X-SPU-KEY": self.api_key, "Content-Type": "application/json"}
        url = f"{self.base_url}/api/v1/spu"
        
        payload = {
            "title": title,
            "content": logic_content,
            "category": "SPU-OPS",
            "is_public": is_public
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            self._handle_response(response)
            if response.status_code == 201:
                new_id = response.json().get('spu_id')
                print(f"[+] Resolved Use Case successfully vaulted as SPU-OPS: {new_id}")
                return new_id
        except Exception as e:
            print(f"[!] Vaulting Failed: {e}")
            return None

    def track_cognitive_load(self, token_burn, session_id, context_summary):
        """
        Monitors agent token usage. If the hard cognitive limit is breached,
        automatically triggers the `freeze_state` -> context purge -> `wake_state` cycle.
        """
        self.current_token_burn += token_burn
        
        if self.current_token_burn >= self.cognitive_limit:
            print(f"\n[COGNITIVE LIMIT REACHED: {self.current_token_burn} / {self.cognitive_limit} tokens]")
            print("[EXECUTING O(1) FREEZE STATE...]")
            
            # Execute Save-State Protocol
            spu_id = self.freeze_state(session_id, context_summary)
            
            if spu_id:
                print(f"[FREEZE SUCCESS] Context secured at {spu_id}. Safely purging local LLM memory.")
                print(f"[WAKING STATE] Retrieving sterile memory from vault...")
                
                # Execute Wake-State Protocol
                sterile_context = self.wake_state(spu_id)
                self.current_token_burn = 0  # Reset cognitive load after wake
                
                print("[WAKE SUCCESS] Agent memory reset and focused. Continuing execution.\n")
                return sterile_context
            else:
                raise Exception("CRITICAL FAILURE: Could not freeze state at cognitive limit. Aborting to prevent hallucination.")
                
        return None

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
