#!/usr/bin/env python3
"""Deterministically validate TIE Studio templates or live workspace artifacts."""

from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path


SESSION_HEADINGS = [
    "# TIE Session:",
    "## Session Goal",
    "## Session Boundary",
    "## Current Understanding",
    "### Confirmed Facts",
    "### User Decisions",
    "### AI Assumptions",
    "### Unresolved Unknowns",
    "## Decision Log",
    "## Rejected Directions",
    "## Latest Decision Receipt",
    "## Decision Spine",
    "## Readiness",
]

BLUEPRINT_HEADINGS = [
    "# TIE Blueprint:",
    "## Review Brief",
    "## Work Definition",
    "## Decisions",
    "## Rejected Directions And Anti-goals",
    "## Scope And Boundaries",
    "## Work-Type Module",
    "## Assumptions And Unknowns",
    "## Eval Contract",
    "## Execution Boundary",
    "## Review State",
]

EXECUTION_HEADINGS = [
    "# TIE Execution:",
    "## Goal",
    "## Decisions To Preserve",
    "## Taste And Intent",
    "## Deliverables And Scope",
    "## Out Of Scope",
    "## Work-Type Requirements",
    "## Unknowns And Assumptions",
    "## Eval Contract",
    "## Execution Rules",
    "## Definition Of Done",
    "## Approval Evidence",
]

HANDOFF_HEADINGS = [
    "# TIE Handoff:",
    "## Transfer Boundary",
    "## Canonical Artifact Map",
    "## Read Order",
    "## Saved Resume Point",
    "## Do Not Do",
    "## Copy-Ready Resume Prompt",
    "## Receipt",
]

MODULE_HEADINGS = {
    "presentation.template.md": [
        "# TIE Module: Presentation",
        "## Audience And Moment",
        "## Thesis And Angle",
        "## Narrative And Use Cases",
        "## Evidence And Delivery",
    ],
    "software.template.md": [
        "# TIE Module: Software",
        "## Users And Situations",
        "## Experience And Behavior",
        "## Scope And Flow",
        "## Technical Boundary",
    ],
    "writing.template.md": [
        "# TIE Module: Writing",
        "## Reader And Context",
        "## Claim And Structure",
        "## Evidence And Voice",
        "## Editorial Eval",
    ],
    "research.template.md": [
        "# TIE Module: Research",
        "## Question And Decision Context",
        "## Evidence Strategy",
        "## Synthesis And Uncertainty",
        "## Research Deliverable",
    ],
}

TIE_HEADINGS = ["# TIE:", "## Intent", "## Taste", "## Eval"]
PLACEHOLDER_RE = re.compile(r"\{\{[^}]+\}\}")


