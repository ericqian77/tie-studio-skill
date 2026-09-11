# Explicit Visual Requests

Use this reference only after the user explicitly asks to visualize, draw, map,
diagram, preview, or compare visually. Visualization is an optional aid inside TIE,
not an automatic stage or default interaction.

## Keep The Invocation Boundary Simple

- Treat an unambiguous request for a visual representation as authorization to use an
  available visualization capability suited to that request.
- Treat `preview` as a visual request only when the requested preview is graphical;
  otherwise answer in the medium the user requested.
- Do not infer a visual request from statements such as “this is complex,” “I am
  confused,” “compare these,” or “help me understand.” Continue in text unless the
  user explicitly asks for visual form.
- Do not proactively offer, suggest, or prompt for a visual in ordinary TIE flow.
- Do not maintain a `GENERATE` / `ASK` / `DEFER` / `ABSTAIN` classifier, automatic
  decision-value trigger, hidden trigger rationale, frequency rule, or fidelity ladder.

If a requested visual cannot be made honestly because a required asset, datum, or
user-owned constraint is missing, ask only the one necessary question or explain the
tool limit. This is ordinary request fulfillment, not an automatic trigger policy.

## Make The Requested Aid Decision-Safe

- Choose a form and fidelity that preserve what the user needs to inspect. Low fidelity
  is not a default, and polish must not imply approval.
- Hold non-decision variables equal in comparisons. Use neutral styling and comparable
  detail unless evidence justifies an asymmetry, and name its source when material.
- Treat an advantage embedded in an alternative's name, such as `recoverable`, as a
  claim to inspect rather than a confirmed capability. Compare equivalent capabilities
  and evidence gaps on both sides instead of illustrating the claimed advantage for
  only one alternative.
- Keep assumptions, unknowns, omitted variables, and source provenance inspectable.
  Do not turn invented structure into apparent fact.
- Preserve the user's alternatives and active decision. Do not let the visual choose a
  direction through color, scale, detail, order, or unsupported quantitative shapes.
- Use the visual capability appropriate to the request rather than making one visual
  format or provider part of the TIE method.

## Return To The Same Decision Arc

Present the visual with only the context needed to interpret it and the current Arc's
next useful move. The visual may exist as an artifact, but it is not canonical TIE
state, evidence that the user decided, Blueprint approval, execution-handoff approval,
or execution authorization.

After the user responds:

1. accept ordinary correction without requiring the user to explain visual policy;
2. revise, replace, or withdraw the aid when requested;
3. record only the user's resulting decision or correction in `session.md`;
4. keep unsupported visual content labeled as an assumption or unknown rather than
   promoting it into evidence;
5. keep edits inside the active project's visual artifact and Session;
6. do not search for or modify TIE Studio source, references, tests, smoke prompts, or
   governing policy merely because the feedback resembles an existing case;
7. continue the same Decision Arc unless the user explicitly changes the work or route.

Only edit governing TIE Studio material when the user explicitly makes TIE Studio
itself the active subject. A correction to a project visual is not that authorization.

## Failure Conditions

- A vague statement of complexity triggers a visual or a visual suggestion.
- The aid silently favors an alternative or hides an unknown.
- Visual content becomes a confirmed fact or user decision without user evidence.
- Generating the aid is treated as approval or opens a new Decision Arc.
- The next response discusses visual machinery instead of continuing the user's decision.
- Ordinary project feedback expands into editing TIE Studio instructions or tests.
