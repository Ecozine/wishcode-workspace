# Wishcode Workspace Mutation Architecture

## Purpose

The Wishcode mutation layer defines the architecture required to move from a read-only MCP environment to a governed execution environment.

The objective is not to make probabilistic AI deterministic.

The objective is to establish a deterministic authority boundary around probabilistic intelligence before any consequential state transition is executed.

MCP provides connectivity.

Wishcode provides governance, authorization, deterministic execution, and provenance.

---

## Architectural Principle

```text
AGENTS.md
    ↓
Governance Context
    ↓
MCP
    ↓
Connectivity
    ↓
Mutation Proposal
    ↓
Wishcode Governance Boundary
    ↓
Deterministic Verification
    ↓
Risk Classification
    ↓
Policy Evaluation
    ↓
Human Approval — when required
    ↓
Authorization Artifact
    ↓
Deterministic Execution
    ↓
Immutable Provenance
```

The central invariant is:

> **No model, agent, MCP tool, connector, service, user instruction, or downstream component may directly authorize consequential execution.**

Execution authority originates from the Wishcode Policy Core.

---

# 1. Mutation Is a Proposal First

An AI agent must not directly transform an external system.

Instead, the agent produces a structured mutation proposal.

Example:

```text
Mutation Proposal

Operation:
    CREATE_INVOICE

Trade:
    TR-1042

Amount:
    125000

Currency:
    USD

Requested By:
    Agent Session

Source Model:
    Model Identity / Version

Timestamp:
    Execution Request Time
```

The proposal is data.

It is not authorization.

The proposal must pass through the Wishcode governance boundary before execution can occur.

---

# 2. MCP Connectivity Boundary

MCP acts as the connectivity interface between compatible AI agents and external tools, systems, resources, or services.

```text
AI Agent
    ↓
MCP
    ↓
External Capability
```

For mutation workflows:

```text
AI Agent
    ↓
MCP
    ↓
Wishcode Governance Boundary
```

MCP must not become the source of execution authority.

MCP tool metadata, annotations, permissions, or client behavior must not be treated as a substitute for Wishcode policy enforcement.

MCP annotations are descriptive hints and are not sufficient as the authoritative security boundary.

Therefore:

> **MCP establishes connectivity. Wishcode establishes authority.**

---

# 3. Deterministic Verification

Every mutation proposal must be validated against deterministic rules before execution.

The validation layer must not rely on model judgment.

Example:

```text
Invoice Amount
        ↓
Schema Validation
        ↓
Trade Validation
        ↓
Threshold Validation
        ↓
Currency Validation
        ↓
Required Document Validation
        ↓
PASS / FAIL
```

Example deterministic rules:

```text
invoice.amount <= authorized_trade_limit

currency ∈ permitted_currencies

trade.status == READY_FOR_INVOICE

required_documents == PRESENT
```

A model may propose a value.

A deterministic validator determines whether that value satisfies the declared rules.

---

# 4. Validation Failure

A failed validation must terminate or redirect the mutation flow.

```text
Mutation Proposal
       ↓
Deterministic Validation
       ↓
       FAIL
       ↓
No Authorization
       ↓
No Execution
```

The system must not allow an AI agent to reinterpret a failed validation as permission to continue.

Where appropriate, the system may return a structured remediation request.

Example:

```text
STATUS: REJECTED

REASON:
Invoice exceeds authorized trade limit.

REQUIRED ACTION:
Submit a revised proposal or obtain an applicable policy exception.
```

---

# 5. Risk Classification

Validated mutation proposals must be classified according to consequence and policy.

Initial capability classes:

```text
READ
PROPOSE
EXECUTE
```

Mutation operations may additionally receive a risk classification:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

Example:

```text
CREATE_DRAFT_INVOICE
    → LOW

SUBMIT_INVOICE
    → MEDIUM

UPDATE_TRADE_STATUS
    → HIGH

ALTER_BILL_OF_LADING
    → HIGH

COMMIT_IRREVERSIBLE_TRANSACTION
    → CRITICAL
```

Risk classification does not itself authorize execution.

It determines which governance controls must be satisfied.

---

# 6. Policy Core

The Policy Core is the authoritative decision layer.

It evaluates:

* validated mutation parameters
* applicable policy version
* risk classification
* user authority
* system state
* transaction state
* required approvals
* applicable governance constraints