def read(path: Path, errors: list[str]) -> str:
    if not path.is_file():
        errors.append(f"missing required file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def require_headings(path: Path, text: str, headings: list[str], errors: list[str]) -> None:
    for heading in headings:
        if heading not in text:
            errors.append(f"{path}: missing heading `{heading}`")


def field(text: str, name: str) -> str | None:
    match = re.search(rf"^{re.escape(name)}:[ \t]*(\S[^\r\n]*)$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def require_field(path: Path, text: str, name: str, errors: list[str]) -> str | None:
    value = field(text, name)
    if value is None:
        errors.append(f"{path}: missing field `{name}:`")
    return value


def require_bullet_field(path: Path, text: str, name: str, errors: list[str]) -> str | None:
    value = bullet_field(text, name)
    if value is None:
        errors.append(f"{path}: missing bullet field `- {name}:`")
    return value


def require_bullet_enum(
    path: Path,
    text: str,
    name: str,
    allowed: set[str],
    errors: list[str],
) -> str | None:
    value = require_bullet_field(path, text, name, errors)
    if value is not None and value not in allowed:
        errors.append(
            f"{path}: `- {name}:` must be one of {sorted(allowed)}, found `{value}`"
        )
    return value


def bullet_field(text: str, name: str) -> str | None:
    match = re.search(rf"^- {re.escape(name)}:[ \t]*(\S[^\r\n]*)$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def require_enum(
    path: Path,
    text: str,
    name: str,
    allowed: set[str],
    errors: list[str],
) -> str | None:
    value = require_field(path, text, name, errors)
    if value is not None and value not in allowed:
        errors.append(f"{path}: `{name}` must be one of {sorted(allowed)}, found `{value}`")
    return value


def optional_enum(
    path: Path,
    text: str,
    name: str,
    allowed: set[str],
    errors: list[str],
) -> str | None:
    value = field(text, name)
    if value is not None and value not in allowed:
        errors.append(f"{path}: `{name}` must be one of {sorted(allowed)}, found `{value}`")
    return value


def between(text: str, start: str, end: str | None = None) -> str:
    start_index = text.find(start)
    if start_index < 0:
        return ""
    content_start = start_index + len(start)
    if end is None:
        return text[content_start:]
    end_index = text.find(end, content_start)
    if end_index < 0:
        return text[content_start:]
    return text[content_start:end_index]


def ids(text: str, prefix: str) -> set[str]:
    return set(re.findall(rf"\b{re.escape(prefix)}-\d+\b", text))


def reject_placeholders(path: Path, text: str, errors: list[str]) -> None:
    match = PLACEHOLDER_RE.search(text)
    if match:
        errors.append(f"{path}: unresolved template placeholder `{match.group(0)}`")


def validate_template_set(root: Path) -> list[str]:
    errors: list[str] = []
    core_files = [
        (root / "session.template.md", SESSION_HEADINGS),
        (root / "blueprint.template.md", BLUEPRINT_HEADINGS),
        (root / "execution.template.md", EXECUTION_HEADINGS),
        (root / "handoff.template.md", HANDOFF_HEADINGS),
    ]
    for path, headings in core_files:
        text = read(path, errors)
        if text:
            require_headings(path, text, headings, errors)

    modules_root = root / "modules"
    for filename, headings in MODULE_HEADINGS.items():
        path = modules_root / filename
        text = read(path, errors)
        if text:
            require_headings(path, text, headings, errors)

    session = read(root / "session.template.md", errors=[])
    if session and field(session, "Execution approval") != "not-requested":
        errors.append(
            f"{root / 'session.template.md'}: default execution approval must be `not-requested`"
        )
    blueprint = read(root / "blueprint.template.md", errors=[])
    if blueprint and field(blueprint, "Blueprint status") != "draft":
        errors.append(
            f"{root / 'blueprint.template.md'}: default Blueprint status must be `draft`"
        )
    execution = read(root / "execution.template.md", errors=[])
    if execution and field(execution, "Execution approval") != "approved":
        errors.append(
            f"{root / 'execution.template.md'}: execution template must require `approved`"
        )
    for legacy in (
        "tie-session.template.md",
        "tie-blueprint.template.md",
        "tie-execution.template.md",
        "build-prompt.template.md",
    ):
        if (root / legacy).exists():
            errors.append(f"{root / legacy}: legacy template name must be removed")
    return errors


def validate_session(session_root: Path) -> list[str]:
    errors: list[str] = []
    session_path = session_root / "session.md"
    blueprint_path = session_root / "blueprint.md"
    execution_path = session_root / "execution.md"
    handoff_path = session_root / "handoff.md"
    legacy_build_path = session_root / "BUILD_PROMPT.md"

    session = read(session_path, errors)

    if session:
        require_headings(session_path, session, SESSION_HEADINGS, errors)
        reject_placeholders(session_path, session, errors)
        session_status = require_enum(
            session_path,
            session,
            "Session status",
            {"active", "paused", "review-ready", "closed"},
            errors,
        )
        if session_status == "paused":
            resume_point = bullet_field(session, "If paused, resume at")
            if resume_point is None or resume_point.lower().startswith("not-paused"):
                errors.append(f"{session_path}: paused Session must preserve `- If paused, resume at:`")
        else:
            resume_point = bullet_field(session, "If paused, resume at")
        session_id = require_field(session_path, session, "Session ID", errors)
        if session_id is not None and session_id != session_root.name:
            errors.append(
                f"{session_path}: `Session ID` must match directory `{session_root.name}`"
            )
        require_field(session_path, session, "Session title", errors)
        require_enum(
            session_path,
            session,
            "Session kind",
            {"work", "studio-development"},
            errors,
        )
        declared_session_path = require_field(session_path, session, "Session path", errors)
        expected_session_path = f"tie/sessions/{session_root.name}"
        if declared_session_path is not None and declared_session_path != expected_session_path:
            errors.append(
                f"{session_path}: `Session path` must be `{expected_session_path}`"
            )
        require_field(session_path, session, "Parent context", errors)
        require_enum(
            session_path,
            session,
            "Interaction model",
            {"persistent-truth-with-guided-decision-arcs"},
            errors,
        )
        session_work_type = require_field(session_path, session, "Work type", errors)
        session_selected_module = require_field(session_path, session, "Selected module", errors)
        module_selection = require_enum(
            session_path,
            session,
            "Module selection",
            {
                "codex-recommended-provisional",
                "codex-recommended-user-confirmed",
                "user-selected",
            },
            errors,
        )
        session_reconciliation = optional_enum(
            session_path,
            session,
            "Canonical reconciliation",
            {"pending", "complete"},
            errors,
        )
        for spine_field in (
            "Arc goal",
            "Settled",
            "Current",
            "Later before gate",
            "Safely deferred",
            "Route changes",
            "Done when",
            "Next gate",
        ):
            require_bullet_field(session_path, session, spine_field, errors)
        execution_approval = require_enum(
            session_path,
            session,
            "Execution approval",
            {"not-requested", "pending", "approved", "rejected"},
            errors,
        )
        blueprint_readiness = require_enum(
            session_path,
            session,
            "Blueprint readiness",
            {"not-ready", "draft-ready", "review-ready", "approved"},
            errors,
        )
        if blueprint_readiness in {"review-ready", "approved"} and module_selection == "codex-recommended-provisional":
            errors.append(
                f"{session_path}: `{blueprint_readiness}` Blueprint readiness requires confirmed module selection"
            )
        if (
            blueprint_readiness in {"review-ready", "approved"}
            and session_reconciliation != "complete"
        ):
            errors.append(
                f"{session_path}: `{blueprint_readiness}` Blueprint readiness requires "
                "`Canonical reconciliation: complete`"
            )
        if (
            session_status in {"active", "review-ready", "paused"}
            and blueprint_readiness in {"review-ready", "approved"}
            and resume_point is not None
            and re.fullmatch(r"D-\d+[.!]?", resume_point)
        ):
            errors.append(
                f"{session_path}: Session resume point must name the "
                "current review gate, not only a Decision ID"
            )

        current_assumptions = between(
            session,
            "### AI Assumptions",
            "### Unresolved Unknowns",
        )
        if module_selection in {
            "codex-recommended-user-confirmed",
            "user-selected",
        } and re.search(
            r"(?i)(module.{0,120}(provisional|await(?:ing)? confirmation|still needs? confirmation)"
            r"|模块.{0,120}(暂|待.{0,12}确认|仍需.{0,12}确认))",
            current_assumptions,
            re.DOTALL,
        ):
            errors.append(
                f"{session_path}: confirmed module selection conflicts with a current "
                "AI assumption that still describes the module as provisional"
            )

        defined_unknown_ids = set(
            re.findall(r"^#### (U-\d+):", session, re.MULTILINE)
        )
        current_facing_session = "".join(
            (
                between(session, "## Latest Decision Receipt", "## Decision Spine"),
                between(session, "## Decision Spine", "## Readiness"),
                between(session, "## Readiness"),
            )
        )
        phantom_unknown_ids = ids(current_facing_session, "U") - defined_unknown_ids
        for unknown_id in sorted(phantom_unknown_ids):
            errors.append(
                f"{session_path}: current-facing state references undefined `{unknown_id}`"
            )

        defined_decision_ids = set(
            re.findall(r"^### (D-\d+):", session, re.MULTILINE)
        )
    else:
        session_status = None
        session_work_type = None
        session_selected_module = None
        module_selection = None
        session_reconciliation = None
        execution_approval = None
        blueprint_readiness = None
        defined_decision_ids = set()

    blueprint_status = None
    if blueprint_path.exists():
        blueprint = read(blueprint_path, errors)
        require_headings(blueprint_path, blueprint, BLUEPRINT_HEADINGS, errors)
        reject_placeholders(blueprint_path, blueprint, errors)
        blueprint_work_type = require_field(blueprint_path, blueprint, "Work type", errors)
        blueprint_selected_module = require_field(
            blueprint_path, blueprint, "Selected module", errors
        )
        blueprint_module_selection = require_enum(
            blueprint_path,
            blueprint,
            "Module selection",
            {
                "codex-recommended-provisional",
                "codex-recommended-user-confirmed",
                "user-selected",
            },
            errors,
        )
        blueprint_reconciliation = optional_enum(
            blueprint_path,
            blueprint,
            "Canonical reconciliation",
            {"pending", "complete"},
            errors,
        )
        source_session = require_field(blueprint_path, blueprint, "Source session", errors)
        if source_session is not None and source_session != "session.md":
            errors.append(f"{blueprint_path}: `Source session` must be `session.md`")
        for brief_field in (
            "Direction",
            "Core Taste",
            "Outcome bet",
            "Main rejected direction",
            "Blockers",
            "Next gate",
        ):
            require_bullet_field(blueprint_path, blueprint, brief_field, errors)
        blueprint_status = require_enum(
            blueprint_path,
            blueprint,
            "Blueprint status",
            {"draft", "review-ready", "approved", "rejected"},
            errors,
        )
        if blueprint_status in {"review-ready", "approved"} and blueprint_module_selection == "codex-recommended-provisional":
            errors.append(
                f"{blueprint_path}: `{blueprint_status}` Blueprint status requires confirmed module selection"
            )
        if (
            blueprint_status in {"review-ready", "approved"}
            and blueprint_reconciliation != "complete"
        ):
            errors.append(
                f"{blueprint_path}: `{blueprint_status}` Blueprint status requires "
                "`Canonical reconciliation: complete`"
            )
        if (
            blueprint_status in {"review-ready", "approved"}
            and "### Operational Boundaries" not in blueprint
        ):
            errors.append(
                f"{blueprint_path}: `{blueprint_status}` Blueprint requires "
                "`### Operational Boundaries`"
            )
        blocking_unknowns = require_field(blueprint_path, blueprint, "Blocking unknowns", errors)
        blocker_approval = require_enum(
            blueprint_path,
            blueprint,
            "Blocking unknown acceptance",
            {"not-requested", "approved", "rejected"},
            errors,
        )
        if (
            blueprint_status == "approved"
            and blocking_unknowns is not None
            and blocking_unknowns.lower().rstrip(".") != "none"
            and blocker_approval != "approved"
        ):
            errors.append(f"{blueprint_path}: approved Blueprint has unaccepted blocking unknowns")

        review_blueprint_status = require_bullet_enum(
            blueprint_path,
            blueprint,
            "Blueprint status",
            {"draft", "review-ready", "approved", "rejected"},
            errors,
        )
        if (
            blueprint_status is not None
            and review_blueprint_status is not None
            and review_blueprint_status != blueprint_status
        ):
            errors.append(
                f"{blueprint_path}: Review State Blueprint status "
                f"`{review_blueprint_status}` does not match header `{blueprint_status}`"
            )
        review_execution_approval = require_bullet_enum(
            blueprint_path,
            blueprint,
            "Execution approval",
            {"not-requested", "pending", "approved", "rejected"},
            errors,
        )
        critical_unknown_acceptance = require_bullet_enum(
            blueprint_path,
            blueprint,
            "Critical unknowns accepted by user",
            {"not-applicable", "yes", "no"},
            errors,
        )
        blockers_are_none = (
            blocking_unknowns is not None
            and blocking_unknowns.lower().rstrip(".") == "none"
        )
        if blockers_are_none and critical_unknown_acceptance != "not-applicable":
            errors.append(
                f"{blueprint_path}: no blocking unknowns requires "
                "`- Critical unknowns accepted by user: not-applicable`"
            )
        if (
            not blockers_are_none
            and blocker_approval == "approved"
            and critical_unknown_acceptance != "yes"
        ):
            errors.append(
                f"{blueprint_path}: approved blocking unknown acceptance requires "
                "`- Critical unknowns accepted by user: yes`"
            )
        if (
            not blockers_are_none
            and blocker_approval != "approved"
            and critical_unknown_acceptance == "yes"
        ):
            errors.append(
                f"{blueprint_path}: critical unknowns cannot be accepted while "
                "`Blocking unknown acceptance` is not `approved`"
            )

        blueprint_decision_section = between(
            blueprint, "## Decisions", "## Rejected Directions And Anti-goals"
        )
        blueprint_decision_ids = set(
            re.findall(r"^### (D-\d+):", blueprint_decision_section, re.MULTILINE)
        )
        blueprint_source_ids = set(
            re.findall(
                r"^- Source decision:\s*(D-\d+)\b",
                blueprint_decision_section,
                re.MULTILINE,
            )
        )
        missing_source_ids = blueprint_decision_ids - blueprint_source_ids
        for decision_id in sorted(missing_source_ids):
            errors.append(
                f"{blueprint_path}: `{decision_id}` is missing its matching "
                "`- Source decision:`"
            )
        undefined_source_ids = blueprint_source_ids - defined_decision_ids
        for decision_id in sorted(undefined_source_ids):
            errors.append(
                f"{blueprint_path}: source decision `{decision_id}` is undefined in session.md"
            )

        for label, session_value, blueprint_value in (
            ("Work type", session_work_type, blueprint_work_type),
            ("Selected module", session_selected_module, blueprint_selected_module),
            ("Module selection", module_selection, blueprint_module_selection),
        ):
            if (
                session_value is not None
                and blueprint_value is not None
                and session_value != blueprint_value
            ):
                errors.append(
                    f"{blueprint_path}: `{label}` value `{blueprint_value}` does not match "
                    f"session.md `{session_value}`"
                )

        if (
            session_reconciliation is not None
            and blueprint_reconciliation is not None
            and session_reconciliation != blueprint_reconciliation
        ):
            errors.append(
                f"{blueprint_path}: `Canonical reconciliation` value "
                f"`{blueprint_reconciliation}` does not match session.md "
                f"`{session_reconciliation}`"
            )

        if (
            execution_approval is not None
            and review_execution_approval is not None
            and execution_approval != review_execution_approval
        ):
            errors.append(
                f"{blueprint_path}: Review State Execution approval "
                f"`{review_execution_approval}` does not match session.md "
                f"`{execution_approval}`"
            )

        # Session activity is not artifact readiness or execution authority.
        # Existing reconciliation, approval and stale-source gates remain independent.
        if blueprint_status == "review-ready":
            if blueprint_readiness != "review-ready":
                errors.append(
                    f"{blueprint_path}: `Blueprint status: review-ready` requires "
                    "`Blueprint readiness: review-ready` in session.md"
                )
            if session_status not in {"active", "review-ready", "paused"}:
                errors.append(
                    f"{blueprint_path}: `Blueprint status: review-ready` requires "
                    "an active or review-ready Session, or a paused Session with a resume point"
                )
        if blueprint_status == "approved":
            if blueprint_readiness != "approved":
                errors.append(
                    f"{blueprint_path}: `Blueprint status: approved` requires "
                    "`Blueprint readiness: approved` in session.md"
                )
            if session_status not in {"active", "review-ready", "paused"}:
                errors.append(
                    f"{blueprint_path}: `Blueprint status: approved` requires "
                    "an active or review-ready Session, or a paused Session with a resume point"
                )

        expected_blueprint_status = {
            "review-ready": "review-ready",
            "approved": "approved",
        }.get(blueprint_readiness)
        if (
            expected_blueprint_status is not None
            and blueprint_status != expected_blueprint_status
        ):
            errors.append(
                f"{session_path}: `Blueprint readiness: {blueprint_readiness}` requires "
                f"`Blueprint status: {expected_blueprint_status}`"
            )
    elif blueprint_readiness in {"draft-ready", "review-ready", "approved"}:
        errors.append(f"{blueprint_path}: required when Blueprint readiness is `{blueprint_readiness}`")

    if execution_approval == "approved" and blueprint_status != "approved":
        errors.append(f"{session_path}: approved execution requires an approved current Blueprint")

    if execution_path.exists():
        execution = read(execution_path, errors)
        require_headings(execution_path, execution, EXECUTION_HEADINGS, errors)
        reject_placeholders(execution_path, execution, errors)
        # Missing marker keeps the original strict gate for existing files. A stale
        # file is retained evidence, never a usable execution source. Its historical
        # Approval Evidence may remain approved; its current header must not be.
        execution_source = optional_enum(
            execution_path, execution, "Execution source", {"current", "stale"}, errors
        ) or "current"
        handoff_approval = require_enum(
            execution_path, execution, "Execution approval",
            {"not-requested", "pending", "approved", "rejected"}, errors,
        )
        if execution_source == "stale":
            require_field(execution_path, execution, "Invalidated by", errors)
            if handoff_approval == "approved" or execution_approval == "approved":
                errors.append(
                    f"{execution_path}: stale execution source cannot carry current approved execution"
                )
            if handoff_approval is not None and handoff_approval != execution_approval:
                errors.append(f"{execution_path}: stale execution source approval must match session.md")
        else:
            if handoff_approval != "approved":
                errors.append(f"{execution_path}: `Execution approval` must be `approved`")
            if execution_approval != "approved":
                errors.append(f"{execution_path}: session.md does not record approved execution")
            if blueprint_status != "approved":
                errors.append(f"{execution_path}: blueprint.md does not record `Blueprint status: approved`")

    if handoff_path.exists():
        handoff = read(handoff_path, errors)
        require_headings(handoff_path, handoff, HANDOFF_HEADINGS, errors)
        reject_placeholders(handoff_path, handoff, errors)
        handoff_status = require_enum(
            handoff_path,
            handoff,
            "Handoff status",
            {"prepared", "received", "superseded"},
            errors,
        )
        require_field(handoff_path, handoff, "TIE Session", errors)
        require_enum(
            handoff_path,
            handoff,
            "Session status at handoff",
            {"paused"},
            errors,
        )
        handoff_blueprint_status = require_enum(
            handoff_path,
            handoff,
            "Blueprint status",
            {"draft", "review-ready", "approved", "rejected"},
            errors,
        )
        handoff_execution_approval = require_enum(
            handoff_path,
            handoff,
            "Execution approval",
            {"not-requested", "pending", "approved", "rejected"},
            errors,
        )
        require_enum(
            handoff_path,
            handoff,
            "Production authorization",
            {"not-requested", "approved", "rejected"},
            errors,
        )
        if handoff_status == "prepared" and session_status != "paused":
            errors.append(f"{handoff_path}: prepared handoff requires `Session status: paused`")
        if handoff_status == "prepared":
            for label, receipt_value, current_value in (
                ("Blueprint status", handoff_blueprint_status, blueprint_status),
                ("Execution approval", handoff_execution_approval, execution_approval),
            ):
                if receipt_value is not None and receipt_value != current_value:
                    errors.append(
                        f"{handoff_path}: prepared handoff `{label}: {receipt_value}` "
                        f"does not match current canonical value `{current_value}`"
                    )

    if legacy_build_path.exists():
        errors.append(f"{legacy_build_path}: legacy handoff must be migrated to `execution.md`")

    return errors


def validate_project(root: Path) -> list[str]:
    errors: list[str] = []
    tie_path = root / "tie" / "TIE.md"
    sessions_root = root / "tie" / "sessions"
    main_session = sessions_root / "main" / "session.md"

    tie = read(tie_path, errors)
    if tie:
        require_headings(tie_path, tie, TIE_HEADINGS, errors)
        reject_placeholders(tie_path, tie, errors)
        if field(tie, "Status") is not None:
            errors.append(
                f"{tie_path}: durable TIE memory must not store live `Status:`; "
                "keep lifecycle state in session.md"
            )
        live_tie_marker = re.search(
            r"(?im)^\s*[-*]?\s*((?:current (?:stage|step|phase)|next action)\b|"
            r"当前阶段|当前步骤|下一步)",
            tie,
        )
        if live_tie_marker:
            errors.append(
                f"{tie_path}: durable TIE memory contains live lifecycle language "
                f"`{live_tie_marker.group(0).strip()}`"
            )
        tie_session_ids = ids(tie, "D") | ids(tie, "U")
        if tie_session_ids:
            errors.append(
                f"{tie_path}: durable TIE memory must not copy Session IDs "
                f"{sorted(tie_session_ids)}"
            )

    if not main_session.is_file():
        errors.append(f"missing required main Session: {main_session}")

    if sessions_root.is_dir():
        for session_root in sorted(path for path in sessions_root.iterdir() if path.is_dir()):
            errors.extend(validate_session(session_root))

    for legacy in (
        "TIE.md",
        "tie-session.md",
        "TIE_BLUEPRINT.md",
        "TIE_EXECUTION.md",
        "BUILD_PROMPT.md",
    ):
        if (root / legacy).exists():
            errors.append(f"{root / legacy}: legacy root artifact must be migrated into `tie/`")

    return errors


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def self_test() -> list[str]:
    failures: list[str] = []
    with tempfile.TemporaryDirectory(prefix="tie-studio-validator-") as temp:
        root = Path(temp)
        write(root / "tie" / "TIE.md", "# TIE: Demo\n\n## Intent\nX\n\n## Taste\nX\n\n## Eval\nX")
        write(
            root / "tie" / "sessions" / "main" / "session.md",
            """
# TIE Session: Demo
Session status: review-ready
Session ID: main
Session title: Demo
Session kind: work
Session path: tie/sessions/main
Parent context: none
Interaction model: persistent-truth-with-guided-decision-arcs
Work type: presentation
Selected module: presentation
Module selection: codex-recommended-user-confirmed
Execution approval: approved
Canonical reconciliation: complete
## Session Goal
X
## Session Boundary
X
## Current Understanding
### Confirmed Facts
X
### User Decisions
X
### AI Assumptions
X
### Unresolved Unknowns
X
## Decision Log
X
## Rejected Directions
X
## Latest Decision Receipt
X
## Decision Spine
- Arc goal: X
- Settled: X
- Current: X
- Later before gate: none
- Safely deferred: none
- Route changes: none
- Done when: X
- Next gate: review
## Readiness
Blueprint readiness: approved
""",
        )
        write(
            root / "tie" / "sessions" / "main" / "blueprint.md",
            """
# TIE Blueprint: Demo
Blueprint status: approved
Work type: presentation
Selected module: presentation
Module selection: codex-recommended-user-confirmed
Blocking unknowns: none
Blocking unknown acceptance: not-requested
Canonical reconciliation: complete
Source session: session.md
## Review Brief
- Direction: X
- Core Taste: X
- Outcome bet: X
- Main rejected direction: X
- Blockers: none
- Next gate: review
## Work Definition
X
## Decisions
X
## Rejected Directions And Anti-goals
X
## Scope And Boundaries
X
### Operational Boundaries
X
## Work-Type Module
X
## Assumptions And Unknowns
X
## Eval Contract
X
## Execution Boundary
X
## Review State
- Decisions reviewed by user: yes
- Critical unknowns accepted by user: not-applicable
- Blueprint status: approved
- Execution approval: approved
""",
        )
        write(
            root / "tie" / "sessions" / "main" / "execution.md",
            """
# TIE Execution: Demo
Execution approval: approved
## Goal
X
## Decisions To Preserve
X
## Taste And Intent
X
## Deliverables And Scope
X
## Out Of Scope
X
## Work-Type Requirements
X
## Unknowns And Assumptions
X
## Eval Contract
X
## Execution Rules
X
## Definition Of Done
X
## Approval Evidence
X
""",
        )

        positive_errors = validate_project(root)
        if positive_errors:
            failures.append("approved fixture should pass: " + "; ".join(positive_errors))

        session_path = root / "tie" / "sessions" / "main" / "session.md"
        blueprint_path = root / "tie" / "sessions" / "main" / "blueprint.md"
        approved_session = session_path.read_text(encoding="utf-8")
        approved_blueprint = blueprint_path.read_text(encoding="utf-8")
        session = approved_session.replace(
            "Execution approval: approved", "Execution approval: not-requested"
        )
        session_path.write_text(session, encoding="utf-8")
        approval_errors = validate_project(root)
        if not any("does not record approved execution" in error for error in approval_errors):
            failures.append("unapproved execution fixture should fail the approval gate")

        session_path.write_text(
            session.replace("Execution approval: not-requested", "Execution approval: approved"),
            encoding="utf-8",
        )
        blueprint = approved_blueprint.replace(
            "Blocking unknowns: none", "Blocking unknowns: U-001"
        )
        blueprint_path.write_text(blueprint, encoding="utf-8")
        blocker_errors = validate_project(root)
        if not any("unaccepted blocking unknowns" in error for error in blocker_errors):
            failures.append("approved Blueprint with unaccepted blocker should fail")

        paused_session = session_path.read_text(encoding="utf-8").replace(
            "Session status: review-ready", "Session status: paused"
        )
        session_path.write_text(paused_session, encoding="utf-8")
        pause_errors = validate_project(root)
        if not any("paused Session must preserve" in error for error in pause_errors):
            failures.append("paused Session without a resume point should fail")

        blueprint_path.write_text(
            blueprint.replace("Blocking unknowns: U-001", "Blocking unknowns: none"),
            encoding="utf-8",
        )
        provisional_session = paused_session.replace(
            "Session status: paused", "Session status: review-ready"
        ).replace(
            "Module selection: codex-recommended-user-confirmed",
            "Module selection: codex-recommended-provisional",
        )
        session_path.write_text(provisional_session, encoding="utf-8")
        provisional_errors = validate_project(root)
        if not any("requires confirmed module selection" in error for error in provisional_errors):
            failures.append("review-ready Session with provisional module should fail")

        session_path.write_text(
            provisional_session.replace(
                "Module selection: codex-recommended-provisional",
                "Module selection: codex-recommended-user-confirmed",
            ).replace("- Next gate: review\n", ""),
            encoding="utf-8",
        )
        spine_errors = validate_project(root)
        if not any("missing bullet field `- Next gate:`" in error for error in spine_errors):
            failures.append("Session with incomplete Decision Spine should fail")

        draft_session = session.replace(
            "Session status: review-ready", "Session status: active"
        ).replace(
            "Module selection: codex-recommended-user-confirmed",
            "Module selection: codex-recommended-provisional",
        ).replace("Blueprint readiness: approved", "Blueprint readiness: draft-ready")
        session_path.write_text(draft_session, encoding="utf-8")
        draft_blueprint = blueprint.replace(
            "Blocking unknowns: U-001", "Blocking unknowns: none"
        ).replace("Blueprint status: approved", "Blueprint status: draft").replace(
            "Module selection: codex-recommended-user-confirmed",
            "Module selection: codex-recommended-provisional",
        ).replace(
            "- Execution approval: approved",
            "- Execution approval: not-requested",
        )
        blueprint_path.write_text(draft_blueprint, encoding="utf-8")
        (root / "tie" / "sessions" / "main" / "execution.md").unlink()
        draft_errors = validate_project(root)
        if draft_errors:
            failures.append("draft fixture with provisional module should pass: " + "; ".join(draft_errors))

        blueprint_path.write_text(
            draft_blueprint.replace("Blueprint status: draft", "Blueprint status: review-ready"),
            encoding="utf-8",
        )
        provisional_blueprint_errors = validate_project(root)
        if not any(
            "Blueprint status requires confirmed module selection" in error
            for error in provisional_blueprint_errors
        ):
            failures.append("review-ready Blueprint with provisional module should fail")

        session_path.write_text(
            approved_session.replace(
                "Canonical reconciliation: complete",
                "Canonical reconciliation: pending",
            ),
            encoding="utf-8",
        )
        blueprint_path.write_text(approved_blueprint, encoding="utf-8")
        reconciliation_errors = validate_project(root)
        if not any(
            "Blueprint readiness requires `Canonical reconciliation: complete`" in error
            for error in reconciliation_errors
        ):
            failures.append("review-ready Session without reconciliation should fail")

        session_path.write_text(approved_session, encoding="utf-8")
        blueprint_path.write_text(
            approved_blueprint.replace(
                "Selected module: presentation",
                "Selected module: research",
            ),
            encoding="utf-8",
        )
        module_mismatch_errors = validate_project(root)
        if not any("does not match session.md" in error for error in module_mismatch_errors):
            failures.append("Blueprint module mismatch should fail")

        blueprint_path.write_text(
            approved_blueprint.replace(
                "- Blueprint status: approved",
                "- Blueprint status: draft",
            ),
            encoding="utf-8",
        )
        review_state_errors = validate_project(root)
        if not any(
            "Review State Blueprint status" in error for error in review_state_errors
        ):
            failures.append("Blueprint Review State status mismatch should fail")

        blueprint_path.write_text(
            approved_blueprint.replace(
                "- Execution approval: approved",
                "- Execution approval: not-requested",
            ),
            encoding="utf-8",
        )
        execution_state_errors = validate_project(root)
        if not any(
            "Review State Execution approval" in error for error in execution_state_errors
        ):
            failures.append("Blueprint execution approval mismatch should fail")

        blueprint_path.write_text(approved_blueprint, encoding="utf-8")
        session_path.write_text(
            approved_session.replace(
                "Session status: review-ready",
                "Session status: active",
            ),
            encoding="utf-8",
        )
        session_status_errors = validate_project(root)
        if session_status_errors:
            failures.append("approved Blueprint may coexist with an active Session: " + "; ".join(session_status_errors))

        session_path.write_text(
            approved_session.replace(
                "- Route changes: none",
                "- Route changes: resolved U-999",
            ),
            encoding="utf-8",
        )
        phantom_unknown_errors = validate_project(root)
        if not any(
            "references undefined `U-999`" in error
            for error in phantom_unknown_errors
        ):
            failures.append("current-facing phantom unknown ID should fail")

        session_path.write_text(approved_session, encoding="utf-8")
        blueprint_path.write_text(
            approved_blueprint.replace(
                "- Critical unknowns accepted by user: not-applicable",
                "- Critical unknowns accepted by user: yes",
            ),
            encoding="utf-8",
        )
        acceptance_errors = validate_project(root)
        if not any(
            "no blocking unknowns requires" in error for error in acceptance_errors
        ):
            failures.append("no-blocker Blueprint with accepted unknowns should fail")

        blueprint_path.write_text(
            approved_blueprint.replace("### Operational Boundaries\nX\n", ""),
            encoding="utf-8",
        )
        boundary_errors = validate_project(root)
        if not any(
            "requires `### Operational Boundaries`" in error
            for error in boundary_errors
        ):
            failures.append("review-ready Blueprint without operational boundaries should fail")

        tie_path = root / "tie" / "TIE.md"
        blueprint_path.write_text(approved_blueprint, encoding="utf-8")
        session_path.write_text(
            approved_session.replace(
                "## Session Boundary\nX",
                "## Session Boundary\n- If paused, resume at: D-001",
            ),
            encoding="utf-8",
        )
        stale_resume_errors = validate_project(root)
        if not any(
            "resume point must name the current review gate" in error
            for error in stale_resume_errors
        ):
            failures.append("review-ready Session with stale Decision resume point should fail")

        session_path.write_text(
            approved_session.replace(
                "### AI Assumptions\nX",
                "### AI Assumptions\n- The module is provisional and still needs confirmation.",
            ),
            encoding="utf-8",
        )
        stale_module_errors = validate_project(root)
        if not any(
            "confirmed module selection conflicts" in error
            for error in stale_module_errors
        ):
            failures.append("confirmed module with provisional assumption should fail")

        session_path.write_text(approved_session, encoding="utf-8")
        tie_path.write_text(
            "# TIE: Demo\nStatus: active\n\n## Intent\nX\n\n## Taste\nX\n\n## Eval\nX\n",
            encoding="utf-8",
        )
        tie_status_errors = validate_project(root)
        if not any(
            "must not store live `Status:`" in error for error in tie_status_errors
        ):
            failures.append("durable TIE with live status should fail")

        tie_path.write_text(
            "# TIE: Demo\n\n## Intent\n- Current stage: draft\n\n"
            "## Taste\nX\n\n## Eval\nX\n",
            encoding="utf-8",
        )
        tie_lifecycle_errors = validate_project(root)
        if not any(
            "contains live lifecycle language" in error
            for error in tie_lifecycle_errors
        ):
            failures.append("durable TIE with live lifecycle language should fail")

        tie_path.write_text(
            "# TIE: Demo\n\n## Intent\nX\n\n## Taste\nX\n\n"
            "## Eval\n- Resolve U-001 next.\n",
            encoding="utf-8",
        )
        tie_id_errors = validate_project(root)
        if not any(
            "must not copy Session IDs" in error
            for error in tie_id_errors
        ):
            failures.append("durable TIE with Session ID should fail")

    return failures


def print_result(errors: list[str], label: str) -> int:
    if errors:
        print(f"FAIL: {label}")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"OK: {label}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--templates", type=Path, help="Template assets directory")
    group.add_argument("--project", type=Path, help="Workspace directory with live TIE artifacts")
    group.add_argument("--self-test", action="store_true", help="Run built-in validator tests")
    args = parser.parse_args()

    if args.templates:
        return print_result(validate_template_set(args.templates.resolve()), "template set")
    if args.project:
        root = args.project.resolve()
        result = print_result(validate_project(root), "project artifacts (structure, not execution authorization)")
        for path in sorted((root / "tie" / "sessions").glob("*/execution.md")):
            if field(path.read_text(encoding="utf-8"), "Execution source") == "stale":
                print(f"NOTE: {path}: retained stale handoff; NOT an execution source")
        return result
    return print_result(self_test(), "validator self-test")


if __name__ == "__main__":
    sys.exit(main())
