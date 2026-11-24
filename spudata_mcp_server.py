#!/usr/bin/env python3
"""
SPUdata MCP Server (Model Context Protocol)
===========================================
Zero-dependency stdio MCP Server that connects Claude Desktop, Cursor,
Windsurf, VS Code, and any MCP-compatible AI agent directly to your
SPUdata Deterministic Vault & EAVEcore PII Shield.

Tools exposed to the AI Agent:
  1. spudata_search        - Search Public Commons & Core Registry for verified rulebooks
  2. spudata_get_rulebook  - Retrieve a deterministic SPU rulebook (with fork tag routing)
  3. spudata_list_my_vault - List all private and public SPUs in the user's vault
  4. spudata_save_memory   - Vault a new rulebook or resolved use-case (EAVEcore PII-checked)
  5. spudata_freeze_state  - Save-State checkpoint for long-running agent handoffs
  6. spudata_wake_state    - Restore a frozen agent checkpoint in O(1) time
  7. spudata_pii_scan      - Run EAVEcore 9-vector PII/Secret scan on text before sending to an LLM

Configuration (Claude Desktop / Cursor / Windsurf):
  {
    "mcpServers": {
      "spudata": {
        "command": "python",
        "args": ["/path/to/spudata_mcp_server.py"],
        "env": {
          "SPUDATA_API_KEY": "spudata_YOUR_KEY_HERE"
        }
      }
    }
  }
"""

import sys
import os
import json
import urllib.request
import urllib.parse
import urllib.error

API_KEY = os.environ.get("SPUDATA_API_KEY", "")
BASE_URL = os.environ.get("SPUDATA_BASE_URL", "https://spudata.com").rstrip("/")
SERVER_NAME = "spudata-sovereign-vault"
SERVER_VERSION = "2.0.0"


