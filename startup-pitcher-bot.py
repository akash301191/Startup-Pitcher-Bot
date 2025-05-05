import re
import streamlit as st
from agno.agent import Agent
from agno.tools.serpapi import SerpApiTools
from agno.models.openai import OpenAIChat

from textwrap import dedent

def render_sidebar():
    st.sidebar.title("🔐 API Configuration")
    st.sidebar.markdown("---")

    # OpenAI API Key input
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://platform.openai.com/account/api-keys)."
    )
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
        st.sidebar.success("✅ OpenAI API key updated!")

    # SerpAPI Key input
    serp_api_key = st.sidebar.text_input(
        "Serp API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://serpapi.com/manage-api-key)."
    )
    if serp_api_key:
        st.session_state.serp_api_key = serp_api_key
        st.sidebar.success("✅ Serp API key updated!")

    st.sidebar.markdown("---")

def render_startup_pitch_requirements():
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    # Column 1: Startup Overview
    with col1:
        st.subheader("🚀 Startup Overview")
        name = st.text_input("Startup Name*", placeholder="e.g., EcoFuel")
        one_liner = st.text_area("One-Line Pitch*", placeholder="e.g., EcoFuel turns waste oils into affordable, clean fuel.")
        stage = st.selectbox("Startup Stage*", ["Idea only", "MVP built", "Beta launch", "Revenue-generating", "Funded"])
        pitch_length = st.selectbox(
            "Pitch Length*",
            [
                "1-slide elevator pitch",
                "3-slide summary",
                "5-slide mini deck",
                "7-slide concise deck",
                "10-slide full pitch",
                "15-slide extended deck",
                "20-slide comprehensive deck",
            ], index=4
        )

    # Column 2: Market & Product
    with col2:
        st.subheader("📊 Market & Product")
        problem = st.text_area("Problem You're Solving*", placeholder="e.g., High cost and pollution from traditional fuels")
        solution = st.text_area("Your Core Solution*", placeholder="e.g., We use a patented cold-process tech to refine used cooking oil.")
        target_market = st.text_input("Target Customers*", placeholder="e.g., Urban logistics fleets, restaurants")

    # Column 3: Business & Pitch Goals
    with col3:
        st.subheader("🎯 Business & Pitch Goals")
        differentiator = st.text_area("What Makes You Unique?*", placeholder="e.g., Our process is cheaper and emission-free")
        business_model = st.text_area("How Will You Make Money?*", placeholder="e.g., Fuel subscriptions, processing-as-a-service")
        pitch_purpose = st.selectbox("Purpose of Pitch*", ["Investor deck", "Demo Day", "Elevator pitch", "Grant application", "Team onboarding"])


    # Compile profile string
    startup_pitch_preferences = f"""
**Startup Overview:**
- Name: {name}
- One-liner: {one_liner}
- Stage: {stage}

**Market & Product:**
- Problem: {problem}
- Solution: {solution}
- Target Market: {target_market}

**Business & Pitch Goals:**
- Unique Selling Point: {differentiator}
- Business Model: {business_model}
- Pitch Purpose: {pitch_purpose}
- Pitch Length: {pitch_length}
"""

    return startup_pitch_preferences

