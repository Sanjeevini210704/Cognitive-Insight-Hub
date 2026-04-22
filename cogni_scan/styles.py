CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');

:root {
  --bg: #F4F3FB;
  --bg-2: #ECEAF7;
  --card: #FFFFFF;
  --card-2: #F7F5FD;
  --border: #E3DFF2;
  --text: #1A1B36;
  --muted: #6B7191;
  --primary: #7C5CE6;
  --primary-2: #6A47D8;
  --accent: #B68BFF;
  --destructive: #E0365F;
  --success: #1FB57A;
}

html, body, [class*="css"], .stApp, .main {
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  background:
    radial-gradient(900px 500px at 10% -10%, rgba(124,92,230,0.18), transparent 60%),
    radial-gradient(900px 500px at 95% 5%, rgba(182,139,255,0.16), transparent 60%),
    var(--bg) !important;
  color: var(--text) !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header[data-testid="stHeader"] {visibility: hidden;}
.stDeployButton {display: none;}
[data-testid="stToolbar"] {display: none;}
.block-container {padding-top: 1rem; max-width: 1200px;}

/* Sidebar */
section[data-testid="stSidebar"] {
  background: #FFFFFF !important;
  border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] * { color: var(--text); }

/* Buttons */
.stButton > button, .stDownloadButton > button, .stFormSubmitButton > button {
  background: linear-gradient(135deg, var(--primary), var(--accent)) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 999px !important;
  font-weight: 600 !important;
  padding: 0.6rem 1.5rem !important;
  transition: all .2s ease;
  box-shadow: 0 6px 22px rgba(124,92,230,0.30);
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 28px rgba(124,92,230,0.40);
}
.stButton > button[kind="secondary"] {
  background: #FFFFFF !important;
  border: 1px solid var(--border) !important;
  color: var(--text) !important;
  box-shadow: 0 1px 3px rgba(20,20,50,0.06);
}
.stButton > button[kind="secondary"]:hover {
  background: var(--card-2) !important;
  border-color: var(--primary) !important;
  color: var(--primary) !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] > div,
.stPasswordInput input {
  background: #FFFFFF !important;
  border: 1px solid var(--border) !important;
  color: var(--text) !important;
  border-radius: 12px !important;
  box-shadow: 0 1px 2px rgba(20,20,50,0.04);
}
.stTextInput > div > div > input:focus,
.stTextArea textarea:focus {
  border-color: var(--primary) !important;
  box-shadow: 0 0 0 3px rgba(124,92,230,0.15) !important;
}
.stTextArea textarea { font-family: 'Space Mono', monospace !important; font-size: 13px !important; }
label, .stTextInput label, .stTextArea label, .stSelectbox label {
  color: var(--muted) !important;
  font-family: 'Space Mono', monospace !important;
  font-size: 11px !important;
  text-transform: uppercase !important;
  letter-spacing: 0.08em !important;
}
.stCheckbox label p { color: var(--text) !important; font-family: 'Plus Jakarta Sans', sans-serif !important; text-transform: none !important; letter-spacing: normal !important; font-size: 14px !important;}

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
  border-radius: 16px;
  padding: 18px 20px;
  box-shadow: 0 4px 18px rgba(20,20,50,0.05);
}
[data-testid="stMetricLabel"] {
  color: var(--muted) !important;
  font-family: 'Space Mono', monospace !important;
  font-size: 10px !important;
  text-transform: uppercase; letter-spacing: 0.1em;
}
[data-testid="stMetricValue"] { color: var(--text) !important; font-weight: 800 !important; }

/* Dataframe */
[data-testid="stDataFrame"] {
  background: var(--card); border-radius: 14px; padding: 4px;
  border: 1px solid var(--border);
  box-shadow: 0 4px 18px rgba(20,20,50,0.05);
}

/* Custom blocks */
.cs-nav {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 22px; border: 1px solid var(--border); border-radius: 16px;
  background: rgba(255,255,255,0.85); backdrop-filter: blur(10px);
  margin-bottom: 28px; box-shadow: 0 4px 24px rgba(20,20,50,0.06);
}
.cs-logo { display: flex; align-items: center; gap: 10px; font-weight: 800; letter-spacing: -0.02em; font-size: 17px; color: var(--text);}
.cs-logo .mark {
  width: 24px; height: 24px; border-radius: 7px;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 4px 12px rgba(124,92,230,0.4);
}
.cs-logo .mark .dot { width: 10px; height: 10px; border-radius: 50%; background: #FFFFFF;}
.cs-tag {
  margin-left: 8px; padding: 3px 10px; border-radius: 6px;
  background: var(--card-2); color: var(--primary);
  font-family: 'Space Mono', monospace; font-size: 10px; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.08em;
  border: 1px solid var(--border);
}

.cs-badge {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 6px 14px; border-radius: 999px;
  background: rgba(124,92,230,0.10); color: var(--primary);
  border: 1px solid rgba(124,92,230,0.25);
  font-family: 'Space Mono', monospace; font-size: 11px; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.08em;
  margin-bottom: 22px;
}
.cs-badge .pulse {
  width: 8px; height: 8px; border-radius: 50%; background: var(--primary);
  box-shadow: 0 0 0 4px rgba(124,92,230,0.25); animation: pulse 1.6s infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.5} }

