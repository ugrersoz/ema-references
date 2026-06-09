import streamlit as st
import pandas as pd
import datetime
import os
import json
import uuid
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="How EMA's First Oral Hearing Spotlighted Patient Collaboration",
    page_icon="📚",
    layout="wide"
)


def _load_admin_password() -> str:
    """
    Resolve the admin password from runtime configuration.

    Lookup order:
      1. Streamlit secrets (`.streamlit/secrets.toml` locally, or the
         "App settings → Secrets" panel on Streamlit Cloud).
      2. The ADMIN_PASSWORD environment variable.
      3. An empty string — which makes the login form unable to grant
         admin access at all. We fail closed on purpose.

    This used to be a hard-coded `PASSWORD = "admin123"` literal in the
    source. That credential is now considered compromised: it is in this
    repository's public Git history. Rotate it on Streamlit Cloud
    immediately and never put a real password back into the code.
    """
    try:
        secret = st.secrets.get("ADMIN_PASSWORD")
        if secret:
            return str(secret)
    except (FileNotFoundError, KeyError, Exception):
        # st.secrets raises if no secrets.toml is present and no Cloud
        # secrets are configured. Fall through to the env var.
        pass
    return os.environ.get("ADMIN_PASSWORD", "")


PASSWORD = _load_admin_password()

# Path to store references data
DATA_FILE = "references_data.json"

# Load references from file
def load_references():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        except:
            return []
    return []

# Save references to file
def save_references(references):
    with open(DATA_FILE, "w") as file:
        json.dump(references, file)

# Session state setup
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if 'references' not in st.session_state:
    st.session_state['references'] = load_references()

if 'edit_id' not in st.session_state:
    st.session_state['edit_id'] = None

if 'show_add_form' not in st.session_state:
    st.session_state['show_add_form'] = False

# Helper functions
def set_edit_id(id):
    st.session_state['edit_id'] = id
    st.session_state['show_add_form'] = False
    st.rerun()

def delete_reference(index):
    st.session_state['references'].pop(index)
    save_references(st.session_state['references'])
    st.success("Reference deleted successfully!")
    st.rerun()

def toggle_add_form():
    st.session_state['show_add_form'] = not st.session_state['show_add_form']
    st.session_state['edit_id'] = None
    st.rerun()

# --- HEADER ---
st.title("📚 How EMA's First Oral Hearing Spotlighted Patient Collaboration")
st.subheader("Increasing Recognition of Patient Engagement in EU Medical Regulation")
st.subheader(" HTW Berlin - M8 Course Presentation References | Developed By Ugur Ersoz")

# --- AUTH ---
col1, col2 = st.columns([5, 1])
with col2:
    if not st.session_state['authenticated']:
        show_login = st.button("🔑 Admin Login")
        if show_login:
            st.session_state['show_login'] = True
    else:
        if st.button("🚪 Logout"):
            st.session_state['authenticated'] = False
            st.session_state['show_add_form'] = False
            st.session_state['edit_id'] = None
            st.rerun()

# --- LOGIN FORM ---
if not st.session_state['authenticated'] and st.session_state.get('show_login', False):
    with st.form("login_form"):
        password = st.text_input("Enter admin password", type="password")
        login_submit = st.form_submit_button("Login")
        if login_submit:
            # Fail-closed: if no admin password has been configured (empty
            # secret/env), refuse login outright — never compare against ""
            # and never log a confirmation that might double as an
            # admin-mode-available signal.
            if not PASSWORD:
                st.error(
                    "Admin login is not available on this deployment. "
                    "An ADMIN_PASSWORD secret has not been configured."
                )
            elif password == PASSWORD:
                st.session_state['authenticated'] = True
                st.session_state['show_login'] = False
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Incorrect password.")

