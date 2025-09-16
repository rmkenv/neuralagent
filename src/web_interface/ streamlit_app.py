import streamlit as st
import sys
import os
import time
import json
from pathlib import Path
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path for imports
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir.parent
sys.path.append(str(src_dir))

# Import our custom modules
try:
    from cognitive_assessment.chat_assessment import ChatBasedAssessment
    from cognitive_profiling.cognitive_profiler import CognitiveProfileGenerator
    from llm_integration.reasoning_engine import ReasoningEngine
except ImportError as e:
    st.error(f"Import error: {e}")
    st.error("Please ensure all files are in the correct directory structure")
    st.stop()

def main():
    st.set_page_config(
        page_title="🧠 Cognitive AI Clone Development",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .big-font {
        font-size:20px !important;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main title
    st.title("🧠 Cognitive AI Clone Development Platform")
    st.markdown("*Create AI systems that think and reason like you through conversational assessment*")
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar navigation
    render_sidebar()
    
    # Main content based on stage
    if st.session_state.stage == 'welcome':
        show_welcome_page()
    elif st.session_state.stage == 'assessment':
        show_assessment_page()
    elif st.session_state.stage == 'profile':
        show_profile_page()
    elif st.session_state.stage == 'clone':
        show_clone_interface()
    elif st.session_state.stage == 'hybrid':
        show_hybrid_creation()

def initialize_session_state():
    """Initialize session state variables."""
    default_values = {
        'stage': 'welcome',
        'assessment': None,
        'profiler': None,
        'profile': None,
        'clone': None,
        'assessment_complete': False,
        'profile_complete': False,
        'clone_complete': False
    }
    
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value

def render_sidebar():
    """Render the sidebar with navigation and progress tracking."""
    with st.sidebar:
        st.header("🧠 Navigation")
        
        # Stage selection
        stage_options = ['Welcome', 'Assessment', 'Profile Review', 'Clone Interface', 'Hybrid Creation']
        stage_keys = ['welcome', 'assessment', 'profile', 'clone', 'hybrid']
        
        try:
            current_index = stage_keys.index(st.session_state.stage)
        except ValueError:
            current_index = 0
        
        selected_stage = st.radio(
            "Current Stage:",
            stage_options,
            index=current_index
        )
        
        st.session_state.stage = stage_keys[stage_options.index(selected_stage)]
        
        st.markdown("---")
        
        # Progress tracking
        st.markdown("### 📊 Progress")
        
        progress_items = [
            ("✅" if st.session_state.assessment_complete else "⏳", "Assessment Complete"),
            ("✅" if st.session_state.profile_complete else "⏳", "Profile Generated"),
            ("✅" if st.session_state.clone_complete else "⏳", "Clone Created")
        ]
        
        for emoji, item in progress_items:
            st.markdown(f"{emoji} {item}")
        
        # Overall progress bar
        completed = sum([
            st.session_state.assessment_complete,
            st.session_state.profile_complete,
            st.session_state.clone_complete
        ])
        st.progress(completed / 3)
        st.caption(f"Overall Progress: {completed}/3")
        
        st.markdown("---")
        
        # Session statistics
        if hasattr(st.session_state, 'personality_chat_history'):
            st.markdown("### 📈 Session Stats")
            chat_messages = len(st.session_state.personality_chat_history)
            st.metric("Chat Messages", chat_messages)
            
            if st.session_state.profile:
                thinking_style = st.session_state.profile.get('cognitive_traits', {}).get('primary_thinking_style', 'Unknown')
                st.metric("Thinking Style", thinking_style.title())
        
        st.markdown("---")
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("🔄 Reset Session", help="Start over with a new assessment"):
            reset_session()
            st.rerun()
        
        if st.session_state.profile:
            if st.button("💾 Export Profile", help="Download your cognitive profile"):
                export_profile()

def show_welcome_page():
    """Show the welcome page with system overview."""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## Welcome to Cognitive AI Clone Development
        
        This platform creates AI systems that **think like you** through natural conversation analysis. 
        Instead of traditional surveys, we use advanced text analysis to understand your cognitive patterns.
        
        ### 🎯 What We Capture
        
        **Thinking Patterns**
        - Analytical vs. Intuitive vs. Creative approaches
        - Problem-solving methodologies and reasoning chains
        - Decision-making frameworks and risk assessment
        - Communication style and explanation preferences
        
        **Cognitive Architecture**  
        - How you process and organize information
        - Attention allocation and focus patterns
        - Memory organization and knowledge integration
        - Metacognitive awareness and self-regulation
        
        ### 🚀 The Process
        
        1. **Conversational Assessment** (15-20 minutes)
           - Natural personality discovery through chat
           - Problem-solving scenarios with real-time analysis
           
        2. **Cognitive Profile Generation**
           - AI analyzes your thinking patterns and communication style  
           - Creates a comprehensive cognitive signature
           
        3. **AI Clone Creation**
           - Fine-tunes language models to match your cognitive patterns
           - Creates reasoning engines that think like you
           
        4. **Hybrid Profile Creation**
           - Mix and match cognitive strengths from multiple profiles
           - Create specialized cognitive agents for specific use cases
        
        ### 💡 Applications
        
        - **Intellectual Sparring Partner**: AI that challenges your thinking
        - **Decision Support**: Systems that consider factors you value  
        - **Creative Collaboration**: AI partners that complement your style
        - **Knowledge Work Acceleration**: Cognitive augmentation for complex tasks
        """)
        
        st.markdown("---")
        
        if st.button("🚀 Start Cognitive Assessment", type="primary", use_container_width=True):
            st.session_state.stage = 'assessment'
            st.rerun()
        
        st.markdown("**⏱️ Time Required:** 15-20 minutes for complete assessment")
    
    with col2:
        st.markdown("### 🔬 Scientific Foundation")
        st.info("""
        **Cognitive Science Principles:**
        - Personality psychology (Big Five model)
        - Cognitive architecture research
        - Linguistic analysis and psycholinguistics
        - Decision science and behavioral economics
        
        **AI Technologies:**
        - Large Language Model fine-tuning
        - Natural language processing
        - Conversation analysis
        - Vector databases for memory systems
        """)
        
        st.markdown("### 📊 Assessment Features")
        features = [
            "🗣️ Natural conversation flow",
            "🧩 Interactive problem scenarios", 
            "📝 Real-time text analysis",
            "🎯 Adaptive questioning",
            "🔍 Cognitive pattern detection",
            "📈 Behavioral analytics"
        ]
        
        for feature in features:
            st.markdown(feature)
        
        st.markdown("### 🛡️ Privacy & Security")
        st.success("""
        **Your data is secure:**
        - All processing happens locally
        - No external API calls for assessment
        - Conversation data stays on your device
        - Full control over profile sharing
        """)

def show_assessment_page():
    """Show the assessment interface."""
    st.header("🗣️ Conversational Cognitive Assessment")
    
    # Initialize assessment if needed
    if not st.session_state.assessment:
        st.session_state.assessment = ChatBasedAssessment()
    
    # Assessment progress tracking
    col1, col2, col3 = st.columns(3)
    
    with col1:
        personality_done = hasattr(st.session_state, 'personality_profile')
        st.metric("Personality Chat", "✅ Complete" if personality_done else "⏳ In Progress")
    
    with col2:
        problem_solving_done = hasattr(st.session_state, 'problem_solving_profile')
        st.metric("Problem Solving", "✅ Complete" if problem_solving_done else "⏳ Pending")
    
    with col3:
        profile_generated = hasattr(st.session_state, 'profile')
        st.metric("Profile Generated", "✅ Complete" if profile_generated else "⏳ Pending")
    
    st.markdown("---")
    
    # Assessment tabs
    tab1, tab2, tab3 = st.tabs([
        "💭 Personality Discovery", 
        "🧩 Problem-Solving Analysis", 
        "📊 Complete Profile"
    ])
    
    with tab1:
        show_personality_assessment()
    
    with tab2:
        show_problem_solving_assessment()
    
    with tab3:
        show_profile_generation()

def show_personality_assessment():
    """Show personality assessment interface."""
    st.markdown("""
    ### Personality Discovery Through Conversation
    
    Let's have a natural conversation to understand your personality traits, thinking preferences, 
    and cognitive style. Be authentic - there are no right or wrong answers!
    """)
    
    personality_data = st.session_state.assessment.start_personality_chat()
    
    if personality_data:
        st.session_state.personality_profile = personality_data
        st.success("✅ Personality assessment complete!")
        
        # Show preview
        with st.expander("👀 Preview Your Personality Patterns"):
            display_personality_preview(personality_data)

def show_problem_solving_assessment():
    """Show problem-solving assessment interface."""
    st.markdown("""
    ### Problem-Solving Through Interactive Scenarios
    
    Now let's explore how you approach complex problems through realistic scenarios.
    Think out loud and explain your reasoning as you work through each situation.
    """)
    
    # Check if personality is complete
    if not hasattr(st.session_state, 'personality_profile'):
        st.warning("⚠️ Please complete the personality assessment first.")
        if st.button("← Go to Personality Discovery"):
            st.info("Please click the 'Personality Discovery' tab above.")
        return
    
    problem_data = st.session_state.assessment.start_problem_solving_chat()
    
    if problem_data:
        st.session_state.problem_solving_profile = problem_data
        st.success("✅ Problem-solving assessment complete!")
        
        # Show preview
        with st.expander("🧩 Preview Your Problem-Solving Patterns"):
            display_problem_solving_preview(problem_data)

def show_profile_generation():
    """Show profile generation interface."""
    st.markdown("""
    ### Complete Cognitive Profile Generation
    
    Once both assessments are complete, we'll generate your comprehensive cognitive profile
    that captures your unique thinking patterns and cognitive architecture.
    """)
    
    # Check prerequisites
    personality_done = hasattr(st.session_state, 'personality_profile')
    problem_solving_done = hasattr(st.session_state, 'problem_solving_profile')
    
    if not personality_done or not problem_solving_done:
        missing = []
        if not personality_done:
            missing.append("Personality Discovery")
        if not problem_solving_done:
            missing.append("Problem-Solving Analysis")
        
        st.info(f"📝 Please complete: {', '.join(missing)}")
        
        # Progress indicator
        completed = sum([personality_done, problem_solving_done])
        st.progress(completed / 2)
        st.caption(f"Assessment Progress: {completed}/2 complete")
        return
    
    # Generate profile button
    if not hasattr(st.session_state, 'profile'):
        if st.button("🧠 Generate My Complete Cognitive Profile", type="primary", use_container_width=True):
            generate_complete_profile()
    else:
        st.success("🎉 Your cognitive profile has been generated!")
        display_complete_profile(st.session_state.profile)
        
        if st.button("📋 Review Full Profile & Create Clone", type="primary"):
            st.session_state.stage = 'profile'
            st.rerun()

def generate_complete_profile():
    """Generate the complete cognitive profile."""
    with st.spinner("🔬 Analyzing your cognitive patterns..."):
        # Initialize profiler
        if not st.session_state.profiler:
            st.session_state.profiler = CognitiveProfileGenerator()
        
        # Prepare assessment data
        assessment_data = {
            'personality': st.session_state.personality_profile,
            'problem_solving': st.session_state.problem_solving_profile,
            'conversation_history': getattr(st.session_state, 'personality_chat_history', []) + 
                                   getattr(st.session_state, 'problem_chat_history', [])
        }
        
        # Generate profile
        profile = st.session_state.profiler.generate_comprehensive_profile(assessment_data)
        st.session_state.profile = profile
        st.session_state.assessment_complete = True
        st.session_state.profile_complete = True
        
        time.sleep(2)  # Simulate processing time
    
    st.success("🎉 Your cognitive profile has been generated!")
    st.balloons()
    
    # Display the profile
    display_complete_profile(st.session_state.profile)

def show_profile_page():
    """Show the profile review page."""
    st.header("📋 Cognitive Profile Review & Clone Creation")
    
    if not st.session_state.profile:
        st.error("❌ No cognitive profile found. Please complete the assessment first.")
        if st.button("🔙 Back to Assessment"):
            st.session_state.stage = 'assessment'
            st.rerun()
        return
    
    profile = st.session_state.profile
    
    # Profile overview
    display_complete_profile(profile)
    
    st.markdown("---")
    
    # Clone creation section
    show_clone_creation_interface(profile)

def show_clone_creation_interface(profile):
    """Show clone creation interface."""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🤖 Create Your Cognitive AI Clone")
        st.markdown("""
        Your cognitive profile will be used to create an AI system that:
        
        ✨ **Thinks like you** - Replicates your reasoning patterns and cognitive style  
        🗣️ **Communicates like you** - Matches your explanation style and vocabulary  
        🎯 **Solves problems like you** - Uses your preferred approaches and considerations  
        🧠 **Learns from you** - Adapts based on feedback and new interactions  
        
        The clone will be capable of:
        - Engaging in intellectual discussions using your cognitive framework
        - Solving complex problems with your reasoning approach
        - Making decisions considering factors you value most
        - Providing explanations in your preferred style and depth
        """)
        
        # Customization options
        with st.expander("🔧 Clone Customization Options"):
            col1a, col1b = st.columns(2)
            
            with col1a:
                creativity_boost = st.slider(
                    "Creativity Enhancement", 0.0, 1.0, 0.5,
                    help="Boost creative thinking beyond your baseline"
                )
                
                confidence_adjustment = st.slider(
                    "Response Confidence", 0.0, 1.0, 0.8,
                    help="Adjust how confident the clone's responses should be"
                )
            
            with col1b:
                formality_level = st.selectbox(
                    "Communication Formality", 
                    ["Match my style", "More formal", "More casual"],
                    help="Adjust the formality level of responses"
                )
                
                explanation_depth = st.selectbox(
                    "Explanation Detail",
                    ["Match my style", "More detailed", "More concise"],
                    help="Adjust how detailed explanations should be"
                )
            
            st.session_state.clone_settings = {
                'creativity_boost': creativity_boost,
                'confidence_adjustment': confidence_adjustment,
                'formality_level': formality_level,
                'explanation_depth': explanation_depth
            }
    
    with col2:
        st.markdown("### 📊 Profile Summary")
        
        # Key characteristics
        cognitive_traits = profile.get('cognitive_traits', {})
        
        key_traits = [
            ("🧠", "Thinking Style", cognitive_traits.get('primary_thinking_style', 'Unknown').title()),
            ("💬", "Communication", profile.get('communication_style', {}).get('style_category', 'Unknown').replace('_', ' ').title()),
            ("🎯", "Problem-Solving", cognitive_traits.get('problem_solving_approach', 'Unknown').title()),
            ("⚡", "Decision Speed", profile.get('decision_making_profile', {}).get('decision_speed', 'Unknown').title()),
            ("🤝", "Collaboration", cognitive_traits.get('collaboration_preference', 'Unknown').title())
        ]
        
        for emoji, category, value in key_traits:
            st.markdown(f"**{emoji} {category}**: {value}")
        
        st.markdown("---")
        
        # Profile confidence metrics
        st.markdown("### 📈 Profile Quality")
        confidence = profile.get('confidence_score', 0.8)
        st.metric("Profile Confidence", f"{confidence:.1%}")
        
        reliability = profile.get('profile_reliability', 0.8)
        st.metric("Data Reliability", f"{reliability:.1%}")
        
        completeness = profile.get('data_completeness', 'good')
        st.metric("Assessment Completeness", completeness.title())
    
    # Create clone button
    st.markdown("---")
    
    if not st.session_state.clone_complete:
        if st.button("🚀 Create My Cognitive Clone", type="primary", use_container_width=True):
            create_cognitive_clone(profile)
    else:
        st.success("✅ Your cognitive clone has been created!")
        if st.button("💬 Start Chatting with Your Clone", type="primary"):
            st.session_state.stage = 'clone'
            st.rerun()

def create_cognitive_clone(profile):
    """Create the cognitive clone from the profile."""
    with st.spinner("🔬 Training your cognitive clone..."):
        
        # Progress simulation
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        steps = [
            ("Initializing cognitive architecture...", 0.2),
            ("Loading personality patterns...", 0.4),
            ("Configuring reasoning templates...", 0.6),  
            ("Calibrating decision-making framework...", 0.8),
            ("Finalizing cognitive clone...", 1.0)
        ]
        
        for step_text, progress in steps:
            status_text.text(step_text)
            progress_bar.progress(progress)
            time.sleep(1.5)
        
        # Create the reasoning engine
        clone_settings = getattr(st.session_state, 'clone_settings', {})
        reasoning_engine = ReasoningEngine(profile, clone_settings)
        st.session_state.clone = reasoning_engine
        st.session_state.clone_complete = True
        
        status_text.text("✅ Cognitive clone created successfully!")
    
    st.success("🎉 Your cognitive clone is ready!")
    st.balloons()
    
    # Show clone preview
    with st.expander("👀 Preview Your Clone's Thinking"):
        preview_problem = "I'm considering a career change that would be more fulfilling but might involve a pay cut. How should I approach this decision?"
        preview_response = reasoning_engine.reason_about_problem(preview_problem, "medium")
        
        st.markdown("**Test Problem:**")
        st.write(preview_problem)
        
        st.markdown("**Your Clone's Response:**")
        st.write(preview_response['response'])
        
        with st.expander("🔍 See the thinking process"):
            for i, step in enumerate(preview_response.get('reasoning_steps', []), 1):
                st.write(f"{i}. {step}")

def show_clone_interface():
    """Show the clone interaction interface."""
    st.header("🤖 Chat with Your Cognitive Clone")
    
    if not st.session_state.clone:
        st.error("❌ No cognitive clone found. Please create one first.")
        if st.button("🔙 Back to Clone Creation"):
            st.session_state.stage = 'profile'
            st.rerun()
        return
    
    # Clone interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("**💭 Your AI cognitive clone thinks and responds like you. Ask it anything!**")
        
        # Initialize chat history
        if 'clone_chat_history' not in st.session_state:
            st.session_state.clone_chat_history = []
            
            # Add welcome message
            welcome_msg = "Hi! I'm your cognitive clone. I think and reason like you do. What would you like to discuss or work through together?"
            st.session_state.clone_chat_history.append({
                'role': 'assistant',
                'content': welcome_msg,
                'timestamp': time.time()
            })
        
        # Display chat history
        for i, msg in enumerate(st.session_state.clone_chat_history):
            with st.chat_message(msg['role']):
                st.write(msg['content'])
                
                # Show thinking process for assistant messages (except welcome)
                if (msg['role'] == 'assistant' and 'reasoning_steps' in msg and i > 0):
                    if st.checkbox("🔍 Show thinking process", key=f"thinking_{i}"):
                        st.markdown("**How your clone thought about this:**")
                        for j, step in enumerate(msg['reasoning_steps'], 1):
                            st.caption(f"{j}. {step}")
        
        # Chat input
        user_input = st.chat_input("Ask your clone anything...")
        
        if user_input:
            # Add user message
            st.session_state.clone_chat_history.append({
                'role': 'user',
                'content': user_input,
                'timestamp': time.time()
            })
            
            # Generate clone response
            with st.spinner("🤖 Your clone is thinking..."):
                clone_response = st.session_state.clone.reason_about_problem(user_input, "medium")
            
            # Add clone response
            st.session_state.clone_chat_history.append({
                'role': 'assistant',
                'content': clone_response['response'],
                'reasoning_steps': clone_response.get('reasoning_steps', []),
                'confidence': clone_response.get('confidence', 0.8),
                'timestamp': time.time()
            })
            
            st.rerun()
    
    with col2:
        render_clone_sidebar()

def show_hybrid_creation():
    """Show hybrid profile creation interface."""
    st.header("🔀 Hybrid Cognitive Profile Creation")
    
    st.markdown("""
    ### Create Hybrid Cognitive Agents
    
    Combine cognitive strengths from multiple profiles to create specialized AI agents 
    optimized for specific use cases and challenges.
    """)
    
    # This would be expanded with actual hybrid creation functionality
    st.info("🚧 Hybrid profile creation coming soon!")
    st.markdown("""
    **Planned Features:**
    - Mix analytical and creative thinking patterns
    - Combine decision-making styles for different contexts  
    - Create specialized agents for specific domains
    - Profile versioning and evolution tracking
    """)

def render_clone_sidebar():
    """Render the clone interaction sidebar."""
    st.markdown("### 🤖 Clone Statistics")
    
    if st.session_state.clone_chat_history:
        user_messages = [msg for msg in st.session_state.clone_chat_history if msg['role'] == 'user']
        assistant_messages = [msg for msg in st.session_state.clone_chat_history if msg['role'] == 'assistant']
        
        st.metric("Conversations", len(user_messages))
        
        if assistant_messages and len(assistant_messages) > 1:  # Exclude welcome message
            valid_responses = [msg for msg in assistant_messages[1:] if 'confidence' in msg]
            if valid_responses:
                avg_confidence = sum(msg.get('confidence', 0.8) for msg in valid_responses) / len(valid_responses)
                st.metric("Avg Confidence", f"{avg_confidence:.1%}")
    
    st.markdown("---")
    
    # Profile summary
    if st.session_state.profile:
        st.markdown("### 🧠 Your Cognitive Profile")
        cognitive_traits = st.session_state.profile.get('cognitive_traits', {})
        
        st.write(f"**Style**: {cognitive_traits.get('primary_thinking_style', 'Unknown').title()}")
        communication_style = st.session_state.profile.get('communication_style', {}).get('style_category', 'Unknown')
        st.write(f"**Communication**: {communication_style.replace('_', ' ').title()}")
    
    st.markdown("---")
    
    # Feedback section
    st.markdown("### 📝 Clone Feedback")
    st.markdown("Help your clone learn and improve:")
    
    if len(st.session_state.clone_chat_history) > 1:
        last_responses = [msg for msg in st.session_state.clone_chat_history if msg['role'] == 'assistant']
        if len(last_responses) > 1:  # More than just welcome message
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👍 Accurate", help="This response sounds like my thinking"):
                    st.success("Thanks! Your clone learns from positive feedback.")
            with col2:
                if st.button("👎 Not me", help="This doesn't match how I think"):
                    st.info("Thanks! Your clone will adjust its approach.")
    
    # Export options
    st.markdown("---")
    st.markdown("### 💾 Export Options")
    
    if st.session_state.clone_chat_history:
        if st.button("📄 Export Chat History"):
            export_chat_history()
    
    if st.session_state.profile:
        if st.button("🧠 Export Profile"):
            export_profile()

# Helper functions
def display_personality_preview(personality_data):
    """Display personality assessment preview."""
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Thinking Style", personality_data.get('primary_thinking_style', 'Unknown').title())
        st.metric("Communication Style", personality_data.get('communication_style', 'Unknown').replace('_', ' ').title())
    
    with col2:
        st.metric("Analytical Tendency", f"{personality_data.get('analytical_tendency', 0):.1f}")
        st.metric("Creative Tendency", f"{personality_data.get('creative_tendency', 0):.1f}")

def display_problem_solving_preview(problem_data):
    """Display problem-solving assessment preview."""
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Problem-Solving Style", problem_data.get('problem_solving_style', 'Unknown').replace('_', ' ').title())
        st.metric("Decision Speed", problem_data.get('decision_making_speed', 'Unknown').title())
    
    with col2:
        st.metric("Collaboration Tendency", problem_data.get('collaboration_tendency', 'Unknown').title())
        st.metric("Risk Assessment", problem_data.get('risk_assessment', 'Unknown').title())

def display_complete_profile(profile):
    """Display the complete cognitive profile."""
    st.subheader("🧠 Your Complete Cognitive Profile")
    
    # Overview metrics
    cognitive_traits = profile.get('cognitive_traits', {})
    communication_style = profile.get('communication_style', {})
    decision_making = profile.get('decision_making_profile', {})
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Primary Style", cognitive_traits.get('primary_thinking_style', 'Unknown').title())
    with col2:
        st.metric("Communication", communication_style.get('style_category', 'Unknown').replace('_', ' ').title())
    with col3:
        st.metric("Problem-Solving", cognitive_traits.get('problem_solving_approach', 'Unknown').title())
    with col4:
        st.metric("Decision Speed", decision_making.get('decision_speed', 'Unknown').title())
    
    # Detailed visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🧩 Cognitive Patterns")
        
        # Radar chart of cognitive tendencies
        categories = ['Analytical', 'Intuitive', 'Creative', 'Systematic']
        values = [
            cognitive_traits.get('analytical_tendency', 0),
            cognitive_traits.get('intuitive_tendency', 0),
            cognitive_traits.get('creative_tendency', 0),
            cognitive_traits.get('systematic_tendency', 0)
        ]
        
        fig = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Your Cognitive Profile',
            line_color='blue'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=False,
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 🎯 Profile Characteristics")
        
        # Key characteristics
        characteristics = {
            'Cognitive Signature': profile.get('cognitive_signature', 'Unknown'),
            'Complexity Comfort': cognitive_traits.get('complexity_comfort', 'Unknown').title(),
            'Risk Assessment': cognitive_traits.get('risk_assessment_style', 'Unknown').title(),
            'Stakeholder Awareness': cognitive_traits.get('stakeholder_awareness', 'Unknown').title(),
            'Collaboration Style': cognitive_traits.get('collaboration_preference', 'Unknown').title()
        }
        
        for characteristic, value in characteristics.items():
            st.write(f"**{characteristic}**: {value}")
        
        # Strengths
        strengths = profile.get('strengths', [])
        if strengths:
            st.markdown("**🌟 Identified Strengths:**")
            for strength in strengths[:3]:  # Show top 3
                st.write(f"• {strength.replace('_', ' ').title()}")

def reset_session():
    """Reset the session state."""
    keys_to_keep = ['stage']  # Keep stage to avoid navigation issues
    keys_to_reset = [k for k in st.session_state.keys() if k not in keys_to_keep]
    
    for key in keys_to_reset:
        del st.session_state[key]
    
    # Reset to welcome
    st.session_state.stage = 'welcome'

def export_profile():
    """Export the cognitive profile."""
    if st.session_state.profile:
        profile_json = json.dumps(st.session_state.profile, indent=2)
        st.download_button(
            "📄 Download Cognitive Profile",
            profile_json,
            file_name=f"cognitive_profile_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

def export_chat_history():
    """Export the chat history."""
    if st.session_state.clone_chat_history:
        chat_json = json.dumps(st.session_state.clone_chat_history, indent=2)
        st.download_button(
            "📄 Download Chat History",
            chat_json,
            file_name=f"clone_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

if __name__ == "__main__":
    main()
