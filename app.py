# app.py – MedTest AI (Streamlit UI)

import os
import json
import asyncio
import pandas as pd
import streamlit as st
from pathlib import Path
from collections import defaultdict

from google.cloud import bigquery
from src.requirement_builder import HealthcareStoryExtractor
from src.testcase_generator import TestCaseGenerator
from src.coverage_analyzer import CoverageAnalyzer
from src.compliance_validator import build_compliance_report

# -------------------- Setup --------------------
OUTPUT_DIR = Path("outputs")
FEATURE_DIR = OUTPUT_DIR / "features"
STEPS_DIR = OUTPUT_DIR / "steps"
for p in [OUTPUT_DIR, FEATURE_DIR, STEPS_DIR]:
    p.mkdir(parents=True, exist_ok=True)

# -------------------- Helpers --------------------
async def run_extraction(file_path, dedupe, dup_threshold, batch_size, inner_batch, test_mode):
    bq_client = bigquery.Client()
    extractor = HealthcareStoryExtractor(project_id=bq_client.project)
    stories = await extractor.extract_from_file(
        file_path,
        dedupe=dedupe,
        dup_threshold=dup_threshold,
        batch_llm_size=batch_size,
        llm_inner_batch=inner_batch,
        TEST=test_mode
    )
    (OUTPUT_DIR / "requirements.json").write_text(
        json.dumps(extractor._last_requirements, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    (OUTPUT_DIR / "stories.json").write_text(
        json.dumps(stories, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    return extractor._last_requirements, stories

def _normalize_to_testcases_csv(traceability_csv_path: Path, out_path: Path) -> pd.DataFrame:
    cols = ["Test Case Title","Step Action","Step Expected","Requirement ID","Priority",
            "Tags","Pages","Story Id","Epic","Area Path","Iteration Path"]
    if not traceability_csv_path.exists():
        # also return alias column so compliance doesn't break
        return pd.DataFrame(columns=cols + ["story_id"])

    df = pd.read_csv(traceability_csv_path)
    def _has(c): return c in df.columns

    df_out = pd.DataFrame()
    df_out["Test Case Title"] = df["scenario_id"] if _has("scenario_id") else ""
    df_out["Step Action"]      = ""
    df_out["Step Expected"]    = ""
    df_out["Requirement ID"]   = df["requirement_id"] if _has("requirement_id") else ""
    df_out["Priority"]         = df["priority"] if _has("priority") else ""
    df_out["Tags"]             = df["tags"] if _has("tags") else ""
    df_out["Pages"]            = df["pages"] if _has("pages") else ""
    df_out["Story Id"]         = df["story_id"] if _has("story_id") else ""
    df_out["Epic"]             = df["epic"] if _has("epic") else ""
    df_out["Area Path"]        = ""
    df_out["Iteration Path"]   = ""

    # ✅ Add lowercase alias for compliance code
    df_out["story_id"] = df_out["Story Id"]

    df_out.to_csv(out_path, index=False, encoding="utf-8")
    return df_out

def run_testcase_generation(stories):
    tcgen = TestCaseGenerator()
    traceability_path = OUTPUT_DIR / "traceability.csv"
    tcgen.generate(
        stories,
        feature_dir=str(FEATURE_DIR),
        steps_dir=str(STEPS_DIR),
        framework="pytest-bdd",
        feature_per_epic=True,
        traceability_csv=str(traceability_path),
    )
    df_trace = pd.read_csv(traceability_path) if traceability_path.exists() else pd.DataFrame()
    df_tests = _normalize_to_testcases_csv(traceability_path, OUTPUT_DIR / "testcases.csv")
    return df_trace, df_tests

def run_compliance(stories_file: Path, testcases_file: Path):
    return build_compliance_report(
        stories_path=str(stories_file),
        testcases_path=str(testcases_file),
        out_csv=str(OUTPUT_DIR / "compliance_evidence.csv"),
        out_xlsx=str(OUTPUT_DIR / "compliance_evidence.xlsx"),
        project_id=bigquery.Client().project,
        use_embeddings=True
    )

def run_coverage():
    analyzer = CoverageAnalyzer(
        requirements_path=str(OUTPUT_DIR / "requirements.json"),
        stories_path=str(OUTPUT_DIR / "stories.json"),
        testcases_path=str(OUTPUT_DIR / "testcases.csv")
    )
    analyzer.run_analysis(
        coverage_output=str(OUTPUT_DIR / "coverage_matrix.csv"),
        epic_output=str(OUTPUT_DIR / "epic_coverage.csv")
    )
    return (
        pd.read_csv(OUTPUT_DIR / "coverage_matrix.csv"),
        pd.read_csv(OUTPUT_DIR / "epic_coverage.csv")
    )

def show_features_by_epic(stories: list):
    groups = defaultdict(list)
    for s in stories or []:
        groups[s.get("epic") or "General"].append(s)
    for epic, group_stories in sorted(groups.items()):
        with st.expander(f"📌 Epic: {epic}", expanded=False):
            st.markdown(f"#### Feature: {epic}")
            for s in group_stories:
                sid = s.get("story_id", "")
                user_story = s.get("user_story", "")
                priority = (s.get("priority") or "Unspecified").replace(" ", "")
                req_tags = [f"@req_{rid}" for rid in (s.get("source_requirement_ids") or [])]
                st.markdown(f"**{sid}** — {user_story}")
                st.caption(" ".join([f"@priority_{priority}", *req_tags]))
                acs = s.get("acceptance_criteria") or []
                if not acs:
                    st.info("No acceptance criteria found.")
                for i, ac in enumerate(acs, 1):
                    scen_id = f"{sid or 'S'}_AC{i}"
                    st.markdown(f"*Scenario {i}:* `{scen_id}`")
                    st.code(
                        f"Given {ac.get('given','<given TBD>')}\n"
                        f"When {ac.get('when','<when TBD>')}\n"
                        f"Then {ac.get('then','<then TBD>')}",
                        language="gherkin"
                    )

TEST=True


# -------------------- UI Theming --------------------
st.set_page_config(page_title="MedTest AI", layout="wide")

st.markdown("""
<style>
section[data-testid="stSidebar"] {
  background-color: #0e2a3f;
}
section[data-testid="stSidebar"] * { color: #fff; }
.sidebar-title { font-size: 1.2rem; font-weight: 700; margin-bottom: 1rem; }
# .card {
#   background: #fff; border: 1px solid #e9eef3; border-radius: 12px;
#   padding: 1.5rem; margin-bottom: 1.5rem;
#   box-shadow: 0 2px 5px rgba(0,0,0,.05);
# }
</style>
""", unsafe_allow_html=True)
# -------------------- Sidebar Navigation --------------------
PAGE_DEFS = [
    {"label": "Upload Documents",        "icon": "<svg width='14' height='14' viewBox='0 0 16 16'><path fill='currentColor' d='M.5 3a2 2 0 0 1 2-2h7.293a1 1 0 0 1 .707.293l3.207 3.207A1 1 0 0 1 14 5.207V13a2 2 0 0 1-2 2H2.5a2 2 0 0 1-2-2V3z'/></svg>"},
    {"label": "Requirements",            "icon": "<svg width='14' height='14' viewBox='0 0 16 16'><path fill='currentColor' d='M14 4.5V14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2h6.5L14 4.5z'/></svg>"},
    {"label": "Test Cases",              "icon": "<svg width='14' height='14' viewBox='0 0 16 16'><path fill='currentColor' d='M2 2h12v12H2V2zm3 2v8h1V4H5zm3 0v8h1V4H8zm3 0v8h1V4h-1z'/></svg>"},
    {"label": "Compliance & Coverage",   "icon": "<svg width='14' height='14' viewBox='0 0 16 16'><path fill='currentColor' d='M2 2h12v12H2V2zm3 5l2 2 4-4'/></svg>"},
    {"label": "Reports",                 "icon": "<svg width='14' height='14' viewBox='0 0 16 16'><path fill='currentColor' d='M3 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1H3z'/><path fill='currentColor' d='M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6z'/></svg>"},
]
PAGE_LABELS = [p["label"] for p in PAGE_DEFS]

# init current page label in session state
if "page" not in st.session_state:
    st.session_state["page"] = PAGE_LABELS[0]

def goto(page_label: str):
    st.session_state["page"] = page_label
    # st.rerun()

def _page_idx() -> int:
    # use PAGE_LABELS (strings), not PAGE_DEFS (dicts)
    return PAGE_LABELS.index(st.session_state["page"])

def _go_prev():
    i = _page_idx()
    if i > 0:
        st.session_state["page"] = PAGE_LABELS[i - 1]

def _go_next():
    i = _page_idx()
    if i < len(PAGE_LABELS) - 1:
        st.session_state["page"] = PAGE_LABELS[i + 1]


def nav_row(next_disabled: bool = False):
    i = _page_idx()
    col_prev, col_sp, col_next = st.columns([1, 6, 1])
    with col_prev:
        st.button("Back", disabled=(i == 0), on_click=_go_prev)
    with col_next:
        st.button("Next", disabled=(i == len(PAGE_LABELS) - 1 or next_disabled), on_click=_go_next)

# ----- Sidebar product header (only on first page) -----
if st.session_state.get("page") == PAGE_LABELS[0]:
    st.sidebar.markdown("""
    <div style="display:flex;align-items:center;gap:10px;margin:6px 0 16px 0;">
      <div style="width:24px;height:24px;color:#ffffff;">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
          <path d="M7 2h10a2 2 0 0 1 2 2v3h-2V4H7v16h10v-3h2v3a2 2 0 0 1-2 2H7a2
                   2 0 0 1-2-2V4a2 2 0 0 1 2-2z"/>
          <path d="M18 8h-6v2h6v2l4-3-4-3v2z"/>
        </svg>
      </div>
      <div>
        <div style="font-size:1.1rem;font-weight:800;line-height:1;color:#ffffff;">MedTest AI</div>
        <div style="font-size:.80rem;opacity:.85;color:#dfe8ef;">Automated Test Case Generation &amp; Compliance for Medical Software</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# actual selection uses plain labels to avoid HTML/selection mismatch
choice_label = st.sidebar.radio(
    "Navigation",
    PAGE_LABELS,
    index=PAGE_LABELS.index(st.session_state["page"]),
    label_visibility="collapsed"
)

# sync session state if user changes radio
if choice_label != st.session_state["page"]:
    st.session_state["page"] = choice_label



# -------------------- Pages --------------------
if choice_label == "Upload Documents":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Upload Requirement Documents")

    uploaded_file = st.file_uploader("Upload SRS (PDF)", type=["pdf"])
    if uploaded_file:
        tmp_path = OUTPUT_DIR / "uploaded.pdf"
        tmp_path.write_bytes(uploaded_file.read())
        st.success(f"Uploaded: {uploaded_file.name}")

    # Back/Next controls (Next enabled only when file saved)
    next_disabled = not (OUTPUT_DIR / "uploaded.pdf").exists()
    nav_row(next_disabled=next_disabled)

    st.markdown('</div>', unsafe_allow_html=True)

elif choice_label == "Requirements":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Requirements Extraction")

    # --- CONFIG FORM (tidy UI) ---
    with st.form("extract_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            test_mode = st.toggle("Test Mode (use cached outputs if available)", value=True)
            dedupe = st.checkbox("Deduplicate stories", value=True)
            dup_threshold = st.slider("Duplicate Threshold", 0.8, 1.0, 0.99)
        with col2:
            batch_size = st.number_input("Batch LLM Size", 1, 50, 20)
            inner_batch = st.number_input("Inner Batch", 1, 20, 5)

        submitted = st.form_submit_button("Run Extraction", use_container_width=True)

    stories = None
    reqs = None

    if submitted:
        uploaded_pdf = OUTPUT_DIR / "uploaded.pdf"
        if not uploaded_pdf.exists():
            st.warning("Please upload a PDF first on the Upload page.")
        else:
            if test_mode:
                # --- LOCAL TEST MODE: read from saved outputs if present ---
                stories_file = OUTPUT_DIR / "stories.json"
                reqs_file = OUTPUT_DIR / "requirements.json"
                if stories_file.exists() and reqs_file.exists():
                    with open(stories_file, "r", encoding="utf-8") as f:
                        stories = json.load(f)
                    with open(reqs_file, "r", encoding="utf-8") as f:
                        reqs = json.load(f)
                else:
                    st.info("Test Mode is ON but no cached outputs found. Running live extraction instead…")
                    with st.spinner("Extracting..."):
                        reqs, stories = asyncio.run(
                            run_extraction(
                                str(uploaded_pdf),
                                dedupe, dup_threshold, batch_size, inner_batch, test_mode
                            )
                        )
            else:
                # --- LIVE EXTRACTION ---
                with st.spinner("Extracting..."):
                    reqs, stories = asyncio.run(
                        run_extraction(
                            str(uploaded_pdf),
                            dedupe, dup_threshold, batch_size, inner_batch, test_mode
                        )
                    )

            if stories is None:
                st.error("No stories were produced.")
            else:
                # Persist to session so tabs render even after reruns
                st.session_state["stories"] = stories
                st.session_state["reqs"] = reqs

                # KPIs
                df_stories_tmp = pd.DataFrame(stories)
                total_stories = len(df_stories_tmp)
                unique_epics = df_stories_tmp["epic"].nunique() if "epic" in df_stories_tmp else 0
                priorities = (
                    df_stories_tmp["priority"].value_counts().to_dict()
                    if "priority" in df_stories_tmp else {}
                )

                st.success("Requirements and Stories generated")

                k1, k2, k3 = st.columns(3)
                k1.metric("Stories", total_stories)
                k2.metric("Epics", unique_epics)
                k3.metric("Unique Priorities", len(priorities))

    # ----- RESULTS AREA (if we have something to show) -----
    stories = st.session_state.get("stories")
    reqs = st.session_state.get("reqs")

    if stories:
        tabs = st.tabs(["Stories Preview", "Features by Epic", "Downloads"])
        with tabs[0]:
            df_stories = pd.DataFrame(stories)
            preview_cols = [c for c in ["story_id", "user_story", "priority", "epic", "source_requirement_ids"] if c in df_stories.columns]
            if not df_stories.empty and preview_cols:
                st.dataframe(df_stories[preview_cols], use_container_width=True, height=380)
            else:
                st.info("No previewable columns found.")

        with tabs[1]:
            show_features_by_epic(stories)

        with tabs[2]:
            c1, c2 = st.columns(2)
            with c1:
                st.download_button(
                    "Download stories.json",
                    data=json.dumps(stories, indent=2).encode("utf-8"),
                    file_name="stories.json",
                    mime="application/json",
                    use_container_width=True
                )
            with c2:
                st.download_button(
                    "Download requirements.json",
                    data=json.dumps(reqs or {}, indent=2).encode("utf-8"),
                    file_name="requirements.json",
                    mime="application/json",
                    use_container_width=True
                )

    # Back/Next controls (Next enabled only if stories.json exists)
    next_disabled = not (OUTPUT_DIR / "stories.json").exists()
    nav_row(next_disabled=next_disabled)

    st.markdown('</div>', unsafe_allow_html=True)
elif choice_label == "Test Cases":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Generate Test Cases")

    stories_path = OUTPUT_DIR / "stories.json"
    if not stories_path.exists():
        st.info("Run extraction first on the Requirements page.")
    else:
        stories = json.loads(stories_path.read_text(encoding="utf-8"))

        # Action row
        with st.form("generate_tests_form", clear_on_submit=False):
            st.markdown("Configure and generate test artifacts.")
            submitted = st.form_submit_button("Generate Test Cases", use_container_width=True)

        if submitted:
            with st.spinner("Generating feature files, step stubs, and test case CSVs..."):
                df_trace, df_tests = run_testcase_generation(stories)

            st.success("Test artifacts generated")

            # KPIs
            feature_count = len(list(FEATURE_DIR.glob("*.feature")))
            total_rows = len(df_trace) if not df_trace.empty else 0
            unique_stories = df_trace["story_id"].nunique() if "story_id" in df_trace.columns else (
                df_trace["Story Id"].nunique() if "Story Id" in df_trace.columns else 0
            )
            unique_requirements = 0
            if "requirement_id" in df_trace.columns:
                req_series = df_trace["requirement_id"].astype(str).str.split(";")
                unique_requirements = len(set(sum(req_series.tolist(), [])))

            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Feature Files", feature_count)
            k2.metric("Traceability Rows", total_rows)
            k3.metric("Stories Covered", unique_stories)
            k4.metric("Requirements Referenced", unique_requirements)

            # Results tabs
            tab1, tab2, tab3 = st.tabs(["Traceability", "Test Cases (normalized)", "Downloads"])
            with tab1:
                if df_trace.empty:
                    st.info("No traceability rows to display.")
                else:
                    st.dataframe(df_trace, use_container_width=True, height=360)

            with tab2:
                if df_tests.empty:
                    st.info("No test cases to display.")
                else:
                    st.dataframe(df_tests, use_container_width=True, height=360)

            with tab3:
                c1, c2 = st.columns(2)
                with c1:
                    st.download_button(
                        "Download traceability.csv",
                        df_trace.to_csv(index=False).encode("utf-8"),
                        "traceability.csv",
                        "text/csv",
                        use_container_width=True
                    )
                with c2:
                    st.download_button(
                        "Download testcases.csv",
                        df_tests.to_csv(index=False).encode("utf-8"),
                        "testcases.csv",
                        "text/csv",
                        use_container_width=True
                    )

    # Back/Next controls (Next enabled only if testcases.csv exists)
    next_disabled = not (OUTPUT_DIR / "testcases.csv").exists()
    nav_row(next_disabled=next_disabled)

    st.markdown('</div>', unsafe_allow_html=True)
elif choice_label == "Compliance & Coverage":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Compliance & Coverage")

    stories_path = OUTPUT_DIR / "stories.json"
    testcases_path = OUTPUT_DIR / "testcases.csv"
    ran = False

    if stories_path.exists() and testcases_path.exists():
        with st.form("compliance_coverage_form", clear_on_submit=False):
            st.markdown("Run compliance evidence generation and coverage analysis.")
            submitted = st.form_submit_button("Run Compliance & Coverage", use_container_width=True)

        if submitted:
            with st.spinner("Running compliance and coverage analysis..."):
                run_compliance(stories_path, testcases_path)
                df_cov, df_epic = run_coverage()
            st.success("Analysis complete")
            ran = True

            # ---- Normalize status labels (handles datasets with or without emojis) ----
            def _norm_status(s: str) -> str:
                if not isinstance(s, str):
                    return "Unknown"
                s = s.replace("✅", "").replace("⚠️", "").replace("❌", "").strip()
                # unify a few variants
                s = s.replace("No tests", "No tests").replace("No stories", "No stories")
                s = s.replace("Missing everything", "Missing everything")
                s = s.replace("Covered", "Covered")
                return s

            status_col = "Coverage Status" if "Coverage Status" in df_cov.columns else None
            if status_col:
                df_cov["_status_norm"] = df_cov[status_col].apply(_norm_status)
                covered_full = int((df_cov["_status_norm"] == "Covered").sum())
                no_tests = int((df_cov["_status_norm"] == "No tests").sum())
                no_stories = int((df_cov["_status_norm"] == "No stories").sum())
                missing_all = int((df_cov["_status_norm"] == "Missing everything").sum())
            else:
                covered_full = no_tests = no_stories = missing_all = 0

            total_reqs = len(df_cov)

            # KPIs
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Total Requirements", total_reqs)
            c2.metric("Fully Covered", covered_full)
            c3.metric("No Tests", no_tests)
            c4.metric("No Stories", no_stories)
            c5.metric("Missing Everything", missing_all)

            # Breakdown chart (optional, simple)
            if status_col:
                breakdown = (
                    df_cov["_status_norm"]
                    .value_counts()
                    .rename_axis("Status")
                    .reset_index(name="Count")
                    .sort_values("Status")
                )
                st.markdown("#### Coverage Breakdown")
                st.bar_chart(breakdown.set_index("Status")["Count"])

            # Tabs for detailed views & downloads
            tab1, tab2, tab3 = st.tabs(["Coverage Matrix", "Coverage by Epic", "Downloads"])

            with tab1:
                st.dataframe(df_cov.drop(columns=["_status_norm"], errors="ignore"),
                             use_container_width=True, height=380)

            with tab2:
                st.dataframe(df_epic, use_container_width=True, height=380)

            with tab3:
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.download_button(
                        "Download coverage_matrix.csv",
                        df_cov.drop(columns=["_status_norm"], errors="ignore").to_csv(index=False).encode("utf-8"),
                        "coverage_matrix.csv",
                        "text/csv",
                        use_container_width=True
                    )
                with c2:
                    st.download_button(
                        "Download epic_coverage.csv",
                        df_epic.to_csv(index=False).encode("utf-8"),
                        "epic_coverage.csv",
                        "text/csv",
                        use_container_width=True
                    )
                with c3:
                    comp_csv = OUTPUT_DIR / "compliance_evidence.csv"
                    if comp_csv.exists():
                        st.download_button(
                            "Download compliance_evidence.csv",
                            comp_csv.read_bytes(),
                            "compliance_evidence.csv",
                            "text/csv",
                            use_container_width=True
                        )
                    else:
                        st.caption("Compliance evidence file not found yet.")
    else:
        st.info("You’ll need stories.json and testcases.csv from previous steps.")

    # Back/Next controls (Next enabled only after analysis ran once)
    next_disabled = not ran
    nav_row(next_disabled=next_disabled)

    st.markdown('</div>', unsafe_allow_html=True)
elif choice_label == "Reports":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Reports & Integrations")

    st.markdown("Export generated artifacts and integrate with external tools.")

    # Artifacts quick actions
    col1, col2, col3 = st.columns(3)
    with col1:
        trace_csv = OUTPUT_DIR / "traceability.csv"
        if trace_csv.exists():
            st.download_button(
                "Download traceability.csv",
                trace_csv.read_bytes(),
                "traceability.csv",
                "text/csv",
                use_container_width=True
            )
        else:
            st.caption("traceability.csv not found")

    with col2:
        tests_csv = OUTPUT_DIR / "testcases.csv"
        if tests_csv.exists():
            st.download_button(
                "Download testcases.csv",
                tests_csv.read_bytes(),
                "testcases.csv",
                "text/csv",
                use_container_width=True
            )
        else:
            st.caption("testcases.csv not found")

    with col3:
        cov_csv = OUTPUT_DIR / "coverage_matrix.csv"
        if cov_csv.exists():
            st.download_button(
                "Download coverage_matrix.csv",
                cov_csv.read_bytes(),
                "coverage_matrix.csv",
                "text/csv",
                use_container_width=True
            )
        else:
            st.caption("coverage_matrix.csv not found")

    # Features.zip (if any feature files exist)
    from io import BytesIO
    import zipfile

    feature_files = list(FEATURE_DIR.glob("*.feature"))
    if feature_files:
        buf = BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for fp in feature_files:
                zf.write(fp, arcname=fp.name)
        st.download_button("Download features.zip", buf.getvalue(), "features.zip",
                        "application/zip", use_container_width=True)
    else:
        st.caption("No feature files found to export.")

    # --- Integrations (always visible) ---
    st.markdown("---")
    st.subheader("Integrations")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### Jira")
        st.caption("Export to Jira (CSV) with configurable field mapping")
        st.button("Export to Jira", use_container_width=True)
    with col2:
        st.markdown("### Azure DevOps")
        st.caption("Export to ADO (CSV) with area/iteration mapping")
        st.button("Export to ADO", use_container_width=True)
    with col3:
        st.markdown("### BigQuery")
        st.caption("Export results to BigQuery (select dataset & table)")
        st.button("Export to BigQuery", use_container_width=True)
