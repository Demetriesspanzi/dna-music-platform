import random
import streamlit as st
import os
import sqlite3
import hashlib

# Set up page configurations for a modern, wide enterprise look
st.set_page_config(page_title="DNA Music Platform", page_icon="🧬", layout="wide")

# Ensure our local storage folders exist on the computer / cloud server
TRACK_DIR = "storage_tracks"
COVER_DIR = "storage_covers"
DEFAULT_ASSET_DIR = os.path.join("D:\\PROJECT\\DNA website", "assets_default")

os.makedirs(TRACK_DIR, exist_ok=True)
os.makedirs(COVER_DIR, exist_ok=True)
os.makedirs(DEFAULT_ASSET_DIR, exist_ok=True)

# Initialize conversational AI message arrays inside memory if not already present
if "ai_chat_history" not in st.session_state:
    st.session_state["ai_chat_history"] = [
        {"role": "assistant", "content": "👋 Welcome to the DNA Support Hub! I am the DNA Entertainment Music Platform Assistant AI and I am ready to assist you. Ask me anything!"}
    ]

# Initialize a temporary storage key for the chat input box text string
if "temp_user_query" not in st.session_state:
    st.session_state["temp_user_query"] = ""

# ==========================================
# 🎨 HIGH-CONTRAST CYBER GREEN THEME ENGINE
# ==========================================
st.markdown("""
    <style>
    /* Global App Background Hues & Font Styling */
    .stApp {
        background: linear-gradient(135deg, #050b05 0%, #0a140a 50%, #020502 100%);
        font-family: 'Consolas', 'Courier New', Helvetica, Arial, sans-serif;
    }
    
    /* Main Header Styling */
    h1 {
        color: #ffffff !important;
        font-weight: 800 !important;
        letter-spacing: -1px !important;
        background: linear-gradient(45deg, #00ff66, #00cc44, #33ff33);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 15px rgba(0, 255, 102, 0.2);
    }
    
    /* Sidebar Navigation Container */
    [data-testid="stSidebar"] {
        background-color: #020502 !important;
        border-right: 1px solid rgba(0, 255, 102, 0.1);
    }
    
    /* Premium Track Card Architecture */
    .music-card {
        background: rgba(0, 255, 102, 0.02);
        border: 1px solid rgba(0, 255, 102, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(10px);
    }
    
    .music-card:hover {
        transform: translateY(-4px);
        background: rgba(0, 255, 102, 0.05);
        border-color: rgba(0, 255, 102, 0.5);
        box-shadow: 0 12px 40px rgba(0, 255, 102, 0.2);
    }
    
    /* Fallback Artwork Box Styling */
    .art-placeholder-box {
        border: 2px dashed #00ff66;
        border-radius: 12px;
        height: 180px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(0, 255, 102, 0.03);
        color: #00ff66;
        font-weight: bold;
        text-align: center;
        box-shadow: inset 0 0 15px rgba(0, 255, 102, 0.1);
    }
    
    /* Analytics Mini Metrics Cards */
    .metric-card {
        background: rgba(0, 255, 102, 0.01);
        border: 1px solid rgba(0, 255, 102, 0.15);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    }
    
    /* Force Deep Dark Input Boxes with Stark White/Green Text */
    div[data-testid="stTextInput"] input {
        color: #00ff66 !important;
        background-color: #0d1a0d !important;
        border: 1px solid rgba(0, 255, 102, 0.3) !important;
        border-radius: 8px !important;
        font-size: 16px !important;
    }
    
    div[data-testid="stTextInput"] input:focus {
        border-color: #00ff66 !important;
        box-shadow: 0 0 12px rgba(0, 255, 102, 0.6) !important;
    }
    
    div[data-baseweb="select"] > div {
        background-color: #0d1a0d !important;
        color: #00ff66 !important;
        border: 1px solid rgba(0, 255, 102, 0.3) !important;
        border-radius: 8px !important;
    }
    
    label p {
        color: #00ff66 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        text-shadow: 0 0 5px rgba(0, 255, 102, 0.3);
    }
    
    audio {
        width: 100%;
        margin-top: 15px;
        border-radius: 8px;
    }

    /* AI Conversation Interface Formatting Rules */
    .chat-bubble-user {
        background: #00cc44;
        color: #000000;
        font-weight: 600;
        padding: 10px 14px;
        border-radius: 14px 14px 2px 14px;
        margin-bottom: 10px;
        text-align: right;
        display: block;
        margin-left: 20%;
        font-size: 14px;
        box-shadow: 0 0 8px rgba(0, 255, 102, 0.3);
    }

    .chat-bubble-bot {
        background: rgba(0, 255, 102, 0.08);
        color: #ffffff;
        border: 1px solid rgba(0, 255, 102, 0.2);
        padding: 10px 14px;
        border-radius: 14px 14px 14px 2px;
        margin-bottom: 10px;
        text-align: left;
        display: block;
        margin-right: 20%;
        font-size: 14px;
    }
    
    /* Standard interactive buttons styling */
    .stButton>button {
        background-color: transparent !important;
        color: #00ff66 !important;
        border: 1px solid #00ff66 !important;
        box-shadow: 0 0 8px rgba(0, 255, 102, 0.1);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #00ff66 !important;
        color: #000000 !important;
        font-weight: bold;
        box-shadow: 0 0 15px rgba(0, 255, 102, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🧠 DYNAMIC AI RESPONSE ENGINE
# ==========================================
def process_ai_response(user_text):
    """Processes user text dynamically with expanded keyword mapping for smarter matching."""
    query = user_text.strip().lower()
    
    if any(x in query for x in ["your name", "who are you", "what are you", "identity"]):
        return "🧬 My name is **DNA Entertainment Music Platform Assistant AI** and I am ready to assist you with any clarity or navigation questions you have about this website!"
    elif any(x in query for x in ["hello", "hi", "hey", "greetings", "yo"]):
        return "👋 Hello! I am the DNA Entertainment Music Platform Assistant AI. How can I assist you with the platform today?"
    elif any(x in query for x in ["admin", "purge", "delete", "remove", "unlink", "clear"]):
        return "🛡️ **Administrative Controls:** The **Admin Operations Deck** allows system operators to check live data storage volumes, audit ledger validity signatures, simulate security compromises, or cleanly unlink records from the storage system."
    elif any(x in query for x in ["upload", "publish", "artist", "add track", "submit", "song release"]):
        return "🚀 **How to Publish:** Head over to the **Artist Upload Center** using the control panel above. Fill out the track title, artist info, select a genre, upload your audio binary file (.mp3), and submit it directly to our secure database network link."
    elif any(x in query for x in ["download", "save", "get track", "export", "transfer"]):
        return "📥 **File Transfers:** In the **Fan Explorer Feed**, each song card has a high-fidelity download pipeline. Simply click the download button to grab a clean copy of the source audio payload asset."
    elif any(x in query for x in ["genre", "afrobeats", "amapiano", "hip-hop", "style", "music"]):
        return "🎵 **Music Navigation:** The system is optimized to filter and group modern music styles like Afrobeats, Amapiano, Hip-Hop, R&B, and more. Use the filtering tools on the discovery feed to query exactly what you want to hear."
    elif any(x in query for x in ["blockchain", "cryptographic", "ledger", "hash", "security", "tamper", "safe"]):
        return "🛡️ **Ledger Architecture Clarity:** This platform uses a Layer-2 blockchain framework. Every song uploaded is compiled into a unique cryptographic block with an immutable SHA-256 validation string. If anyone modifies the records outside the application, our scanners flag the structural breach instantly."
    else:
        return f"💡 **DNA Assistant Response:** You asked about '{user_text}'. As the DNA Platform Assistant AI, I can clarify that this application is split into three main hubs: the **Fan Explorer Feed** for streaming/downloading, the **Artist Upload Center** for secure publishing, and the **Admin Deck** for verifying our cryptographic database ledger chain integrity. Let me know if you need more specifics on any of these elements!"

# ==========================================
# 🛠️ CHAT PIPELINE AUTOCLEAR SYSTEM HANDLER
# ==========================================
def submit_ai_query_action():
    """Extracts user submission message input parameters, saves responses, and purges the box state value."""
    raw_query_text = st.session_state["ai_input_bar_field"]
    
    if raw_query_text.strip() != "":
        st.session_state["ai_chat_history"].append({"role": "user", "content": raw_query_text})
        ai_reply = process_ai_response(raw_query_text)
        st.session_state["ai_chat_history"].append({"role": "assistant", "content": ai_reply})
        st.session_state["ai_input_bar_field"] = ""

# ==========================================
# 🔐 🛠️ FIXED: PERSISTENT DATABASE UPGRADE
# ==========================================
# Changing from memory to a physical local file guarantees permanent cloud storage retention
DB_FILE = "dna_database.db"

if "sqlite_memory_connection" not in st.session_state:
    st.session_state["sqlite_memory_connection"] = sqlite3.connect(DB_FILE, check_same_thread=False)
    cursor = st.session_state["sqlite_memory_connection"].cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tracks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            artist TEXT NOT NULL,
            genre TEXT,
            audio_path TEXT,
            cover_path TEXT,
            current_hash TEXT,
            previous_hash TEXT
        )
    """)
    st.session_state["sqlite_memory_connection"].commit()

