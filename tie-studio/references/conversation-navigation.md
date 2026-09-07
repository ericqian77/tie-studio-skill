# Conversation Navigation

Use this reference when opening or resuming a Decision Arc, asking a material
question, changing the route, responding to `continue`, or summarizing progress.

## The User-Visible Unit Is A Decision Arc

A Decision Arc resolves one user-understandable stage outcome. Examples include
choosing the experience the next version must prove, establishing a presentation's
core argument, or deciding the evidence standard for a research brief.

Do not create a new Arc for every micro-decision. Several related choices may belong
to one Arc when the user's original request already authorizes that exploration.

## Keep One Canonical Decision Spine

Store the current route in the selected `session.md` under `## Decision Spine`:

- **Arc goal**: the stage outcome this Arc resolves
- **Settled**: decisions already constraining the route
- **Current**: the decision group now in focus
- **Later before gate**: named groups still expected before the Arc ends
- **Safely deferred**: visible work that does not block the next gate
- **Route changes**: what was added, removed, reordered, or deferred and why
- **Done when**: the condition that completes the Arc
- **Next gate**: review, Blueprint approval, execution handoff, Session transition, or pause

Do not create a separate route file or persistent chat summary. The Decision Spine is
a navigational view of canonical decisions and unknowns, not a second decision record.

## Show A Compact Route

At Arc create, resume, material route change, or explicit status request, show a
compact natural-language route. A new or resumed Arc must show this route before its
first material question. Name decision groups instead of showing only a count.

One or two natural sentences can name the current focus, what follows, what can wait,
and the next gate. Do not expose every Decision Spine field as a mandatory chat block.
The route is an estimate, not a fixed questionnaire. If new evidence changes it, say
what changed and update the Decision Spine.

If a material Must Ask group was not named in the current route, do not let it appear
silently. Briefly state what group was added, which new evidence made it necessary,
and what was reordered or deferred. Then update `Route changes` before asking. A more
specific question inside an already named group is not a route change.

## Give Every Question A Causal Bridge

Before a material question or proposal, supply what the user needs to decide in chat:

1. what the user's last answer or current evidence settled
2. the concrete candidate, difference or consequential unknown being judged
3. what the answer changes, including its tradeoff and the scope of any approval
4. the one reaction, correction, or judgment that would help

An artifact link is supporting detail, not a substitute for this decision basis. At an
approval gate summarize the actual deliverable and bounds before asking; do not force
the user to reopen a long document or reconstruct earlier messages. Use natural prose
rather than repeating a fixed four-line form. Reuse clearly scoped prior approval.

Example:

```text
You chose a calm, trust-first experience. I suggest a quiet opening with one clear
action; it sacrifices an immediate overview to reduce distraction. Would that still
give your first user enough context, or is the missing overview important here?
```

For the first question, use evidence from the user's request and workspace in place of
a previous answer. Never present an internal schema question as if it were the user's
product decision.

## Classify Before Asking

First check that an answer would change the next deliverable at the intended outcome
level. If a coherent revisable whole is already possible, prefer presenting it; retain
material unknowns instead of inventing decisions to complete it. Then classify:

### Must Ask

Ask before turning material Taste, Intent, Eval, scope, evidence acceptance, risk, or
approval into a commitment. This does not require an open question before a concrete
proposal. When the user has not formed the judgment, provide something useful to react to.

### Agent Recommends

Proceed with an internal choice only when it is supported, reversible, low-risk, and
within agreed bounds. AI may also propose consequential designs, with real tradeoffs
and uncertainty, but must not treat them as accepted or execute them without authority.

### Safely Defer

Keep the unknown visible and move on when the specific next claim or action does not
depend on it. State when it would need to be reopened. Missing history is not a blanket
blocker; provisional design does not fill it in as fact.

## Continue Inside The Authorized Arc

After the user answers:

1. update affected canonical Session content for a material delta; do not expand every
   short answer into a complete decision argument
2. acknowledge in one or two natural sentences what the answer settled
3. if useful work remains in the authorized Arc, actually deliver its next appropriate
   read-only method with a causal bridge; announcing a forthcoming review alone is not progress
4. otherwise recommend, defer, checkpoint, or complete the Arc

Do not end an ordinary turn with `reply continue`, `shall I continue?`, or a menu whose
only function is to reveal the next question. The user may interrupt, redirect, ask for
status, or pause at any time.

A bare `continue` carries no new approval. If the next useful method is already clear,
briefly restore the route and use it within existing authority. Never interpret
`continue` as accepting an unseen decision, a route change, Blueprint approval,
execution handoff, or execution authorization.

Do not ask for a second approval that merely restates the same already-authorized scope.
Different permissions remain distinct, but a user's explicit instruction can cover more
than one when the concrete scope was visible. Record what it covers without ceremony.

## Use Receipts At Real Boundaries

Keep the full decision record in `session.md`. In chat, use a short acknowledgment
after ordinary answers. Show a fuller Decision Receipt only when:

- accepted evidence materially changes the route
- the internal question ceiling triggers a checkpoint
- the Arc completes
- the user asks for a receipt or status

A route-change receipt names what was added, removed, reordered, or deferred. A receipt
must never become a repeated form after every micro-decision.

## Preserve Ownership

If the user answers `A`, `A + C`, or another short choice, record that choice as the
user decision. Explanations, implications, or prose generated by the agent remain AI
synthesis or assumptions unless the user stated or later confirmed them.

Ask the user to confirm an expanded rationale only when it would materially constrain
later scope, execution, or Eval. Do not turn a small answer into a large body of
apparently user-owned intent.

## Keep Stages And Gates Visible

When stage ambiguity is plausible, name the current stage in plain language:

- **TIE exploration**: resolving decisions and evidence
- **Blueprint review**: inspecting the compiled decision set
- **Execution handoff**: defining what Codex may later execute
- **Execution**: producing the approved outcome

Moving between these stages requires the existing approval rules. Automatic in-Arc
continuation never crosses a Session transition or approval gate.

## Failure Conditions

- A question appears without a causal bridge.
- A new or resumed Arc asks its first material question without a compact named route.
- The route is represented only as a remaining count.
- Module selection is the first user question even though it changes no material outcome.
- The user must type `continue` to discover an ordinary next question.
- `continue` is treated as approval of an unasked decision.
- A full receipt repeats after every answer.
- Agent-generated rationale is recorded as the user's words.
- A new material question group appears without an explicit route change.
- A stage or gate changes without being named.