The Policy Core produces one of the following states:

```text
DENY
REQUIRE_HITL
AUTHORIZE
```

The Policy Core is the only component permitted to create execution authority.

---

# 7. Human-in-the-Loop Gateway

High-consequence mutations may require explicit human approval.

Example:

```text
AI Proposal
     ↓
MCP
     ↓
Validation
     ↓
Risk Classification
     ↓
HIGH RISK
     ↓
HITL Required
     ↓
Manager Review
     ↓
APPROVE / REJECT
     ↓
Policy Core
```

Human approval must not directly execute the mutation.

Instead, the approval becomes an input to the Policy Core.

This preserves the same authority model:

```text
Human Decision
      ↓
Policy Evaluation
      ↓
Authorization
      ↓
Execution
```

rather than:

```text
Human Dashboard
      ↓
Direct Database Mutation
```

---

# 8. Cryptographic Execution Sigil

An authorized mutation must receive a unique execution artifact.

The execution artifact binds the authorization decision to the specific state transition.

Conceptually:

```text
Execution Sigil
│
├── transaction_id
├── proposal_hash
├── user_identity
├── session_identity
├── model_identity
├── model_version
├── MCP tool identity
├── schema_version
├── policy_version
├── validation_result
├── risk_classification
├── HITL decision
├── authorization state
├── timestamp
└── parent_state
```

The exact cryptographic implementation will be defined separately.

The architectural requirement is:

> **An authorization artifact must be bound to the specific mutation it authorizes.**

It must not become a reusable general-purpose permission.

---

# 9. Single-Use Authorization

Execution authorization must be:

* policy-version bound
* state-transition bound
* transaction bound
* cryptographically verifiable
* non-reusable
* invalidated after execution

Conceptually:

```text
PROPOSAL
   ↓
HASH
   ↓
VALIDATION
   ↓
POLICY DECISION
   ↓
HITL — if required
   ↓
EXECUTION SIGIL
   ↓
EXECUTION
   ↓
SIGIL INVALIDATED
```

A previously authorized mutation must not be replayable against a different transaction or system state.

---

# 10. Deterministic Execution Core

The Execution Core performs only an already-authorized state transition.

It must not:

* interpret user intent
* resolve ambiguity
* calculate authorization
* assign GT Score
* make policy decisions
* override safety controls
* independently authorize mutations

Its responsibility is:

```text
Authorized State Transition
        ↓
Deterministic Execution
        ↓
Result
```

The Execution Core therefore remains intentionally narrow.

> **The component that executes must not be the component that decides.**

---

# 11. Immutable Provenance

Every consequential mutation must produce an immutable provenance record.

The provenance chain should preserve the relationship between:

```text
User
 ↓
Session
 ↓
Agent
 ↓
Model
 ↓
Proposal
 ↓
MCP Tool
 ↓
Schema
 ↓
Validation
 ↓
Policy
 ↓
HITL
 ↓
Authorization
 ↓
Execution
 ↓
Result
```

The objective is deterministic ancestry.

A future auditor should be able to determine:

> **Why was this state transition permitted, under which rules, by whom, from which proposal, and against which system state?**

---

# 12. State Transition Integrity

A mutation is valid only when the authorized transition matches the state for which authorization was issued.

Example:

```text
Authorized State:

TRADE-1042
STATUS = READY_FOR_INVOICE
```

If the trade changes before execution:

```text
TRADE-1042
STATUS = SUSPENDED
```

the previous authorization must become invalid.

Therefore:

```text
Authorized State ≠ Current State
        ↓
Authorization Invalid
        ↓
No Execution
```

This prevents stale authorization from being replayed against a changed system state.

---

# 13. Mutation Lifecycle

The canonical mutation lifecycle is:

```text
1. INTENT
      ↓
2. PROPOSAL
      ↓
3. MCP TRANSPORT
      ↓
4. SCHEMA VALIDATION
      ↓
5. DETERMINISTIC VERIFICATION
      ↓
6. RISK CLASSIFICATION
      ↓
7. POLICY EVALUATION
      ↓
8. HITL — IF REQUIRED
      ↓
9. AUTHORIZATION
      ↓
10. EXECUTION SIGIL
      ↓
11. DETERMINISTIC EXECUTION
      ↓
12. STATE VERIFICATION
      ↓
13. PROVENANCE RECORD
      ↓
14. AUTHORIZATION INVALIDATION
```

