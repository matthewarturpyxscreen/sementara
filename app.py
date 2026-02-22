import streamlit as st
import pandas as pd

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Portal NPSN",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# 🎨 MODERN CSS UI
# =========================
st.markdown("""
<style>

/* BACKGROUND */
.stApp {
    background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
    color:white;
}

/* NAVBAR TITLE */
.title {
    font-size:38px;
    font-weight:700;
    text-align:center;
    margin-bottom:10px;
    animation: fadeUp 1s ease-in-out;
}

/* CARD STYLE */
.card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    padding:20px;
    border-radius:16px;
    box-shadow:0 0 25px rgba(0,0,0,0.2);
    animation: fadeUp 0.7s ease-in-out;
}

/* INPUT STYLE */
input {
    border-radius:10px !important;
}

/* ANIMATION */
@keyframes fadeUp {
    from {opacity:0; transform:translateY(15px);}
    to {opacity:1; transform:translateY(0);}
}

</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">🎓 Portal Pencarian Data Sekolah</p>', unsafe_allow_html=True)

# =========================
# 🎬 SIDEBAR PLAYLIST
# =========================
st.sidebar.title("🎧 Playlist")

playlist_url = st.sidebar.text_input(
    "Link Playlist YouTube",
    placeholder="https://www.youtube.com/embed/videoseries?list=XXXX"
)

if playlist_url:
    st.sidebar.video(playlist_url)

# =========================
# 📄 INPUT LINK DATA
# =========================
st.markdown('<div class="card">', unsafe_allow_html=True)

sheet_url = st.text_input(
    "Masukkan Link Spreadsheet"
)

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# LOAD DATA
# =========================
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

# =========================
# 🔎 SEARCH UI
# =========================
if sheet_url:

    try:
        df = load_data(sheet_url)

        col1, col2 = st.columns([3,1])

        with col1:
            npsn = st.text_input("Cari NPSN")

        if npsn:

            if "npsn" not in df.columns:
                st.error("Kolom npsn tidak ditemukan")
            else:
                hasil = df[df["npsn"].astype(str) == str(npsn)]

                if len(hasil) > 0:

                    data = hasil.iloc[0].to_dict()

                    st.markdown('<div class="card">', unsafe_allow_html=True)

                    for k,v in data.items():
                        st.markdown(f"**{k.upper()}** : {v}")

                    st.markdown('</div>', unsafe_allow_html=True)

                else:
                    st.warning("Data tidak ditemukan")

        with st.expander("Preview Data"):
            st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"Error: {e}")

else:
    st.info("Masukkan link spreadsheet terlebih dahulu.")
    
