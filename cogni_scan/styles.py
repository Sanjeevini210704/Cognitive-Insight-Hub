CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');

:root {
  --bg: #0F1430;
  --bg-2: #141A3B;
  --card: #161D40;
  --card-2: #1B2349;
  --border: #262E55;
  --text: #E6E9F5;
  --muted: #9AA3B8;
  --primary: #8B5DDB;
  --primary-2: #7C3AED;
  --accent: #9D6BFF;
  --destructive: #D9265E;
}

html, body, [class*="css"], .stApp, .main {
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  background: var(--bg) !important;
  color: var(--text) !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header[data-testid="stHeader"] {visibility: hidden;}
.stDeployButton {display: none;}
[data-testid="stToolbar"] {display: none;}
.block-container {padding-top: 1rem; max-width: 1200px;}

/* Sidebar */
section[data-testid="stSidebar"] {
  background: #0B1029 !important;
  border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] * { color: var(--text); }

/* Buttons */
.stButton > button, .stDownloadButton > button, .stFormSubmitButton > button {
  background: var(--primary) !important;
  color: #fff !important;
  border: 1px solid var(--primary-2) !important;
  border-radius: 999px !important;
  font-weight: 600 !important;
  padding: 0.55rem 1.4rem !important;
  transition: all .2s ease;
  box-shadow: 0 4px 18px rgba(139,93,219,0.25);
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
  background: var(--accent) !important;
  box-shadow: 0 6px 24px rgba(139,93,219,0.45);
}
.stButton > button[kind="secondary"] {
  background: transparent !important;
  border: 1px solid var(--border) !important;
  color: var(--text) !important;
  box-shadow: none;
}
.stButton > button[kind="secondary"]:hover { background: var(--card-2) !important; }

/* Inputs */
.stTextInput > div > div > input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] > div,
.stPasswordInput input {
  background: #1A2148 !important;
  border: 1px solid var(--border) !important;
  color: var(--text) !important;
  border-radius: 10px !important;
}
.stTextArea textarea { font-family: 'Space Mono', monospace !important; font-size: 13px !important; }
label, .stTextInput label, .stTextArea label, .stSelectbox label {
  color: var(--muted) !important;
  font-family: 'Space Mono', monospace !important;
  font-size: 11px !important;
  text-transform: uppercase !important;
  letter-spacing: 0.08em !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 6px; border-bottom: 1px solid var(--border); }
.stTabs [data-baseweb="tab"] {
  background: transparent; color: var(--muted);
  font-family: 'Space Mono', monospace; font-size: 12px;
  text-transform: uppercase; letter-spacing: 0.08em;
  padding: 8px 16px; border-radius: 8px 8px 0 0;
}
.stTabs [aria-selected="true"] { color: var(--primary) !important; border-bottom: 2px solid var(--primary); }

/* Metrics */
[data-testid="stMetric"] {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 16px 18px;
}
[data-testid="stMetricLabel"] {
  color: var(--muted) !important;
  font-family: 'Space Mono', monospace !important;
  font-size: 10px !important;
  text-transform: uppercase; letter-spacing: 0.1em;
}
[data-testid="stMetricValue"] { color: var(--text) !important; font-weight: 800 !important; }

/* Dataframe */
[data-testid="stDataFrame"] { background: var(--card); border-radius: 12px; padding: 4px; border: 1px solid var(--border);}

/* Custom blocks */
.cs-nav {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 22px; border: 1px solid var(--border); border-radius: 14px;
  background: rgba(15,20,48,0.85); backdrop-filter: blur(8px);
  margin-bottom: 28px;
}
.cs-logo { display: flex; align-items: center; gap: 10px; font-weight: 800; letter-spacing: -0.02em; font-size: 17px;}
.cs-logo .mark { width: 22px; height: 22px; border-radius: 5px; background: var(--primary); display: flex; align-items: center; justify-content: center;}
.cs-logo .mark .dot { width: 10px; height: 10px; border-radius: 50%; background: var(--bg);}
.cs-tag {
  margin-left: 8px; padding: 3px 8px; border-radius: 6px;
  background: var(--card-2); color: var(--muted);
  font-family: 'Space Mono', monospace; font-size: 10px;
  text-transform: uppercase; letter-spacing: 0.08em;
}