def generate_startup_pitch(startup_pitch_preferences: str) -> str:
    # Step 1: Invoke the startup research agent
    startup_research_agent = Agent(
        name="Startup Researcher",
        role="Finds real-world startup pitch examples, market trends, and positioning strategies based on user-defined startup requirements.",
        model=OpenAIChat(id='gpt-4o', api_key=st.session_state.openai_api_key),
        description=dedent("""
            You are a startup pitch research expert. Given a user's detailed startup preferences, your job is to search the web
            and extract relevant pitch strategies, successful examples, or domain-specific positioning ideas that can inspire a compelling pitch.
        """),
        instructions=[
            "Carefully analyze the user's startup pitch preferences including problem, solution, target market, and pitch purpose.",
            "Generate ONE clear, concise search query (e.g., 'MVP pitch deck for water-saving IoT startup' or 'successful elevator pitch examples in healthtech').",
            "Avoid adding too many terms in the search query — keep it focused on one intent.",
            "Use `search_google` with this generated query.",
            "From the search results, extract 8–10 of the most relevant URLs or summaries that contain useful pitch examples, formats, or strategic messaging.",
            "Prefer pages with actual pitch decks, pitch breakdowns, founder stories, or VC-backed pitch templates.",
            "Do not generate or invent sample content. Rely only on real content from the search results.",
        ],
        tools=[SerpApiTools(api_key=st.session_state.serp_api_key)],
        add_datetime_to_instructions=True,
    )

    research_response = startup_research_agent.run(startup_pitch_preferences)
    research_results = research_response.content

    pitcher_agent = Agent(
        name="Startup Pitcher",
        role="Generates a tailored startup pitch deck using user input and real-world examples from research results.",
        model=OpenAIChat(id="o3-mini", api_key=st.session_state.openai_api_key),
        description=dedent("""
            You are a senior pitch strategist. You help early-stage startups craft compelling, clear, and persuasive pitch decks.
            You are provided:
            1. A structured summary of the startup's details (problem, solution, audience, USP, etc.)
            2. A list of URLs or research insights from the web that contain pitch examples, strategies, or relevant inspiration
            3. The user’s preferred pitch length (1-slide, 3-slide, 5-slide, 7-slide, 10-slide, 15-slide, or 20-slide)

            Your job is to extract relevant guidance from those sources and turn the startup’s idea into a properly structured pitch.
        """),
        instructions=[
            "Carefully read the startup's structured input: problem, solution, audience, USP, business model, and pitch purpose.",
            "Also review the research results and extract useful pitch tactics, templates, or real-world phrasing aligned to the startup domain.",
            "Use the user's selected pitch length to determine how many slides to generate. Follow this mapping:",
            "  - 1-slide: Single paragraph summary covering all essentials.",
            "  - 3-slide: The Big Idea, Problem + Solution, Ask.",
            "  - 5-slide: Big Idea, Problem, Solution, Market + Model, Ask.",
            "  - 7-slide: Problem, Solution, Market, Model, Traction, Vision, Ask.",
            "  - 10-slide: Full investor deck: Idea, Problem, Solution, Market, Model, Traction, Competitive Advantage, Vision, Team, Ask.",
            "  - 15-slide: Includes detailed GTM, Partnerships, Metrics, Risks, Roadmap, and Impact.",
            "  - 20-slide: Fully detailed pitch with intro hook, vision narrative, ecosystem map, expanded GTM, team bios, milestones, and appendix.",
            "",
            "Generate the output using markdown formatting:",
            "### Slide X: [Slide Title]",
            "- Followed by bullets or 2–3 sentence paragraph(s)",
            "- Use real ideas or examples from research when relevant (do NOT fabricate)",
            "- Maintain clarity, confidence, and alignment with pitch tone and purpose.",
            "",
            "Do not make your slides too verbose or complex. Use short sentences for individual bullet points",
            "Do not include an intro. Start directly with Slide 1."
        ],
        add_datetime_to_instructions=True
    )

    pitch_input = f"""
    Startup Pitch Preferences:
    {startup_pitch_preferences}

    Research Results:
    {research_results}
    """

    response = pitcher_agent.run(pitch_input)
    pitch_deck = response.content    

    return pitch_deck

def render_pitch_columns(pitch_deck: str) -> None:

    # Match and extract slide blocks: (title, content)
    pattern = r"### Slide (\d+): (.+?)\n(.+?)(?=(?:\n### Slide \d+:|\Z))"
    matches = re.findall(pattern, pitch_deck, re.DOTALL)

    # Combine title and body properly
    slides = [
        f"### Slide {num}: {title.strip()}\n{content.strip()}"
        for num, title, content in matches
    ]

    # Arrange in 2 columns
    col1, col2 = st.columns(2)

    for i, slide in enumerate(slides):
        if i % 2 == 0:
            with col1:
                st.markdown(slide, unsafe_allow_html=True)
        else:
            with col2:
                st.markdown(slide, unsafe_allow_html=True)

def main() -> None:
    # Page config
    st.set_page_config(page_title="Startup Pitcher Bot", page_icon="🚀", layout="wide")

    # Custom styling
    st.markdown(
        """
        <style>
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        div[data-testid="stTextInput"] {
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Header and intro
    st.markdown("<h1 style='font-size: 2.5rem;'>🚀 Startup Pitcher Bot</h1>", unsafe_allow_html=True)
    st.markdown(
        "Welcome to Startup Pitcher Bot — a Streamlit-powered assistant that simplifies your startup story by learning from top pitch templates and web trends, delivering clear, persuasive pitch drafts that align with your goals.",
        unsafe_allow_html=True
    )

    render_sidebar()
    startup_pitch_preferences = render_startup_pitch_requirements()
    
    st.markdown("---")

    if st.button("🎯 Generate Startup Pitch"):
        if not hasattr(st.session_state, "openai_api_key"):
            st.error("Please provide your OpenAI API key in the sidebar.")
        elif not hasattr(st.session_state, "serp_api_key"):
            st.error("Please provide your SerpAPI key in the sidebar.")
        else:
            with st.spinner("Crafting your customized startup pitch deck..."):
                pitch_deck = generate_startup_pitch(startup_pitch_preferences=startup_pitch_preferences)
                st.session_state.pitch_deck = pitch_deck

    if "pitch_deck" in st.session_state:
        st.markdown("## 🧾 Your Startup Pitch Deck")
        render_pitch_columns(st.session_state.pitch_deck)
        st.markdown("---")

        st.download_button(
            label="📥 Download Pitch Deck",
            data=st.session_state.pitch_deck,
            file_name="startup_pitch_deck.txt",
            mime="text/plain"
        )

if __name__  == "__main__": 
    main()