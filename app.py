import streamlit as st
import pandas as pd

# =============================
# CONFIG
# =============================
st.set_page_config(
    page_title="Portal NPSN",
    layout="wide"
)

# =============================
# 🎨 SUPER CLEAN CSS
# =============================
st.markdown("""
<style>

/* BACKGROUND CLEAN */
.stApp {
    background:#f6f8fb;
}

/* NAVBAR */
.navbar {
    background:white;
    padding:18px;
    border-radius:14px;
    box-shadow:0 4px 20px rgba(0,0,0,0.06);
    margin-bottom:25px;
}

/* TITLE */
.big-title {
    font-size:34px;
    font-weight:700;
    text-align:center;
    color:#0f172a;
    margin-top:20px;
    animation:fadeUp 0.6s ease-in-out;
}

/* SEARCH BOX */
.search-box {
    background:white;
    padding:30px;
    border-radius:16px;
    box-shadow:0 10px 35px rgba(0,0,0,0.07);
    margin-top:20px;
}

/* RESULT CARD */
.result-card {
    background:white;
    padding:25px;
    border-radius:14px;
    box-shadow:0 8px 25px rgba(0,0,0,0.05);
    margin-top:20px;
    animation:fadeUp 0.5s ease-in-out;
}

/* SIDEBAR MINI PLAYER */
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
# 🎬 MINI PLAYLIST PLAYER
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
# 📄 SEARCH AREA
# =============================
st.markdown('<div class="search-box">', unsafe_allow_html=True)

sheet_url = st.text_input(
    "Masukkan Link Spreadsheet"
)

npsn = st.text_input("Masukkan NPSN")

st.markdown('</div>', unsafe_allow_html=True)

# =============================
# LOAD DATA
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
# 🔎 RESULT AREA
# =============================
if sheet_url and npsn:

    try:
        df = load_data(sheet_url)

        if "npsn" not in df.columns:
            st.error("Kolom npsn tidak ditemukan")
        else:
            hasil = df[df["npsn"].astype(str) == str(npsn)]

            if len(hasil) > 0:

                data = hasil.iloc[0].to_dict()

                st.markdown('<div class="result-card">', unsafe_allow_html=True)

                for k,v in data.items():
                    st.write(f"**{k.upper()}** : {v}")

                st.markdown('</div>', unsafe_allow_html=True)

            else:
                st.warning("Data tidak ditemukan")

    except Exception as e:
        st.error(f"Error: {e}")
        
