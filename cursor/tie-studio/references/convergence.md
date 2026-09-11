# Convergence Guardrails

Use this reference to decide when a Decision Arc has enough user input, when to
checkpoint, and what may be recommended or deferred. Conversation shape and route
visibility are defined in `conversation-navigation.md`.

## Question Ceiling

An Arc may ask at most three material user questions before a short checkpoint. This
is an internal guardrail, not a visible budget ceremony, a target, or three separate
runs. Stop earlier when the Arc is coherent or another question has diminishing value.

Count a question only when Cursor needs consequential user judgment or missing evidence
before progress can continue. Do not count status updates, acknowledgments, route
views, direct answers, or an approval request already required by a real gate.

Do not ask a weak question merely because capacity remains. Do not reset the ceiling
after every micro-decision.

## Trigger A Checkpoint

Show a short checkpoint when any of these is true:

- the user asks for status or synthesis
- the route materially changes
- the Arc is coherent enough to complete or review
- another question has diminishing downstream value
- three material user questions have been asked since the last checkpoint

The checkpoint is a conversational view of canonical `session.md` state. It is not a
new file, a second source of truth, a new Arc, Blueprint status, or approval.

## Checkpoint Shape

Include only what helps the user remain oriented:

```text
Checkpoint
Settled: <current coherent direction>
Still needs you: <material user judgment, or none>
I recommend: <reversible evidence-supported choice, or none>
Can wait: <non-blocking unknowns>
Next gate: <what completes the Arc or requires approval>
```

If another must-ask question remains inside the already authorized Arc, provide its
causal bridge and ask it after the checkpoint. Do not ask the user to type `continue`
merely to receive it.

## Guard Recommendations

Proceed with an internal choice without new confirmation only when it is:

- reversible without changing the outcome bet
- supported by current evidence or a stated convention
- low-risk if temporarily wrong
- independent of material Taste, Intent, Eval, scope, evidence acceptance, or approval

Keep consequential judgment under `Still needs you`. Make recommendations individually
correctable and record them as agent recommendations or assumptions. Silence is never
evidence that the user decided them.

This restriction governs adoption and action, not the ability to propose a consequential
design. AI can offer a concrete candidate before the user has formed a preference, with
its tradeoff and unknowns visible. A question the user cannot answer may need a different
method, not a longer wait or a smaller question about the same absent fact.

## Complete The Arc

A next artifact is sufficiently determined when it can be proposed or produced within
the actual authority without inventing a major outcome, Taste, scope or Eval choice.
Non-blocking uncertainty keeps its specific reopening condition. Do not require every
future service, implementation or editorial detail before presenting a coherent whole.
Do not optimize for fewer questions alone: an unresolved delivery or permission boundary
can still justify a focused question, however small it sounds.

Complete an Arc when its `Done when` condition in the Decision Spine is satisfied or
when the user explicitly pauses it. On completion:

- summarize the stage outcome and actual tradeoff or rejected direction, if any
- name remaining deferred unknowns
- state the next real gate
- update the Decision Spine and canonical receipt

Do not open another Arc automatically if it expands beyond the user's original request.
Do not create or approve a Blueprint merely because the Arc converged.

A sufficient local judgment is not completion of a wider authorized Arc. Stop asking
about the settled judgment and continue the remaining in-scope work until the Arc's
done condition or a real gate. Reopen only consequences affected by a correction.

## Manual Review

An Arc passes only when:

- each material question changes a consequential decision or resolves evidence
- the agent stops early when enough is known
- no fourth material question appears without a checkpoint
- recommendations contain no hidden user judgment
- unknowns remain visible
- the result makes the next choice clearer through a distinction, useful combination,
  or justified exclusion rather than merely producing more text
- the checkpoint preserves momentum instead of becoming a request for `continue`

## Failure Conditions

- Treating three questions as a target or three separate runs.
- Repeating a budget block on ordinary turns.
- Resetting the count after every answer.
- Converting consequential uncertainty into a bundled default.
- Using a checkpoint as a pause before an already-known next question.
- Calling a checkpoint a draft Blueprint, approval, or execution authorization.