Any failed mandatory stage must prevent execution.

---

# 14. Failure-Safe Behavior

The default state of the mutation system must be non-executing.

If a required component is unavailable, ambiguous, inconsistent, or unverifiable:

```text
UNKNOWN
   ↓
NO AUTHORIZATION
   ↓
NO EXECUTION
```

Examples include:

* missing policy
* invalid schema
* failed validation
* stale state
* missing human approval
* invalid authorization artifact
* policy version mismatch
* provenance failure
* signature verification failure

The system must fail closed for consequential mutations.

---

# 15. Architectural Separation

The mutation architecture maintains explicit separation between interpretation and execution.

```text
Probabilistic Intelligence
        ↓
      INTERPRETS

Ambiguity Resolution
        ↓
      STRUCTURES

GT Score
        ↓
      ESTIMATES

Risk Topology
        ↓
        MAPS

Policy Core
        ↓
       DECIDES

Execution Core
        ↓
      EXECUTES

State Ledger
        ↓
      PRESERVES
```

Therefore:

> **Interpretation ≠ Authorization**

> **GT Score ≠ Truth**

> **User intent ≠ Safety override**

> **MCP connectivity ≠ Execution authority**

> **Human approval ≠ Direct execution**

> **Probabilistic output ≠ Deterministic execution**

---

# 16. Implementation Phases

The mutation architecture will be implemented incrementally.

### Phase 1 — Read-Only MCP

Establish connectivity without mutation authority.

```text
Agent
 ↓
MCP
 ↓
Read-Only Tool
 ↓
Response
```

### Phase 2 — Proposal Layer

Allow agents to construct structured mutation proposals without executing them.

```text
Agent
 ↓
MCP
 ↓
Mutation Proposal
 ↓
No Execution
```

### Phase 3 — Deterministic Validation

Introduce schemas and hard-coded validation rules.

```text
Proposal
 ↓
Schema
 ↓
Rules
 ↓
PASS / FAIL
```

### Phase 4 — Policy Core

Introduce explicit authorization decisions.

```text
Validated Proposal
 ↓
Policy Core
 ↓
DENY / HITL / AUTHORIZE
```

### Phase 5 — Human-in-the-Loop

Introduce approval workflows for high-consequence mutations.

### Phase 6 — Cryptographic Authorization

Introduce execution-bound authorization artifacts and cryptographic verification.

### Phase 7 — Deterministic Execution

Introduce narrowly scoped execution capabilities.

### Phase 8 — Immutable Provenance

Complete the mutation lifecycle with operational provenance and state-transition records.

---

# 17. Initial Mutation Targets

The first mutation capabilities should remain intentionally narrow.

Potential future operations include:

```text
CREATE_INVOICE
UPDATE_TRADE_STATUS
SUBMIT_COMPLIANCE_FORM
UPDATE_SHIPMENT_RECORD
ALTER_BILL_OF_LADING
```

These operations must not be implemented as unrestricted tools.

Each operation requires its own:

* schema
* validation rules
* risk classification
* policy requirements
* authorization requirements
* execution contract
* provenance requirements

---

# 18. Security Boundary

The following components are considered untrusted from an execution-authority perspective:

```text
Model
Agent
Prompt
MCP Client
MCP Tool
Connector
External API
User Instruction
Generated Output
```

They may provide information, proposals, or requests.

They do not independently grant execution authority.

The trusted authority chain is:

```text
Validated State
      ↓
Policy Core
      ↓
Authorization Artifact
      ↓
Deterministic Execution Core
      ↓
Immutable Provenance
```

---

# 19. Design Invariant

Wishcode does not attempt to eliminate probabilistic intelligence.

It places probabilistic intelligence inside a controlled execution boundary.

The model may change.

The agent may change.

The MCP server may change.

The external system may change.

The governance boundary remains.

---

## Core Principle

> **MCP establishes connectivity.**

> **Wishcode establishes authority.**

> **Policy decides.**

> **Execution obeys.**

> **The ledger remembers.**

---

## Final Architectural Statement

> **Open connectivity at the boundary.**
>
> **Deterministic governance within the boundary.**
>
> **Cryptographically bound authority at execution.**
>
> **Immutable provenance after execution.**

**Myth decides. Math precises. System endures.**
