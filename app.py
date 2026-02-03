import streamlit as st
import pandas as pd
import io

# Set page configuration
st.set_page_config(page_title="World Cup 2026 Fixture Filter", layout="wide")

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

.stApp {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    font-family: 'Poppins', sans-serif !important;
}

h1, h2, h3, h4, h5, h6, p, label, .stSelectbox, .stMarkdown, .stText, button {
    color: #000000;
    font-family: 'Poppins', sans-serif !important;
}

/* Specific overrides for Selectbox to ensure text is visible */
.stSelectbox > div > div {
    color: #000000 !important;
}

/* Dropdown menu background and text */
div[data-baseweb="select"] > div, div[data-baseweb="base-input"] {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    border-color: #000000 !important;
}

div[data-baseweb="menu"], div[data-baseweb="popover"] {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}

div[data-baseweb="menu"] div, div[data-baseweb="popover"] div {
    color: #000000 !important;
    background-color: #FFFFFF !important;
}

/* Highlighted option in dropdown */
div[data-baseweb="menu"] li[aria-selected="true"], div[data-baseweb="menu"] li:hover {
    background-color: #F0F0F0 !important;
    color: #000000 !important;
}

/* Match Card Styling */
.match-card {
    border: 2px solid black;
    border-radius: 15px;
    margin-bottom: 20px;
    background-color: white;
    overflow: hidden; /* Ensures header background respects rounded corners */
}

.match-header {
    border-bottom: 2px solid black;
    padding: 10px 15px;
    font-weight: 700;
    font-size: 2em;
}

.header-canada {
    background-color: rgb(196, 60, 44) !important;
    color: white !important;
}

.header-mexico {
    background-color: rgb(82, 162, 90) !important;
    color: black !important;
}

.header-usa {
    background-color: rgb(13, 42, 213) !important;
    color: white !important;
}

.match-body {
    padding: 15px;
}

.group-label {
    font-size: 0.9em;
    margin-bottom: 5px;
}

.teams {
    font-size: 1.5em;
    font-weight: 600;
    # text-align: center;
}

</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center;'>World Cup 2026<sup>&trade;</sup> Fixture Finder</h1>", unsafe_allow_html=True)



