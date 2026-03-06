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
.hero p { color: rgba(255,255,255,0.7); font-size: 0.95rem; }
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
.player-card p { color: rgba(255,255,255,0.7); font-size: 0.85rem; margin: 0.15rem 0; }
.divider {
    border: none;
    height: 1px;
    background: linear-gradient(to right, transparent, rgba(255,255,255,0.15), transparent);
    margin: 1.5rem 0;
}
footer { text-align: center; color: rgba(255,255,255,0.4); font-size: 0.75rem; padding: 2rem 0; letter-spacing: 0.1em; }
.stSelectbox label { color: white !important; }
.stTextInput label { color: white !important; }
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
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<a href="/" target="_self"><button style="width:100%; padding:0.7rem; background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15); border-radius:10px; color:white; font-size:0.9rem; cursor:pointer;">💬 AI Chat</button></a>', unsafe_allow_html=True)
with col2:
    st.markdown('<a href="/Dashboard" target="_self"><button style="width:100%; padding:0.7rem; background:rgba(64,145,108,0.35); border:1px solid #40916c; border-radius:10px; color:white; font-size:0.9rem; cursor:pointer;">📊 Dashboard</button></a>', unsafe_allow_html=True)
with col3:
    st.markdown('<a href="/Predictions" target="_self"><button style="width:100%; padding:0.7rem; background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15); border-radius:10px; color:white; font-size:0.9rem; cursor:pointer;">🔮 Predictions</button></a>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

def chart_layout(title=""):
    return dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,0.04)',
        font=dict(color='white', family='DM Sans'),
        margin=dict(l=10, r=10, t=40, b=10),
        title=title,
        title_font=dict(color='#f9e04b', size=13)
    )

team_colors = {
    "India": "#0057A8", "Australia": "#FFD700", "England": "#CF0A0A",
    "Pakistan": "#006600", "West Indies": "#7B3F00", "New Zealand": "#1a1a1a",
    "South Africa": "#FF69B4", "Sri Lanka": "#00D4FF"
}

teams = list(team_colors.keys())

# ── TOURNAMENT FILTER ──────────────────────────────
st.markdown('<div class="section-title">🏆 Tournament Overview</div>', unsafe_allow_html=True)
tournament = st.selectbox("", ["All Formats", "ODI World Cup", "T20 World Cup", "IPL", "Test Cricket"], label_visibility="collapsed")

if tournament in ["All Formats", "ODI World Cup"]:
    col1, col2 = st.columns(2)
    with col1:
        wc_data = {"Team": ["Australia", "India", "West Indies", "Pakistan", "Sri Lanka", "England"], "Titles": [5, 3, 2, 1, 1, 1]}
        fig = px.pie(wc_data, values="Titles", names="Team", title="🌍 ODI World Cup Titles",
                     color_discrete_sequence=["#FFD700", "#0057A8", "#7B3F00", "#006600", "#00D4FF", "#CF0A0A"])
        fig.update_layout(**chart_layout())
        fig.update_traces(textfont_color='white')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        odi_runs = {"Player": ["Sachin Tendulkar", "Ricky Ponting", "Sanath Jayasuriya", "Mahela Jayawardene", "Inzamam-ul-Haq"], "Runs": [18426, 13704, 13430, 12650, 11739]}
        fig2 = px.bar(odi_runs, x="Runs", y="Player", orientation='h', title="🏏 ODI All-Time Top Run Scorers",
                      color="Runs", color_continuous_scale=["#1b4332", "#40916c", "#f9e04b"])
        fig2.update_layout(**chart_layout(), coloraxis_showscale=False)
        fig2.update_xaxes(gridcolor='rgba(255,255,255,0.08)')
        fig2.update_yaxes(gridcolor='rgba(255,255,255,0.08)')
        st.plotly_chart(fig2, use_container_width=True)

