# TIE Handoff: {{work_name}}

Handoff status: prepared
Handoff type: cross-conversation
TIE Session: {{workspace_qualified_session_id}}
Session status at handoff: paused
Blueprint status: {{draft_review-ready_approved_or_rejected}}
Execution approval: {{not-requested_pending_approved_or_rejected}}
Production authorization: {{not-requested_approved_or_rejected}}
Prepared on: {{iso_date}}

## Transfer Boundary

- From: {{current_codex_conversation_and_session}}
- To: {{next_codex_conversation_same_tie_session}}
- Purpose: {{why_the_work_is_moving}}
- Identity rule: resume the same TIE Work Session; do not create a peer Session for a conversation-only transfer.
- Source-of-truth rule: this file routes the transfer but does not replace or duplicate canonical decisions.
- Currency rule: prepared status requires agreement with canonical Blueprint and approval fields; refresh or supersede after a relevant change. Mark received when resumed.

## Canonical Artifact Map

- Shared TIE: {{relative_path_to_shared_tie}}
- Session state: session.md
- Approved or current Blueprint: blueprint.md
- Execution handoff: execution.md
- Project state: {{relative_path_to_project_state}}

## Read Order

1. {{project_instructions}}
2. This `handoff.md`
3. The shared TIE
4. `session.md`
5. `blueprint.md`
6. `execution.md`
7. Project state and only the evidence needed for the saved resume point

## Saved Resume Point

- Resume action: {{Point to session.md Decision Spine's exact next gate; do not retell the full current state}}
- Blocking decisions: {{none_or_ids}}
- Blocking unknowns: {{none_or_ids}}
- Approval boundary: {{what_is_and_is_not_authorized}}

## Do Not Do

- Do not create another TIE Work Session for this conversation-only transfer.
- Do not infer production authorization from Blueprint or execution-handoff approval.
- Do not duplicate canonical decisions into this routing receipt.
- Do not begin work outside the saved resume point without explicit user direction.

## Copy-Ready Resume Prompt

```text
{{prompt_for_the_next_codex_conversation}}
```

## Receipt

- Pause reason: {{why_the_current_conversation_stopped}}
- Last accepted decision: {{decision_id_and_summary}}
- Exact next question or action: {{question_or_action}}
- Execution approval: {{state}}
- Production authorization: {{state}}
