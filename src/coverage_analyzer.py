import json
import pandas as pd
import numpy as np
from typing import List, Dict, Any
from pathlib import Path

class CoverageAnalyzer:
    """
    Analyzes and reports on requirement, story, and test case coverage.
    """

    def __init__(self, requirements_path: str, stories_path: str, testcases_path: str):
        self.requirements_path = Path(requirements_path)
        self.stories_path = Path(stories_path)
        self.testcases_path = Path(testcases_path)
        
        self.df_reqs = None
        self.df_stories = None
        self.testcases = None
        self.matrix = None
        self.epic_rollup = None

    def _load_data(self):
        """Loads and initializes data from JSON and CSV files."""
        try:
            with open(self.requirements_path, "r", encoding="utf-8") as f:
                self.df_reqs = pd.DataFrame(json.load(f))
            
            with open(self.stories_path, "r", encoding="utf-8") as f:
                self.df_stories = pd.DataFrame(json.load(f))
            
            self.testcases = pd.read_csv(self.testcases_path)
            print("✔️ Data loaded successfully.")
            
        except FileNotFoundError as e:
            print(f"Error: {e}. Please check file paths.")
            raise

    def _normalize_data(self):
        """Normalizes and prepares dataframes for merging."""
        # Normalize Requirements
        if "epic" not in self.df_reqs.columns:
            self.df_reqs["epic"] = "General"
        self.df_reqs = self.df_reqs.rename(columns={
            "req_id": "Requirement ID",
            "text": "Requirement Text",
            "epic": "Epic (Req)"
        })

        # Normalize Stories
        self.df_stories["Story Id"] = self.df_stories["story_id"]
        # Ensure source_requirement_ids is a list, as explode() expects it
        self.df_stories["source_requirement_ids"] = self.df_stories["source_requirement_ids"].apply(
            lambda x: x if isinstance(x, list) else []
        )
        
        def format_citations(cites: List[Dict[str, Any]]):
            if not cites:
                return ""
            return "; ".join([f"p{c.get('page')}:{c.get('snippet','')[:80]}" for c in cites])
        
        self.df_stories["Citations"] = self.df_stories["citations"].apply(format_citations)

    def _create_coverage_matrix(self):
        """Generates the main coverage matrix."""
        # Explode stories by requirement ID, creating a row for each requirement
        # A more efficient and "pandas-idiomatic" alternative to the manual loop
        df_map = self.df_stories.explode("source_requirement_ids").rename(
            columns={"source_requirement_ids": "Requirement ID"}
        )

        # Test Case Mapping
        print(self.testcases)
        tc_counts = self.testcases.groupby("story_id").size().reset_index(name="Test Case Count")

        # Merge all dataframes
        self.matrix = (
            self.df_reqs
            .merge(df_map, on="Requirement ID", how="left")
            .merge(tc_counts, on="story_id", how="left")
            .fillna({"Test Case Count": 0})
        )
        
        # Use a vectorized approach to classify coverage status
        conditions = [
            (self.matrix["Story Id"].notna()) & (self.matrix["Test Case Count"] > 0),
            (self.matrix["Story Id"].notna()) & (self.matrix["Test Case Count"] == 0),
            (self.matrix["Story Id"].isna()),
        ]
        choices = [
            "✅ Covered",
            "⚠️ No tests",
            "⚠️ No stories"
        ]
        self.matrix["Coverage Status"] = np.select(conditions, choices, default="❌ Missing everything")

    def _create_epic_rollup(self):
        """Calculates epic-level coverage metrics."""
        self.epic_rollup = (
            self.matrix.groupby("Epic (Req)")
            .agg(
                total_reqs=("Requirement ID", "nunique"),
                with_stories=("Story Id", lambda x: x.notna().sum()),
                with_tests=("Test Case Count", lambda x: (x > 0).sum())
            )
            .reset_index()
        )
        self.epic_rollup["% Story Coverage"] = (self.epic_rollup["with_stories"] / self.epic_rollup["total_reqs"] * 100).round(1)
        self.epic_rollup["% Test Coverage"] = (self.epic_rollup["with_tests"] / self.epic_rollup["total_reqs"] * 100).round(1)

    def run_analysis(self, coverage_output: str = "coverage_matrix.csv", epic_output: str = "epic_coverage.csv"):
        """
        Runs the full coverage analysis and saves the reports.
        
        Args:
            coverage_output (str): The filename for the requirement-level coverage matrix.
            epic_output (str): The filename for the epic-level rollup report.
        """
        self._load_data()
        self._normalize_data()
        self._create_coverage_matrix()
        self._create_epic_rollup()

        self.matrix.to_csv(coverage_output, index=False, encoding="utf-8")
        self.epic_rollup.to_csv(epic_output, index=False, encoding="utf-8")

        print(f"✅ Requirement-level coverage: {coverage_output}")
        print(f"✅ Epic-level rollup: {epic_output}")
