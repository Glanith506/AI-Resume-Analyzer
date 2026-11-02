import streamlit as st
from backend import extract_resume_text, compare_skills, calculate_match_percentage, generate_suggestions

# Page configuration
st.set_page_config(
    page_title="ResumeLens | AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# Styling
st.markdown(
    """
<style>
.stApp {
    background: #f5f7fc;
    color: #172554;
}
.block-container {
    max-width: 1200px;
    padding-top: 3rem;
    padding-bottom: 2rem;
}
[data-testid="stSidebar"] {
    background: #eef1fb;
}
.resume-navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    flex-wrap: wrap;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 16px 24px;
    margin-bottom: 24px;
    box-shadow: 0 4px 20px rgba(30, 41, 59, 0.04);
}
.resume-brand {
    display: flex;
    align-items: center;
    gap: 12px;
}
.resume-logo {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 44px;
    height: 44px;
    border-radius: 13px;
    background: linear-gradient(135deg, #6366f1, #4338ca);
    color: white;
    font-size: 22px;
    font-weight: 800;
}
.resume-brand-name {
    color: #172554;
    font-size: 22px;
    font-weight: 750;
    line-height: 1.3;
}
.resume-brand-caption {
    color: #64748b;
    font-size: 12px;
}
.resume-navbar a.resume-nav-link {
    display: inline-block;
    background: #eef2ff;
    color: #4338ca;
    padding: 10px 18px;
    border-radius: 10px;
    text-decoration: none;
    font-size: 14px;
    font-weight: 600;
}
.resume-navbar a.resume-nav-link:hover {
    background: #e0e7ff;
}
.resume-navbar a.resume-nav-link:focus-visible {
    outline: 3px solid #818cf8;
    outline-offset: 3px;
}
.hero {
    padding: 32px;
    margin-bottom: 26px;
    border-radius: 22px;
    background: linear-gradient(120deg, #172554, #4338ca);
    color: white;
}
.hero h1 {
    color: white;
    font-size: clamp(26px, 3vw, 38px);
    padding: 8px 0;
    margin: 0;
}
.hero p {
    color: #e0e7ff;
    font-size: 17px;
    margin-bottom: 0;
}
.hero-label {
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #c7d2fe;
}
[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e2e8f0;
    padding: 22px;
    border-radius: 16px;
}
[data-testid="stMetricValue"] {
    color: #4338ca;
}
div.stButton > button {
    border-radius: 12px;
    font-weight: 600;
    min-height: 48px;
}
div.stButton > button[kind="primary"] {
    background: #4338ca;
    border: 1px solid #4338ca;
    color: white;
}
div.stButton > button[kind="primary"]:hover {
    background: #3730a3;
    border-color: #3730a3;
    color: white;
}
.resume-footer {
    text-align: center;
    margin-top: 50px;
    padding: 22px;
    border-top: 1px solid #e2e8f0;
    color: #64748b;
    font-size: 14px;
}
.resume-footer strong {
    color: #4338ca;
}
@media (max-width: 600px) {
    .resume-navbar {
        padding: 14px;
    }
    .hero {
        padding: 22px;
    }
}
</style>
""",
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    /* Sidebar background */
    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #102b50 0%,
            #09182e 100%
        );
        border-right: 1px solid #244365;
    }

    /* Sidebar spacing */
    [data-testid="stSidebarUserContent"] {
        padding: 2rem 1.5rem;
    }

    /* Brand */
    [data-testid="stSidebar"] h1 {
        color: #ffffff;
        font-size: 1.7rem;
        font-weight: 800;
        letter-spacing: -0.5px;
    }

    /* Section headings */
    [data-testid="stSidebar"] h3 {
        color: #93c5fd;
        font-size: 1.05rem;
        font-weight: 700;
    }

    /* Instructions and checkbox labels */
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] strong,
    [data-testid="stSidebar"] label {
        color: #e2e8f0;
        line-height: 1.7;
    }

    /* Supporting text */
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
        color: #a9bdd5;
        font-size: 0.85rem;
    }

    /* Dividers */
    [data-testid="stSidebar"] hr {
        border-color: rgba(148, 180, 215, 0.22);
        margin: 1.8rem 0;
    }

    /* Checkbox section */
    [data-testid="stSidebar"] [data-testid="stCheckbox"] {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(147, 197, 253, 0.18);
        border-radius: 10px;
        padding: 10px 12px;
    }

    /* Links */
    [data-testid="stSidebar"] a {
        color: #93c5fd;
    }

    /* Sidebar collapse control */
    [data-testid="stSidebar"] button[kind="headerNoPadding"] {
        color: #e2e8f0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar
# Sidebar
with st.sidebar:
    st.title("📄 ResumeLens")
    st.caption("Resume analysis and skill preparation")
    st.divider()

    st.subheader("How it works")

    st.markdown(
        """
**1. Upload your resume**  
Choose a PDF with selectable text.

**2. Add a job description**  
Compare matching skills and skills to review.

**3. Add learning material**  
Upload notes or guides to your saved knowledge base.

**4. Ask questions**  
Get answers using your documents, with source references.
"""
    )

    st.divider()
    st.subheader("Resume feedback")

    include_ai = st.checkbox(
        "Include AI suggestions",
        value=False
    )

    st.divider()
    st.caption(
        "Python • Streamlit • MiniLM • ChromaDB • Groq"
    )
    

# Navbar
st.markdown(
    """
<nav class="resume-navbar" aria-label="Main navigation">
    <div class="resume-brand">
        <div class="resume-logo">R</div>
        <div>
            <div class="resume-brand-name">ResumeLens</div>
            <div class="resume-brand-caption">
                Make your experience stand out
            </div>
        </div>
    </div>
    <a class="resume-nav-link" href="#resume-inputs"
       target="_self">Analyze resume ↗</a>
</nav>
""",
    unsafe_allow_html=True
)

# Banner
st.markdown(
    """
<div class="hero">
    <div class="hero-label">AI RESUME ANALYZER</div>
    <h1>Find your fit. Shape your next move.</h1>
    <p>
        Compare your resume with a job description and
        discover where your skills connect.
    </p>
</div>
""",
    unsafe_allow_html=True
)

# Inputs
st.markdown(
    '<div id="resume-inputs"></div>',
    unsafe_allow_html=True
)

left, right = st.columns(2, gap="large")

with left:
    with st.container(border=True):
        st.subheader("📄 Your resume")
        st.caption("Upload a PDF with selectable text.")

        uploaded_file = st.file_uploader(
            "Choose your resume",
            type=["pdf"]
        )

        if uploaded_file is not None:
            st.success("Resume ready to analyze")

with right:
    with st.container(border=True):
        st.subheader("💼 Your next role")
        st.caption("Paste the responsibilities and skills for the role.")

        job_description = st.text_area(
            "Job description",
            height=200,
            placeholder=(
                "We are looking for a developer with "
                "Python, SQL, React..."
            )
        )

st.write("")

analyze = st.button(
    "Analyze my resume →",
    type="primary",
    width="stretch"
)

# Clear old results when inputs or settings change
current_inputs = (
    uploaded_file.getvalue() if uploaded_file is not None else None,
    job_description,
    include_ai
)

if st.session_state.get("analysis_inputs") != current_inputs:
    st.session_state.pop("analysis_result", None)
    st.session_state["analysis_inputs"] = current_inputs

# Run analysis
if analyze:
    if uploaded_file is None:
        st.warning("Upload your resume to get started.")

    elif not job_description.strip():
        st.warning("Add a job description to compare your skills.")

    else:
        resume_text = ""
        pdf_error = False

        try:
            with st.spinner("Reading your resume..."):
                resume_text = extract_resume_text(uploaded_file)

        except Exception:
            pdf_error = True
            st.error(
                "Could not read this PDF. "
                "Please upload a valid, unlocked PDF."
            )

        if not pdf_error:
            if not resume_text.strip():
                st.warning(
                    "No text could be extracted. "
                    "Please upload a PDF with selectable text."
                )
            else:
                (resume_skills, job_skills, matching_skills,
                 missing_skills) = compare_skills(resume_text, job_description)

                suggestions = None
                ai_error = False

                if include_ai:
                    try:
                        with st.spinner("Preparing AI feedback..."):
                            suggestions = generate_suggestions(
                                resume_text,
                                job_description,
                                matching_skills,
                                missing_skills
                            )

                    except Exception as error:
                        ai_error = True
                        print(
                            "Groq error:",
                            type(error).__name__,
                            str(error)
                        )
                        print("Underlying cause:", repr(error.__cause__))

                st.session_state["analysis_result"] = {
                    "resume_text": resume_text,
                    "resume_skills": resume_skills,
                    "job_skills": job_skills,
                    "matching_skills": matching_skills,
                    "missing_skills": missing_skills,
                    "suggestions": suggestions,
                    "ai_error": ai_error
                }

# Display stored results
result = st.session_state.get("analysis_result")

if result is not None:
    resume_skills = result["resume_skills"]
    job_skills = result["job_skills"]
    matching_skills = result["matching_skills"]
    missing_skills = result["missing_skills"]

    st.divider()
    st.subheader("Your resume at a glance")
    st.caption("A comparison of the skills detected in your documents.")

    score_col, match_col, gap_col = st.columns(3)

    if job_skills:
        match_percentage = calculate_match_percentage(
            matching_skills, job_skills
        )

        score_col.metric(
            "Detected skill coverage",
            f"{match_percentage:.1f}%"
        )
        match_col.metric("Matching skills", len(matching_skills))
        gap_col.metric("Skills to review", len(missing_skills))

        st.write("")
        st.progress(
            match_percentage / 100,
            text=(
                f"{len(matching_skills)} of {len(job_skills)} "
                "detected job skills appear in your resume"
            )
        )

    else:
        score_col.metric("Detected skill coverage", "N/A")
        match_col.metric("Matching skills", "N/A")
        gap_col.metric("Skills to review", "N/A")

        st.info(
            "No skills from our current list were detected "
            "in the job description."
        )

    st.caption(
        "Coverage uses a predefined skill list and counts required "
        "and preferred skills equally. It is not an official ATS "
        "score or a prediction of interview selection."
    )

    skills_tab, ai_tab, text_tab = st.tabs(
        ["🎯 Skill breakdown", "✨ AI feedback", "📃 Resume text"]
    )

    with skills_tab:
        matched_col, missing_col = st.columns(2, gap="large")

        with matched_col:
            with st.container(border=True):
                st.subheader("✅ Matching skills")

                if matching_skills:
                    for skill in matching_skills:
                        st.markdown(f"✓ **{skill.title()}**")
                else:
                    st.write("No matching skills detected.")

        with missing_col:
            with st.container(border=True):
                st.subheader("🔎 Skills to review")

                if missing_skills:
                    for skill in missing_skills:
                        st.markdown(f"• **{skill.title()}**")

                    st.caption(
                        "These were not detected in your resume. "
                        "This does not prove that you lack them."
                    )
                elif job_skills:
                    st.write("No missing skills detected.")
                else:
                    st.write("No job skills were detected for comparison.")

        with st.expander("Explore all detected skills"):
            st.markdown("**In your resume**")
            st.write(", ".join(resume_skills) or "None detected")

            st.markdown("**In the job description**")
            st.write(", ".join(job_skills) or "None detected")

    with ai_tab:
        if not include_ai:
            st.info(
                "Enable 'Include AI suggestions' in the sidebar, "
                "then click 'Analyze my resume' again."
            )
        elif result["ai_error"]:
            st.error(
                "AI feedback is unavailable right now. "
                "Your skill comparison is still available. "
                "Check the VS Code terminal for the Groq error."
            )
        elif result["suggestions"]:
            with st.container(border=True):
                st.subheader("✨ A closer look at your resume")
                st.markdown(result["suggestions"])
                st.caption(
                    "Review AI suggestions before using them. "
                    "Include only skills and experience that are true."
                )
        else:
            st.info("No feedback was returned. Try analyzing again.")

    with text_tab:
        st.caption("Check the text extracted from your uploaded PDF.")
        st.text_area(
            "Extracted resume",
            value=result["resume_text"],
            height=400,
            disabled=True
        )

elif not analyze:
    st.caption(
        "Ready when you are — upload your resume and add a role above."
    )

# Source-grounded learning workspace
st.divider()
st.header("📚 Study materials")
st.caption("Your learning index is saved locally in ChromaDB and reopened after a restart.")
from rag import read_document, KnowledgeBase, grounded_answer
from backend import call_llm
from pathlib import Path
import traceback

@st.cache_resource
def load_encoder():
    import torch
    from sentence_transformers import SentenceTransformer
    torch.set_num_threads(1)
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")

@st.cache_resource
def open_saved_knowledge_base():
    return KnowledgeBase(encoder_factory=load_encoder)


def learning_error(message, error):
    st.error(f"{message}: {type(error).__name__}: {error}")
    traceback.print_exc()


kb = None
try:
    kb = open_saved_knowledge_base()
except Exception as error:
    learning_error("Could not open saved ChromaDB index", error)
    st.info("Keep a backup of data/chroma. Check the terminal and README before changing database versions.")

learning_files = st.file_uploader("	Upload notes (maximum 10 files))",
                                  type=["pdf", "txt", "md"], accept_multiple_files=True, key="learning_files")
st.caption("Adding documents keeps existing ones. Identical file contents are skipped, even when renamed. A changed file is a new document; remove the older version if desired.")
if st.button("Save documents", disabled=not learning_files or kb is None):
    try:
        if len(learning_files) > 10:
            raise ValueError("Upload at most 10 documents at once.")
        with st.spinner("Creating embeddings and saving document passages to ChromaDB..."):
            chunks = []
            for f in learning_files:
                chunks.extend(read_document(f.name, f.getvalue()))
            if len(chunks) > 2000:
                raise ValueError("Use fewer or shorter documents (maximum 2,000 passages).")
            stats = kb.add_chunks(chunks)
        st.session_state.pop("learning_answer", None)
        st.success(f"Knowledge base ready: {stats['added']} new passages saved; {stats['skipped']} already indexed passages skipped.")
    except Exception as error:
        learning_error("Could not add documents", error)
        st.info("Earlier completed batches may be saved. Retrying the same files skips those passages. Native crashes require the terminal log; persistence alone does not fix them.")

if kb is not None:
    try:
        docs = kb.documents()
        st.metric("Saved passages", kb.count())
        if docs:
            st.success("Your documents are ready.")
            st.dataframe([{"Document": d["source"], "File ID": d["document_id"][:12],
                           "Passages": d["passages"]} for d in docs], hide_index=True, use_container_width=True)
        else:
            st.info("No saved learning documents yet. Upload notes above to get started.")
        with st.expander("Manage documents"):
            st.caption("This local app uses one personal knowledge base shared by tabs on this computer. These actions affect that saved collection.")
            if docs:
                doc_id = st.selectbox("Document to remove", [d['document_id'] for d in docs],
                                     format_func=lambda value: next(f"{d['source']} ({value[:12]})" for d in docs if d['document_id'] == value))
                confirm_remove = st.checkbox("Confirm removal of the selected saved document", key="confirm_remove")
                if st.button("Remove selected document", disabled=not confirm_remove):
                    kb.delete_document(doc_id)
                    st.session_state.pop("learning_answer", None)
                    st.rerun()
            confirm_clear = st.checkbox("Confirm deletion of ALL saved learning passages", key="confirm_clear")
            if st.button("Clear saved knowledge base", disabled=not confirm_clear):
                kb.clear()
                st.session_state.pop("learning_answer", None)
                st.rerun()
    except Exception as error:
        learning_error("Could not read or manage saved documents", error)

missing = result["missing_skills"] if result else []
if missing:
    st.write("Skills not detected in your resume: " + ", ".join(missing))
    chosen = st.selectbox("Choose a skill to study", missing)
else:
    chosen = "a topic in these documents"
question = st.text_input("Ask a question", placeholder="What is Docker, and what should I practise first?")
consent = st.checkbox("Send my question, missing-skill names and retrieved passages to Groq", key="rag_consent")
if st.button("Get answer", type="primary"):
    if kb is None or kb.count() == 0:
        st.warning("Add learning documents to the saved knowledge base first.")
    elif not consent:
        st.warning("Enable the Groq checkbox to generate an answer.")
    else:
        q = question.strip() or f"Explain {chosen} and suggest a beginner practice plan."
        if len(q) > 2000:
            st.warning("Keep the question under 2,000 characters.")
        else:
            try:
                with st.spinner("Retrieving saved passages and preparing your answer..."):
                    hits = kb.search(q)
                    answer = grounded_answer(q, hits, missing, call_llm)
                    st.session_state["learning_answer"] = (q, answer, hits)
            except Exception as error:
                # Keep API error details out of the page; no credentials or prompts are logged.
                st.error(f"Learning answer unavailable ({type(error).__name__}). Check your Groq key, model name, quota and connection. Your saved documents remain available.")
if st.session_state.get("learning_answer"):
    q, answer, hits = st.session_state["learning_answer"]
    st.subheader(q)
    st.markdown(answer)
    st.caption("AI-generated answer: review it against the retrieved passages below. Citations are model-generated and may need checking.")
    for i, hit in enumerate(hits, 1):
        with st.expander(f"[S{i}] {hit['source']} · page {hit['page']} · passage {hit['chunk']}"):
            st.write(hit["text"])
            st.caption(f"Retrieval similarity: {hit['similarity']} (not answer confidence)")
    st.download_button("Download learning answer", q + "\n\n" + answer + "\n\nSOURCES\n" +
                       "\n\n".join(f"[S{i}] {h['source']} page {h['page']}\n{h['text']}" for i,h in enumerate(hits,1)),
                       file_name="learning_plan.txt")

# Footer
st.markdown(
    """
<div class="resume-footer">
    Developed by <strong>Glanith Dcunha</strong>
</div>
""",
    unsafe_allow_html=True
)