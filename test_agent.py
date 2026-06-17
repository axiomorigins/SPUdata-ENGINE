from spu_agent import SovereignAgent
import os

# Use the key you provided (will be rotated after)
os.environ["SPUDATA_API_KEY"] = "spudata_VUtY5C9TwZFZCgEIP_Eu49o1I7LDmpi-yEEHOeereXc"

agent = SovereignAgent()

# Test 1: Basic governed prompt (uses a known example SPU)
try:
    TARGET = "SPU-650c4309"
    query = "Draft an internal memo regarding the new procurement contract with Vendor X."
    safe_prompt = agent.build_governed_prompt(TARGET, query)
    print("✅ build_governed_prompt succeeded")
    print(safe_prompt[:500] + "...")   # truncated
except Exception as e:
    print(f"❌ Failed: {type(e).__name__}: {e}")

# Test 2: Try freeze_state (should 403 on public key - expected & correct per FUP)
try:
    handoff = agent.freeze_state("TEST-SESSION-001", "This is a test frozen context summary.")
    print(f"freeze_state returned: {handoff}")
except PermissionError as e:
    print(f"✅ Correctly blocked (public key): {e}")
except Exception as e:
    print(f"❌ Unexpected error on freeze: {type(e).__name__}: {e}")
