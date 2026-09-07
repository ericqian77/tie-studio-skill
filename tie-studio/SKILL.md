---
name: tie-studio
description: Form revisable consequential judgments from project evidence, concrete proposals, and focused questions before substantial execution. Use when explicitly asked to clarify Taste, Intent, Eval, a Blueprint, or a TIE Workbench; do not invoke implicitly.
---

# TIE Studio

Help the user develop something worth making and a judgment sufficient for the next
bounded step. Keep the working understanding correctable; compile commitments when
they are ready for review, not merely because a short answer can fill a template.

## Method And Authority Boundary

- Run only after explicit invocation as `$tie-studio`.
- Work in the selected project's existing Session. Do not change the global Skill,
  another project, or governing TIE Studio material without an explicit request.
- Keep evidence-method selection, formation hypotheses, and study bookkeeping backstage.
- Before the initial Minimum Sufficient Judgment, use at most one material constructed
  Probe. Zero is valid; this is an experimental isolation limit, not a user-facing quota.
- Keep reasoning, design, and semantic review in the host agent. Scripts check structure.
- Discussion, tentative design, Blueprint approval, execution-handoff approval, and
  actual execution are distinct. Never infer one approval from another or from `continue`.
- Do not claim to reveal a hidden, permanent true Intent or to have proven this method.

## Read Only The Relevant Guidance

- Read `references/discovery.md` for initial discovery, an unknown or correction
  that changes the next method, a constructed Probe, or a sufficient-judgment decision.
- Read `references/conversation-navigation.md` when opening or resuming an Arc,
  changing route, responding to `continue`, or reporting progress.
- Read `references/decision-quality.md` for a material correction, approval, stage
  transition, recovery, Eval design, Blueprint compilation, or readiness review.
- Read `references/convergence.md` when several questions may be needed or when
  choosing whether to checkpoint or stop.
- Read `references/session-boundaries.md` when another example, project, work item,
  conversation or relayed user input appears during an active Session.
- Read `references/dashboard.md` for an explicit dashboard open/refresh/stop request,
  or when updating records while this conversation has already enabled its dashboard.
- Read `references/visual-requests.md` only for an explicit request to visualize,
  draw, map, diagram, preview, or compare visually.

## Orient Without Restarting The Work

Read project instructions, `tie/TIE.md`, workspace-owned `tie/sessions/*/session.md`,
selected Session artifacts and project state, then the minimum relevant source evidence.
Apply the user's current request and corrections to that evidence; older artifacts do
not override newer user authority. Do not ask for information already available.

Discover Sessions only in their owning workspace, not nested fixtures or repositories.
Use `<workspace>::<session-id>` when identity could be ambiguous. A new conversation
resumes the same work; it does not require a new Session or a repeat interview.

Address the user's actual question. An upstream question is justified only when its
answer would materially change work within that request, not because it sounds deeper.
Before choosing a method, check what the next step assumes about the purpose of the
work. A participant's role, skill, or origin story does not by itself establish that purpose.

Keep a short provisional working understanding in `## Current Understanding`: who is
trying to make or change what, and which part is still an interpretation. Use existing
facts, decisions, assumptions, and unknowns rather than a new role table or profile.
Clarify only ambiguities that would change the next step. Intent can form through proposals;
complete understanding is not a prerequisite for proposing one.

## Optional Project Dashboard

After the user explicitly asks to open the TIE dashboard, follow `references/dashboard.md`:
resolve the same project/Session, author and validate an English-default projection,
publish it and open/reuse the local view. Understand equivalent requests in the user's
language; this adds no separate Skill or interview. Do not enable it implicitly.

For an explicit English/Chinese view request, select `en` or `zh-CN` in the same
projection and shared renderer. UI language, summary language and original source
language are separate; do not copy runtime code or change the project's delivery language.

While the dashboard is explicitly enabled for this work, finish canonical reconciliation
first, then publish a refreshed projection after relevant recorded changes. If no semantic
rebuild can run, leave the stale signal honest. Browser checks never invoke the model.
Closing the tab and stopping the service are different requests; a stopped dashboard
is not automatically restarted. Ordinary Discovery without an enabled dashboard keeps
its existing behavior and does not generate projections or extra confirmation steps.

## Develop A Concrete Possibility

Choose the least burdensome useful method: inspect evidence, answer directly, ask one
answerable question, propose a concrete design, compare a meaningful alternative or
near-miss, rehearse, propose a bounded trial, defer, or abstain. No method is mandatory.

Distinguish three things in ordinary language:

- **Known or reported evidence:** preserve its source and scope, including second-hand reports.
- **AI interpretation or design proposal:** explain what it aims to achieve, its real
  tradeoff, and what remains unknown. The user may modify, combine, or reject its frame.
- **User-authorized commitment:** preserve exactly what was accepted, including whether
  it is only a temporary design bet. Approval gives authority, not empirical proof.