if tournament in ["All Formats", "T20 World Cup"]:
    col3, col4 = st.columns(2)
    with col3:
        t20_data = {"Team": ["India", "England", "West Indies", "Australia", "Pakistan", "Sri Lanka"], "Titles": [2, 2, 2, 1, 1, 1]}
        fig3 = px.bar(t20_data, x="Team", y="Titles", title="⚡ T20 World Cup Titles",
                      color="Team", color_discrete_map=team_colors)
        fig3.update_layout(**chart_layout(), coloraxis_showscale=False, showlegend=False)
        fig3.update_xaxes(gridcolor='rgba(255,255,255,0.08)')
        fig3.update_yaxes(gridcolor='rgba(255,255,255,0.08)')
        st.plotly_chart(fig3, use_container_width=True)
    with col4:
        t20_runs = {"Player": ["Rohit Sharma", "Virat Kohli", "Babar Azam", "Martin Guptill", "David Warner"], "Runs": [4231, 4188, 3985, 3531, 3277]}
        fig4 = px.bar(t20_runs, x="Player", y="Runs", title="🏏 T20I Top Run Scorers",
                      color="Runs", color_continuous_scale=["#1b4332", "#40916c", "#f9e04b"])
        fig4.update_layout(**chart_layout(), coloraxis_showscale=False)
        fig4.update_xaxes(gridcolor='rgba(255,255,255,0.08)')
        fig4.update_yaxes(gridcolor='rgba(255,255,255,0.08)')
        st.plotly_chart(fig4, use_container_width=True)

if tournament in ["All Formats", "IPL"]:
    col5, col6 = st.columns(2)
    with col5:
        ipl_runs = {"Player": ["Virat Kohli", "Shikhar Dhawan", "Rohit Sharma", "David Warner", "AB de Villiers"], "Runs": [8161, 6769, 6628, 6397, 5162]}
        fig5 = px.bar(ipl_runs, x="Player", y="Runs", title="🏏 IPL All-Time Top Run Scorers",
                      color="Runs", color_continuous_scale=["#1b4332", "#40916c", "#f9e04b"])
        fig5.update_layout(**chart_layout(), coloraxis_showscale=False)
        fig5.update_xaxes(gridcolor='rgba(255,255,255,0.08)')
        fig5.update_yaxes(gridcolor='rgba(255,255,255,0.08)')
        st.plotly_chart(fig5, use_container_width=True)
    with col6:
        ipl_wickets = {"Player": ["Yuzvendra Chahal", "DJ Bravo", "Lasith Malinga", "Amit Mishra", "Piyush Chawla"], "Wickets": [221, 183, 170, 166, 157]}
        fig6 = px.bar(ipl_wickets, x="Wickets", y="Player", orientation='h', title="🎯 IPL All-Time Top Wicket Takers",
                      color="Wickets", color_continuous_scale=["#1b4332", "#ff6b35", "#f9e04b"])
        fig6.update_layout(**chart_layout(), coloraxis_showscale=False)
        fig6.update_xaxes(gridcolor='rgba(255,255,255,0.08)')
        fig6.update_yaxes(gridcolor='rgba(255,255,255,0.08)')
        st.plotly_chart(fig6, use_container_width=True)

if tournament in ["All Formats", "Test Cricket"]:
    col7, col8 = st.columns(2)
    with col7:
        test_teams = ["Australia", "India", "England", "New Zealand", "South Africa", "Pakistan", "Sri Lanka", "West Indies"]
        ratings = [128, 121, 110, 98, 95, 88, 75, 68]
        fig7 = px.bar(x=ratings, y=test_teams, orientation='h', title="🏆 ICC Test Team Rankings",
                      color=test_teams, color_discrete_map=team_colors,
                      labels={"x": "Rating Points", "y": "Team"})
        fig7.update_layout(**chart_layout(), coloraxis_showscale=False, showlegend=False)
        fig7.update_xaxes(gridcolor='rgba(255,255,255,0.08)')
        fig7.update_yaxes(gridcolor='rgba(255,255,255,0.08)')
        st.plotly_chart(fig7, use_container_width=True)
    with col8:
        legends = {
            "Player": ["Sachin Tendulkar", "Ricky Ponting", "Jacques Kallis", "Rahul Dravid", "Kumar Sangakkara", "Brian Lara"],
            "Runs": [15921, 13378, 13289, 13288, 12400, 11953],
            "Country": ["India", "Australia", "South Africa", "India", "Sri Lanka", "West Indies"]
        }
        fig8 = px.bar(legends, x="Player", y="Runs", color="Country", title="👑 Legend Batsmen - Career Test Runs",
                      color_discrete_map={"India": "#0057A8", "Australia": "#FFD700", "South Africa": "#FF69B4", "Sri Lanka": "#00D4FF", "West Indies": "#7B3F00"})
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
    team1 = st.selectbox("Select Team 1", teams, key="cmp_t1")
with col2:
    team2 = st.selectbox("Select Team 2", teams, index=1, key="cmp_t2")

