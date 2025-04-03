import streamlit as st
import base64
import os
import app.config as config

def get_base64_of_bin_file(bin_file):
    """Get base64 encoding of binary file"""
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background():
    """Set the background image with darken blend mode"""
    try:
        bin_str = get_base64_of_bin_file(config.BACKGROUND_IMAGE)
        page_bg_img = '''
        <style>
        .stApp::before {
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: url("data:image/png;base64,%s");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            filter: brightness(0.4) contrast(1.2);
            mix-blend-mode: darken;
            z-index: -1;
        }
        
        .stApp {
            background-color: rgba(0, 0, 0, 0.85);
        }
        </style>
        ''' % bin_str
        st.markdown(page_bg_img, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error setting background: {e}")
        # Fallback to gradient background
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(to bottom, #0a0a14, #1f1f36);
        }
        </style>
        """, unsafe_allow_html=True)

def apply_styling():
    """Apply all styling to the application"""
    # Set background
    set_background()
    
    # Apply CSS styles
    try:
        with open(os.path.join('app/utils/styles.css'), 'r') as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading CSS: {e}")
        # Fallback basic styling
        st.markdown("""
        <style>
        .main {
            background-color: rgba(10, 10, 18, 0.95);
            border-radius: 10px;
            padding: 20px;
        }
        .container {
            background-color: rgba(15, 15, 25, 0.97);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .header {
            color: #ffffff;
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 15px;
        }
        </style>
        """, unsafe_allow_html=True)