# CSV Data Inlined
CSV_DATA = """Date,Group,Home Team,Away Team,City
2026-06-11,A,Mexico,South Africa,Mexico City
2026-06-11,A,Korea Republic,Czechia/Denmark/North Macedonia/Republic of Ireland,Guadalajara
2026-06-12,B,Canada,Bosnia and Herzegovina/Italy/Northern Ireland/Wales,Toronto
2026-06-12,D,USA,Paraguay,Los Angeles
2026-06-13,C,Haiti,Scotland,Boston
2026-06-13,D,Australia,Kosovo/Romania/Slovakia/Türkiye,Vancouver
2026-06-13,C,Brazil,Morocco,New York/New Jersey
2026-06-13,B,Qatar,Switzerland,San Francisco Bay Area
2026-06-14,E,Côte d'Ivoire,Ecuador,Philadelphia
2026-06-14,E,Germany,Curaçao,Houston
2026-06-14,F,Netherlands,Japan,Dallas
2026-06-14,F,Albania/Poland/Sweden/Ukraine,Tunisia,Monterrey
2026-06-15,H,Saudi Arabia,Uruguay,Miami
2026-06-15,H,Spain,Cabo Verde,Atlanta
2026-06-15,G,IR Iran,New Zealand,Los Angeles
2026-06-15,G,Belgium,Egypt,Seattle
2026-06-16,I,France,Senegal,New York/New Jersey
2026-06-16,I,Bolivia/Iraq/Suriname,Norway,Boston
2026-06-16,J,Argentina,Algeria,Kansas City
2026-06-16,J,Austria,Jordan,San Francisco Bay Area
2026-06-17,L,Ghana,Panama,Toronto
2026-06-17,L,England,Croatia,Dallas
2026-06-17,K,Portugal,Congo DR/Jamaica/New Caledonia,Houston
2026-06-17,K,Uzbekistan,Colombia,Mexico City
2026-06-18,A,Czechia/Denmark/North Macedonia/Republic of Ireland,South Africa,Atlanta
2026-06-18,B,Switzerland,Bosnia and Herzegovina/Italy/Northern Ireland/Wales,Los Angeles
2026-06-18,B,Canada,Qatar,Vancouver
2026-06-18,A,Mexico,Korea Republic,Guadalajara
2026-06-19,C,Brazil,Haiti,Philadelphia
2026-06-19,C,Scotland,Morocco,Boston
2026-06-19,D,Kosovo/Romania/Slovakia/Türkiye,Paraguay,San Francisco Bay Area
2026-06-19,D,USA,Australia,Seattle
2026-06-20,E,Germany,Côte d'Ivoire,Toronto
2026-06-20,E,Ecuador,Curaçao,Kansas City
2026-06-20,F,Netherlands,Albania/Poland/Sweden/Ukraine,Houston
2026-06-20,F,Tunisia,Japan,Monterrey
2026-06-21,H,Uruguay,Cabo Verde,Miami
2026-06-21,H,Spain,Saudi Arabia,Atlanta
2026-06-21,G,Belgium,IR Iran,Los Angeles
2026-06-21,G,New Zealand,Egypt,Vancouver
2026-06-22,I,Norway,Senegal,New York/New Jersey
2026-06-22,I,France,Bolivia/Iraq/Suriname,Philadelphia
2026-06-22,J,Argentina,Austria,Dallas
2026-06-22,J,Jordan,Algeria,San Francisco Bay Area
2026-06-23,L,England,Ghana,Boston
2026-06-23,L,Panama,Croatia,Toronto
2026-06-23,K,Portugal,Uzbekistan,Houston
2026-06-23,K,Colombia,Congo DR/Jamaica/New Caledonia,Guadalajara
2026-06-24,C,Scotland,Brazil,Miami
2026-06-24,C,Morocco,Haiti,Atlanta
2026-06-24,B,Switzerland,Canada,Vancouver
2026-06-24,B,Bosnia and Herzegovina/Italy/Northern Ireland/Wales,Qatar,Seattle
2026-06-24,A,Czechia/Denmark/North Macedonia/Republic of Ireland,Mexico,Mexico City
2026-06-24,A,South Africa,Korea Republic,Monterrey
2026-06-25,E,Curaçao,Côte d'Ivoire,Philadelphia
2026-06-25,E,Ecuador,Germany,New York/New Jersey
2026-06-25,F,Japan,Albania/Poland/Sweden/Ukraine,Dallas
2026-06-25,F,Tunisia,Netherlands,Kansas City
2026-06-25,D,Kosovo/Romania/Slovakia/Türkiye,USA,Los Angeles
2026-06-25,D,Paraguay,Australia,San Francisco Bay Area
2026-06-26,I,Norway,France,Boston
2026-06-26,I,Senegal,Bolivia/Iraq/Suriname,Toronto
2026-06-26,G,Egypt,IR Iran,Seattle
2026-06-26,G,New Zealand,Belgium,Vancouver
2026-06-26,H,Cabo Verde,Saudi Arabia,Houston
2026-06-26,H,Uruguay,Spain,Guadalajara
2026-06-27,L,Panama,England,New York/New Jersey
2026-06-27,L,Croatia,Ghana,Philadelphia
2026-06-27,J,Algeria,Austria,Kansas City
2026-06-27,J,Jordan,Argentina,Dallas
2026-06-27,K,Colombia,Portugal,Miami
2026-06-27,K,Congo DR/Jamaica/New Caledonia,Uzbekistan,Atlanta"""