categories = ["ODI Titles", "T20 Titles", "Test Rating", "WC Appearances"]
t1_values = [team_data[team1][c] for c in categories]
t2_values = [team_data[team2][c] for c in categories]

fig_compare = go.Figure()
fig_compare.add_trace(go.Bar(name=team1, x=categories, y=t1_values, marker_color=team_colors.get(team1, "#f9e04b")))
fig_compare.add_trace(go.Bar(name=team2, x=categories, y=t2_values, marker_color=team_colors.get(team2, "#ff6b35")))
fig_compare.update_layout(**chart_layout(f"⚔️ {team1} vs {team2}"), barmode='group', legend=dict(font=dict(color='white')))
fig_compare.update_xaxes(gridcolor='rgba(255,255,255,0.08)')
fig_compare.update_yaxes(gridcolor='rgba(255,255,255,0.08)')
st.plotly_chart(fig_compare, use_container_width=True)

# ── HEAD TO HEAD ───────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🆚 Head to Head Records</div>', unsafe_allow_html=True)

head_to_head = {
    ("India", "Australia"):     {"Matches": 150, "India Wins": 55, "Australia Wins": 78, "No Result": 17},
    ("India", "England"):       {"Matches": 120, "India Wins": 55, "England Wins": 54, "No Result": 11},
    ("India", "Pakistan"):      {"Matches": 132, "India Wins": 73, "Pakistan Wins": 50, "No Result": 9},
    ("India", "West Indies"):   {"Matches": 130, "India Wins": 65, "West Indies Wins": 55, "No Result": 10},
    ("India", "New Zealand"):   {"Matches": 110, "India Wins": 56, "New Zealand Wins": 48, "No Result": 6},
    ("India", "South Africa"):  {"Matches": 85,  "India Wins": 40, "South Africa Wins": 40, "No Result": 5},
    ("India", "Sri Lanka"):     {"Matches": 160, "India Wins": 90, "Sri Lanka Wins": 58, "No Result": 12},
    ("Australia", "England"):   {"Matches": 180, "Australia Wins": 95, "England Wins": 72, "No Result": 13},
    ("Australia", "Pakistan"):  {"Matches": 100, "Australia Wins": 67, "Pakistan Wins": 28, "No Result": 5},
    ("Australia", "West Indies"):{"Matches": 120, "Australia Wins": 72, "West Indies Wins": 42, "No Result": 6},
    ("England", "Pakistan"):    {"Matches": 95,  "England Wins": 48, "Pakistan Wins": 41, "No Result": 6},
    ("Pakistan", "West Indies"):{"Matches": 90,  "Pakistan Wins": 49, "West Indies Wins": 36, "No Result": 5},
}

col1, col2 = st.columns(2)
with col1:
    h2h_t1 = st.selectbox("Team 1", teams, key="h2h_t1")
with col2:
    h2h_t2 = st.selectbox("Team 2", [t for t in teams if t != h2h_t1], key="h2h_t2")

key1 = (h2h_t1, h2h_t2)
key2 = (h2h_t2, h2h_t1)
h2h = head_to_head.get(key1) or head_to_head.get(key2)

if h2h:
    t1_wins = h2h.get(f"{h2h_t1} Wins", h2h.get(list(h2h.keys())[1], 0))
    t2_wins = h2h.get(f"{h2h_t2} Wins", h2h.get(list(h2h.keys())[2], 0))
    nr = h2h.get("No Result", 0)

    fig_h2h = go.Figure(go.Bar(
        x=[h2h_t1, h2h_t2, "No Result"],
        y=[t1_wins, t2_wins, nr],
        marker_color=[team_colors.get(h2h_t1, "#f9e04b"), team_colors.get(h2h_t2, "#ff6b35"), "rgba(255,255,255,0.3)"]
    ))
    fig_h2h.update_layout(**chart_layout(f"🆚 {h2h_t1} vs {h2h_t2} — Total {h2h['Matches']} Matches"))
    fig_h2h.update_xaxes(gridcolor='rgba(255,255,255,0.08)')
    fig_h2h.update_yaxes(gridcolor='rgba(255,255,255,0.08)')
    st.plotly_chart(fig_h2h, use_container_width=True)
else:
    st.info("Head to head data not available for this combination yet.")

# ── PLAYER CAREER TIMELINE ─────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📈 Player Career Timeline</div>', unsafe_allow_html=True)

