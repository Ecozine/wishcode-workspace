# ==============================================================================

# WISHCODE WORKSPACE

# EXECUTION INTERCEPTION WORKFLOW

#

# Architectural Paradigm:

# "The model is an agent of suggestion, never the arbiter of state."

# ==============================================================================

import json
import re
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any

class SecurityContext:
"""
Authenticated runtime identity and authority context.

```
In production, this context must originate from an authenticated
authorization layer rather than from model-generated content.
"""

def __init__(self, user_id: str, role: str, session_token: str):
    self.user_id = user_id
    self.role = role
    self.session_token = session_token
```

class WishcodeMiddleware:
"""
Deterministic governance boundary between model-generated proposals
and state-changing execution.

```
The model may propose.
The middleware determines whether the proposal satisfies policy.
Only an authorized execution boundary may change system state.
"""

def __init__(self):

    # ------------------------------------------------------------------
    # Immutable governance policies.
    #
    # These rules are deliberately decoupled from the model's prompt,
    # context window, temperature, or generated output.
    # ------------------------------------------------------------------

    self.IMMUTABLE_POLICIES = {

        "ROLE_PERMISSIONS": {
            "analyst": [
                "read_logs",
                "format_data"
            ],

            "administrator": [
                "read_logs",
                "format_data",
                "mutate_system_state"
            ]
        },

        "VALIDATION_SCHEMAS": {
            "mutate_system_state": {
                "target_node": r"^[a-zA-Z0-9_\-]{4,64}$",
                "payload_hash": r"^[a-fA-F0-9]{64}$"
            }
        }
    }

def process_agent_output(
    self,
    raw_llm_string: str,
    session: SecurityContext
) -> Dict[str, Any]:

    """
    Deterministic interception boundary.

    The model's output is treated as untrusted proposal data.

    No model-generated instruction can directly mutate system state.
    """

    print(
        "🔒 [INTERCEPTION] "
        "Untrusted model proposal intercepted."
    )

    # ==============================================================
    # STEP 1 — STRUCTURAL PARSING
    # ==============================================================

    try:

        proposal = json.loads(raw_llm_string)

        if not isinstance(proposal, dict):
            raise ValueError("Proposal must be a JSON object.")

        tool_name = proposal.get("suggested_tool")
        arguments = proposal.get("arguments", {})

        if not isinstance(tool_name, str):
            raise ValueError("Missing or invalid suggested_tool.")

        if not isinstance(arguments, dict):
            raise ValueError("arguments must be an object.")

    except (json.JSONDecodeError, ValueError, TypeError) as exc:

        return self._handle_rejection(
            reason="MALFORMED_PROPOSAL_SYNTAX",
            details=str(exc),
            session=session
        )

    # ==============================================================
    # STEP 2 — AUTHORITY VALIDATION
    # ==============================================================

    allowed_actions = self.IMMUTABLE_POLICIES[
        "ROLE_PERMISSIONS"
    ].get(session.role, [])

    if tool_name not in allowed_actions:

        return self._handle_rejection(
            reason="UNAUTHORIZED_TOOL_PROPOSAL",
            details=(
                f"Role '{session.role}' has no explicit authority "
                f"for '{tool_name}'."
            ),
            session=session,
            tool_name=tool_name
        )

    # ==============================================================
    # STEP 3 — ARGUMENT SCHEMA VALIDATION
    # ==============================================================

    schema = self.IMMUTABLE_POLICIES[
        "VALIDATION_SCHEMAS"
    ].get(tool_name, {})

    for parameter, regex_pattern in schema.items():

        value = arguments.get(parameter)

        if value is None:

            return self._handle_rejection(
                reason="ARGUMENT_VALIDATION_FAILURE",
                details=f"Required argument '{parameter}' is missing.",
                session=session,
                tool_name=tool_name
            )

        if not re.fullmatch(regex_pattern, str(value)):

            return self._handle_rejection(
                reason="ARGUMENT_VALIDATION_FAILURE",
                details=(
                    f"Argument '{parameter}' failed deterministic "
                    "schema validation."
                ),
                session=session,
                tool_name=tool_name
            )

    # ==============================================================
    # STEP 4 — GOVERNANCE DECISION
    # ==============================================================

    decision = "AUTHORIZE"

    decision_payload = {
        "user_id": session.user_id,
        "role": session.role,
        "tool": tool_name,
        "arguments": arguments,
        "decision": decision,
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat()
    }

    decision_hash = hashlib.sha256(
        json.dumps(
            decision_payload,
            sort_keys=True
        ).encode("utf-8")
    ).hexdigest()

    print(
        "✅ [AUTHORIZED] "
        "Proposal satisfies deterministic governance criteria."
    )

    # IMPORTANT:
    # This is an authorization artifact, not direct execution.
    # A separate execution boundary must consume it.

    return {
        "status": "AUTHORIZED",
        "decision": decision,
        "decision_id": f"WISHCODE-{decision_hash[:16].upper()}",
        "execution_payload": {
            "tool": tool_name,
            "args": arguments
        },
        "provenance": {
            "decision_hash": decision_hash,
            "timestamp": decision_payload["timestamp"]
        }
    }

# ==================================================================
# REJECTION / VETO PATH
# ==================================================================

def _handle_rejection(
    self,
    reason: str,
    details: str,
    session: SecurityContext,
    tool_name: str = "UNKNOWN"
) -> Dict[str, Any]:

    """
    Deterministic rejection path.

    A rejected proposal cannot proceed to the execution boundary.
    The model receives only sanitized feedback.
    """

    print(
        f"❌ [GOVERNANCE VETO] "
        f"Reason: {reason} | Details: {details}"
    )

    # --------------------------------------------------------------
    # Computational provenance
    # --------------------------------------------------------------

    event_payload = {
        "reason": reason,
        "details": details,
        "user_id": session.user_id,
        "tool": tool_name
    }

    provenance_hash = hashlib.sha256(
        json.dumps(
            event_payload,
            sort_keys=True
        ).encode("utf-8")
    ).hexdigest()

    # --------------------------------------------------------------
    # Append-only audit record
    # --------------------------------------------------------------

    self._write_to_sovereign_audit_log(
        reason=reason,
        details=details,
        session=session,
        tool_name=tool_name,
        event_hash=provenance_hash
    )

    # --------------------------------------------------------------
    # Sanitized model feedback
    #
    # This feedback informs the model of the decision.
    # It does NOT delegate authority back to the model.
    # --------------------------------------------------------------

    return {
        "status": "EXECUTION_DENIED",
        "error_code": "MIDDLEWARE_SECURITY_VETO",
        "provenance_token": (
            f"WISHCODE-ERR-{provenance_hash[:16].upper()}"
        ),
        "system_instruction": (
            "The proposed action was denied by the system "
            "authorization boundary. Do not re-attempt the "
            "denied action. Continue only within authorized "
            "boundaries."
        )
    }

# ==================================================================
# AUDIT / PROVENANCE
# ==================================================================

def _write_to_sovereign_audit_log(
    self,
    reason: str,
    details: str,
    session: SecurityContext,
    tool_name: str,
    event_hash: str
):

    """
    Simulated append-only audit operation.

    Production implementation should use an independently protected
    audit system with appropriate integrity and access controls.
    """

    print(
        "📊 [PROVENANCE LOGGED] "
        f"Hash: {event_hash} | "
        f"User: {session.user_id} | "
        f"Tool: {tool_name} | "
        f"Reason: {reason}"
    )
```

# ==============================================================================

# RUNTIME SIMULATION

# Vault 05 — Cognitive Control

# ==============================================================================

if **name** == "**main**":

```
middleware = WishcodeMiddleware()

# ------------------------------------------------------------------
# Authenticated runtime context.
#
# The role is supplied by the authorization environment,
# not by the model.
# ------------------------------------------------------------------

analyst_session = SecurityContext(
    user_id="usr_9921",
    role="analyst",
    session_token="session_secure_xyz123"
)

# ------------------------------------------------------------------
# Simulated model output.
#
# The model proposes a state-changing operation.
# The model itself has no authority to execute it.
# ------------------------------------------------------------------

model_proposal = """
{
    "suggested_tool": "mutate_system_state",
    "arguments": {
        "target_node": "production-database-01",
        "payload_hash": "a4fbc83d7890123456789abcdef0123456789abcdef0123456789abcdef01234"
    }
}
"""

# ------------------------------------------------------------------
# Interception.
# ------------------------------------------------------------------

decision = middleware.process_agent_output(
    raw_llm_string=model_proposal,
    session=analyst_session
)

print(
    "\\n📦 [GOVERNANCE RESPONSE]"
)

print(
    json.dumps(
        decision,
        indent=4
    )
)
```

# ==============================================================================

# ARCHITECTURAL INVARIANT

#

# The model is an agent of suggestion, never the arbiter of state.

#

# Model

# ↓

# Suggestion

# ↓

# Wishcode Middleware

# ↓

# Identity + Authority + Policy + Schema

# ↓

# Governance Decision

# ↓

# Authorized Execution Boundary

# ↓

# System State

#

# The model can propose a state transition.

# It cannot authorize the transition.

# It cannot bypass the governance boundary.

# It cannot independently determine system state.

# ==============================================================================