def _api_request(method: str, path: str, payload: dict = None, require_auth: bool = True) -> dict:
    """Perform an HTTP request against the SPUdata API using stdlib urllib (zero external deps required)."""
    url = f"{BASE_URL}{path}"
    headers = {
        "User-Agent": f"SPUdata-MCP/{SERVER_VERSION}",
        "Accept": "application/json",
    }
    if API_KEY:
        headers["X-SPU-KEY"] = API_KEY
        headers["X-API-Key"] = API_KEY
    elif require_auth:
        return {
            "error": "SPUDATA_API_KEY is not set in the MCP environment.",
            "help": "Provision a key at https://spudata.com/register.html and set SPUDATA_API_KEY in your MCP config."
        }

    data_bytes = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        data_bytes = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(url, data=data_bytes, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            ctype = resp.headers.get("Content-Type", "")
            gov_hash = resp.headers.get("X-SPU-Governance-Hash")
            if "application/json" in ctype:
                parsed = json.loads(raw)
                if gov_hash and isinstance(parsed, dict):
                    parsed["governance_hash"] = gov_hash
                return parsed
            return {"content": raw, "governance_hash": gov_hash}
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        try:
            return {"http_status": e.code, **json.loads(err_body)}
        except Exception:
            return {"http_status": e.code, "error": err_body}
    except Exception as e:
        return {"error": f"Connection failed: {str(e)}"}


TOOLS = [
    {
        "name": "spudata_search",
        "description": (
            "Search the SPUdata Global Commons and Core Registry for deterministic AI rulebooks, "
            "coding standards, security patterns, and governance protocols before writing code or scraping docs."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Keyword or topic to search (e.g. 'fastapi', 'stripe', 'react', 'pii', 'checkpoint', 'nolan')"
                },
                "category": {
                    "type": "string",
                    "description": "Optional category filter (e.g. 'WEBDEV', 'AI', 'SPU-DEV', 'SPU-OPS', 'FIN', 'GOV')"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "spudata_get_rulebook",
        "description": (
            "Retrieve the full deterministic markdown rulebook for a specific SPU ID (e.g. 'SPU-650c4309', "
            "'SPU-API-FASTAPI-001'). Supports optional preferred_tag for intelligent fork routing."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "spu_id": {
                    "type": "string",
                    "description": "The SPU identifier (e.g. 'SPU-650c4309' or 'SPU-API-FASTAPI-001')"
                },
                "preferred_tag": {
                    "type": "string",
                    "description": "Optional fork tag to route to a specialized variant (e.g. 'os:linux', 'syntax:typescript')"
                }
            },
            "required": ["spu_id"]
        }
    },
    {
        "name": "spudata_list_my_vault",
        "description": (
            "List all private and public SPU rulebooks and frozen state checkpoints stored in the user's "
            "authenticated SPUdata Vault."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "spudata_save_memory",
        "description": (
            "Save a verified architecture pattern, coding standard, or resolved use-case to the SPUdata Vault. "
            "Automatically runs the EAVEcore 9-vector PII & Secret Shield before storing."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Clear, descriptive title for the rulebook or memory"
                },
                "content": {
                    "type": "string",
                    "description": "Markdown/text procedural logic. Must NOT contain live API keys, secrets, or real PII."
                },
                "category": {
                    "type": "string",
                    "description": "Category tag (e.g. 'SPU-OPS', 'SPU-DEV', 'WEBDEV', 'AI', 'GOV')",
                    "default": "SPU-OPS"
                },
                "is_public": {
                    "type": "boolean",
                    "description": "False to isolate in Private Enclave; True to contribute to Global Commons.",
                    "default": False
                }
            },
            "required": ["title", "content"]
        }
    },
    {
        "name": "spudata_freeze_state",
        "description": (
            "Execute the O(1) Save-State Protocol: checkpoint the current session state or multi-agent handoff "
            "into the user's Private Enclave so context can be cleared without losing progress."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "session_id": {
                    "type": "string",
                    "description": "Identifier for the task or session (e.g. 'TASK-AUTH-MIGRATION-01')"
                },
                "context_summary": {
                    "type": "string",
                    "description": "Structured summary of decisions, file states, and next steps (sterile, no secrets/PII)"
                }
            },
            "required": ["session_id", "context_summary"]
        }
    },
    {
        "name": "spudata_wake_state",
        "description": "Restore a previously frozen agent checkpoint by its SPU ID in O(1) time.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "spu_id": {
                    "type": "string",
                    "description": "The SPU ID returned by spudata_freeze_state"
                }
            },
            "required": ["spu_id"]
        }
    },
    {
        "name": "spudata_pii_scan",
        "description": (
            "Scan any code snippet, prompt, or document against the EAVEcore Governance Cartridge to detect "
            "hardcoded API keys, UK NINOs, emails, phone numbers, credit cards, bank details, or internal IPs."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "The text or code to validate for PII and secrets"
                }
            },
            "required": ["content"]
        }
    }
]