player_timelines = {
    "Sachin Tendulkar": {
        "Years": [1990, 1995, 2000, 2003, 2007, 2010, 2013],
        "Runs":  [1000, 4000, 8000, 13000, 16000, 18000, 18426],
        "Wickets": [10, 40, 80, 120, 150, 180, 201]
    },
    "Virat Kohli": {
        "Years": [2010, 2012, 2014, 2016, 2018, 2020, 2023],
        "Runs":  [1000, 4000, 8000, 13000, 18000, 22000, 26000],
        "Wickets": [0, 1, 2, 3, 4, 4, 4]
    },
    "Ricky Ponting": {
        "Years": [1996, 2000, 2003, 2006, 2009, 2012],
        "Runs":  [1000, 5000, 10000, 16000, 22000, 27483],
        "Wickets": [1, 2, 3, 4, 5, 5]
    },
    "MS Dhoni": {
        "Years": [2005, 2007, 2010, 2013, 2016, 2019],
        "Runs":  [500, 3000, 7000, 11000, 14000, 17266],
        "Wickets": [0, 0, 0, 0, 0, 0]
    },
}

selected_player = st.selectbox("Select Player", list(player_timelines.keys()), key="timeline_player")
timeline = player_timelines[selected_player]

fig_timeline = go.Figure()
fig_timeline.add_trace(go.Scatter(
    x=timeline["Years"], y=timeline["Runs"],
    mode='lines+markers', name='Runs',
    line=dict(color='#f9e04b', width=3),
    marker=dict(size=8)
))
fig_timeline.update_layout(**chart_layout(f"📈 {selected_player} — Career Runs Timeline"),
                            legend=dict(font=dict(color='white')))
fig_timeline.update_xaxes(gridcolor='rgba(255,255,255,0.08)')
fig_timeline.update_yaxes(gridcolor='rgba(255,255,255,0.08)')
st.plotly_chart(fig_timeline, use_container_width=True)

# ── BOWLING ANALYSIS ───────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🎯 Bowling Analysis</div>', unsafe_allow_html=True)

bowling_data = {
    "Player":       ["Wasim Akram", "Shane Warne", "Muralitharan", "Glenn McGrath", "James Anderson", "Anil Kumble"],
    "Wickets":      [916, 708, 1347, 563, 700, 619],
    "Economy":      [3.9, 3.2, 3.5, 2.5, 2.8, 2.7],
    "Strike Rate":  [28.8, 57.4, 55.0, 51.9, 57.0, 65.9],
    "Average":      [23.6, 25.2, 22.7, 21.6, 26.4, 29.6],
    "Type":         ["Pace", "Spin", "Spin", "Pace", "Pace", "Spin"]
}

col1, col2 = st.columns(2)
with col1:
    fig_bowl1 = px.scatter(bowling_data, x="Economy", y="Wickets",
                           size="Wickets", color="Type", text="Player",
                           title="🎯 Economy vs Wickets",
                           color_discrete_map={"Pace": "#ff6b35", "Spin": "#00d4ff"})
    fig_bowl1.update_traces(textposition='top center', textfont=dict(color='white', size=9))
    fig_bowl1.update_layout(**chart_layout(), legend=dict(font=dict(color='white')))
    fig_bowl1.update_xaxes(gridcolor='rgba(255,255,255,0.08)')
    fig_bowl1.update_yaxes(gridcolor='rgba(255,255,255,0.08)')
    st.plotly_chart(fig_bowl1, use_container_width=True)

with col2:
    fig_bowl2 = px.bar(bowling_data, x="Player", y="Average",
                       title="📊 Bowling Average (lower is better)",
                       color="Type",
                       color_discrete_map={"Pace": "#ff6b35", "Spin": "#00d4ff"})
    fig_bowl2.update_layout(**chart_layout(), legend=dict(font=dict(color='white')))
    fig_bowl2.update_xaxes(gridcolor='rgba(255,255,255,0.08)')
    fig_bowl2.update_yaxes(gridcolor='rgba(255,255,255,0.08)')
    st.plotly_chart(fig_bowl2, use_container_width=True)

# ── WIN/LOSS BY VENUE ─────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🏟️ Win/Loss Ratio by Venue</div>', unsafe_allow_html=True)

