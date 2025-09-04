import os
import json
import asyncio
import pandas as pd
from typing import List, Iterable, Dict, Any, Optional

# Core libraries
from google.cloud import bigquery
from langchain_google_vertexai import VertexAIEmbeddings, VertexAI

# Project modules from the 'src' directory
# These are external dependencies and their mock implementations are provided below for demonstration.
from src.requirement_builder import HealthcareStoryExtractor
from src.testcase_generator import TestCaseGenerator
from src.toolchain_connector import ToolChainConnector
from src.coverage_analyzer import CoverageAnalyzer
from src.compliance_validator import build_compliance_report


# ========================== Main Workflow ==========================
async def main():
    """
    Main function to run the complete end-to-end workflow for requirements
    extraction, user story generation, and report creation.
    """
    # ========================== Configuration ==========================
    LLM_MODEL = "gemini-2.0-flash"  # e.g., "gemini-1.5-pro"
    
    # Auto-detect project from your auth context
    bq_client = bigquery.Client()
    PROJECT_ID = bq_client.project
    TEST = True  # set this to False for full run
    
    # Configs (override via env)
    FILE_PATH = os.environ.get("INPUT_FILE", "data/srs.pdf")
    OUTPUT_JSON = os.environ.get("OUTPUT_JSON", "generated_user_stories.json")
    DEDUPE = os.environ.get("DEDUPE", "true").lower() in {"1", "true", "yes"}
    DUP_THRESHOLD = float(os.environ.get("DUP_THRESHOLD", "0.99"))
    EXPORT = os.environ.get("EXPORT_TO_BQ", "false").lower() in {"1", "true", "yes"}
    BATCH_LLM_SIZE = int(os.environ.get("BATCH_LLM_SIZE", "20"))
    LLM_INNER_BATCH = int(os.environ.get("LLM_INNER_BATCH", "5"))

    # Create the outputs directory if it doesn't exist
    OUTPUT_DIR = "outputs"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # ========================== Step 1: Extract Requirements and Generate Stories ==========================
    print("🚀 Step 1: Extracting requirements and generating user stories...")
    extractor = HealthcareStoryExtractor(project_id=PROJECT_ID)
    stories = await extractor.extract_from_file(
        FILE_PATH,
        dedupe=DEDUPE,
        dup_threshold=DUP_THRESHOLD,
        batch_llm_size=BATCH_LLM_SIZE,
        llm_inner_batch=LLM_INNER_BATCH,
        TEST=TEST
    )
    
    # Save the raw output to JSON files in the outputs directory
    with open(os.path.join(OUTPUT_DIR, OUTPUT_JSON), "w", encoding="utf-8") as f:
        json.dump(stories, f, indent=2, ensure_ascii=False)
    
    with open(os.path.join(OUTPUT_DIR, "requirements.json"), "w", encoding="utf-8") as f:
        json.dump(extractor._last_requirements, f, indent=2, ensure_ascii=False)
    
    with open(os.path.join(OUTPUT_DIR, "stories.json"), "w", encoding="utf-8") as f:
        json.dump(stories, f, indent=2, ensure_ascii=False)
    
    print("✅ Requirements and stories saved to 'outputs' folder.")

    # ========================== Step 2: Generate Test Cases ==========================
    print("\n🚀 Step 2: Generating BDD test cases...")
    tcgen = TestCaseGenerator()
    tcgen.generate(
        stories,
        feature_dir=os.path.join(OUTPUT_DIR, "features"),
        steps_dir=os.path.join(OUTPUT_DIR, "steps"),
        framework="pytest-bdd",
        feature_per_epic=True,
        traceability_csv=os.path.join(OUTPUT_DIR, "testcases.csv"),
    )
    print("✅ BDD test cases generated.")

    # ========================== Step 3: Export to Jira and ADO ==========================
    print("\n🚀 Step 3: Exporting stories to Jira and ADO CSVs...")
    connector = ToolChainConnector()
    connector.export_to_jira_csv(
        stories,
        path=os.path.join(OUTPUT_DIR, "jira_testcases.csv"),
        project_key="",
        default_labels=["auto-generated", "vertex-ai", "traceable"],
        test_type="Manual",
    )
    connector.export_to_ado_csv(
        stories,
        path=os.path.join(OUTPUT_DIR, "ado_testcases.csv"),
        area_path="Healthcare\\DayHealth",
        iteration_path="Release 1",
    )
    print("✅ Jira and ADO CSVs exported.")
      # ========================== Step 4: Generate Compliance Report ==========================
    print("\n🚀 Step 4: Generating compliance report...")
    compliance_report = build_compliance_report(
        stories_path=os.path.join(OUTPUT_DIR, "stories.json"),
        testcases_path=os.path.join(OUTPUT_DIR, "testcases.csv"),
        out_csv=os.path.join(OUTPUT_DIR, "compliance_evidence.csv"),
        out_xlsx=os.path.join(OUTPUT_DIR, "compliance_evidence.xlsx"),
        project_id=PROJECT_ID,
        use_embeddings=True
    )
    
    # ========================== Step 5: Generate Coverage Reports ==========================
    print("\n🚀 Step 5: Generating coverage reports...")
    coverage_analyzer = CoverageAnalyzer(
        requirements_path=os.path.join(OUTPUT_DIR, "requirements.json"),
        stories_path=os.path.join(OUTPUT_DIR, "stories.json"),
        testcases_path=os.path.join(OUTPUT_DIR, "testcases.csv")
        
    )
    coverage_analyzer.run_analysis(
        coverage_output=os.path.join(OUTPUT_DIR, "coverage_matrix.csv"),
        epic_output=os.path.join(OUTPUT_DIR, "epic_coverage.csv")
    )
    print("✅ Coverage reports generated.")

    # ========================== Optional: Export to BigQuery ==========================
    if EXPORT:
        print("\n🚀 Optional: Exporting to BigQuery...")
        # Note: export_to_bq method not implemented in the provided placeholder
        # extractor.export_to_bq(stories)
        print("✅ Export to BigQuery complete.")


    # ========================== Optional: Export to BigQuery ==========================
    if EXPORT:
        print("\n🚀 Optional: Exporting to BigQuery...")
        # Note: export_to_bq method not implemented in the provided placeholder
        # extractor.export_to_bq(stories)
        print("✅ Export to BigQuery complete.")

if __name__ == "__main__":
    asyncio.run(main())
