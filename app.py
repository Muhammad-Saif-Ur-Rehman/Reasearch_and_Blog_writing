import streamlit as st
import streamlit.components.v1 as components
import os
from pathlib import Path
import time
import base64
import html
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Blog Generator",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Dark Glassmorphism CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    /* Dark background */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        background-attachment: fixed;
        min-height: 100vh;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Glass card */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 2rem;
        margin: 1rem 0;
    }

    /* Title */
    .main-title {
        font-size: 2.8rem;
        font-weight: 700;
        color: #ffffff;
        text-align: center;
        margin-bottom: 0.3rem;
        letter-spacing: -0.5px;
    }

    .subtitle {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.4);
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
        letter-spacing: 0.5px;
    }

    /* Text input - remove all Streamlit containers */
    .stTextInput,
    .stTextInput > div,
    [data-testid="stTextInput"],
    [data-testid="stTextInput"] > div {
        background: transparent !important;
    }

    .stTextInput > div > div {
        background: transparent !important;
        border: none !important;
    }

    .stTextInput > label,
    .stTextInput > label *,
    [data-testid="stTextInput"] > label,
    [data-testid="stTextInput"] > label *,
    .stTextInput label[data-testid="stWidgetLabel"] {
        display: none !important;
        height: 0 !important;
        visibility: hidden !important;
        overflow: hidden !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    .stTextInput > div > div::before,
    .stTextInput > div > div::after {
        display: none !important;
    }

    /* Glassmorphism input */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.06) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
        font-size: 1rem !important;
        padding: 1rem 1.2rem !important;
        transition: all 0.3s ease !important;
    }

    .stTextInput > div > div > input:hover {
        border: 1px solid rgba(255, 255, 255, 0.18) !important;
        background: rgba(255, 255, 255, 0.08) !important;
    }

    .stTextInput > div > div > input:focus {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(108, 99, 255, 0.5) !important;
        box-shadow: 0 0 20px rgba(108, 99, 255, 0.15) !important;
        outline: none !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.3) !important;
        font-weight: 400 !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6c63ff 0%, #3b82f6 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-size: 0.95rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(108, 99, 255, 0.25);
        cursor: pointer;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(108, 99, 255, 0.35);
        background: linear-gradient(135deg, #5b52ff 0%, #2970e6 100%);
    }

    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 10px rgba(108, 99, 255, 0.2);
    }

    /* Blog content */
    .blog-content {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 2.5rem;
        margin: 1rem 0;
        color: rgba(255, 255, 255, 0.85);
        line-height: 1.8;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }

    .blog-content h1, .blog-content h2, .blog-content h3 {
        color: #ffffff;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
        font-weight: 600;
    }

    .blog-content h1 {
        font-size: 1.8rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 0.5rem;
    }

    .blog-content h2 {
        font-size: 1.4rem;
    }

    .blog-content h3 {
        font-size: 1.15rem;
    }

    .blog-content p {
        margin-bottom: 1rem;
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.75);
    }

    .blog-content ul, .blog-content ol {
        margin-bottom: 1rem;
        padding-left: 1.5rem;
        color: rgba(255, 255, 255, 0.75);
    }

    .blog-content li {
        margin-bottom: 0.4rem;
    }

    .blog-content code {
        background: rgba(108, 99, 255, 0.15);
        padding: 0.15rem 0.4rem;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        color: #a5b4fc;
    }

    .blog-content pre {
        background: rgba(0, 0, 0, 0.3);
        padding: 1rem;
        border-radius: 10px;
        overflow-x: auto;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    .blog-content a {
        color: #6c63ff;
        text-decoration: none;
    }

    .blog-content a:hover {
        text-decoration: underline;
    }

    .blog-content blockquote {
        border-left: 3px solid rgba(108, 99, 255, 0.5);
        padding-left: 1rem;
        margin: 1rem 0;
        color: rgba(255, 255, 255, 0.6);
        font-style: italic;
    }

    /* Info box */
    .info-box {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        color: rgba(255, 255, 255, 0.5);
        margin: 1.5rem 0;
        border-left: 3px solid rgba(108, 99, 255, 0.4);
        line-height: 1.8;
        font-size: 0.9rem;
    }

    .info-box strong {
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.95rem;
        display: block;
        margin-bottom: 0.4rem;
    }

    /* Topic header */
    .topic-header {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }

    .topic-header h2 {
        color: #ffffff;
        margin: 0;
        font-size: 1.2rem;
        font-weight: 600;
    }

    .topic-header p {
        color: rgba(255, 255, 255, 0.35);
        margin: 0.3rem 0 0 0;
        font-size: 0.85rem;
    }

    /* Input label */
    .input-label {
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.85rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Loading */
    .loading-text {
        color: rgba(255, 255, 255, 0.5);
        text-align: center;
        font-size: 0.95rem;
        margin: 1.5rem 0;
    }

    /* Column gap */
    .row-widget.stHorizontal {
        gap: 0.75rem;
    }

    /* Spinner */
    .stSpinner > div {
        border-top-color: #6c63ff !important;
    }

    /* Alerts */
    .stAlert, [data-baseweb="notification"] {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        color: rgba(255, 255, 255, 0.8) !important;
    }

    /* Success alert */
    .element-container:has(.stSuccess) [data-baseweb="notification"] {
        border-left: 3px solid #22c55e !important;
    }

    /* Error alert */
    .element-container:has(.stError) [data-baseweb="notification"] {
        border-left: 3px solid #ef4444 !important;
    }

    /* Footer */
    .footer-text {
        text-align: center;
        color: rgba(255, 255, 255, 0.2);
        font-size: 0.8rem;
        padding: 2rem 0 1rem 0;
        letter-spacing: 0.5px;
    }

    /* Streamlit elements override */
    .stMarkdown, .stMarkdown p {
        color: rgba(255, 255, 255, 0.8);
    }

    [data-testid="stVerticalBlock"] {
        gap: 0.5rem;
    }

    /* Download button styling - matches stButton gradient */
    .download-btn {
        display: inline-block;
        background: linear-gradient(135deg, #6c63ff 0%, #3b82f6 100%);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-size: 0.95rem;
        cursor: pointer;
        font-weight: 600;
        text-decoration: none;
        text-align: center;
        width: 100%;
        box-sizing: border-box;
        transition: all 0.3s ease;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 4px 20px rgba(108, 99, 255, 0.25);
        
    }

    .download-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(108, 99, 255, 0.35);
        background: linear-gradient(135deg, #5b52ff 0%, #2970e6 100%);
        color: white;
        text-decoration: none;
    }

    .download-btn:active {
        transform: translateY(0);
        box-shadow: 0 2px 10px rgba(108, 99, 255, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'blog_content' not in st.session_state:
    st.session_state.blog_content = None
if 'generated_topic' not in st.session_state:
    st.session_state.generated_topic = None

def run_blog_crew(topic: str) -> str:
    """Run the CrewAI blog generation crew"""
    try:
        from src.research_and_blog_crew.crew import ResearchAndBlogCrew

        # Prepare inputs
        inputs = {'topic': topic}

        # Run the crew
        crew = ResearchAndBlogCrew().crew()
        crew.kickoff(inputs=inputs)

        # Read the generated blog
        blog_path = Path("blogs/blog.md")
        if blog_path.exists():
            with open(blog_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return "Blog generation completed but output file not found."

    except Exception as e:
        return f"Error generating blog: {str(e)}"

def create_download_link(content: str, filename: str) -> str:
    """Create a download link for the blog content"""
    b64 = base64.b64encode(content.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}" class="download-btn">Download .md</a>'

# Header
st.markdown('<h1 class="main-title">AI Blog Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Powered by CrewAI</p>', unsafe_allow_html=True)

# Main container
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Input section
    # st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<p class="input-label">Topic</p>', unsafe_allow_html=True)

    topic = st.text_input(
        "topic",
        placeholder="What should we write about?",
        key="topic_input",
        label_visibility="collapsed"
    )

    st.markdown('<div style="height: 0.75rem;"></div>', unsafe_allow_html=True)
    generate_button = st.button("Generate Blog", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Info box
    if not st.session_state.blog_content:
        st.markdown("""
        <div class="info-box">
            <strong>How it works</strong>
            1. Enter a topic above<br>
            2. AI agents research and write a blog<br>
            3. Copy or download the result
        </div>
        """, unsafe_allow_html=True)

    # Generate blog
    if generate_button:
        if not topic or topic.strip() == "":
            st.error("Please enter a topic")
        else:
            with st.spinner("Generating..."):
                st.markdown('<p class="loading-text">Researching and writing...</p>', unsafe_allow_html=True)

                blog_content = run_blog_crew(topic)

                st.session_state.blog_content = blog_content
                st.session_state.generated_topic = topic

                st.success("Blog generated successfully")
                time.sleep(0.5)
                st.rerun()

    # Display blog
    if st.session_state.blog_content:
        # Topic header
        st.markdown(f"""
        <div class="topic-header">
            <h2>{html.escape(st.session_state.generated_topic)}</h2>
            <p>{datetime.now().strftime("%B %d, %Y")}</p>
        </div>
        """, unsafe_allow_html=True)

        # Blog content
        st.markdown('<div class="blog-content">', unsafe_allow_html=True)
        st.markdown(st.session_state.blog_content)
        st.markdown('</div>', unsafe_allow_html=True)

        # Action buttons
        col_copy, col_download, col_new = st.columns([1, 1, 1])

        with col_copy:
            if st.button("Copy to Clipboard", use_container_width=True, key="copy_btn"):
                encoded = base64.b64encode(st.session_state.blog_content.encode('utf-8')).decode('utf-8')
                copy_js = f"""
                <script>
                (function() {{
                    try {{
                        var encoded = "{encoded}";
                        var text = atob(encoded);
                        navigator.clipboard.writeText(text).then(
                            function() {{ console.log('Copied via clipboard API'); }},
                            function() {{
                                var ta = document.createElement('textarea');
                                ta.value = text;
                                ta.style.position = 'fixed';
                                ta.style.left = '-9999px';
                                document.body.appendChild(ta);
                                ta.select();
                                document.execCommand('copy');
                                document.body.removeChild(ta);
                                console.log('Copied via execCommand fallback');
                            }}
                        );
                    }} catch(e) {{
                        console.error('Copy failed:', e);
                    }}
                }})();
                </script>
                """
                components.html(copy_js, height=0)
                st.success("Copied to clipboard")

        with col_download:
            filename = f"blog_{st.session_state.generated_topic.replace(' ', '_')[:30]}_{datetime.now().strftime('%Y%m%d')}.md"
            st.markdown(create_download_link(st.session_state.blog_content, filename), unsafe_allow_html=True)

        with col_new:
            if st.button("New Blog", use_container_width=True):
                st.session_state.blog_content = None
                st.session_state.generated_topic = None
                st.rerun()

# Footer
st.markdown('<p class="footer-text">Built with Streamlit & CrewAI</p>', unsafe_allow_html=True)
