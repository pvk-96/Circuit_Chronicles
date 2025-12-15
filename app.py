
#Please Do-not Change anything
#I do not know how it is working and removing even one line might break this again.
import streamlit as st
import fastf1


from components.track_map import show_track_map
from utils.cache import enable_cache
from components.telemetry_compare import show_telemetry_comparison
from components.session_summary import show_session_summary
from components.lap_analysis import show_lap_analysis
from components.driver_highlight import show_driver_highlight
from components.lap_time_chart import show_lap_time_chart
from components.position_evolution import show_position_evolution
from components.gp_selector import select_grand_prix
from components.battle_gap import show_battle_gap
from components.overtake_detector import show_overtake_detector

# Load custom CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Logo
st.markdown("<img src='assets/logo.png' class='logo-center'>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    ### Circuit Chronicles  
    **F1 Data Analysis Suite**
    
    Explore sessions, laps, telemetry, battles, and overtakes.
    """)
    st.markdown("""   
<div class='footer'>
    Made with ❤️ by PVK · Powered by FastF1 . Contact: praneethvarmakopperla@gmail.com 
</div>
""", unsafe_allow_html=True)


# Cache
enable_cache()

st.markdown("""
<div class='app-header'>
    <img src='assets/logo.png' class='app-logo'>
    <h1>Circuit Chronicles</h1>
    <p class='tagline'>Precision Motorsport Analytics</p>
</div>
""", unsafe_allow_html=True)


# ---- GRAND PRIX SELECTOR ----
year, event = select_grand_prix()

# --- GP FLAG ---
from utils.flags import FLAG_MAP
flag = FLAG_MAP.get(event["Country"], "")

# --- HEADER ---
st.markdown(f"""
<div class='app-header'>
    <h1>Circuit Chronicles {flag}</h1>
    <p class='tagline'>{event["EventName"]}</p>
</div>
""", unsafe_allow_html=True)


# ---- SESSION SELECTOR ----
session_map = {
    "Practice 1": "FP1",
    "Practice 2": "FP2",
    "Practice 3": "FP3",
    "Qualifying": "Q",
    "Sprint Shootout": "SS",
    "Sprint": "Sprint",
    "Race": "R"
}

session_label = st.selectbox(
    "Select Session",
    list(session_map.keys()),
    key="session_selector"
)

session_name = session_map[session_label]


# ---- LOAD SESSION ----
from components.car_loader import show_car_loader
# Car animation loader
loading_text = f"Loading {event['EventName']} — {session_label}..."
loader = show_car_loader(loading_text)

# Load session
session = fastf1.get_session(year, event["RoundNumber"], session_name)
session.load()
laps = session.laps

# Remove loader after session finishes loading
loader.empty()



# ---- MODULES ----
show_session_summary(session, laps)
show_track_map(session, laps)
show_lap_analysis(laps)
show_driver_highlight(laps)
show_telemetry_comparison(session, laps)
show_lap_time_chart(session)
show_position_evolution(session)
show_battle_gap(laps)
show_overtake_detector(session)



