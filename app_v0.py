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

# Custom CSS styling
st.markdown("""
<style>
    /* Main styling elements */
    .main-header {
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.8rem !important;
        font-weight: 600 !important;
        color: #2563EB;
        margin-bottom: 1.5rem;
    }
    .section-header {
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        color: #1E40AF;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #E5E7EB;
    }
    .reference-title {
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        color: #1E3A8A;
    }
    
    /* Form and container styling */
    .stExpander {
        border-radius: 10px;
        border: 1px solid #E5E7EB;
        margin-bottom: 1.2rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .stAlert {
        border-radius: 8px;
    }
    
    /* Login form styling */
    [data-testid="stForm"] {
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #E5E7EB;
        background-color: #F9FAFB;
    }
    
    /* Button styling */
    .stButton>button {
        border-radius: 6px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    button[kind="primary"] {
        background-color: #2563EB;
        color: white;
    }
    button[kind="secondary"] {
        background-color: #6B7280;
        color: white;
    }
    button[kind="danger"] {
        background-color: #DC2626;
        color: white;
    }
    
    /* Reference list styling */
    .ref-box {
        padding: 1.2rem;
        border-radius: 8px;
        border: 1px solid #E5E7EB;
        margin-bottom: 1rem;
        transition: all 0.2s ease;
    }
    .ref-box:hover {
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .ref-title {
        font-size: 1.4rem !important;
        font-weight: 700 !important;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
    }
    .ref-meta {
        font-size: 0.9rem;
        color: #6B7280;
    }
    .ref-description {
        margin: 0.8rem 0;
    }
    
    /* Footer styling */
    .footer {
        font-size: 0.9rem;
        color: #6B7280;
        text-align: center;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #E5E7EB;
    }
    
    /* Divider styling */
    hr {
        margin: 2rem 0;
        border-color: #E5E7EB;
    }
    
    /* This targets the expander header text */
    .st-emotion-cache-ztfqz8 [data-testid="stExpander"] summary p {
        font-size: 1.2rem !important;
        font-weight: 700 !important;
    }
    
    /* Backup selectors for compatibility */
    [data-testid="stExpander"] summary div p,
    .st-emotion-cache-r421ms p,
    .st-emotion-cache-r421ms .st-bf,
    .st-aw div, 
    .st-d2 p,
    [data-testid="stExpander"] div p {
        font-size: 1.2rem !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# Application title and subtitle
st.markdown('<p class="main-header">How EMA\'s First Oral Hearing Spotlighted Patient Collaboration</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Increasing Recognition of Patient Engagement in EU Medical Regulation</p>', unsafe_allow_html=True)

# Create a password for admin access
PASSWORD = "admin123"  # You can change this password

# Path to store references data
DATA_FILE = "references_data.json"

# Function to load existing references
def load_references():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        except:
            return []
    return []

# Function to save references
def save_references(references):
    with open(DATA_FILE, "w") as file:
        json.dump(references, file)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if 'references' not in st.session_state:
    st.session_state['references'] = load_references()
    
if 'edit_id' not in st.session_state:
    st.session_state['edit_id'] = None

# Login section
if not st.session_state['authenticated']:
    with st.container():
        st.markdown('<p class="section-header">Admin Login</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            with st.form("login_form"):
                password = st.text_input("Enter password to access admin features:", type="password")
                col_btn1, col_btn2 = st.columns([1, 4])
                with col_btn1:
                    login_submit = st.form_submit_button("Login", use_container_width=True)
                
                if login_submit:
                    if password == PASSWORD:
                        st.session_state['authenticated'] = True
                        st.success("Authentication successful!")
                        st.rerun()
                    else:
                        st.error("Incorrect password. Please try again.")

# Admin section (only shown when authenticated)
if st.session_state['authenticated']:
    with st.container():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown('<p class="section-header">Reference Management</p>', unsafe_allow_html=True)
        with col2:
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state['authenticated'] = False
                st.rerun()
    
    st.success("✅ Admin Mode Active - You can add, edit, and delete references")
    
    # Check if we're editing an existing reference
    if st.session_state['edit_id'] is not None:
        # Find the reference we're editing
        edit_index = None
        edit_reference = None
        for i, ref in enumerate(st.session_state['references']):
            if ref.get('id') == st.session_state['edit_id']:
                edit_index = i
                edit_reference = ref
                break
        
        if edit_reference:
            st.markdown('<p class="section-header">Edit Reference</p>', unsafe_allow_html=True)
            
            with st.form("edit_reference_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    edited_title = st.text_input("Reference Title", value=edit_reference.get('title', ''))
                    edited_type = st.selectbox(
                        "Reference Type", 
                        ["Article", "Journal Paper", "Report", "Guideline", "Website", "Video", "Presentation", "Other"],
                        index=["Article", "Journal Paper", "Report", "Guideline", "Website", "Video", "Presentation", "Other"].index(edit_reference.get('type', 'Article'))
                    )
                
                with col2:
                    edited_url = st.text_input("URL Link", value=edit_reference.get('url', ''))
                    edited_description = st.text_area("Brief Description", value=edit_reference.get('description', ''))
                
                col3, col4, col5 = st.columns([1, 1, 2])
                with col3:
                    submit_edit = st.form_submit_button("💾 Save Changes", use_container_width=True)
                with col4:
                    cancel_edit = st.form_submit_button("❌ Cancel", use_container_width=True)
            
            if submit_edit:
                if edited_title and edited_url:
                    # Create updated reference
                    updated_ref = {
                        "id": edit_reference.get('id'),
                        "title": edited_title,
                        "type": edited_type,
                        "url": edited_url,
                        "description": edited_description,
                        "date": edit_reference.get('date'),
                        "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    # Update reference in the list
                    st.session_state['references'][edit_index] = updated_ref
                    
                    # Save to file
                    save_references(st.session_state['references'])
                    
                    # Reset edit mode
                    st.session_state['edit_id'] = None
                    
                    st.success(f"Reference '{edited_title}' updated successfully!")
                    st.rerun()
                else:
                    st.error("Title and URL are required fields.")
            
            if cancel_edit:
                st.session_state['edit_id'] = None
                st.rerun()
    else:
        # Add new reference form
        st.markdown('<p class="section-header">Add New Reference</p>', unsafe_allow_html=True)
        
        with st.form("new_reference_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                title = st.text_input("Reference Title")
                ref_type = st.selectbox(
                    "Reference Type", 
                    ["Article", "Journal Paper", "Report", "Guideline", "Website", "Video", "Presentation", "Other"]
                )
            
            with col2:
                url = st.text_input("URL Link")
                description = st.text_area("Brief Description")
            
            col_btn1, col_btn2 = st.columns([1, 3])
            with col_btn1:
                submit_button = st.form_submit_button("➕ Add Reference", use_container_width=True)
        
        # Process form submission outside the form to avoid Streamlit form refresh issues
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
                st.success(f"Reference '{title}' added successfully!")
                st.rerun()
            else:
                st.error("Title and URL are required fields.")
    
    # Admin view of references with edit buttons
    st.markdown('<p class="section-header">Manage References</p>', unsafe_allow_html=True)
    
    if st.session_state['references']:
        for i, ref in enumerate(st.session_state['references']):
            with st.expander(f"📌 {ref['title']}", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**Type:** {ref['type']}")
                    st.markdown(f"**Description:** {ref['description']}")
                    st.markdown(f"**URL:** [{ref['url']}]({ref['url']})")
                    
                    col_meta1, col_meta2 = st.columns(2)
                    with col_meta1:
                        st.markdown(f"**Added:** {ref['date']}")
                    with col_meta2:
                        if ref.get('updated'):
                            st.markdown(f"**Updated:** {ref['updated']}")
                
                with col2:
                    # Action buttons
                    st.button("✏️ Edit", key=f"edit_{i}", use_container_width=True, on_click=lambda id=ref.get('id'): set_edit_id(id))
                    st.button("🗑️ Delete", key=f"del_{i}", use_container_width=True, on_click=lambda i=i: delete_reference(i))
    else:
        st.info("No references have been added yet.")

# Function to set edit ID
def set_edit_id(id):
    st.session_state['edit_id'] = id
    st.rerun()

# Function to delete reference
def delete_reference(index):
    st.session_state['references'].pop(index)
    save_references(st.session_state['references'])
    st.success("Reference deleted successfully!")
    st.rerun()

# Public view section - always shown
st.markdown('<p class="section-header">M8 Course Presentation References</p>', unsafe_allow_html=True)

if st.session_state['references']:
    # Add search functionality
    search_query = st.text_input("🔍 Search references", "")
    
    # Filter references based on search query
    filtered_refs = st.session_state['references']
    if search_query:
        filtered_refs = [ref for ref in st.session_state['references'] 
                         if search_query.lower() in ref['title'].lower() or 
                            search_query.lower() in ref['description'].lower() or
                            search_query.lower() in ref['type'].lower()]
    
    # Display reference count
    st.write(f"Showing {len(filtered_refs)} references")
    
    # Display references in a more visually appealing way
    for i, ref in enumerate(filtered_refs):
        with st.expander(f"📌 {ref['title']}", expanded=False):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"<p><strong>Type:</strong> {ref['type']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='ref-description'><strong>Description:</strong> {ref['description']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p><strong>URL:</strong> <a href='{ref['url']}' target='_blank'>{ref['url']}</a></p>", unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"<p class='ref-meta'><strong>Added:</strong> {ref['date']}</p>", unsafe_allow_html=True)
                if ref.get('updated'):
                    st.markdown(f"<p class='ref-meta'><strong>Updated:</strong> {ref['updated']}</p>", unsafe_allow_html=True)
                
                # Download button for URL content (This is just a visual element, would need more code to implement)
                if st.button("🔗 Visit Link", key=f"url_{i}"):
                    st.markdown(f"<script>window.open('{ref['url']}', '_blank');</script>", unsafe_allow_html=True)
else:
    st.info("No references available yet. Please check back later or contact the administrator to add references.")

# Footer
st.markdown('<p class="footer">© 2025 | EMA Patient Engagement References Tool | Developed for academic purposes</p>', unsafe_allow_html=True)