venue_data = {
    "India": {
        "Venue": ["Wankhede", "Eden Gardens", "Chepauk", "Chinnaswamy", "Lords", "MCG", "SCG", "Oval"],
        "Wins":  [18, 15, 14, 12, 5, 4, 3, 6],
        "Losses":[5,  7,  4,  6,  8, 9, 7, 5]
    },
    "Australia": {
        "Venue": ["MCG", "SCG", "Gabba", "WACA", "Lords", "Headingley", "Wankhede", "Eden Gardens"],
        "Wins":  [45, 38, 42, 30, 20, 18, 8, 6],
        "Losses":[10, 12, 8,  9,  15, 12, 10, 9]
    },
    "England": {
        "Venue": ["Lords", "Oval", "Headingley", "Edgbaston", "MCG", "SCG", "Wankhede", "Chepauk"],
        "Wins":  [40, 35, 28, 30, 12, 10, 5, 4],
        "Losses":[15, 18, 20, 14, 18, 16, 9, 8]
    },
}

venue_team = st.selectbox("Select Team", list(venue_data.keys()), key="venue_team")
vd = venue_data[venue_team]

fig_venue = go.Figure()
fig_venue.add_trace(go.Bar(name='Wins', x=vd["Venue"], y=vd["Wins"], marker_color=team_colors.get(venue_team, "#40916c")))
fig_venue.add_trace(go.Bar(name='Losses', x=vd["Venue"], y=vd["Losses"], marker_color='rgba(255,255,255,0.2)'))
fig_venue.update_layout(**chart_layout(f"🏟️ {venue_team} — Win/Loss by Venue"),
                        barmode='group', legend=dict(font=dict(color='white')))
fig_venue.update_xaxes(gridcolor='rgba(255,255,255,0.08)')
fig_venue.update_yaxes(gridcolor='rgba(255,255,255,0.08)')
st.plotly_chart(fig_venue, use_container_width=True)

# ── TOURNAMENT STATS ──────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🏆 Tournament Statistics</div>', unsafe_allow_html=True)

tourn_filter = st.selectbox("Select Tournament", ["ODI World Cup", "T20 World Cup", "IPL"], key="tourn_stats")

if tourn_filter == "ODI World Cup":
    col1, col2 = st.columns(2)
    with col1:
        high_scores = {"Player": ["Martin Guptill", "Chris Gayle", "Rohit Sharma", "Sachin Tendulkar", "Ricky Ponting"],
                       "Score": [237, 215, 264, 200, 140]}
        fig_hs = px.bar(high_scores, x="Player", y="Score", title="🏏 Highest Individual Scores",
                        color="Score", color_continuous_scale=["#1b4332", "#40916c", "#f9e04b"])
        fig_hs.update_layout(**chart_layout(), coloraxis_showscale=False)
        fig_hs.update_xaxes(gridcolor='rgba(255,255,255,0.08)')
        fig_hs.update_yaxes(gridcolor='rgba(255,255,255,0.08)')
        st.plotly_chart(fig_hs, use_container_width=True)
    with col2:
        best_bowl = {"Player": ["Glenn McGrath", "Mitchell Starc", "Zaheer Khan", "Wasim Akram", "Javagal Srinath"],
                     "Wickets": [71, 52, 44, 55, 44]}
        fig_bb = px.bar(best_bowl, x="Player", y="Wickets", title="🎯 Most Wickets in World Cups",
                        color="Wickets", color_continuous_scale=["#1b4332", "#ff6b35", "#f9e04b"])
        fig_bb.update_layout(**chart_layout(), coloraxis_showscale=False)
        fig_bb.update_xaxes(gridcolor='rgba(255,255,255,0.08)')
        fig_bb.update_yaxes(gridcolor='rgba(255,255,255,0.08)')
        st.plotly_chart(fig_bb, use_container_width=True)

elif tourn_filter == "T20 World Cup":
    col1, col2 = st.columns(2)
    with col1:
        t20_top = {"Player": ["Virat Kohli", "Rohit Sharma", "Tillakaratne Dilshan", "Chris Gayle", "Mahela Jayawardene"],
                   "Runs": [1216, 1083, 1016, 920, 1016]}
        fig_t1 = px.bar(t20_top, x="Player", y="Runs", title="🏏 Most Runs in T20 World Cups",
                        color="Runs", color_continuous_scale=["#1b4332", "#40916c", "#f9e04b"])
        fig_t1.update_layout(**chart_layout(), coloraxis_showscale=False)
        fig_t1.update_xaxes(gridcolor='rgba(255,255,255,0.08)')
        fig_t1.update_yaxes(gridcolor='rgba(255,255,255,0.08)')
        st.plotly_chart(fig_t1, use_container_width=True)
    with col2:
        t20_bowl = {"Player": ["Lasith Malinga", "Shakib Al Hasan", "Imad Wasim", "Samuel Badree", "Umar Gul"],
                    "Wickets": [38, 47, 30, 28, 34]}
        fig_t2 = px.bar(t20_bowl, x="Player", y="Wickets", title="🎯 Most Wickets in T20 World Cups",
                        color="Wickets", color_continuous_scale=["#1b4332", "#ff6b35", "#f9e04b"])
        fig_t2.update_layout(**chart_layout(), coloraxis_showscale=False)
        fig_t2.update_xaxes(gridcolor='rgba(255,255,255,0.08)')
        fig_t2.update_yaxes(gridcolor='rgba(255,255,255,0.08)')
        st.plotly_chart(fig_t2, use_container_width=True)

