# layer3_test_generator.py
# ========================== Layer-3: Test Generation ==========================
# Generates:
#   - Gherkin .feature files (1 Scenario per AC) with tags: @priority_*, @req_*, @HIPAA...
#   - Step-definition stubs (pytest-bdd or behave) with E2E placeholders
#   - RTM coverage CSV (requirements ↔ stories ↔ scenarios)

from __future__ import annotations

import re
import csv
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Any, Tuple

_SAFE = re.compile(r"[^A-Za-z0-9._-]+")

def _safe_name(s: str, default: str = "item") -> str:
    s = (s or "").strip()
    if not s:
        return default
    s = re.sub(_SAFE, "_", s)
    return s[:80] or default  # keep filenames short-ish

def _ensure_dir(path: str | Path):
    Path(path).mkdir(parents=True, exist_ok=True)

class TestCaseGenerator:
    """Encapsulates generation of Gherkin features, step stubs, and RTM."""

    # ------------------------ helpers ------------------------
    @staticmethod
    def _detect_compliance_tags(story: Dict[str, Any]) -> List[str]:
        """Return compliance tags like HIPAA, FDA21CFR11, ISO13485, IEC62304, ISO27001."""
        tags = set()
        text_blobs = []
        for nfr in (story.get("non_functional") or []):
            text_blobs.append(nfr or "")
        for c in (story.get("citations") or []):
            text_blobs.append((c or {}).get("snippet", "") or "")
        blob = " ".join(text_blobs).lower()
        if "hipaa" in blob:
            tags.add("HIPAA")
        if any(k in blob for k in ["21 cfr part 11", "fda 21 cfr part 11", "21cfr part 11"]):
            tags.add("FDA21CFR11")
        if "iso 13485" in blob:
            tags.add("ISO13485")
        if "iec 62304" in blob:
            tags.add("IEC62304")
        if "iso 27001" in blob:
            tags.add("ISO27001")
        return sorted(tags)

    @staticmethod
    def _story_scenarios(story: Dict[str, Any]) -> List[Tuple[str, Dict[str, str]]]:
        """Return [(scenario_id, ac_dict), ...] where ac_dict has given/when/then."""
        out: List[Tuple[str, Dict[str, str]]] = []
        acs = story.get("acceptance_criteria") or []
        for idx, ac in enumerate(acs, 1):
            sid = f"{story.get('story_id','S')}_AC{idx}"
            out.append((sid, ac))
        return out

    @staticmethod
    def _extract_requirements(story: Dict[str, Any]) -> List[str]:
        r = story.get("source_requirement_ids") or []
        return [re.sub(_SAFE, "_", str(x))[:80] for x in r if x]

    @staticmethod
    def _priority_tag(priority: str | None) -> str:
        p = (priority or "").strip() or "Unspecified"
        p = re.sub(r"\s+", "", p)
        return f"priority_{p}"

    # ------------------------ feature files ------------------------
    def export_gherkin_features(
        self,
        stories: List[Dict[str, Any]],
        out_dir: str = "features",
        feature_per_epic: bool = True,
    ) -> List[Path]:
        """
        Write .feature files from stories.
        - Group by 'epic' (default) OR one file per story if feature_per_epic=False
        - One Scenario per AC
        - Tags: @priority_*, @req_REQ-123, @HIPAA, @FDA21CFR11, ...
        """
        _ensure_dir(out_dir)

        groups: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        if feature_per_epic:
            for s in stories:
                key = s.get("epic") or "General"
                groups[key].append(s)
        else:
            for s in stories:
                key = s.get("story_id") or "Story"
                groups[key].append(s)

        files: List[Path] = []
        for group_key, group_stories in groups.items():
            fname = _safe_name(group_key or "feature")
            path = Path(out_dir) / f"{fname}.feature"

            with open(path, "w", encoding="utf-8") as f:
                f.write(f"Feature: {group_key or 'User Stories'}\n\n")
                for s in group_stories:
                    # Comment with the story text (nice for humans)
                    f.write(f"  # {s.get('user_story','')}\n")

                    # Build base tags
                    tags = [f"@{self._priority_tag(s.get('priority'))}"]
                    # Requirement tags
                    for rid in self._extract_requirements(s):
                        tags.append(f"@req_{rid}")
                    # Compliance tags
                    for t in self._detect_compliance_tags(s):
                        tags.append(f"@{t}")

                    # Emit Scenarios (one per AC)
                    for scenario_id, ac in self._story_scenarios(s):
                        f.write("  " + " ".join(tags) + "\n")
                        scen_title = _safe_name(scenario_id, "Scenario")
                        f.write(f"  Scenario: {scen_title}\n")
                        f.write(f"    Given {ac.get('given','<given TBD>')}\n")
                        f.write(f"    When {ac.get('when','<when TBD>')}\n")
                        f.write(f"    Then {ac.get('then','<then TBD>')}\n\n")

            files.append(path)

        print(f"🧪 Wrote {len(files)} Gherkin feature file(s) to {out_dir}")
        return files

    # ------------------------ step stubs ------------------------
    _PYTEST_BDD_TEMPLATE = """# Auto-generated pytest-bdd step definitions.
# Run: pytest -k feature
import pytest
from pytest_bdd import given, when, then, scenarios

# Link feature(s)
scenarios("{feature_glob}")

# Example shared test data (E2E placeholders)
TEST_CONTEXT = {{
    "patient_id": "PAT-001",
    "session_id": "SES-001",
    "clinician_id": "DOC-123",
}}

@given("{given_text}")
def step_given():
    # TODO: implement setup for: {given_text}
    # e.g., create patient in DB using TEST_CONTEXT["patient_id"]
    pass

@when("{when_text}")
def step_when():
    # TODO: implement action for: {when_text}
    # e.g., call API to sign in/out, upload document, etc.
    pass

@then("{then_text}")
def step_then():
    # TODO: implement assertion for: {then_text}
    # e.g., assert response.status_code == 200 or record exists in DB
    pass
"""

    _BEHAVE_TEMPLATE = """# Auto-generated behave step definitions.
# Run: behave -i {feature_glob}
from behave import given, when, then

# Example shared test data (E2E placeholders)
TEST_CONTEXT = {{
    "patient_id": "PAT-001",
    "session_id": "SES-001",
    "clinician_id": "DOC-123",
}}

@given('{given_text}')
def step_impl_given(context):
    # TODO: implement setup for: {given_text}
    pass

@when('{when_text}')
def step_impl_when(context):
    # TODO: implement action for: {when_text}
    pass

@then('{then_text}')
def step_impl_then(context):
    # TODO: implement assertion for: {then_text}
    pass
"""

    def export_step_stubs(
        self,
        stories: List[Dict[str, Any]],
        out_dir: str = "steps",
        framework: str = "pytest-bdd",  # or "behave"
        feature_glob: str = "features/*.feature",
    ) -> Path:
        """Produce a single step file with example stubs and E2E placeholders."""
        _ensure_dir(out_dir)

        # Pick first non-empty AC as examples
        given_text = when_text = then_text = "TBD"
        for s in stories:
            for _, ac in self._story_scenarios(s):
                given_text = ac.get("given") or "a precondition"
                when_text  = ac.get("when")  or "an action occurs"
                then_text  = ac.get("then")  or "an expected result"
                break
            if given_text != "TBD":
                break

        if framework.lower() == "behave":
            body = self._BEHAVE_TEMPLATE.format(
                feature_glob=feature_glob,
                given_text=given_text.replace('"', '\\"'),
                when_text=when_text.replace('"', '\\"'),
                then_text=then_text.replace('"', '\\"'),
            )
            path = Path(out_dir) / "steps_behave.py"
        else:
            body = self._PYTEST_BDD_TEMPLATE.format(
                feature_glob=feature_glob,
                given_text=given_text,
                when_text=when_text,
                then_text=then_text,
            )
            path = Path(out_dir) / "test_steps_bdd.py"

        with open(path, "w", encoding="utf-8") as f:
            f.write(body)

        print(f"🧩 Wrote step stubs for {framework} to {path}")
        return path

    # ------------------------ RTM / coverage ------------------------
    def _build_rtm_rows(self, stories: List[Dict[str, Any]]) -> List[List[str]]:
        """Rows: requirement_id, story_id, epic, priority, scenario_id, tags, pages"""
        rows: List[List[str]] = []
        for s in stories:
            pages = sorted({c.get("page") for c in (s.get("citations") or []) if isinstance(c.get("page"), int)})
            tags = [f"@{self._priority_tag(s.get('priority'))}"] + [f"@req_{rid}" for rid in self._extract_requirements(s)]
            tags += [f"@{t}" for t in self._detect_compliance_tags(s)]

            scenarios = self._story_scenarios(s)
            if scenarios:
                for scen_id, _ in scenarios:
                    rows.append([
                        ";".join(s.get("source_requirement_ids") or ["-"]),
                        s.get("story_id", ""),
                        s.get("epic", ""),
                        s.get("priority", ""),
                        scen_id,
                        " ".join(tags),
                        ";".join(map(str, pages)) if pages else "",
                    ])
            else:
                rows.append([
                    ";".join(s.get("source_requirement_ids") or ["-"]),
                    s.get("story_id", ""),
                    s.get("epic", ""),
                    s.get("priority", ""),
                    "",  # no scenario
                    " ".join(tags),
                    ";".join(map(str, pages)) if pages else "",
                ])
        return rows

    def export_traceability_csv(self, stories: List[Dict[str, Any]], path: str = "traceability.csv") -> Path:
        rows = self._build_rtm_rows(stories)
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["requirement_id", "story_id", "epic", "priority", "scenario_id", "tags", "pages"])
            w.writerows(rows)
        print(f"📊 Wrote RTM to {path} ({len(rows)} rows)")
        return Path(path)

    def flag_requirements_with_no_scenarios(self, stories: List[Dict[str, Any]]) -> List[str]:
        """Return list of requirement IDs that do not map to any Scenario."""
        req_to_scen: Dict[str, int] = defaultdict(int)
        for s in stories:
            rids = s.get("source_requirement_ids") or ["-"]
            scen_count = len(self._story_scenarios(s))
            for rid in rids:
                req_to_scen[rid] += scen_count
        return sorted([rid for rid, n in req_to_scen.items() if n == 0])

    # ------------------------ Orchestrator ------------------------
    def generate(
        self,
        stories: List[Dict[str, Any]],
        feature_dir: str = "features",
        steps_dir: str = "steps",
        framework: str = "pytest-bdd",   # or "behave"
        feature_per_epic: bool = True,
        traceability_csv: str = "traceability.csv",
    ) -> Dict[str, Any]:
        """One-call orchestrator for Layer-3 outputs."""
        feature_files = self.export_gherkin_features(
            stories, out_dir=feature_dir, feature_per_epic=feature_per_epic
        )
        step_file = self.export_step_stubs(
            stories, out_dir=steps_dir, framework=framework, feature_glob=f"{feature_dir}/*.feature"
        )
        rtm_file = self.export_traceability_csv(stories, path=traceability_csv)
        gaps = self.flag_requirements_with_no_scenarios(stories)

        if gaps:
            print(f"⚠️ Requirements with 0 scenarios: {gaps}")
        else:
            print("✅ All requirements have at least one scenario.")

        return {
            "feature_files": [str(p) for p in feature_files],
            "step_file": str(step_file),
            "rtm_csv": str(rtm_file),
            "gaps": gaps,
        }

# --------------------- Backward-compatible function ---------------------
def generate_tests_from_stories(
    stories: List[Dict[str, Any]],
    feature_dir: str = "features",
    steps_dir: str = "steps",
    framework: str = "pytest-bdd",     # or "behave"
    feature_per_epic: bool = True,
    traceability_csv: str = "traceability.csv",
) -> Dict[str, Any]:
    """Thin wrapper to keep your previous call site working."""
    return Layer3TestGenerator().generate(
        stories=stories,
        feature_dir=feature_dir,
        steps_dir=steps_dir,
        framework=framework,
        feature_per_epic=feature_per_epic,
        traceability_csv=traceability_csv,
    )

# ======================== End Layer-3: Test Generation ========================