.cs-badge {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 5px 12px; border-radius: 999px;
  background: rgba(139,93,219,0.12); color: var(--accent);
  border: 1px solid rgba(139,93,219,0.35);
  font-family: 'Space Mono', monospace; font-size: 11px; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.08em;
  margin-bottom: 22px;
}
.cs-badge .pulse {
  width: 8px; height: 8px; border-radius: 50%; background: var(--accent);
  box-shadow: 0 0 0 4px rgba(157,107,255,0.3); animation: pulse 1.6s infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.5} }

.cs-hero h1 {
  font-size: clamp(34px, 5vw, 64px); font-weight: 800;
  letter-spacing: -0.03em; line-height: 1.05; margin: 0 0 18px;
}
.cs-hero h1 .grad {
  background: linear-gradient(90deg, var(--primary), var(--accent));
  -webkit-background-clip: text; background-clip: text; color: transparent;
}
.cs-hero p { color: var(--muted); font-size: 17px; max-width: 640px; margin: 0 auto 28px; line-height: 1.55;}

.cs-card {
  background: var(--card); border: 1px solid var(--border);
  border-radius: 16px; padding: 22px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.25);
}
.cs-card h3 {
  font-family: 'Space Mono', monospace; font-size: 11px; color: var(--muted);
  text-transform: uppercase; letter-spacing: 0.1em; margin: 0 0 14px;
}

.cs-step .num {
  font-family: 'Space Mono', monospace; font-size: 44px; font-weight: 700;
  color: var(--border); margin-bottom: 8px; line-height: 1;
}
.cs-step h4 { font-size: 19px; font-weight: 700; margin: 0 0 6px;}
.cs-step p { color: var(--muted); margin: 0; line-height: 1.5;}

.cs-window {
  border-radius: 16px; border: 1px solid var(--border); overflow: hidden;
  background: var(--card); box-shadow: 0 24px 60px rgba(0,0,0,0.45);
}
.cs-window-bar {
  height: 38px; background: var(--card-2); border-bottom: 1px solid var(--border);
  display: flex; align-items: center; gap: 8px; padding: 0 14px; position: relative;
}
.cs-dot { width: 11px; height: 11px; border-radius: 50%;}
.cs-dot.r { background: var(--destructive);}
.cs-dot.y { background: var(--accent);}
.cs-dot.g { background: var(--primary);}
.cs-window-url {
  position: absolute; left: 50%; transform: translateX(-50%);
  font-family: 'Space Mono', monospace; font-size: 11px; color: var(--muted);
  background: var(--bg); padding: 3px 12px; border-radius: 6px; border: 1px solid var(--border);
}

.cs-risk-box {
  background: var(--card); border: 1px solid var(--border);
  border-radius: 14px; padding: 18px 22px; text-align: center; min-width: 180px;
}
.cs-risk-box .lbl {
  color: var(--muted); font-family: 'Space Mono', monospace;
  font-size: 10px; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 4px;
}
.cs-risk-box .val { font-size: 48px; font-weight: 900; line-height: 1;}
.cs-risk-box .val.high { color: var(--destructive);}
.cs-risk-box .val.mid  { color: var(--accent);}
.cs-risk-box .val.low  { color: var(--primary);}

.cs-pill {
  display: inline-block; padding: 4px 10px; border-radius: 999px;
  background: rgba(139,93,219,0.12); color: var(--primary);
  font-family: 'Space Mono', monospace; font-size: 11px;
  text-transform: uppercase; letter-spacing: 0.08em; font-weight: 700;
  margin-right: 8px;
}
.cs-meta {
  font-family: 'Space Mono', monospace; font-size: 11px; color: var(--muted);
}

.cs-hr { height: 1px; background: var(--border); margin: 18px 0;}

.cs-impact {
  background: rgba(139,93,219,0.07); border: 1px solid rgba(139,93,219,0.25);
  border-left: 3px solid var(--primary);
  padding: 14px 18px; border-radius: 10px; color: var(--text); line-height: 1.55;
}

.cs-foot {
  margin-top: 50px; padding: 22px 0; border-top: 1px solid var(--border);
  display: flex; justify-content: space-between; align-items: center;
  color: var(--muted); font-family: 'Space Mono', monospace; font-size: 12px;
}

@media print {
  section[data-testid="stSidebar"], .cs-nav, .stButton { display: none !important; }
}
</style>
"""