def calculate_block_hash(index, title, artist, genre, audio_path, cover_path, previous_hash):
    """Generates a secure SHA-256 validation string acting as an immutable digital fingerprint."""
    payload_string = f"{index}{title}{artist}{genre}{audio_path}{cover_path}{previous_hash}"
    return hashlib.sha256(payload_string.encode('utf-8')).hexdigest()

def save_track_to_db(title, artist, genre, audio_path, cover_path):
    """Chains a new submission securely using verification hashing into database layers."""
    conn = st.session_state["sqlite_memory_connection"]
    cursor = conn.cursor()
    cursor.execute("SELECT current_hash FROM tracks ORDER BY id DESC LIMIT 1")
    last_row = cursor.fetchone()
    
    if last_row and last_row[0] != "":
        previous_hash = last_row[0]
    else:
        previous_hash = "0000000000000000000000000000000000000000000000000000000000000000"
    
    cursor.execute("SELECT max(id) FROM tracks")
    max_id = cursor.fetchone()[0]
    next_id = (max_id + 1) if max_id else 1
    
    current_hash = calculate_block_hash(next_id, title, artist, genre, audio_path, cover_path, previous_hash)
    
    cursor.execute("""
        INSERT INTO tracks (title, artist, genre, audio_path, cover_path, current_hash, previous_hash)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (title, artist, genre, audio_path, cover_path, current_hash, previous_hash))
    conn.commit()

def fetch_all_tracks():
    """Retrieves all registered releases chronologically, guaranteeing schema safety tags."""
    conn = st.session_state["sqlite_memory_connection"]
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tracks ORDER BY id DESC")
    return [dict(row) for row in cursor.fetchall()]

def verify_ledger_integrity():
    """Audits the chain to identify any unauthorized data manipulation."""
    conn = st.session_state["sqlite_memory_connection"]
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tracks ORDER BY id ASC")
    all_blocks = [dict(row) for row in cursor.fetchall()]
    
    expected_previous = "0000000000000000000000000000000000000000000000000000000000000000"
    
    for block in all_blocks:
        curr_h = block.get("current_hash", "") or ""
        prev_h = block.get("previous_hash", "") or ""
        if curr_h == "" and prev_h == "":
            continue
        if prev_h != expected_previous:
            return False, f"Broken Chain Link at Track ID {block['id']} ('{block['title']}')."
            
        recalculated = calculate_block_hash(
            block["id"], block["title"], block["artist"], block["genre"],
            block["audio_path"], block["cover_path"], prev_h
        )
        if curr_h != recalculated:
            return False, f"Data Alteration Detected inside Track ID {block['id']} ('{block['title']}')."
        expected_previous = curr_h
        
    return True, "Ledger verified. All structural properties are untampered and structurally authentic."

def simulate_malicious_tamper():
    """Forces an unauthorized backend update directly into SQL to test tamper-evidence alerts."""
    conn = st.session_state["sqlite_memory_connection"]
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM tracks ORDER BY id DESC LIMIT 1")
    target = cursor.fetchone()
    if target:
        tampered_title = f"{target[1]} (HACKED_PAYLOAD)"
        cursor.execute("UPDATE tracks SET title = ? WHERE id = ?", (tampered_title, target[0]))
        conn.commit()
        return True, target[0]
    return False, None

def delete_track_from_db(track_id, audio_path, cover_path):
    """Safely unlinks assets and deletes the record row."""
    if audio_path and os.path.exists(audio_path):
        try: os.remove(audio_path)
        except: pass
    if cover_path and os.path.exists(cover_path):
        try: os.remove(cover_path)
        except: pass
        
    conn = st.session_state["sqlite_memory_connection"]
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tracks WHERE id = ?", (track_id,))
    conn.commit()
    realign_ledger_hashes()

def realign_ledger_hashes():
    """Rebuilds verification hash links when an admin removes an entry cleanly."""
    conn = st.session_state["sqlite_memory_connection"]
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tracks ORDER BY id ASC")
    rows = [dict(row) for row in cursor.fetchall()]
    
    expected_prev = "0000000000000000000000000000000000000000000000000000000000000000"
    for r in rows:
        if (r.get("current_hash") or "") == "" and (r.get("previous_hash") or "") == "":
            continue
        new_curr = calculate_block_hash(
            r["id"], r["title"], r["artist"], r["genre"],
            r["audio_path"], r["cover_path"], expected_prev
        )
        cursor.execute("UPDATE tracks SET current_hash = ?, previous_hash = ? WHERE id = ?", (new_curr, expected_prev, r["id"]))
        expected_prev = new_curr
    conn.commit()

# ==========================================
# HEADER & APPLICATION BANNER LAYOUT
# ==========================================
st.title("🧬 Determined Notable Achievers (DNA) Music Platform")
st.markdown("<h5 style='color: #88af88; margin-top:-10px;'>Empowering talent, preserving sound architecture, and distributing greatness permanently.</h5>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 🧭 CONTROL PANEL & SIDEBAR CONTEXT HUBS
# ==========================================
st.sidebar.title("🧭 DNA Control Panel")
st.sidebar.write("Welcome to the **DNA Network Server**.")
app_mode = st.sidebar.radio("Go to Panel:", ["🎧 Fan Explorer Feed", "🚀 Artist Upload Center", "🛡️ Admin Operations Deck"])

st.sidebar.markdown("---")

st.sidebar.subheader("💬 DNA System Assistant")
st.sidebar.caption("Ask questions to clarify how platform modules work.")

for dialogue in st.session_state["ai_chat_history"]:
    bubble_style = "chat-bubble-user" if dialogue["role"] == "user" else "chat-bubble-bot"
    st.sidebar.markdown(f'<div class="{bubble_style}">{dialogue["content"]}</div>', unsafe_allow_html=True)

st.sidebar.text_input(
    "Clarify something:", 
    key="ai_input_bar_field", 
    placeholder="e.g., What is your name?",
    on_change=submit_ai_query_action
)
st.sidebar.caption("💡 *Tip: Press Enter on your keyboard inside the field to send immediately!*")

# ==========================================
# MODULE 1: ARTIST UPLOAD CENTER
# ==========================================
if app_mode == "🚀 Artist Upload Center":
    st.header("🚀 DNA Artist Release Studio")
    st.subheader("Publish your audio waves directly to the permanent global discovery pipeline.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📝 Release Metadata")
        track_title = st.text_input("Track Title", placeholder="e.g., Midnight Drive")
        artist_name = st.text_input("Artist Name / Group", placeholder="e.g., Demetries")
        track_genre = st.selectbox("Primary Sonic Genre", [
            "Afrobeats", "Hip-Hop / Rap", "R&B / Soul", "Amapiano", 
            "Electronic / Dance", "Reggae", "Acoustic / Indie"
        ])
    with col2:
        st.markdown("### 📁 Media Asset Pipelines")
        uploaded_audio = st.file_uploader("Upload Audio Track (.mp3 format)", type=["mp3"])
        uploaded_cover = st.file_uploader("Upload Cover Visual Asset (.jpg / .png)", type=["jpg", "png", "jpeg"])

    st.markdown("---")
    if st.button("⚡ Broadcast Release to DNA Network Feed", use_container_width=True):
        if not track_title or not artist_name:
            st.error("Submission Error: Track title and Artist name parameters cannot be left blank.")
        elif not uploaded_audio:
            st.warning("Missing Assets: Please attach a valid audio payload (.mp3 file) to register track data.")
        else:
            safe_filename = f"{track_title}_{artist_name}".replace(" ", "_")
            audio_destination = os.path.join(TRACK_DIR, f"{safe_filename}.mp3")
            with open(audio_destination, "wb") as f:
                f.write(uploaded_audio.getbuffer())
                
            cover_destination = None
            if uploaded_cover:
                cover_destination = os.path.join(COVER_DIR, f"{safe_filename}.png")
                with open(cover_destination, "wb") as f:
                    f.write(uploaded_cover.getbuffer())
                    
            save_track_to_db(track_title, artist_name, track_genre, audio_destination, cover_destination)
            st.success(f"✨ Success! '{track_title}' has been verified via SHA-256 and chained to the DNA database ledger.")
            st.balloons()

# ==========================================
# MODULE 2: FAN EXPLORER & MUSIC DISCOVERY FEED
# ==========================================
elif app_mode == "🎧 Fan Explorer Feed":
    st.header("🎧 DNA Live Stream & Asset Distribution Deck")
    st.write("Browse permanent database releases, preview audio instantly, and grab direct high-fidelity file transfers.")
    
    # Permanent layout images row
    st.markdown("### ⚡ Featured Fan Visuals")
    img_col1, img_col2, img_col3 = st.columns(3)
    with img_col1:
        st.image("https://images.unsplash.com/photo-1546435770-a3e426bf472b?q=80&w=600&auto=format&fit=crop", caption="Neon Beats Studio", use_container_width=True)
    with img_col2:
        st.image("https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?q=80&w=600&auto=format&fit=crop", caption="Digital Audio Waves", use_container_width=True)
    with img_col3:
        st.image("https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?q=80&w=600&auto=format&fit=crop", caption="Live Sound Control", use_container_width=True)
    
    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    
    search_col, filter_col = st.columns([2, 1])
    with search_col:
        search_query = st.text_input("🔍 Search Tracks or Artists", placeholder="Type a song title or artist name...")
    with filter_col:
        genre_filter = st.selectbox("🏷️ Filter by Genre", [
            "All Genres", "Afrobeats", "Hip-Hop / Rap", "R&B / Soul", "Amapiano", 
            "Electronic / Dance", "Reggae", "Acoustic / Indie"
        ])
    
    st.markdown("<br>", unsafe_allow_html=True)
    db_catalog = fetch_all_tracks()
    filtered_catalog = []
    for song in db_catalog:
        matches_search = (search_query.lower() in song["title"].lower() or search_query.lower() in song["artist"].lower())
        matches_genre = (genre_filter == "All Genres" or song["genre"] == genre_filter)
        if matches_search and matches_genre:
            filtered_catalog.append(song)
            
    if len(db_catalog) == 0:
        st.info("The discovery pipeline is currently empty. Switch to the Artist Center to publish the platform's very first track!")
    elif len(filtered_catalog) == 0:
        st.warning("No matching tracks found. Try adjusting your search keywords or genre filter parameters.")
    else:
        for index, song in enumerate(filtered_catalog):
            st.markdown(f'<div class="music-card"><div style="display: flex; flex-wrap: wrap; align-items: center;"><div id="card_body_{index}" style="flex: 1; min-width: 200px;"></div></div></div>', unsafe_allow_html=True)
            with st.container():
                col_img, col_info, col_actions = st.columns([1.5, 4, 2.5])
                with col_img:
                    if song["cover_path"] and os.path.exists(song["cover_path"]):
                        st.image(song["cover_path"], use_container_width=True)
                    else:
                        local_placeholders = ["headphones.jpg", "waves.jpg", "soundboard.jpg"]
                        chosen_filename = local_placeholders[song["id"] % len(local_placeholders)]
                        full_local_path = os.path.join(DEFAULT_ASSET_DIR, chosen_filename)
                        
                        if os.path.exists(full_local_path):
                            st.image(full_local_path, use_container_width=True)
                        else:
                            st.markdown(f'<div class="art-placeholder-box">🧬 DNA STUDIO<br>TRACK ID: {song["id"]}</div>', unsafe_allow_html=True)
                        
                with col_info:
                    st.markdown(f'<div style="color:#00ff66; font-size:22px; font-weight:bold;">{song["title"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div style="color:#ffffff; margin: 4px 0;">🏆 {song["artist"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div style="color:#88af88; font-size:14px;">🏷️ {song["genre"]}</div>', unsafe_allow_html=True)
                    if song["audio_path"] and os.path.exists(song["audio_path"]):
                        with open(song["audio_path"], "rb") as audio_file:
                            st.audio(audio_file.read(), format="audio/mp3")
                    else:
                        st.warning("⚠️ Streaming file missing from server storage.")
                with col_actions:
                    st.write(" "); st.write(" "); st.write(" ")
                    if song["audio_path"] and os.path.exists(song["audio_path"]):
                        with open(song["audio_path"], "rb") as download_target:
                            st.download_button(
                                label="📥 Download High-Fi Track",
                                data=download_target,
                                file_name=f"{song['title']} - {song['artist']}.mp3",
                                mime="audio/mp3",
                                key=f"dl_{song['id']}_{index}",
                                use_container_width=True
                            )
                    else:
                        st.button("🔒 File Unavailable", disabled=True, use_container_width=True, key=f"disabled_{index}")
            st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# MODULE 3: ADMIN OPERATIONS & ANALYTICS DECK
# ==========================================
elif app_mode == "🛡️ Admin Operations Deck":
    # 🌌 IMMERSIVE COMMAND CENTER BACKGROUND IMAGE INJECTION
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(rgba(5, 11, 5, 0.88), rgba(2, 5, 2, 0.92)), 
                        url("https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=1600&auto=format&fit=crop") !important;
            background-size: cover !important;
            background-position: center !important;
            background-attachment: fixed !important;
        }
        .metric-card {
            background: rgba(0, 20, 5, 0.70) !important;
            backdrop-filter: blur(16px) !important;
            border: 1px solid rgba(0, 255, 102, 0.35) !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.8) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.header("🛡️ Secure Infrastructure Operations Panel")
    st.subheader("Manage active system catalogs, view hardware analytics, and monitor ledger integrity.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    admin_catalog = fetch_all_tracks()
    
    st.markdown("### 🔐 Cryptographic Ledger Integrity Scan")
    is_valid, alert_msg = verify_ledger_integrity()
    if is_valid:
        st.success(f"💚 **SYSTEM SECURE:** {alert_msg}")
    else:
        st.error(f"🚨 **SECURITY BREACH DETECTED:** {alert_msg}")
        if st.button("🔧 Force Cryptographic Chain Realignment", use_container_width=True):
            realign_ledger_hashes()
            st.toast("Re-anchored entire ledger successfully!", icon="✅")
            st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        
    st.markdown("---")
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.markdown(f'<div class="metric-card"><h4 style="color:#88af88; margin:0;">Total Catalog Releases</h4><h1 style="margin:10px 0 0 0; color:#00ff66;">{len(admin_catalog)}</h1></div>', unsafe_allow_html=True)
    with m_col2:
        audio_files_count = len([f for f in os.listdir(TRACK_DIR) if f.endswith('.mp3')])
        st.markdown(f'<div class="metric-card"><h4 style="color:#88af88; margin:0;">Disk Audio Assets</h4><h1 style="margin:10px 0 0 0; color:#00ff66;">{audio_files_count} Files</h1></div>', unsafe_allow_html=True)
    with m_col3:
        cover_files_count = len([f for f in os.listdir(COVER_DIR) if f.endswith(('.png', '.jpg', '.jpeg'))])
        st.markdown(f'<div class="metric-card"><h4 style="color:#88af88; margin:0;">Disk Visual Assets</h4><h1 style="margin:10px 0 0 0; color:#00ff66;">{cover_files_count} Items</h1></div>', unsafe_allow_html=True)
        
    st.markdown("<br><br>### ⚠️ Security Simulation Lab", unsafe_allow_html=True)
    st.write("Inject an unauthorized title modification directly into a SQLite data row to verify how mathematical validation immediately breaks.")
    if len(admin_catalog) == 0:
        st.info("Upload at least one track to unlock the security testing lab.")
    else:
        if st.button("💥 Simulate Malicious Ledger Tampering", type="secondary"):
            success, target_id = simulate_malicious_tamper()
            if success:
                st.toast(f"Tampered row element ID {target_id} directly inside SQLite!", icon="☣️")
                st.rerun()

    st.markdown("<br><br>### 📋 System Catalog Auditor & Record Unlinker", unsafe_allow_html=True)
    if len(admin_catalog) == 0:
        st.info("The system database ledger is currently clear. No active records allocated to memory.")
    else:
        for idx, row in enumerate(admin_catalog):
            with st.container():
                c_title, c_artist, c_hash, c_action = st.columns([2.5, 2, 2.5, 2])
                with c_title:
                    st.markdown(f"**Track:** <span style='color:#00ff66;'>{row['title']}</span>", unsafe_allow_html=True)
                with c_artist:
                    st.markdown(f"**Artist:** {row['artist']}")
                with c_hash:
                    track_hash = row.get('current_hash', '') or ''
                    display_hash = f"...{str(track_hash)[-12:]}" if track_hash else "LEGACY REC"
                    st.markdown(f"📂 `{display_hash}`")
                with c_action:
                    if st.button("🗑️ Purge Release", key=f"del_btn_{row['id']}_{idx}", use_container_width=True):
                        delete_track_from_db(row['id'], row['audio_path'], row['cover_path'])
                        st.toast(f"Purged: '{row['title']}' unlinked successfully!", icon="🔥")
                        st.rerun()
            st.markdown("<hr style='margin:10px 0; border-color:rgba(0,255,102,0.1);'>", unsafe_allow_html=True)