.cs-hero h1 {
  font-size: clamp(34px, 5vw, 64px); font-weight: 800;
  letter-spacing: -0.03em; line-height: 1.05; margin: 0 0 18px;
  color: var(--text);
}
.cs-hero h1 .grad {
  background: linear-gradient(90deg, var(--primary), var(--accent), #E37BC4);
  -webkit-background-clip: text; background-clip: text; color: transparent;
}
.cs-hero p { color: var(--muted); font-size: 17px; max-width: 640px; margin: 0 auto 28px; line-height: 1.55;}

.cs-card {
  background: var(--card); border: 1px solid var(--border);
  border-radius: 18px; padding: 24px;
  box-shadow: 0 6px 28px rgba(20,20,50,0.06);
}
.cs-card h3 {
  font-family: 'Space Mono', monospace; font-size: 11px; color: var(--muted);
  text-transform: uppercase; letter-spacing: 0.1em; margin: 0 0 14px;
}

.cs-step {
  background: var(--card); border: 1px solid var(--border);
  border-radius: 18px; padding: 24px;
  box-shadow: 0 6px 28px rgba(20,20,50,0.05);
  transition: transform .2s ease, box-shadow .2s ease;
}
.cs-step:hover { transform: translateY(-3px); box-shadow: 0 12px 36px rgba(124,92,230,0.15);}
.cs-step .num {
  font-family: 'Space Mono', monospace; font-size: 44px; font-weight: 700;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  -webkit-background-clip: text; background-clip: text; color: transparent;
  margin-bottom: 8px; line-height: 1;
}
.cs-step h4 { font-size: 19px; font-weight: 700; margin: 0 0 6px; color: var(--text);}
.cs-step p { color: var(--muted); margin: 0; line-height: 1.5;}

.cs-window {
  border-radius: 18px; border: 1px solid var(--border); overflow: hidden;
  background: var(--card); box-shadow: 0 24px 60px rgba(124,92,230,0.18);
}
.cs-window-bar {
  height: 40px; background: var(--card-2); border-bottom: 1px solid var(--border);
  display: flex; align-items: center; gap: 8px; padding: 0 14px; position: relative;
}
.cs-dot { width: 11px; height: 11px; border-radius: 50%;}
.cs-dot.r { background: #FF6058;}
.cs-dot.y { background: #FFBD2E;}
.cs-dot.g { background: #28CA42;}
.cs-window-url {
  position: absolute; left: 50%; transform: translateX(-50%);
  font-family: 'Space Mono', monospace; font-size: 11px; color: var(--muted);
  background: #FFFFFF; padding: 4px 14px; border-radius: 6px; border: 1px solid var(--border);
}

.cs-risk-box {
  background: var(--card); border: 1px solid var(--border);
  border-radius: 16px; padding: 20px 24px; text-align: center; min-width: 180px;
  box-shadow: 0 6px 24px rgba(20,20,50,0.06);
}
.cs-risk-box .lbl {
  color: var(--muted); font-family: 'Space Mono', monospace;
  font-size: 10px; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px;
}
.cs-risk-box .val { font-size: 52px; font-weight: 900; line-height: 1;}
.cs-risk-box .val.high { color: var(--destructive);}
.cs-risk-box .val.mid  { color: #E89A2E;}
.cs-risk-box .val.low  { color: var(--success);}

.cs-pill {
  display: inline-block; padding: 5px 12px; border-radius: 999px;
  background: rgba(124,92,230,0.12); color: var(--primary);
  font-family: 'Space Mono', monospace; font-size: 11px;
  text-transform: uppercase; letter-spacing: 0.08em; font-weight: 700;
  margin-right: 8px; border: 1px solid rgba(124,92,230,0.18);
}
.cs-meta {
  font-family: 'Space Mono', monospace; font-size: 11px; color: var(--muted);
}

.cs-hr { height: 1px; background: var(--border); margin: 18px 0;}

.cs-impact {
  background: linear-gradient(135deg, rgba(124,92,230,0.08), rgba(182,139,255,0.05));
  border: 1px solid rgba(124,92,230,0.20);
  border-left: 4px solid var(--primary);
  padding: 16px 20px; border-radius: 12px; color: var(--text); line-height: 1.55;
}

.cs-foot {
  margin-top: 50px; padding: 22px 0; border-top: 1px solid var(--border);
  display: flex; justify-content: space-between; align-items: center;
  color: var(--muted); font-family: 'Space Mono', monospace; font-size: 12px;
}

/* Alerts */
[data-testid="stAlert"] {
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  color: var(--text) !important;
}

@media print {
  section[data-testid="stSidebar"], .cs-nav, .stButton { display: none !important; }
}
</style>
"""
