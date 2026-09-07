# Session Boundaries

Use this reference whenever another example, project, or work item appears during an active TIE conversation.

## Three Different Things

Keep these states distinct:

1. **Reference example**: helps explain or test an idea inside the current Session. It creates no separate artifacts and does not change the active subject.
2. **TIE Work Session**: a real outcome with its own `tie/sessions/<session-id>/session.md`, decisions, and readiness state, inheriting repository principles from `tie/TIE.md` by default.
3. **Execution**: producing the approved outcome. This begins only after Blueprint and execution approval; opening a Work Session is not execution authorization.

TIE Studio development is a special Work Session whose subject is the TIE method and Skill itself.

## One Active Session Per Conversation

Keep only one TIE Session active in the current conversation. Other Sessions may remain persisted as `paused` or `closed`.

Do not infer a switch because the user mentions another task. Treat it as a reference example unless the user clearly asks to work on it or confirms a proposed switch.

If several session artifacts are visible, do not select one silently. State which appears active, list the plausible target, and ask or confirm before changing state.

Discover Sessions only inside the current owning workspace's `tie/sessions/`. Do not recursively treat nested repositories, fixtures, or linked workspaces as ordinary sibling Sessions. Follow another workspace only when an explicit artifact link or user request makes cross-workspace inspection relevant.

`Session ID` is unique only inside its owning workspace. When reporting or transitioning across workspaces, qualify identity as `<owning workspace>::<session-id>`; never rely on `main` alone.

## Response Visibility

Show this compact line when a Session is created, resumed, switched, paused, reported,
or could be ambiguous:

```text
TIE Session: <short session name> · <active or paused>
```

Keep the label short and human-readable. Do not repeat it, workspace paths, approval
state, blockers, or the full boundary on ordinary turns.

Show the full Context Transition Receipt only when a Session is created, switched, paused, resumed, or when identity is ambiguous or the user asks for status.

## Transition Protocol

Before entering another Session:

1. State the current Session and the proposed target.
2. Explain whether the target is still an example or will become real work.
3. State what will be paused and what will remain untouched.
4. Get clear user confirmation unless the user already gave an explicit switch command.
5. Save the current Decision Spine and set its status to `paused`.
6. Orient to the target's artifacts and use the resume status rule below: `review-ready`
   for an unchanged approved/review-ready Blueprint, otherwise `active`. Show a Context
   Transition Receipt; neither status gives production authority.

Use this concise receipt:

```text
TIE Context Transition
From: <session and workspace>
To: <session and workspace>
Purpose: <why the switch happened>
Saved resume point: <Arc, current group, and next question or action>
Execution approval: <state>
```

On resume, show the target's compact route from its Decision Spine, including settled
direction, blockers, current group, and next gate, before asking a new question.

## Artifact Boundary

Keep every real Work Session under `tie/sessions/<session-id>/`. Initialize `main`; add peer Sessions only when one Session cannot stay coherent. Do not write one Session's decisions into another Session's `session.md`.

Keep `tie/TIE.md` as the single repository-shared TIE. Do not create a per-Session TIE file. Record Session-specific Taste, Intent, and Eval in decisions and the compiled Blueprint.

The method-development Session may record product learnings from a pilot, but it must link them as evidence rather than copy the pilot's work decisions into the product decision log.

Do not create a Session registry or global active-session file in V1. Discover Sessions from `tie/sessions/*/session.md`; use conversation focus and Session-local metadata.

## Pause And Resume

Pausing must preserve:

- why the Session paused
- the last accepted decision
- unresolved blockers
- the current Arc, route position, and exact next question or action
- execution approval state

Do not continue asking work-specific questions from a paused Session. Resume only after an explicit user request or confirmed transition.

Pause is not revocation. If the plan's basis did not change, keep its Blueprint and
execution-handoff approvals intact, with Session status `paused`. Reconciliation and
confirmed-module requirements still apply. If a premise changed, invalidate only the
dependent approvals before pausing; a new conversation cannot revive stale authority.

## Moving The Same Work To A New Codex Conversation

A Codex conversation and a TIE Work Session are different boundaries. When the user wants a fresh Codex conversation to continue the same outcome, do not create a peer `tie/sessions/<id>/` directory. The owning workspace, Session ID, Blueprint, Eval, execution approval, and lifecycle have not changed.

Use this protocol:

1. Pause the current TIE Work Session and preserve the exact resume point.
2. Create or refresh Session-local `handoff.md` as a thin routing receipt.
3. Point it to the shared `tie/TIE.md`, canonical `session.md`, `blueprint.md`, `execution.md`, and relevant project state.
4. Record the approval boundary exactly; Blueprint or execution-handoff approval must not be interpreted as production authorization.
5. Include a copy-ready resume prompt naming the workspace-qualified TIE Session.
6. Before calling the receipt `prepared`, compare its Blueprint/approval fields with
   the canonical files. If those change before transfer, refresh it or mark it `superseded`.
7. In the new Codex conversation, read the canonical artifacts, verify that the handoff
   is still current, mark it `received`, reactivate the same Session, and show a resume
   receipt. For an unchanged review-ready or approved Blueprint use Session status
   `review-ready`; otherwise use `active`. Neither status authorizes production.

Do not copy the full decision history into `handoff.md`. Duplication creates drift. If the new conversation changes the outcome, Blueprint, Eval, approval lifecycle, or independent lifecycle, evaluate whether that is a genuine new TIE Work Session instead.

## Receiving Relayed Input

A message from another task can faithfully convey a user decision and also contain that
agent's interpretations. Preserve attribution in existing `User evidence` / `AI synthesis`
fields rather than recording the entire relay as user-authored constraints.

A useful short relay separates:

```text
User statement or faithful paraphrase: "Keep client names private; show how I work."
Source: <task and turn/time, if available>; <direct transcript or reported statement>.
Relayer interpretation: an illustrative method section may help; not user-approved copy.
Requested action: reconcile the selected Session and continue its authorized discussion.
```

Do not require transcripts for every harmless paraphrase. For a new prohibition, material
scope or execution approval, check an available original if the relay's authority is
ambiguous. If it remains unavailable, preserve the uncertainty and ask only when it
blocks the next action. Existing clearly scoped authorization remains usable without
repeat confirmation. A later user correction supersedes only the affected interpretation;
do not infer its opposite or discard compatible decisions. This guidance controls the
receiver's compilation; it cannot guarantee how an unrelated sending agent behaves.

## Failure Conditions

- A reference example silently becomes an active project.
- The conversation discusses one Session while writing another Session's files.
- Two Sessions appear active in the same conversation without an explicit orchestration mode.
- A paused Session continues producing questions or artifacts.
- Opening or resuming a Session is treated as approval to execute.
- A new Codex conversation creates a duplicate TIE Work Session for the same outcome.
- A handoff receipt becomes a second source of truth instead of pointing to canonical artifacts.
