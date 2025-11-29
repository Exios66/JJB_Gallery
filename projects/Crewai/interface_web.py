"""
CrewAI Streamlit Web Interface.
Provides a chat-like interface for interacting with Agent Swarms.
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Import config first to set up LLM environment
from config import config
from llm_config import configure_crewai_environment, get_setup_instructions

# Configure LLM provider on startup
configure_crewai_environment()

from main import run_analysis, get_crew_class
from router import MetaRouter

st.set_page_config(page_title="CrewAI Swarm Chat", page_icon="🤖", layout="wide")

st.title("🤖 CrewAI Multi-Agent Swarm Chat")
st.markdown("Interact with specialized AI agent swarms for ML, Research, Business, and more.")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    routing_mode = st.radio(
        "Routing Mode",
        ["Manual Selection", "Meta-Agent Router"],
        help="Choose 'Manual' to pick a swarm yourself, or 'Meta-Agent' to let AI decide."
    )
    
    if routing_mode == "Manual Selection":
        crew_options = [
            "ml", "research", "research_academic", "research_content",
            "business_intelligence", "dev_code", "documentation"
        ]
        selected_crew = st.selectbox("Select Swarm", crew_options)
    else:
        selected_crew = None
        st.info("Meta-Agent will analyze your message to pick the best swarm.")

    input_mode = st.radio(
        "Input Mode",
        ["Dynamic (Chat)", "Static (Default Workflow)"],
        help="Dynamic passes your message as the topic. Static runs the hardcoded default workflow."
    )

# Main Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Describe your task or topic..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Agents are working..."):
            try:
                # Determine Crew
                if routing_mode == "Meta-Agent Router":
                    status_placeholder = st.empty()
                    status_placeholder.info("🔄 Meta-Agent is routing your request...")
                    target_crew = MetaRouter.route_query(prompt)
                    status_placeholder.success(f"✅ Routed to: **{target_crew.replace('_', ' ').title()}**")
                else:
                    target_crew = selected_crew

                # Prepare Inputs
                inputs = {"topic": prompt} if input_mode == "Dynamic (Chat)" else None
                
                # Execute
                crew_class = get_crew_class(target_crew)
                crew = crew_class()
                result = crew.kickoff(inputs=inputs)
                
                st.markdown(f"### 🏁 Result from {target_crew.replace('_', ' ').title()} Swarm")
                st.markdown(str(result))
                
                st.session_state.messages.append({"role": "assistant", "content": str(result)})

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