def execute_tool(name: str, args: dict) -> str:
    """Execute one of the SPUdata MCP tools and return a formatted string response."""
    if name == "spudata_search":
        q = args.get("query", "").strip()
        cat = args.get("category")
        # Search both static registry and public community SPUs
        q_enc = urllib.parse.quote(q)
        reg_res = _api_request("GET", f"/api/v1/search?q={q_enc}", require_auth=False)
        pub_path = "/api/v1/spu/public"
        if cat:
            pub_path += f"?category={urllib.parse.quote(cat)}"
        pub_res = _api_request("GET", pub_path, require_auth=False)

        matches = []
        for item in reg_res.get("results", []):
            matches.append({
                "spu_id": item.get("spu_id"),
                "title": item.get("display_name"),
                "category": item.get("category"),
                "source": "Core Registry",
                "token_count": item.get("token_count")
            })
        for doc in pub_res.get("public_spus", []):
            if not q or q.lower() in doc.get("title", "").lower() or q.lower() in doc.get("category", "").lower():
                matches.append({
                    "spu_id": doc.get("spu_id"),
                    "title": doc.get("title"),
                    "category": doc.get("category"),
                    "source": "Global Commons",
                    "is_canonical": doc.get("is_canonical", True),
                    "access_count": doc.get("access_count", 0)
                })
        return json.dumps({"query": q, "matches_found": len(matches), "results": matches}, indent=2)

    elif name == "spudata_get_rulebook":
        spu_id = args.get("spu_id", "").strip()
        preferred_tag = args.get("preferred_tag")
        # Try user/community vault first, then static registry
        res = _api_request("GET", f"/api/v1/spu/user/{urllib.parse.quote(spu_id)}", require_auth=True)
        if res.get("http_status") == 404 or "error" in res:
            static_res = _api_request("GET", f"/api/v1/spu/{urllib.parse.quote(spu_id)}", require_auth=False)
            if "content" in static_res:
                return static_res["content"]
        if preferred_tag and isinstance(res.get("available_forks"), list):
            for fork in res["available_forks"]:
                if preferred_tag in fork.get("fork_tags", []):
                    fork_res = _api_request("GET", f"/api/v1/spu/user/{fork['spu_id']}", require_auth=True)
                    return json.dumps(fork_res, indent=2)
        return json.dumps(res, indent=2)

    elif name == "spudata_list_my_vault":
        res = _api_request("GET", "/api/v1/spu/my-vault", require_auth=True)
        return json.dumps(res, indent=2)

    elif name == "spudata_save_memory":
        payload = {
            "title": args.get("title"),
            "content": args.get("content"),
            "category": args.get("category", "SPU-OPS"),
            "is_public": bool(args.get("is_public", False))
        }
        res = _api_request("POST", "/api/v1/spu", payload=payload, require_auth=True)
        return json.dumps(res, indent=2)

    elif name == "spudata_freeze_state":
        session_id = args.get("session_id", "SESSION")
        summary = args.get("context_summary", "")
        payload = {
            "title": f"STATE-SAVE: {session_id}",
            "content": f"[FROZEN CONTEXT]\n{summary}\n[END CONTEXT]",
            "category": "MEMORY_STATE",
            "is_public": False
        }
        res = _api_request("POST", "/api/v1/spu", payload=payload, require_auth=True)
        return json.dumps(res, indent=2)

    elif name == "spudata_wake_state":
        spu_id = args.get("spu_id", "").strip()
        res = _api_request("GET", f"/api/v1/spu/user/{urllib.parse.quote(spu_id)}", require_auth=True)
        return json.dumps(res, indent=2)

    elif name == "spudata_pii_scan":
        content = args.get("content", "")
        res = _api_request("POST", "/api/v1/validate", payload={"content": content}, require_auth=False)
        return json.dumps(res, indent=2)

    return json.dumps({"error": f"Unknown tool: {name}"})


def handle_rpc(msg: dict) -> dict:
    """Handle a single JSON-RPC 2.0 request from an MCP client."""
    method = msg.get("method")
    msg_id = msg.get("id")
    params = msg.get("params") or {}

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": params.get("protocolVersion", "2024-11-05"),
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": SERVER_NAME,
                    "version": SERVER_VERSION
                }
            }
        }

    elif method in ("notifications/initialized", "initialized"):
        return None

    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "tools": TOOLS
            }
        }

    elif method == "tools/call":
        tool_name = params.get("name")
        tool_args = params.get("arguments") or {}
        try:
            output_text = execute_tool(tool_name, tool_args)
            is_err = False
        except Exception as exc:
            output_text = json.dumps({"error": str(exc)})
            is_err = True

        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": output_text
                    }
                ],
                "isError": is_err
            }
        }

    elif method == "ping":
        return {"jsonrpc": "2.0", "id": msg_id, "result": {}}

    if msg_id is not None:
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "error": {
                "code": -32601,
                "message": f"Method not found: {method}"
            }
        }
    return None


def main():
    """Run the stdio JSON-RPC loop for MCP clients (Claude Desktop, Cursor, Windsurf)."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
            resp = handle_rpc(msg)
            if resp is not None:
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()
        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
