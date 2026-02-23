import streamlit as st
import pandas as pd

# ===================================
# CONFIG
# ===================================
st.set_page_config(
    page_title="Portal NPSN V8 Cinema",
    layout="wide"
)

# ===================================
# 🎨 CLEAN CINEMA CSS
# ===================================
st.markdown("""
<style>

.stApp{
    background:#f4f7fb;
}

.navbar{
    position:sticky;
    top:0;
    z-index:999;
    background:white;
    padding:18px 25px;
    border-radius:14px;
    box-shadow:0 6px 25px rgba(0,0,0,0.06);
    margin-bottom:25px;
}

.big-title{
    text-align:center;
    font-size:40px;
    font-weight:700;
    color:#0f172a;
    margin-top:30px;
}

.search-area{
    background:white;
    padding:35px;
    border-radius:16px;
    box-shadow:0 10px 40px rgba(0,0,0,0.07);
    max-width:900px;
    margin:auto;
    margin-top:20px;
}

.result-area{
    background:white;
    padding:20px;
    border-radius:14px;
    box-shadow:0 8px 30px rgba(0,0,0,0.05);
    margin-top:25px;
}

.player-full{
    background:white;
    padding:20px;
    border-radius:18px;
    box-shadow:0 15px 45px rgba(0,0,0,0.15);
    margin-top:25px;
}

input{
    border-radius:12px !important;
}

</style>
""", unsafe_allow_html=True)

# ===================================
# NAVBAR
# ===================================
st.markdown("""
<div class="navbar">
<h3 style='margin:0;color:#0f172a;'>🎓 Portal Data Sekolah — CINEMA PLAYER</h3>
</div>
""", unsafe_allow_html=True)

# ===================================
# 🎧 INPUT LINK PLAYER
# ===================================
media_link = st.text_input(
    "Masukkan Link YouTube (Playlist atau Video)",
    placeholder="https://www.youtube.com/playlist?list=XXXX atau https://youtu.be/XXXX"
)

# ===================================
# 🎬 PLAYER RENDER FLEXIBLE
# ===================================
if media_link:

    embed_url = None

    # PLAYLIST
    if "list=" in media_link:
        playlist_id = media_link.split("list=")[-1].split("&")[0]
        embed_url = f"https://www.youtube.com/embed/videoseries?list={playlist_id}&autoplay=1&loop=1"

    # VIDEO BIASA
    elif "watch?v=" in media_link:
        video_id = media_link.split("watch?v=")[-1].split("&")[0]
        embed_url = f"https://www.youtube.com/embed/{video_id}?autoplay=1"

    elif "youtu.be/" in media_link:
        video_id = media_link.split("youtu.be/")[-1].split("?")[0]
        embed_url = f"https://www.youtube.com/embed/{video_id}?autoplay=1"

    if embed_url:

        st.markdown('<div class="player-full">', unsafe_allow_html=True)

        st.components.v1.iframe(
            embed_url,
            height=520,
            scrolling=False
        )

        st.markdown('</div>', unsafe_allow_html=True)

# ===================================
# TITLE
# ===================================
st.markdown('<p class="big-title">Cari Data Sekolah Berdasarkan NPSN</p>', unsafe_allow_html=True)

# ===================================
# SEARCH AREA
# ===================================
st.markdown('<div class="search-area">', unsafe_allow_html=True)

sheet_url = st.text_input("Masukkan Link Spreadsheet")
npsn = st.text_input("Masukkan NPSN")

st.markdown('</div>', unsafe_allow_html=True)

# ===================================
# LOAD DATA
# ===================================
@st.cache_data
def load_data(url):

    if "docs.google.com" in url:
        url = url.replace("/edit?usp=sharing", "/export?format=csv")
        df = pd.read_csv(url)
    elif url.endswith(".csv"):
        df = pd.read_csv(url)
    else:
        df = pd.read_excel(url)

    df.columns = df.columns.astype(str).str.lower().str.strip()
    df = df.loc[:, ~df.columns.duplicated()]
    df = df.reset_index(drop=True)

    return df

# ===================================
# RESULT TABLE OUTPUT
# ===================================
if sheet_url and npsn:

    try:
        df = load_data(sheet_url)

        if "npsn" not in df.columns:
            st.error("Kolom npsn tidak ditemukan")
        else:
            hasil = df[df["npsn"].astype(str) == str(npsn)]

            if len(hasil) > 0:

                st.markdown('<div class="result-area">', unsafe_allow_html=True)

                st.dataframe(
                    hasil,
                    use_container_width=True,
                    hide_index=True
                )

                st.markdown('</div>', unsafe_allow_html=True)

            else:
                st.warning("Data tidak ditemukan")

    except Exception as e:
        st.error(f"Error: {e}")
