import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def generate_diagram(description, diagram_type):
    """Generate Mermaid diagram code from natural language."""
    prompt = f"""Convert this description into a Mermaid {diagram_type} diagram.
Return ONLY the Mermaid code, no explanations.

Description: {description}

Guidelines:
- For flowcharts: use 'graph TD' or 'graph LR'
- For sequence: use 'sequenceDiagram'
- For class: use 'classDiagram'
- Keep it clear and concise
"""
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=600
        )
        
        code = response.choices[0].message.content.strip()
        code = code.replace('```mermaid', '').replace('```', '').strip()
        return code
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="AI Diagram Generator", page_icon="🚀")

st.title("🚀 AI Diagram Generator")
st.markdown("Convert natural language into professional diagrams")

# Input controls
diagram_type = st.selectbox(
    "Diagram Type",
    ["flowchart", "sequence", "class"]
)

description = st.text_area(
    "Describe Your Process",
    placeholder="Example: A user logs in, the system validates credentials, if valid show dashboard, else show error message",
    height=100
)

if st.button("Generate Diagram", type="primary"):
    if description.strip():
        with st.spinner("🤖 AI is creating your diagram..."):
            mermaid_code = generate_diagram(description, diagram_type)
            
            if mermaid_code.startswith("Error:"):
                st.error(mermaid_code)
            else:
                st.code(mermaid_code, language="mermaid")
                st.markdown(f"```mermaid\n{mermaid_code}\n```")
    else:
        st.warning("Please enter a description")

# Footer
st.markdown("---")
st.markdown("**Examples:**")
st.markdown("- Flowchart: 'User registration process with email verification'")
st.markdown("- Sequence: 'User authenticates, server validates, return token'")
st.markdown("- Class: 'Blog system with User, Post, and Comment classes'")