elif tourn_filter == "IPL":
    col1, col2 = st.columns(2)
    with col1:
        ipl_champs = {"Team": ["Mumbai Indians", "Chennai Super Kings", "Kolkata Knight Riders", "Rajasthan Royals", "Sunrisers Hyderabad"],
                      "Titles": [5, 5, 3, 2, 1]}
        fig_i1 = px.pie(ipl_champs, values="Titles", names="Team", title="🏆 IPL Champions",
                        color_discrete_sequence=["#0057A8", "#f9e04b", "#7B3F00", "#ff69b4", "#ff6b35"])
        fig_i1.update_layout(**chart_layout())
        fig_i1.update_traces(textfont_color='white')
        st.plotly_chart(fig_i1, use_container_width=True)
    with col2:
        ipl_sixes = {"Player": ["Chris Gayle", "AB de Villiers", "Rohit Sharma", "MS Dhoni", "Virat Kohli"],
                     "Sixes": [357, 251, 248, 229, 253]}
        fig_i2 = px.bar(ipl_sixes, x="Player", y="Sixes", title="💥 Most Sixes in IPL",
                        color="Sixes", color_continuous_scale=["#1b4332", "#ff6b35", "#f9e04b"])
        fig_i2.update_layout(**chart_layout(), coloraxis_showscale=False)
        fig_i2.update_xaxes(gridcolor='rgba(255,255,255,0.08)')
        fig_i2.update_yaxes(gridcolor='rgba(255,255,255,0.08)')
        st.plotly_chart(fig_i2, use_container_width=True)

# ── PLAYER SEARCH ──────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🔍 Player Search</div>', unsafe_allow_html=True)

players_db = {
    "Sachin Tendulkar": {"Country": "India", "Runs": 34357, "Wickets": 201, "Matches": 664, "Role": "Batsman", "Era": "1989-2013"},
    "Virat Kohli":      {"Country": "India", "Runs": 26000, "Wickets": 4,   "Matches": 500, "Role": "Batsman", "Era": "2008-Present"},
    "MS Dhoni":         {"Country": "India", "Runs": 17266, "Wickets": 0,   "Matches": 538, "Role": "WK-Batsman", "Era": "2004-2020"},
    "Rohit Sharma":     {"Country": "India", "Runs": 18000, "Wickets": 15,  "Matches": 470, "Role": "Batsman", "Era": "2007-Present"},
    "Ricky Ponting":    {"Country": "Australia", "Runs": 27483, "Wickets": 5, "Matches": 560, "Role": "Batsman", "Era": "1995-2012"},
    "Brian Lara":       {"Country": "West Indies", "Runs": 22358, "Wickets": 4, "Matches": 430, "Role": "Batsman", "Era": "1990-2007"},
    "AB de Villiers":   {"Country": "South Africa", "Runs": 20014, "Wickets": 0, "Matches": 420, "Role": "WK-Batsman", "Era": "2004-2018"},
    "Babar Azam":       {"Country": "Pakistan", "Runs": 14000, "Wickets": 0, "Matches": 300, "Role": "Batsman", "Era": "2015-Present"},
    "Wasim Akram":      {"Country": "Pakistan", "Runs": 3717, "Wickets": 916, "Matches": 460, "Role": "Bowler", "Era": "1984-2003"},
    "Shane Warne":      {"Country": "Australia", "Runs": 3154, "Wickets": 708, "Matches": 194, "Role": "Bowler", "Era": "1992-2007"},
    "Muttiah Muralitharan": {"Country": "Sri Lanka", "Runs": 1261, "Wickets": 1347, "Matches": 495, "Role": "Bowler", "Era": "1992-2011"},
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