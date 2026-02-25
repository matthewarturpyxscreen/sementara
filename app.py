import streamlit as st
import pandas as pd
import base64

# ===================================
# CONFIG
# ===================================
st.set_page_config(page_title="Portal NPSN GAME ENGINE", layout="wide")

# ===================================
# FUNCTION LOAD FOTO BASE64 (WAJIB CLOUD)
# ===================================
def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img1 = img_to_base64("foto1.jpg")
img2 = img_to_base64("foto2.jpg")
img3 = img_to_base64("foto3.jpg")
img4 = img_to_base64("foto4.jpg")

# ===================================
# 🎮 GAME ENGINE CSS (ANIMASI BERANTEM BENERAN)
# ===================================
st.markdown(f"""
<style>

.stApp{{background:#f4f7fb;}}

.navbar{{
    background:white;
    padding:18px 25px;
    border-radius:14px;
    box-shadow:0 6px 25px rgba(0,0,0,0.06);
    margin-bottom:25px;
}}

.fight-area{{
    display:flex;
    justify-content:center;
    gap:90px;
    margin-top:20px;
}}

.stickman{{
    position:relative;
    width:120px;
    height:230px;
}}

.head{{
    width:90px;
    height:90px;
    border-radius:50%;
    position:absolute;
    top:0;
    left:15px;
    border:4px solid white;
    object-fit:cover;
    box-shadow:0 6px 18px rgba(0,0,0,0.2);
    animation: headBounce 0.7s infinite alternate;
}}

.body{{
    position:absolute;
    top:90px;
    left:58px;
    width:4px;
    height:70px;
    background:black;
}}

.arm-left{{
    position:absolute;
    width:60px;
    height:4px;
    background:black;
    top:110px;
    left:0px;
    transform-origin:right;
    animation:punchLeft 0.5s infinite alternate;
}}

.arm-right{{
    position:absolute;
    width:60px;
    height:4px;
    background:black;
    top:110px;
    left:60px;
    transform-origin:left;
    animation:punchRight 0.5s infinite alternate;
}}

.leg-left{{
    position:absolute;
    width:60px;
    height:4px;
    background:black;
    top:160px;
    left:10px;
    transform-origin:right;
    animation:kickLeft 0.6s infinite alternate;
}}

.leg-right{{
    position:absolute;
    width:60px;
    height:4px;
    background:black;
    top:160px;
    left:50px;
    transform-origin:left;
    animation:kickRight 0.6s infinite alternate;
}}

@keyframes punchLeft{{
    0%{{transform:rotate(-10deg);}}
    100%{{transform:rotate(40deg);}}
}}

@keyframes punchRight{{
    0%{{transform:rotate(10deg);}}
    100%{{transform:rotate(-40deg);}}
}}

@keyframes kickLeft{{
    0%{{transform:rotate(10deg);}}
    100%{{transform:rotate(-30deg);}}
}}

@keyframes kickRight{{
    0%{{transform:rotate(-10deg);}}
    100%{{transform:rotate(30deg);}}
}}

@keyframes headBounce{{
    0%{{transform:translateY(0px);}}
    100%{{transform:translateY(-8px);}}
}}

</style>

<div class="navbar">
<h3>🎮 Portal Data Sekolah — GAME ENGINE PRO MAX</h3>
</div>

<div class="fight-area">

<div class="stickman">
<img src="data:image/jpeg;base64,{img1}" class="head">
<div class="body"></div>
<div class="arm-left"></div>
<div class="arm-right"></div>
<div class="leg-left"></div>
<div class="leg-right"></div>
</div>

<div class="stickman">
<img src="data:image/jpeg;base64,{img2}" class="head">
<div class="body"></div>
<div class="arm-left"></div>
<div class="arm-right"></div>
<div class="leg-left"></div>
<div class="leg-right"></div>
</div>

<div class="stickman">
<img src="data:image/jpeg;base64,{img3}" class="head">
<div class="body"></div>
<div class="arm-left"></div>
<div class="arm-right"></div>
<div class="leg-left"></div>
<div class="leg-right"></div>
</div>

<div class="stickman">
<img src="data:image/jpeg;base64,{img4}" class="head">
<div class="body"></div>
<div class="arm-left"></div>
<div class="arm-right"></div>
<div class="leg-left"></div>
<div class="leg-right"></div>
</div>

</div>
""", unsafe_allow_html=True)

# ===================================
# 🎧 PLAYER
# ===================================
st.markdown("### 🎧 Player")

media_link = st.text_input("Masukkan Link YouTube")

if media_link:

    embed_url=None

    if "list=" in media_link:
        playlist_id=media_link.split("list=")[-1].split("&")[0]
        embed_url=f"https://www.youtube.com/embed/videoseries?list={playlist_id}&autoplay=1&loop=1"

    elif "watch?v=" in media_link:
        video_id=media_link.split("watch?v=")[-1].split("&")[0]
        embed_url=f"https://www.youtube.com/embed/{video_id}?autoplay=1"

    elif "youtu.be/" in media_link:
        video_id=media_link.split("youtu.be/")[-1].split("?")[0]
        embed_url=f"https://www.youtube.com/embed/{video_id}?autoplay=1"

    if embed_url:
        st.components.v1.iframe(embed_url,height=520)

# ===================================
# 🔎 SEARCH AREA
# ===================================
st.markdown("### 🔎 Pencarian")

c1,c2,c3=st.columns([1,2,1])

with c2:
    sheet_url=st.text_input("Masukkan Link Spreadsheet")
    sheet_filter_input=st.text_input("Filter Sheet (pisahkan koma)")
    npsn=st.text_input("Masukkan NPSN")

# ===================================
# LOAD DATA (ANTI LAG)
# ===================================
@st.cache_data(show_spinner=False)
def load_data(url,filters):

    if "docs.google.com" in url:
        url=url.replace("/edit?usp=sharing","/export?format=xlsx")

    excel=pd.ExcelFile(url)

    selected=[]
    if filters:
        for name in filters:
            if name in excel.sheet_names:
                selected.append(name)
    else:
        selected=excel.sheet_names

    all_df=[]

    for sheet_name in selected:

        raw=pd.read_excel(excel,sheet_name=sheet_name,header=None)

        header_row=None
        for i in range(min(10,len(raw))):
            row_values=raw.iloc[i].astype(str).str.lower().tolist()
            if any("npsn" in v for v in row_values):
                header_row=i
                break

        if header_row is not None:
            df=raw.iloc[header_row+1:].copy()
            df.columns=raw.iloc[header_row].astype(str).str.lower().str.strip()
        else:
            df=raw.copy()
            df.columns=[f"kolom_{i}" for i in range(len(df.columns))]

        df["source_sheet"]=sheet_name
        df=df.loc[:,~df.columns.duplicated()]
        all_df.append(df)

    final_df=pd.concat(all_df,ignore_index=True,sort=False)
    return final_df.reset_index(drop=True)

# ===================================
# RESULT SUPER CEPAT
# ===================================
if sheet_url:

    filters=[s.strip() for s in sheet_filter_input.split(",")] if sheet_filter_input else []

    if "cached_df" not in st.session_state:
        st.session_state.cached_df=load_data(sheet_url,filters)

    df=st.session_state.cached_df

    if npsn and "npsn" in df.columns:

        hasil=df[df["npsn"].astype(str)==str(npsn)]

        if len(hasil)>0:
            st.dataframe(hasil,use_container_width=True,hide_index=True)
        else:
            st.warning("Data tidak ditemukan")