# Team Flags Mapping
TEAM_FLAGS = {
    "Algeria": "🇩🇿", "Argentina": "🇦🇷", "Australia": "🇦🇺", "Austria": "🇦🇹",
    "Belgium": "🇧🇪", "Brazil": "🇧🇷", "Cabo Verde": "🇨🇻", "Canada": "🇨🇦",
    "Colombia": "🇨🇴", "Croatia": "🇭🇷", "Curaçao": "🇨🇼", "Côte d'Ivoire": "🇨🇮",
    "Ecuador": "🇪🇨", "Egypt": "🇪🇬", "England": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "France": "🇫🇷",
    "Germany": "🇩🇪", "Ghana": "🇬🇭", "Haiti": "🇭🇹", "IR Iran": "🇮🇷",
    "Japan": "🇯🇵", "Jordan": "🇯🇴", "Korea Republic": "🇰🇷", "Mexico": "🇲🇽",
    "Morocco": "🇲🇦", "Netherlands": "🇳🇱", "New Zealand": "🇳🇿", "Norway": "🇳🇴",
    "Panama": "🇵🇦", "Paraguay": "🇵🇾", "Portugal": "🇵🇹", "Qatar": "🇶🇦",
    "Saudi Arabia": "🇸🇦", "Scotland": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "Senegal": "🇸🇳",
    "South Africa": "🇿🇦", "Spain": "🇪🇸", "Switzerland": "🇨🇭", "Tunisia": "🇹🇳",
    "USA": "🇺🇸", "Uruguay": "🇺🇾", "Uzbekistan": "🇺🇿"
}

def format_team(name):
    if "/" in name or name in ["Home Team", "Away Team"]:
        return name
    flag = TEAM_FLAGS.get(name, "")
    return f"{flag} {name}" if flag else name

try:
    # Load data from inlined CSV string
    df = pd.read_csv(io.StringIO(CSV_DATA))
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by="Date")
    
    # Get unique cities sorted alphabetically
    cities = sorted(df['City'].unique())
    cities.insert(0, "All")
    
    # Get unique teams sorted alphabetically (Home and Away combined)
    teams = sorted(pd.concat([df['Home Team'], df['Away Team']]).unique())
    teams.insert(0, "All")
    
    # Create columns for side-by-side filters
    col1, col2 = st.columns(2)
    
    with col1:
        # City selection
        selected_city = st.selectbox("Filter by city", cities)
        
    with col2:
        # Team selection
        selected_team = st.selectbox("Filter by team", teams)
    
    # Filter data based on selections
    if selected_city != "All":
        df = df[df['City'] == selected_city]
        
    if selected_team != "All":
        df = df[(df['Home Team'] == selected_team) | (df['Away Team'] == selected_team)]
    
    # Get unique dates (after filtering)
    unique_dates = df['Date'].unique()

    for date in unique_dates:
        # Convert numpy datetime64 to pandas timestamp for easier formatting/access if needed
        # or just use string representation
        ts = pd.to_datetime(date)
        date_str = ts.strftime('%A, %B %d')
        
        st.header(date_str)
        
        # Filter data for this date
        day_schedule = df[df['Date'] == date]
        
        # Display matches in boxes
        for idx, row in day_schedule.iterrows():
            # match_str = f"{row['Home Team']} v {row['Away Team']} at {row['City']}"
            
            # Dynamic header style based on city/country
            city = row['City']
            if city in ["Toronto", "Vancouver"]:
                # Canada: RGB(196, 60, 44), White text
                header_class = "header-canada"
            elif city in ["Mexico City", "Guadalajara", "Monterrey"]:
                # Mexico: RGB(82, 162, 90), Black text
                header_class = "header-mexico"
            else:
                # USA (default): RGB(13, 42, 213), White text
                header_class = "header-usa"

            # Structure matches the user request:
            # City Header
            # Group (prefixed)
            # Home v Away
            
            st.markdown(
                f"""
                <div id="match-{idx}" class="match-card">
                    <div class="match-header {header_class}">{row['City']}</div>
                    <div class="match-body">
                        <div class="group-label">Group {row['Group']}</div>
                        <div class="teams">{format_team(row['Home Team'])}</div>
                        <div class="teams">{format_team(row['Away Team'])}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

except Exception as e:
    st.error(f"An error occurred: {e}")