# --- ADMIN PANEL ---
if st.session_state['authenticated']:
    st.success("✅ Admin Mode Active")

    if not st.session_state['edit_id'] and not st.session_state['show_add_form']:
        if st.button("➕ Add New Reference"):
            toggle_add_form()

    # --- EDIT FORM ---
    if st.session_state['edit_id'] is not None:
        edit_index = None
        edit_reference = None
        for i, ref in enumerate(st.session_state['references']):
            if ref.get('id') == st.session_state['edit_id']:
                edit_index = i
                edit_reference = ref
                break

        if edit_reference:
            with st.form("edit_reference_form"):
                col1, col2 = st.columns(2)
                with col1:
                    edited_title = st.text_input("Title", value=edit_reference.get('title', ''))
                    edited_type = st.selectbox("Type", 
                        ["Article", "Journal Paper", "Report", "Guideline", "Website", "Video", "Presentation", "Other"],
                        index=["Article", "Journal Paper", "Report", "Guideline", "Website", "Video", "Presentation", "Other"].index(edit_reference.get('type', 'Article'))
                    )
                with col2:
                    edited_url = st.text_input("URL", value=edit_reference.get('url', ''))
                    edited_description = st.text_area("Description", value=edit_reference.get('description', ''))

                submit_edit = st.form_submit_button("💾 Save")
                cancel_edit = st.form_submit_button("❌ Cancel")

            if submit_edit:
                if edited_title and edited_url:
                    updated_ref = {
                        "id": edit_reference.get('id'),
                        "title": edited_title,
                        "type": edited_type,
                        "url": edited_url,
                        "description": edited_description,
                        "date": edit_reference.get('date'),
                        "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    st.session_state['references'][edit_index] = updated_ref
                    save_references(st.session_state['references'])
                    st.session_state['edit_id'] = None
                    st.success("Reference updated!")
                    st.rerun()
                else:
                    st.error("Title and URL are required.")
            if cancel_edit:
                st.session_state['edit_id'] = None
                st.rerun()

    # --- ADD NEW FORM ---
    elif st.session_state['show_add_form']:
        with st.form("new_reference_form"):
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Title")
                ref_type = st.selectbox("Type", 
                    ["Article", "Journal Paper", "Report", "Guideline", "Website", "Video", "Presentation", "Other"])
            with col2:
                url = st.text_input("URL")
                description = st.text_area("Description")

            submit_button = st.form_submit_button("➕ Add Reference")
            cancel_button = st.form_submit_button("❌ Cancel")

        if submit_button:
            if title and url:
                new_ref = {
                    "id": str(uuid.uuid4()),
                    "title": title,
                    "type": ref_type,
                    "url": url,
                    "description": description,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state['references'].append(new_ref)
                save_references(st.session_state['references'])
                st.session_state['show_add_form'] = False
                st.success("Reference added!")
                st.rerun()
            else:
                st.error("Title and URL are required.")

        if cancel_button:
            st.session_state['show_add_form'] = False
            st.rerun()

# --- SEARCH ---
search_query = st.text_input("🔍 Search references")
filtered_refs = st.session_state['references']
if search_query:
    filtered_refs = [
        ref for ref in filtered_refs if search_query.lower() in ref['title'].lower()
        or search_query.lower() in ref['description'].lower()
        or search_query.lower() in ref['type'].lower()
    ]

st.write(f"Showing {len(filtered_refs)} references")

# --- DISPLAY REFERENCES ---
for i, ref in enumerate(filtered_refs):
    with st.expander(f"📌 {ref['title']}"):
        st.markdown(f"**Type:** {ref['type']}")
        st.markdown(f"**Description:** {ref['description']}")
        st.markdown(f"**URL:** [{ref['url']}]({ref['url']})")
        st.markdown(f"**Date Added:** {ref['date']}")
        if ref.get('updated'):
            st.markdown(f"**Last Updated:** {ref['updated']}")
        if st.session_state['authenticated']:
            st.button("✏️ Edit", key=f"edit_{i}", on_click=lambda id=ref.get('id'): set_edit_id(id))
            st.button("🗑️ Delete", key=f"delete_{i}", on_click=lambda i=i: delete_reference(i))

# --- BACKUP & RESTORE ---
st.markdown("---")
st.subheader("💾 Backup and Restore")

# Download JSON
json_data = json.dumps(st.session_state['references'], indent=4)
st.download_button("📥 Download References (JSON)", data=json_data, file_name="references_backup.json", mime="application/json")

# Upload JSON
uploaded_file = st.file_uploader("📤 Upload Backup File (JSON)", type=["json"])
if uploaded_file:
    try:
        uploaded_refs = json.load(uploaded_file)
        if isinstance(uploaded_refs, list):
            st.session_state['references'] = uploaded_refs
            save_references(uploaded_refs)
            st.success("Backup restored successfully!")
            st.rerun()
        else:
            st.error("The uploaded file is not a valid reference list.")
    except Exception as e:
        st.error(f"Error: {e}")

# --- FOOTER ---
st.markdown('<p style="text-align: center; font-size: 0.9rem; color: gray; margin-top: 3rem;">© 2025 | EMA Patient Engagement References Tool | Developed for academic purposes | Developed by Ugur Ersoz</p>', unsafe_allow_html=True)