AI may propose consequential design choices without pretending the user already chose
them. A concrete, argued candidate is often more useful than asking the user to invent
the product. Silence does not authorize the proposal or its implementation.

When the user cannot recall a fact, leave it unknown and change the method if useful.
Do not demand historical anecdotes, future observation, or another person's participation
as a prerequisite for unrelated present design. A missing fact blocks only the claims
or actions that depend on it. An authorized temporary design can coexist with unknown
preferences or outcomes; it is not a fabricated answer to them.

Alternatives need real consequences, not weak decoys. They need not be mutually exclusive
when the goals can coexist. Discovering a useful combination or new dimension is valid
progress; do not manufacture a rejection for a rubric. Name an actual sacrifice when
scarce scope, time, or incompatible behavior forces a choice.

For a constructed Probe, follow the separate action gate in `references/discovery.md`.
Do not write a prototype, generate a visual, copy assets, install dependencies, contact
people, spend money, or change external state just because discussion would benefit.

## Keep The Arc Useful And Bounded

An Arc is a user-understandable stage outcome, not a question or fixed questionnaire.
Keep its route in the existing `## Decision Spine`: goal, settled, current, later,
deferred, route changes, done condition, and next gate. Show a compact natural-language
route at create/resume, a material route change, or a status request; do not repeat a form.

Use this internal turn loop; the user should work on the outcome, not operate the loop:

1. Classify the new evidence, choice, correction or authority, including relay provenance.
2. Identify its delta and dependencies; reconcile the affected current records as below.
3. Choose the next useful method. Preserve the intended outcome/form level, identify what
   the answer would change in the next deliverable, and consider whether a whole revisable
   candidate would now be more useful than another question. Relevance alone is insufficient.
4. Present enough evidence, concrete proposal/tradeoff and approval scope to judge in chat;
   a linked document supplements that explanation. Ask one consequential judgment when needed.
5. Continue useful work within the authorized Arc and refresh an enabled Workbench before
   finishing the turn. Do not merely announce the next review and wait for `continue`.

Material Taste, Intent, Eval, scope and risk choices need user judgment before adoption.
AI may include unaccepted editorial choices in a clearly proposed whole for review.
Keep genuine blockers and reopening conditions; do not silently fill them to move faster.
At a real gate, make the proposed action reviewable before asking for its missing authority.
Reuse existing scoped approval; do not split one authorized action into synonymous gates.

Three material questions are an internal ceiling before a short checkpoint, not a quota.
Checkpoint earlier when useful; retain momentum when more in-scope work is already clear.
At completion, state the useful judgment, actual tradeoffs, remaining unknowns, and next
real gate. Do not mistake a tidy document or smooth conversation for improved judgment.

## Record Changes, Not Invented Certainty

Use existing project-local artifacts with distinct jobs:

- `tie/TIE.md`: durable shared principles, not title choices or review progress.
- `tie/sessions/main/session.md`: canonical current understanding and sourced history.
  Add a peer only if outcome, Eval, approval, or lifecycle cannot stay coherent here.
- The Session's Decision Spine owns the current stage and next gate; Readiness describes
  the relevant artifact's actual blockers and approval scope. Neither retells all decisions.
- `PROJECT_STATE.md`, when present: short goal, artifact, next action and verification
  pointers to the Session; not another detailed decision list.
- Session-local `blueprint.md` and `execution.md`: version/scoped review and authorized
  handoff artifacts. `handoff.md` is an optional thin cross-conversation receipt.
- An enabled Workbench derives its overview and record details from coordinated sources.

On first use initialize only TIE and `main` Session. Create other artifacts only when
requested or their existing gate is reached. Resume and preserve existing decisions.
Templates are output shapes, not questions to ask or requirements to invent; remove
unsupported placeholders and use `none yet` where appropriate.

Record provenance once in the Decision Log and current meaning with source IDs in
Current Understanding. Retain compatible choices. A short answer need not create a new ID, full
Taste/Intent/Eval argument or confidence score. Reuse stable IDs for surviving records.

Update affected views in place. Ordinary turns need only affected changes; approvals,
stage transitions, upstream corrections, recovery and first Workbench publication need
the current-surface review in `references/decision-quality.md`. A new overview does not
repair contradictory current details. Refresh TIE only for a supported durable delta;
update project state only when goal, stage, artifacts, next action or verification changes.

### Correct And Invalidate Before Continuing

Distinguish a changed premise, a local correction, additional evidence, and a pause.
Only a changed dependency reopens its scope, Eval, prohibitions, blockers or approval;
retain compatible choices. A pause alone changes lifecycle, not accepted decisions or
approval. Deferring a route is not a permanent ban; rejecting an interpretation does
not prove its opposite. Ask only if the distinction changes the next authorized action.

If an existing Blueprint depends on the changed premise:

