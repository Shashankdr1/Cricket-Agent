import streamlit as st
import fitz  # PyMuPDF
import os
import plotly.express as px
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
    background: rgba(0, 0, 0, 0.75);
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
    padding: 2rem 0 1rem 0;
}

.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: 3.5rem;
    font-weight: 900;
    background: linear-gradient(135deg, #ffffff 30%, #f9e04b 70%, #ffffff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.5rem 0;
}

.hero p {
    color: #ffffff;
    text-shadow: 1px 1px 4px rgba(0,0,0,0.9);
    font-size: 1rem;
}

.stat-card {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    margin-bottom: 1rem;
}

.stat-card h2 {
    font-family: 'Playfair Display', serif;
    font-size: 2.5rem;
    color: #f9e04b;
    margin: 0;
}

.stat-card p {
    color: #ffffff;
    font-size: 0.85rem;
    margin: 0.3rem 0 0 0;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

.divider {
    border: none;
    height: 1px;
    background: linear-gradient(to right, transparent, #2d4a3e, transparent);
    margin: 1rem 0;
}

footer {
    text-align: center;
    color: #ffffff;
    font-size: 0.75rem;
    padding: 2rem 0;
    letter-spacing: 0.1em;
}
</style>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero">
    <div style="display:inline-block; background:linear-gradient(135deg,#2d6a4f,#1b4332); border:1px solid #40916c; color:#95d5b2; font-size:0.7rem; letter-spacing:0.25em; text-transform:uppercase; padding:0.4rem 1rem; border-radius:2rem; margin-bottom:1rem;">📊 Live Dashboard</div>
    <h1>Cricket Dashboard</h1>
    <p>Stats, Rankings & Tournament History</p>
</div>
<hr class="divider">
""", unsafe_allow_html=True)

# Load PDFs
pdf_folder = "pdfs"
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]
page_count = 0
word_count = 0

for filename in pdf_files:
    path = os.path.join(pdf_folder, filename)
    pdf = fitz.open(path)
    for page in pdf:
        word_count += len(page.get_text().split())
    page_count += len(pdf)

# Row 1
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🏆 ICC Test Team Rankings")
    teams = ["Australia", "India", "England", "New Zealand", "South Africa", "Pakistan", "Sri Lanka", "West Indies"]
    ratings = [128, 121, 110, 98, 95, 88, 75, 68]
    fig = px.bar(x=ratings, y=teams, orientation='h', color=ratings,
                 color_continuous_scale=["#ffffff", "#f9e04b", "#ff6b35"],
                 labels={"x": "Rating Points", "y": "Team"})
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0.3)',
                      font=dict(color='white'), coloraxis_showscale=False,
                      margin=dict(l=0, r=0, t=0, b=0))
    fig.update_xaxes(gridcolor='rgba(255,255,255,0.1)')
    fig.update_yaxes(gridcolor='rgba(255,255,255,0.1)')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### 🌍 ODI World Cup Winners")
    wc_data = {"Team": ["Australia", "India", "West Indies", "Pakistan", "Sri Lanka", "England"],
               "Titles": [5, 3, 2, 1, 1, 1]}
    fig2 = px.pie(wc_data, values="Titles", names="Team",
                  color_discrete_sequence=["#ff6b35", "#f9e04b", "#ffffff", "#00d4ff", "#ff3366", "#00ff88"])
    fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'),
                       margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig2, use_container_width=True)

# Row 2
col3, col4 = st.columns(2)

with col3:
    st.markdown("#### 🏏 IPL All-Time Top Run Scorers")
    ipl_runs = {"Player": ["Virat Kohli", "Shikhar Dhawan", "Rohit Sharma", "David Warner", "AB de Villiers"],
                "Runs": [8161, 6769, 6628, 6397, 5162]}
    fig3 = px.bar(ipl_runs, x="Player", y="Runs", color="Runs",
                  color_continuous_scale=["#1b4332", "#40916c", "#f9e04b"])
    fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0.3)',
                       font=dict(color='white'), coloraxis_showscale=False,
                       margin=dict(l=0, r=0, t=0, b=0))
    fig3.update_xaxes(gridcolor='rgba(255,255,255,0.1)')
    fig3.update_yaxes(gridcolor='rgba(255,255,255,0.1)')
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.markdown("#### ⚡ T20 World Cup Winners")
    t20_data = {"Team": ["India", "England", "West Indies", "Australia", "Pakistan", "Sri Lanka"],
                "Titles": [2, 2, 2, 1, 1, 1]}
    fig4 = px.bar(t20_data, x="Team", y="Titles", color="Titles",
                  color_continuous_scale=["#1b4332", "#40916c", "#f9e04b"])
    fig4.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0.3)',
                       font=dict(color='white'), coloraxis_showscale=False,
                       margin=dict(l=0, r=0, t=0, b=0))
    fig4.update_xaxes(gridcolor='rgba(255,255,255,0.1)')
    fig4.update_yaxes(gridcolor='rgba(255,255,255,0.1)')
    st.plotly_chart(fig4, use_container_width=True)

# Row 3 - Player comparison
st.markdown("---")
st.markdown("#### 👑 Legend Batsmen - Career Test Runs")
legends = {
    "Player": ["Sachin Tendulkar", "Ricky Ponting", "Jacques Kallis", "Rahul Dravid", "Kumar Sangakkara", "Brian Lara"],
    "Runs": [15921, 13378, 13289, 13288, 12400, 11953],
    "Country": ["India", "Australia", "South Africa", "India", "Sri Lanka", "West Indies"]
}
fig5 = px.bar(legends, x="Player", y="Runs", color="Country",
              color_discrete_map={"India": "#40916c", "Australia": "#f9e04b",
                                  "South Africa": "#c9a96e", "Sri Lanka": "#2d6a4f", "West Indies": "#95d5b2"})
fig5.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0.3)',
                   font=dict(color='white'), margin=dict(l=0, r=0, t=0, b=0))
fig5.update_xaxes(gridcolor='rgba(255,255,255,0.1)')
fig5.update_yaxes(gridcolor='rgba(255,255,255,0.1)')
st.plotly_chart(fig5, use_container_width=True)

# Footer
st.markdown("""
<hr class="divider">
<footer>CRICKET DASHBOARD · POWERED BY AI · 2026</footer>
""", unsafe_allow_html=True)