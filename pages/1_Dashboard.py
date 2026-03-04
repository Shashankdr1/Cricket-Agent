import streamlit as st
import fitz
import os
import plotly.express as px
import plotly.graph_objects as go
import base64

# Page config
st.set_page_config(
    page_title="Cricket Dashboard",
    page_icon="📊",
    layout="wide"
)

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
    background: linear-gradient(135deg, #2d6a4f, #1b4332);
    border: 1px solid #40916c;
    color: #95d5b2;
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
.player-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 0.5rem;
}
.player-card h3 {
    font-family: 'Playfair Display', serif;
    color: #f9e04b;
    margin: 0 0 0.3rem 0;
    font-size: 1.1rem;
}
.player-card p {
    color: rgba(255,255,255,0.7);
    font-size: 0.85rem;
    margin: 0.15rem 0;
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
div[data-baseweb="select"] { background: rgba(255,255,255,0.08) !important; }
</style>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero">
    <div class="badge">📊 Live Dashboard</div>
    <h1>Cricket Dashboard</h1>
    <p>Stats, Rankings & Tournament History</p>
</div>
""", unsafe_allow_html=True)

# Navigation
col1, col2 = st.columns(2)
with col1:
    st.markdown('<a href="/" target="_self"><button style="width:100%; padding:0.7rem; background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15); border-radius:10px; color:white; font-size:0.95rem; cursor:pointer;">💬 AI Chat</button></a>', unsafe_allow_html=True)
with col2:
    st.markdown('<a href="/Dashboard" target="_self"><button style="width:100%; padding:0.7rem; background:rgba(64,145,108,0.35); border:1px solid #40916c; border-radius:10px; color:white; font-size:0.95rem; cursor:pointer;">📊 Dashboard</button></a>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── TOURNAMENT FILTER ──────────────────────────────
st.markdown('<div class="section-title">🏆 Tournament Overview</div>', unsafe_allow_html=True)

tournament = st.selectbox("", ["All Formats", "ODI World Cup", "T20 World Cup", "IPL", "Test Cricket"], label_visibility="collapsed")

def chart_layout():
    return dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,0.04)',
        font=dict(color='white', family='DM Sans'),
        margin=dict(l=10, r=10, t=30, b=10),
        title_font=dict(color='#f9e04b', size=13)
    )

if tournament in ["All Formats", "ODI World Cup"]:
    col1, col2 = st.columns(2)
    with col1:
        wc_data = {
            "Team": ["Australia", "India", "West Indies", "Pakistan", "Sri Lanka", "England"],
            "Titles": [5, 3, 2, 1, 1, 1]
        }
        fig = px.pie(wc_data, values="Titles", names="Team",
                     title="🌍 ODI World Cup Titles",
                     color_discrete_sequence=["#FFD700", "#0057A8", "#7B3F00", "#006600", "#00D4FF", "#CF0A0A"])
        fig.update_layout(**chart_layout())
        fig.update_traces(textfont_color='white')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        odi_runs = {
            "Player": ["Sachin Tendulkar", "Ricky Ponting", "Sanath Jayasuriya", "Mahela Jayawardene", "Inzamam-ul-Haq"],
            "Runs": [18426, 13704, 13430, 12650, 11739]
        }
        fig2 = px.bar(odi_runs, x="Runs", y="Player", orientation='h',
                      title="🏏 ODI All-Time Top Run Scorers",
                      color="Runs",
                      color_continuous_scale=["#1b4332", "#40916c", "#f9e04b"])
        fig2.update_layout(**chart_layout(), coloraxis_showscale=False)
        fig2.update_xaxes(gridcolor='rgba(255,255,255,0.08)')
        fig2.update_yaxes(gridcolor='rgba(255,255,255,0.08)')
        st.plotly_chart(fig2, use_container_width=True)

if tournament in ["All Formats", "T20 World Cup"]:
    col3, col4 = st.columns(2)
    with col3:
        t20_data = {
            "Team": ["India", "England", "West Indies", "Australia", "Pakistan", "Sri Lanka"],
            "Titles": [2, 2, 2, 1, 1, 1]
        }
        fig3 = px.bar(t20_data, x="Team", y="Titles",
                      title="⚡ T20 World Cup Titles",
                      color="Titles",
                      color_continuous_scale=["#1b4332", "#40916c", "#f9e04b"])
        fig3.update_layout(**chart_layout(), coloraxis_showscale=False)
        fig3.update_xaxes(gridcolor='rgba(255,255,255,0.08)')
        fig3.update_yaxes(gridcolor='rgba(255,255,255,0.08)')
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        t20_runs = {
            "Player": ["Virat Kohli", "Rohit Sharma", "Martin Guptill", "Babar Azam", "David Warner"],
            "Runs": [4188, 4231, 3531, 3985, 3277]
        }
        fig4 = px.bar(t20_runs, x="Player", y="Runs",
                      title="🏏 T20I Top Run Scorers",
                      color="Runs",
                      color_continuous_scale=["#1b4332", "#40916c", "#f9e04b"])
        fig4.update_layout(**chart_layout(), coloraxis_showscale=False)
        fig4.update_xaxes(gridcolor='rgba(255,255,255,0.08)')
        fig4.update_yaxes(gridcolor='rgba(255,255,255,0.08)')
        st.plotly_chart(fig4, use_container_width=True)

if tournament in ["All Formats", "IPL"]:
    col5, col6 = st.columns(2)
    with col5:
        ipl_runs = {
            "Player": ["Virat Kohli", "Shikhar Dhawan", "Rohit Sharma", "David Warner", "AB de Villiers"],
            "Runs": [8161, 6769, 6628, 6397, 5162]
        }
        fig5 = px.bar(ipl_runs, x="Player", y="Runs",
                      title="🏏 IPL All-Time Top Run Scorers",
                      color="Runs",
                      color_continuous_scale=["#1b4332", "#40916c", "#f9e04b"])
        fig5.update_layout(**chart_layout(), coloraxis_showscale=False)
        fig5.update_xaxes(gridcolor='rgba(255,255,255,0.08)')
        fig5.update_yaxes(gridcolor='rgba(255,255,255,0.08)')
        st.plotly_chart(fig5, use_container_width=True)

    with col6:
        ipl_wickets = {
            "Player": ["Yuzvendra Chahal", "DJ Bravo", "Lasith Malinga", "Amit Mishra", "Piyush Chawla"],
            "Wickets": [221, 183, 170, 166, 157]
        }
        fig6 = px.bar(ipl_wickets, x="Wickets", y="Player", orientation='h',
                      title="🎯 IPL All-Time Top Wicket Takers",
                      color="Wickets",
                      color_continuous_scale=["#1b4332", "#ff6b35", "#f9e04b"])
        fig6.update_layout(**chart_layout(), coloraxis_showscale=False)
        fig6.update_xaxes(gridcolor='rgba(255,255,255,0.08)')
        fig6.update_yaxes(gridcolor='rgba(255,255,255,0.08)')
        st.plotly_chart(fig6, use_container_width=True)

if tournament in ["All Formats", "Test Cricket"]:
    col7, col8 = st.columns(2)
    with col7:
        teams = ["Australia", "India", "England", "New Zealand", "South Africa", "Pakistan", "Sri Lanka", "West Indies"]
        ratings = [128, 121, 110, 98, 95, 88, 75, 68]
        fig7 = px.bar(x=ratings, y=teams, orientation='h',
                      title="🏆 ICC Test Team Rankings",
                      color=ratings,
                      color_continuous_scale=["#1b4332", "#40916c", "#f9e04b"],
                      labels={"x": "Rating Points", "y": "Team"})
        fig7.update_layout(**chart_layout(), coloraxis_showscale=False)
        fig7.update_xaxes(gridcolor='rgba(255,255,255,0.08)')
        fig7.update_yaxes(gridcolor='rgba(255,255,255,0.08)')
        st.plotly_chart(fig7, use_container_width=True)

    with col8:
        legends = {
            "Player": ["Sachin Tendulkar", "Ricky Ponting", "Jacques Kallis", "Rahul Dravid", "Kumar Sangakkara", "Brian Lara"],
            "Runs": [15921, 13378, 13289, 13288, 12400, 11953],
            "Country": ["India", "Australia", "South Africa", "India", "Sri Lanka", "West Indies"]
        }
        fig8 = px.bar(legends, x="Player", y="Runs", color="Country",
                      title="👑 Legend Batsmen - Career Test Runs",
                      color_discrete_map={
                                "India": "#0057A8",
                                "Australia": "#FFD700",
                                "England": "#CF0A0A",
                                "Pakistan": "#006600",
                                "West Indies": "#7B3F00",
                                "New Zealand": "#000000",
                                "South Africa": "#FF69B4",
                                "Sri Lanka": "#00D4FF"
                            })
        fig8.update_layout(**chart_layout())
        fig8.update_xaxes(gridcolor='rgba(255,255,255,0.08)')
        fig8.update_yaxes(gridcolor='rgba(255,255,255,0.08)')
        st.plotly_chart(fig8, use_container_width=True)

# ── TEAM COMPARISON ────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-title">⚔️ Team Comparison</div>', unsafe_allow_html=True)

team_data = {
    "India":        {"ODI Titles": 3, "T20 Titles": 2, "Test Rating": 121, "WC Appearances": 13},
    "Australia":    {"ODI Titles": 5, "T20 Titles": 1, "Test Rating": 128, "WC Appearances": 13},
    "England":      {"ODI Titles": 1, "T20 Titles": 2, "Test Rating": 110, "WC Appearances": 13},
    "Pakistan":     {"ODI Titles": 1, "T20 Titles": 1, "Test Rating": 88,  "WC Appearances": 13},
    "West Indies":  {"ODI Titles": 2, "T20 Titles": 2, "Test Rating": 68,  "WC Appearances": 13},
    "New Zealand":  {"ODI Titles": 0, "T20 Titles": 0, "Test Rating": 98,  "WC Appearances": 13},
    "South Africa": {"ODI Titles": 0, "T20 Titles": 0, "Test Rating": 95,  "WC Appearances": 9},
    "Sri Lanka":    {"ODI Titles": 1, "T20 Titles": 1, "Test Rating": 75,  "WC Appearances": 13},
}

col1, col2 = st.columns(2)
with col1:
    team1 = st.selectbox("Select Team 1", list(team_data.keys()), index=0)
with col2:
    team2 = st.selectbox("Select Team 2", list(team_data.keys()), index=1)

if team1 and team2:
    categories = ["ODI Titles", "T20 Titles", "Test Rating", "WC Appearances"]
    t1_values = [team_data[team1][c] for c in categories]
    t2_values = [team_data[team2][c] for c in categories]

    fig_compare = go.Figure()
    team_colors = {
    "India": "#0057A8", "Australia": "#FFD700", "England": "#CF0A0A",
    "Pakistan": "#006600", "West Indies": "#7B3F00", "New Zealand": "#1a1a1a",
    "South Africa": "#FF69B4", "Sri Lanka": "#00D4FF"
        }
    fig_compare.add_trace(go.Bar(name=team1, x=categories, y=t1_values, marker_color=team_colors.get(team1, "#f9e04b")))
    fig_compare.add_trace(go.Bar(name=team2, x=categories, y=t2_values, marker_color=team_colors.get(team2, "#ff6b35")))

    fig_compare.update_layout(
        **chart_layout(),
        barmode='group',
        legend=dict(font=dict(color='white')),
        title=f"⚔️ {team1} vs {team2}"
    )
    fig_compare.update_xaxes(gridcolor='rgba(255,255,255,0.08)')
    fig_compare.update_yaxes(gridcolor='rgba(255,255,255,0.08)')
    st.plotly_chart(fig_compare, use_container_width=True)

# ── PLAYER SEARCH ──────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🔍 Player Search</div>', unsafe_allow_html=True)

players_db = {
    "Sachin Tendulkar": {"Country": "India", "Format": "All", "Runs": 34357, "Wickets": 201, "Matches": 664, "Role": "Batsman", "Era": "1989-2013"},
    "Virat Kohli":      {"Country": "India", "Format": "All", "Runs": 26000, "Wickets": 4,   "Matches": 500, "Role": "Batsman", "Era": "2008-Present"},
    "MS Dhoni":         {"Country": "India", "Format": "All", "Runs": 17266, "Wickets": 0,   "Matches": 538, "Role": "WK-Batsman", "Era": "2004-2020"},
    "Rohit Sharma":     {"Country": "India", "Format": "All", "Runs": 18000, "Wickets": 15,  "Matches": 470, "Role": "Batsman", "Era": "2007-Present"},
    "Ricky Ponting":    {"Country": "Australia", "Format": "All", "Runs": 27483, "Wickets": 5, "Matches": 560, "Role": "Batsman", "Era": "1995-2012"},
    "Brian Lara":       {"Country": "West Indies", "Format": "All", "Runs": 22358, "Wickets": 4, "Matches": 430, "Role": "Batsman", "Era": "1990-2007"},
    "AB de Villiers":   {"Country": "South Africa", "Format": "All", "Runs": 20014, "Wickets": 0, "Matches": 420, "Role": "WK-Batsman", "Era": "2004-2018"},
    "Babar Azam":       {"Country": "Pakistan", "Format": "All", "Runs": 14000, "Wickets": 0, "Matches": 300, "Role": "Batsman", "Era": "2015-Present"},
    "Wasim Akram":      {"Country": "Pakistan", "Format": "All", "Runs": 3717, "Wickets": 916, "Matches": 460, "Role": "Bowler", "Era": "1984-2003"},
    "Shane Warne":      {"Country": "Australia", "Format": "Test", "Runs": 3154, "Wickets": 708, "Matches": 194, "Role": "Bowler", "Era": "1992-2007"},
    "Muttiah Muralitharan": {"Country": "Sri Lanka", "Format": "All", "Runs": 1261, "Wickets": 1347, "Matches": 495, "Role": "Bowler", "Era": "1992-2011"},
}

search = st.text_input("", placeholder="Type player name e.g. Virat Kohli, Sachin...", label_visibility="collapsed")

if search:
    results = {k: v for k, v in players_db.items() if search.lower() in k.lower()}
    if results:
        for name, stats in results.items():
            st.markdown(f"""
            <div class="player-card">
                <h3>🏏 {name}</h3>
                <p>🌍 Country: {stats['Country']} &nbsp;|&nbsp; 🎭 Role: {stats['Role']} &nbsp;|&nbsp; 📅 Era: {stats['Era']}</p>
                <p>🏟️ Matches: {stats['Matches']} &nbsp;|&nbsp; 🏏 Runs: {stats['Runs']:,} &nbsp;|&nbsp; 🎯 Wickets: {stats['Wickets']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<p style="color:rgba(255,255,255,0.5); text-align:center;">No player found. Try another name!</p>', unsafe_allow_html=True)

# Footer
st.markdown("""
<hr class="divider">
<footer>CRICKET AGENT · RAG POWERED · 2026 · Built by Shashank DR</footer>
""", unsafe_allow_html=True)