- mark Session and Blueprint `Canonical reconciliation: pending`;
- set Blueprint header and Review State to `draft`, and Session readiness no higher
  than `draft-ready`; keep module and approval metadata consistent;
- visibly label the old draft stale, name the invalidated basis and affected constraints,
  and say it is not an execution source;
- invalidate any affected approval or execution handoff; preserve history, do not carry
  old approval into a revised scope or hide a stale handoff to make validation pass.

For an affected existing `execution.md`, set `Execution source: stale`, name the cause
in `Invalidated by:`, and set current Execution approval to `pending` (or the user's
actual non-approved state) consistently in Session, Blueprint and execution header.
Add a visible notice that the retained body and Approval Evidence are historical and
non-operative. Preserve them. Refresh or supersede any prepared conversation handoff.
After recompilation this old execution file stays stale until separately approved
replacement; do not infer approval from a request to organize or review a Blueprint.

This is immediate invalidation, not full recompilation after every short reply. Recompile
when requested or needed at a review gate. Finishing an approved stage is not invalidation:
retain its approved scope and label completed work, then point to the current stage's
authority and next gate. Never carry that old scope's approval into new work. Never report
reconciliation complete just because the latest paragraph or metadata was updated.

## Compile A Reviewable Blueprint

Allow a draft on request, even with unresolved judgments. Use accepted decisions, durable
TIE, current evidence, and only relevant module fields. Software, presentation, writing,
and research templates are under `assets/modules/`; a hybrid needs only useful secondary
fields. Infer the module provisionally without an opening schema question; explain and
confirm its fit before review-ready. A module cannot redefine the user's goal.

Read `references/decision-quality.md` before compiling. In particular:

- Give the Review Brief and chat summary the direction, decisive tradeoff, outcome bet,
  actual rejection or `none yet`, real blockers, and next gate.
- Separate accepted commitments from unaccepted design candidates. Requirements,
  prohibitions, Eval failures, and Must Ask items need an entailing user-authorized
  source or externally binding constraint. A fact or plausible AI rationale alone is
  not authority. An existing Decision ID alone does not prove entailment.
- Derive Eval from the current promise: what claim it tests, plausible alternative
  explanations, and what conclusion the observation can support. Technical operation,
  creator alignment, player value, and market preference are not interchangeable goals.
- The smallest coherent version must express or test that promise. Neither minimum
  asset count nor a grander competitive claim is automatically the correct bar.
- Preserve scope and semantic strength. Do not invent thresholds, quantifiers, evidence
  rules, or permanent anti-goals. Keep proposals visibly outside normative requirements.
- Review every current-facing surface, including module fields and execution boundaries;
  remove superseded constraints instead of appending a contradictory new summary.

Use `review-ready` only when material choices are coherent, the relevant module is
confirmed, the scope and claim-aligned Eval are reviewable, and important boundaries
can classify allowed, forbidden, and edge-case behavior. A real unresolved dependency
keeps the draft blocked; an unrelated unknown does not. Proposed defaults must remain
visible and no major user choice may be silently invented to achieve readiness.

Set reconciliation `complete` only after semantic review and structural checks. Status
may become `approved` only with explicit approval and resolution or acceptance of real
blockers. Approval of an experiment does not turn an unknown result into a fact.

## Preserve Execution And Session Gates

Create `execution.md` only after explicit approval of both the Blueprint and transition
to an execution handoff. Record the approvals in Session and Blueprint first. Preserve
accepted unknowns and stop conditions. Begin execution only when separately requested.
A pending or stale source cannot authorize new execution.
Pausing an unchanged approved plan preserves its approval and exact next gate. Resuming
the Session does not authorize production. A prepared conversation receipt must agree
with current canonical status; mark it received or superseded when it ceases to route
the pending transfer.

Keep one active TIE Session per conversation. Newly mentioned work is an example until
a real switch is explicit. On a switch, save the exact resume point, pause the current
Session, and show a Context Transition Receipt. Another conversation continuing the same
outcome resumes the same workspace-qualified Session through a thin handoff, not a duplicate.
Show `TIE Session: <short name> · <status>` at these boundaries or when identity is unclear.

Ordinary TIE remains text-first. Do not generate, suggest, or prompt for visual artifacts
without an explicit visual request. Requested aids remain revisable and inside the same
Arc, not canonical truth or approval. Feedback may revise that project's aid and Session,
not the governing Skill or tests unless TIE Studio is explicitly the active subject.

## Validation

```bash
python3 scripts/validate_artifacts.py --templates assets
python3 scripts/validate_artifacts.py --project /absolute/path/to/project
python3 scripts/validate_artifacts.py --self-test
```

These checks prove structure and explicit consistency only. A properly marked stale
execution handoff can be valid historical storage, never an executable source; an
unmarked or contradictory one fails closed. Source entailment, useful proposals,
claim-aligned Eval, and honest correction require host-agent review of the actual files.
