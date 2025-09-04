import csv
from pathlib import Path
from typing import List, Dict, Any, Optional

class ToolChainConnector:
    """
    A class to handle exporting stories and scenarios to CSV files
    compatible with Jira and Azure DevOps (ADO) test management tools.
    """

    def _flatten_scenarios(self, stories: List[Dict[str, Any]]):
        """
        Yields rows: {
          requirement_id, story_id, epic, priority, scenario_id,
          given, when, then, tags (space-delimited), pages (semicolon-delimited)
        }
        Each AC (Given/When/Then) becomes ONE scenario row.
        """
        rows = []
        # These helper functions are not defined in the original code,
        # but are needed for the _flatten_scenarios method to work.
        # Placeholder implementations are provided here.
        def _priority_tag(priority: Optional[str]) -> str:
            return priority.lower() if priority else "unassigned"

        def _extract_requirements(story: Dict[str, Any]) -> List[str]:
            return story.get("source_requirement_ids", [])

        def _detect_compliance_tags(story: Dict[str, Any]) -> List[str]:
            return story.get("compliance_tags", [])
        
        def _story_scenarios(story: Dict[str, Any]) -> List[tuple[str, Dict[str, Any]]]:
            # Assuming 'scenarios' is a key in the story dictionary
            return story.get("scenarios", [])

        for s in stories:
            rids = s.get("source_requirement_ids") or ["-"]
            pages = sorted({c.get("page") for c in (s.get("citations") or []) if isinstance(c.get("page"), int)})
            tags = [f"@{_priority_tag(s.get('priority'))}"] + [f"@req_{rid}" for rid in _extract_requirements(s)]
            tags += [f"@{t}" for t in _detect_compliance_tags(s)]

            scenarios = _story_scenarios(s)
            if not scenarios:
                # still emit a row with empty scenario so importers can see the gap
                rows.append({
                    "requirement_id": ";".join(rids),
                    "story_id": s.get("story_id", ""),
                    "epic": s.get("epic", ""),
                    "priority": s.get("priority", ""),
                    "scenario_id": "",
                    "given": "",
                    "when": "",
                    "then": "",
                    "tags": " ".join(tags),
                    "pages": ";".join(map(str, pages)) if pages else "",
                    "user_story": s.get("user_story", ""),
                })
                continue

            for scen_id, ac in scenarios:
                rows.append({
                    "requirement_id": ";".join(rids),
                    "story_id": s.get("story_id", ""),
                    "epic": s.get("epic", ""),
                    "priority": s.get("priority", ""),
                    "scenario_id": scen_id,
                    "given": (ac or {}).get("given", ""),
                    "when": (ac or {}).get("when", ""),
                    "then": (ac or {}).get("then", ""),
                    "tags": " ".join(tags),
                    "pages": ";".join(map(str, pages)) if pages else "",
                    "user_story": s.get("user_story", ""),
                })
        return rows


    def export_to_jira_csv(
        self,
        stories: List[Dict[str, Any]],
        path: str = "jira_testcases.csv",
        project_key: str | None = None,
        default_labels: list[str] | None = None,
        test_type: str = "Manual",
    ):
        """
        Produce a CSV that works well with Jira test plugins (Xray/Zephyr/TM4J) via CSV import.
        """
        default_labels = default_labels or ["auto-generated", "vertex-ai", "traceable"]
        rows = self._flatten_scenarios(stories)

        headers = [
            "Issue Type", "Project Key", "Summary", "Priority", "Labels",
            "Requirement Keys", "Test Type", "Step Action", "Step Data", "Step Result",
            "Description", "Tags", "Pages", "Story Id", "Epic"
        ]

        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(headers)
            for r in rows:
                summary = r["user_story"][:255] if r["user_story"] else (r["scenario_id"] or "Generated Test")
                step_action = " | ".join([x for x in [r["given"], r["when"]] if x])
                step_result = r["then"]
                labels_str = ",".join(default_labels)
                req_keys = r["requirement_id"]

                w.writerow([
                    "Test",
                    project_key or "",
                    summary,
                    r["priority"] or "",
                    labels_str,
                    req_keys,
                    test_type,
                    step_action,
                    "",
                    step_result,
                    r["user_story"],
                    r["tags"],
                    r["pages"],
                    r["story_id"],
                    r["epic"],
                ])

        print(f"🗂️  Wrote Jira-friendly CSV to {path}")
        return Path(path)


    def export_to_ado_csv(
        self,
        stories: List[Dict[str, Any]],
        path: str = "ado_testcases.csv",
        area_path: str | None = None,
        iteration_path: str | None = None,
    ):
        """
        Produce an Azure DevOps Test Plans friendly CSV.
        """
        rows = self._flatten_scenarios(stories)

        headers = [
            "Test Case Title", "Step Action", "Step Expected",
            "Requirement ID", "Priority", "Tags", "Pages",
            "Story Id", "Epic", "Area Path", "Iteration Path"
        ]

        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(headers)
            for r in rows:
                title = r["user_story"][:255] if r["user_story"] else (r["scenario_id"] or "Generated Test")
                step_action = " | ".join([x for x in [r["given"], r["when"]] if x])
                step_expected = r["then"]

                w.writerow([
                    title,
                    step_action,
                    step_expected,
                    r["requirement_id"],
                    r["priority"] or "",
                    r["tags"],
                    r["pages"],
                    r["story_id"],
                    r["epic"],
                    area_path or "",
                    iteration_path or "",
                ])

        print(f"🗂️  Wrote ADO-friendly CSV to {path}")
        return Path(path)