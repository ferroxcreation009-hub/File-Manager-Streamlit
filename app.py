"""
File Manager — a small Streamlit UI over basic CRUD file operations.

Run with:
    pip install streamlit
    streamlit run file_manager_app.py

Security note: all operations are sandboxed to a local "workspace" folder.
User-supplied filenames are stripped of any path components so this app
can't be used to read/write/delete files outside that folder (no path
traversal via "../../" or absolute paths).
"""

import streamlit as st
from pathlib import Path
from datetime import datetime

# ----------------------------- setup -----------------------------

st.set_page_config(page_title="File Manager", page_icon="🗂️", layout="centered")

WORKDIR = Path("file_manager_workspace")
WORKDIR.mkdir(exist_ok=True)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap');

    :root {
        --accent: #6C5CE7;
        --accent-light: #A29BFE;
        --accent-dark: #4834D4;
        --surface: #F8F7FC;
        --border: #E4E1F5;
        --text-dark: #2D2A3D;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* overall canvas */
    .stApp {
        background: linear-gradient(180deg, #FAFAFF 0%, #F3F1FB 100%);
    }
    .main > div {padding-top: 1rem;}
    .block-container {padding-top: 2rem; padding-bottom: 3rem;}

    /* hero banner */
    .hero {
        background: linear-gradient(135deg, var(--accent) 0%, var(--accent-dark) 100%);
        border-radius: 18px;
        padding: 2rem 2.2rem;
        margin-bottom: 1.8rem;
        box-shadow: 0 10px 30px rgba(108, 92, 231, 0.25);
    }
    .hero h1 {
        font-family: 'Poppins', sans-serif;
        color: white;
        font-size: 2rem;
        margin: 0 0 0.3rem 0;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    .hero p {
        color: rgba(255,255,255,0.85);
        margin: 0;
        font-size: 0.95rem;
    }

    /* section subheaders */
    h2, h3 {
        font-family: 'Poppins', sans-serif !important;
        color: var(--text-dark) !important;
        font-weight: 600 !important;
    }

    /* sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFFFFF 0%, #F3F1FB 100%);
        border-right: 1px solid var(--border);
    }
    section[data-testid="stSidebar"] h2 {
        font-family: 'Poppins', sans-serif !important;
        color: var(--accent-dark) !important;
        font-size: 1.1rem !important;
    }
    section[data-testid="stSidebar"] .stCaption, section[data-testid="stSidebar"] p {
        color: #6B6880 !important;
    }

    /* radio pills in sidebar */
    div[role="radiogroup"] label {
        background: white;
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 0.5rem 0.8rem !important;
        margin-bottom: 0.4rem;
        transition: all 0.15s ease;
        width: 100%;
    }
    div[role="radiogroup"] label:hover {
        border-color: var(--accent);
        background: #F5F3FF;
    }

    /* buttons */
    .stButton>button, .stDownloadButton>button, .stFormSubmitButton>button {
        border-radius: 10px;
        font-weight: 600;
        padding: 0.55rem 1.3rem;
        border: none;
        background: linear-gradient(135deg, var(--accent) 0%, var(--accent-dark) 100%);
        color: white;
        transition: transform 0.12s ease, box-shadow 0.12s ease;
        box-shadow: 0 4px 12px rgba(108, 92, 231, 0.25);
    }
    .stButton>button:hover, .stDownloadButton>button:hover, .stFormSubmitButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(108, 92, 231, 0.35);
        color: white;
    }
    .stButton>button:disabled {
        background: #D8D5EA;
        box-shadow: none;
        color: #9A96B5;
    }

    /* text inputs / textareas */
    .stTextInput>div>div>input,
    .stTextArea textarea,
    .stSelectbox div[data-baseweb="select"] {
        border-radius: 10px !important;
        border: 1px solid var(--border) !important;
    }
    .stTextInput>div>div>input:focus,
    .stTextArea textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px rgba(108,92,231,0.15) !important;
    }

    /* file cards */
    .file-card {
        background: white;
        border: 1px solid var(--border);
        border-left: 4px solid var(--accent);
        border-radius: 10px;
        padding: 0.7rem 1.1rem;
        margin-bottom: 0.5rem;
        font-size: 0.92rem;
        color: var(--text-dark);
        box-shadow: 0 2px 6px rgba(108, 92, 231, 0.06);
        transition: transform 0.12s ease;
    }
    .file-card:hover {
        transform: translateX(3px);
    }

    /* alerts */
    div[data-testid="stAlert"] {
        border-radius: 10px;
    }

    /* checkboxes */
    .stCheckbox {
        margin-top: 0.3rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def safe_path(filename: str) -> Path | None:
    """Resolve a user-supplied filename to a path strictly inside WORKDIR."""
    if not filename:
        return None
    name = Path(filename).name  # strips any directory components
    if not name or name in (".", ".."):
        return None
    return WORKDIR / name


def list_files():
    return sorted(p.name for p in WORKDIR.iterdir() if p.is_file())


# ----------------------------- header -----------------------------

st.markdown(
    """
    <div class="hero">
        <h1>🗂️ File Manager</h1>
        <p>Create, read, update, and delete text files — all safely sandboxed to one folder.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("📋 Menu")
    action = st.radio(
        "Choose an action",
        ["📁 Browse", "➕ Create", "📖 Read", "✏️ Update", "🗑️ Delete"],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption(f"Workspace: `{WORKDIR}/`")
    files = list_files()
    st.markdown(
        f'<div style="background:#EDEBFB;color:#4834D4;border-radius:20px;'
        f'padding:0.35rem 0.9rem;display:inline-block;font-size:0.85rem;font-weight:600;">'
        f'{len(files)} file(s) stored</div>',
        unsafe_allow_html=True,
    )

# ----------------------------- Browse -----------------------------

if action == "📁 Browse":
    st.subheader("Files in workspace")
    files = list_files()
    if not files:
        st.info("No files yet — create one from the sidebar.")
    else:
        for f in files:
            p = WORKDIR / f
            size = p.stat().st_size
            modified = datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
            st.markdown(
                f'<div class="file-card">📄 <b>{f}</b> — {size} bytes — last modified {modified}</div>',
                unsafe_allow_html=True,
            )

# ----------------------------- Create -----------------------------

elif action == "➕ Create":
    st.subheader("Create a new file")
    with st.form("create_form"):
        name = st.text_input("File name", placeholder="notes.txt")
        content = st.text_area("Content", height=150, placeholder="Type the file's contents here...")
        submitted = st.form_submit_button("Create file")

    if submitted:
        path = safe_path(name)
        if path is None:
            st.error("Please enter a valid file name.")
        elif path.exists():
            st.error(f"'{path.name}' already exists.")
        else:
            try:
                path.write_text(content)
                st.success(f"Created '{path.name}' successfully.")
            except Exception as err:
                st.error(f"Error occurred: {err}")

# ----------------------------- Read -----------------------------

elif action == "📖 Read":
    st.subheader("Read a file")
    files = list_files()
    if not files:
        st.info("No files to read yet.")
    else:
        name = st.selectbox("Choose a file", files)
        if name:
            path = safe_path(name)
            try:
                content = path.read_text()
                st.text_area("Content", content, height=200, disabled=True)
                st.download_button("Download this file", content, file_name=path.name)
            except Exception as err:
                st.error(f"Error occurred: {err}")

# ----------------------------- Update -----------------------------

elif action == "✏️ Update":
    st.subheader("Update a file")
    files = list_files()
    if not files:
        st.info("No files to update yet.")
    else:
        name = st.selectbox("Choose a file", files)
        op = st.radio("Operation", ["Rename", "Append", "Overwrite"], horizontal=True)
        path = safe_path(name)

        if op == "Rename":
            new_name = st.text_input("New file name")
            if st.button("Rename"):
                new_path = safe_path(new_name)
                if new_path is None:
                    st.error("Please enter a valid new name.")
                elif new_path.exists():
                    st.error(f"'{new_path.name}' already exists.")
                else:
                    try:
                        path.rename(new_path)
                        st.success(f"Renamed to '{new_path.name}'.")
                    except Exception as err:
                        st.error(f"Error occurred: {err}")

        elif op == "Append":
            extra = st.text_area("Text to append", height=120)
            if st.button("Append"):
                try:
                    with open(path, "a") as fs:
                        fs.write("\n" + extra)
                    st.success(f"Appended to '{path.name}'.")
                except Exception as err:
                    st.error(f"Error occurred: {err}")

        elif op == "Overwrite":
            new_content = st.text_area("New content (replaces everything)", height=150)
            confirm = st.checkbox("I understand this replaces the file's current contents.")
            if st.button("Overwrite", disabled=not confirm):
                try:
                    path.write_text(new_content)
                    st.success(f"Overwrote '{path.name}'.")
                except Exception as err:
                    st.error(f"Error occurred: {err}")

# ----------------------------- Delete -----------------------------

elif action == "🗑️ Delete":
    st.subheader("Delete a file")
    files = list_files()
    if not files:
        st.info("No files to delete yet.")
    else:
        name = st.selectbox("Choose a file", files)
        confirm = st.checkbox(f"I'm sure I want to permanently delete '{name}'.")
        if st.button("Delete file", disabled=not confirm, type="primary"):
            path = safe_path(name)
            try:
                path.unlink()
                st.success(f"Deleted '{name}'.")
                st.rerun()
            except Exception as err:
                st.error(f"Error occurred: {err}")
