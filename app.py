import streamlit as st
import pandas as pd

# =============================
# CONFIG
# =============================
st.set_page_config(
    page_title="Portal NPSN Ultra Clean",
    layout="wide"
)

# =============================
# 🎨 ULTRA CLEAN CSS
# =============================
st.markdown("""
<style>

/* BACKGROUND SUPER CLEAN */
.stApp {
    background:#f5f7fb;
}

/* NAVBAR */
.navbar {
    background:white;
    padding:18px 25px;
    border-radius:14px;
    box-shadow:0 6px 25px rgba(0,0,0,0.05);
    margin-bottom:30px;
}

/* TITLE CENTER */
.big-title {
    text-align:center;
    font-size:36px;
    font-weight:700;
    color:#0f172a;
    margin-top:40px;
    animation:fadeUp 0.6s ease-in-out;
}

/* SEARCH BOX */
.search-area {
    background:white;
    padding:35px;
    border-radius:16px;
    box-shadow:0 10px 40px rgba(0,0,0,0.06);
    max-width:900px;
    margin:auto;
    margin-top:20px;
}

/* RESULT TABLE AREA */
.result-area {
    background:white;
    padding:20px;
    border-radius:14px;
    box-shadow:0 8px 30px rgba(0,0,0,0.05);
    margin-top:25px;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background:#ffffff;
}

/* INPUT STYLE */
input {
    border-radius:12px !important;
}

/* ANIMATION */
@keyframes fadeUp {
    from {opacity:0; transform:translateY(10px);}
    to {opacity:1; transform:translateY(0);}
}

</style>
""", unsafe_allow_html=True)

# =============================
# 🧭 NAVBAR
# =============================
st.markdown("""
<div class="navbar">
<h3 style='margin:0;color:#0f172a;'>🎓 Portal Data Sekolah</h3>
</div>
""", unsafe_allow_html=True)

# =============================
# 🎬 MINI PLAYER PLAYLIST
# =============================
st.sidebar.title("🎧 Mini Player")

playlist_url = st.sidebar.text_input(
    "Playlist YouTube",
    placeholder="https://www.youtube.com/embed/videoseries?list=XXXX"
)

if playlist_url:
    st.sidebar.video(playlist_url)

# =============================
# 🧾 TITLE
# =============================
st.markdown('<p class="big-title">Cari Data Sekolah Berdasarkan NPSN</p>', unsafe_allow_html=True)

# =============================
# 🔎 SEARCH AREA
# =============================
st.markdown('<div class="search-area">', unsafe_allow_html=True)

sheet_url = st.text_input("Masukkan Link Spreadsheet")
npsn = st.text_input("Masukkan NPSN")

st.markdown('</div>', unsafe_allow_html=True)

# =============================
# LOAD DATA FUNCTION
# =============================
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

# =============================
# 🔥 RESULT OUTPUT (ROW STYLE)
# =============================
if sheet_url and npsn:

    try:
        df = load_data(sheet_url)

        if "npsn" not in df.columns:
            st.error("Kolom npsn tidak ditemukan")
        else:
            hasil = df[df["npsn"].astype(str) == str(npsn)]

            if len(hasil) > 0:

                st.markdown('<div class="result-area">', unsafe_allow_html=True)

                # OUTPUT BARIS TABLE
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
