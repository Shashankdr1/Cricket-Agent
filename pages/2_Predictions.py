import streamlit as st
import base64
import os

# Page config
st.set_page_config(
    page_title="Cricket Predictions",
    page_icon="🔮",
    layout="centered"
)

from groq import Groq

def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img = get_base64_image("cricket.jpg")

st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpeg;base64,{img}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
[data-testid="stAppViewContainer"]::before {{
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: rgba(0, 0, 0, 0.82);
    z-index: 0;
}}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap');

* { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'DM Sans', sans-serif;
    color: white;
}
[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"] { display: none; }

.hero {
    text-align: center;
    padding: 2rem 0 0.5rem 0;
}
.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 900;
    background: linear-gradient(135deg, #ffffff 30%, #f9e04b 70%, #ffffff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.5rem 0;
}
.hero p {
    color: rgba(255,255,255,0.7);
    font-size: 0.95rem;
}
.badge {
    display: inline-block;
    background: linear-gradient(135deg, #4a1d96, #2d1b69);
    border: 1px solid #7c3aed;
    color: #c4b5fd;
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    padding: 0.35rem 0.9rem;
    border-radius: 2rem;
    margin-bottom: 1rem;
}
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.2rem;
    color: #f9e04b;
    margin: 1.5rem 0 0.8rem 0;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}
.prediction-box {
    background: linear-gradient(135deg, rgba(124,58,237,0.15), rgba(45,27,105,0.1));
    border: 1px solid #7c3aed;
    border-radius: 16px;
    padding: 1.5rem;
    margin-top: 1rem;
    position: relative;
    overflow: hidden;
}
.prediction-box h3 {
    color: #c4b5fd;
    font-size: 0.8rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin: 0 0 1rem 0;
}
.prediction-box p {
    color: white;
    line-height: 1.8;
    font-size: 0.95rem;
    margin: 0;
}
.divider {
    border: none;
    height: 1px;
    background: linear-gradient(to right, transparent, rgba(255,255,255,0.15), transparent);
    margin: 1.5rem 0;
}
footer {
    text-align: center;
    color: rgba(255,255,255,0.4);
    font-size: 0.75rem;
    padding: 2rem 0;
    letter-spacing: 0.1em;
}
.stSelectbox label { color: white !important; }
.stTextInput label { color: white !important; }
.stRadio label { color: white !important; }
</style>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero">
    <div class="badge">🔮 AI Predictions</div>
    <h1>Cricket Predictions</h1>
    <p>AI-powered match & player predictions</p>
</div>
""", unsafe_allow_html=True)

# Navigation
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<a href="/" target="_self"><button style="width:100%; padding:0.7rem; background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15); border-radius:10px; color:white; font-size:0.9rem; cursor:pointer;">💬 AI Chat</button></a>', unsafe_allow_html=True)
with col2:
    st.markdown('<a href="/Dashboard" target="_self"><button style="width:100%; padding:0.7rem; background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15); border-radius:10px; color:white; font-size:0.9rem; cursor:pointer;">📊 Dashboard</button></a>', unsafe_allow_html=True)
with col3:
    st.markdown('<a href="/Predictions" target="_self"><button style="width:100%; padding:0.7rem; background:rgba(124,58,237,0.35); border:1px solid #7c3aed; border-radius:10px; color:white; font-size:0.9rem; cursor:pointer;">🔮 Predictions</button></a>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

api_key = st.secrets.get("GROQ_API_KEY", "")

teams = ["India", "Australia", "England", "Pakistan", "New Zealand",
         "South Africa", "West Indies", "Sri Lanka", "Bangladesh", "Afghanistan"]

formats = ["T20I", "ODI", "Test"]

venues = ["Mumbai (Wankhede)", "Chennai (Chepauk)", "Kolkata (Eden Gardens)",
          "Melbourne (MCG)", "Lords (London)", "Sydney (SCG)",
          "Lahore (Gaddafi)", "Bridgetown (Kensington Oval)", "Cape Town (Newlands)",
          "Dubai (ICC Academy)"]

weather_options = ["Sunny & Dry", "Overcast & Humid", "Partly Cloudy", "Hot & Dry", "Cool & Windy"]

pitch_options = ["Flat Batting Pitch", "Green Seaming Pitch", "Dusty Spin Pitch", "Hard Bouncy Pitch", "Slow Low Pitch"]

def get_ai_prediction(prompt):
    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# ── 1. MATCH WINNER ────────────────────────────────
st.markdown('<div class="section-title">⚔️ Match Winner Prediction</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    team1 = st.selectbox("Team 1", teams, key="mw_t1")
with col2:
    team2 = st.selectbox("Team 2", [t for t in teams if t != team1], key="mw_t2")

col3, col4 = st.columns(2)
with col3:
    match_format = st.selectbox("Format", formats, key="mw_format")
with col4:
    venue = st.selectbox("Venue", venues, key="mw_venue")

if st.button("🔮 Predict Match Winner", key="btn_mw"):
    if not api_key:
        st.warning("⚠️ API key not found.")
    else:
        with st.spinner("Analyzing..."):
            prompt = f"""You are a cricket expert analyst. Predict the winner of this cricket match:
Team 1: {team1}
Team 2: {team2}
Format: {match_format}
Venue: {venue}

Provide:
1. Predicted Winner with confidence percentage
2. Key reasons (3 points)
3. Players to watch from each team
4. Predicted scorecard (approximate)
5. Important disclaimer that this is AI prediction only

Keep it concise and structured."""
            result = get_ai_prediction(prompt)
        st.markdown(f'<div class="prediction-box"><h3>🔮 Match Prediction</h3><p>{result.replace(chr(10), "<br>")}</p></div>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── 2. GROUND & WEATHER ANALYSIS ──────────────────
st.markdown('<div class="section-title">🌍 Ground & Weather Analysis</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    gw_venue = st.selectbox("Ground", venues, key="gw_venue")
    gw_weather = st.selectbox("Weather", weather_options, key="gw_weather")
with col2:
    gw_pitch = st.selectbox("Pitch Type", pitch_options, key="gw_pitch")
    gw_format = st.selectbox("Format", formats, key="gw_format")

if st.button("🌍 Analyse Conditions", key="btn_gw"):
    if not api_key:
        st.warning("⚠️ API key not found.")
    else:
        with st.spinner("Analyzing conditions..."):
            prompt = f"""You are a cricket pitch and conditions expert. Analyze these match conditions:
Ground: {gw_venue}
Weather: {gw_weather}
Pitch Type: {gw_pitch}
Format: {gw_format}

Provide a structured analysis:
1. Batting or Bowling first? (Toss decision recommendation)
2. Best type of bowler for these conditions:
   - Pace/Seam bowlers advantage (1-10)
   - Spin bowlers advantage (1-10)
   - Swing bowlers advantage (1-10)
3. Batting conditions (easy/medium/difficult)
4. Expected pitch behavior (early, middle, late overs)
5. Ideal team composition for these conditions

Be specific and practical."""
            result = get_ai_prediction(prompt)
        st.markdown(f'<div class="prediction-box"><h3>🌍 Conditions Analysis</h3><p>{result.replace(chr(10), "<br>")}</p></div>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── 3. PLAYER PERFORMANCE ─────────────────────────
st.markdown('<div class="section-title">🏏 Player Performance Predictor</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    player_name = st.text_input("Player Name", placeholder="e.g. Virat Kohli", key="pp_player")
    pp_format = st.selectbox("Format", formats, key="pp_format")
with col2:
    pp_opponent = st.selectbox("Opponent", teams, key="pp_opponent")
    pp_venue = st.selectbox("Venue", venues, key="pp_venue")

if st.button("🏏 Predict Performance", key="btn_pp"):
    if not api_key:
        st.warning("⚠️ API key not found.")
    elif not player_name:
        st.warning("⚠️ Please enter a player name.")
    else:
        with st.spinner("Predicting..."):
            prompt = f"""You are a cricket analyst. Predict the performance of {player_name} in the upcoming match:
Format: {pp_format}
Opponent: {pp_opponent}
Venue: {pp_venue}

Provide:
1. Predicted runs (if batsman) OR wickets (if bowler) OR both (if allrounder)
2. Historical performance vs this opponent (approximate)
3. Form analysis
4. Key strengths and weaknesses in these conditions
5. Confidence level (%)
6. Disclaimer that this is AI prediction only

Be specific and use cricket knowledge."""
            result = get_ai_prediction(prompt)
        st.markdown(f'<div class="prediction-box"><h3>🏏 Player Prediction</h3><p>{result.replace(chr(10), "<br>")}</p></div>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── 4. TOURNAMENT WINNER ──────────────────────────
st.markdown('<div class="section-title">🏆 Tournament Winner Predictor</div>', unsafe_allow_html=True)

tournament = st.selectbox("Select Tournament", [
    "ICC T20 World Cup 2026", "IPL 2025", "ICC ODI World Cup 2027",
    "ICC Champions Trophy 2025", "The Ashes 2025", "BBL 2025"
], key="tw_tournament")

if st.button("🏆 Predict Tournament Winner", key="btn_tw"):
    if not api_key:
        st.warning("⚠️ API key not found.")
    else:
        with st.spinner("Analyzing tournament..."):
            prompt = f"""You are a cricket expert. Predict the winner of {tournament}.

Provide:
1. Top 3 contenders with win probability %
2. Dark horse team (unexpected contender)
3. Key players who will be decisive
4. Why the predicted winner will win
5. Biggest threat to the favorites
6. Important disclaimer that this is AI prediction only

Be analytical and specific."""
            result = get_ai_prediction(prompt)
        st.markdown(f'<div class="prediction-box"><h3>🏆 Tournament Prediction</h3><p>{result.replace(chr(10), "<br>")}</p></div>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── 5. BEST XI SELECTOR ───────────────────────────
st.markdown('<div class="section-title">👥 Best XI Team Selector</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    xi_team = st.selectbox("Select Team", teams, key="xi_team")
    xi_format = st.selectbox("Format", formats, key="xi_format")
with col2:
    xi_opponent = st.selectbox("Opponent", [t for t in teams if t != xi_team], key="xi_opponent")
    xi_conditions = st.selectbox("Pitch Conditions", pitch_options, key="xi_conditions")

if st.button("👥 Select Best XI", key="btn_xi"):
    if not api_key:
        st.warning("⚠️ API key not found.")
    else:
        with st.spinner("Selecting best XI..."):
            prompt = f"""You are a cricket selector. Pick the best playing XI for {xi_team} against {xi_opponent}:
Format: {xi_format}
Pitch Conditions: {xi_conditions}

Provide:
1. Best XI with batting order
2. Role of each player (opener, middle order, all-rounder, spinner, pacer)
3. Why this combination for these conditions
4. Captain and Vice-captain recommendation
5. Bowling attack breakdown
6. Note that player availability may have changed

Be specific with current/recent players."""
            result = get_ai_prediction(prompt)
        st.markdown(f'<div class="prediction-box"><h3>👥 Best XI Selection</h3><p>{result.replace(chr(10), "<br>")}</p></div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<hr class="divider">
<footer>CRICKET AGENT · RAG POWERED · 2026 · Built by Shashank D R</footer>
""", unsafe_allow_html=True)