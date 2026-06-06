import streamlit as st
import time

# ==============================================================================
# 1. KONFIGURASI HALAMAN
# ==============================================================================
st.set_page_config(
    page_title="OrganicChem | Edu-Lab Platform",
    page_icon="🧪",
    layout="wide"
)

# ==============================================================================
# 2. CUSTOM CSS INTERAKTIF (VERSI MODERN)
# ==============================================================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f0f9ff, #f8fafc);
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f766e, #14b8a6);
}
[data-testid="stSidebar"] * {
    color: white !important;
}
.banner-utama {
    background: linear-gradient(135deg, #06b6d4, #3b82f6);
    padding: 35px;
    border-radius: 15px;
    color: white;
    margin-bottom: 30px;
    box-shadow: 0 6px 20px rgba(59,130,246,0.25);
}
.stButton > button {
    border-radius: 12px;
    border: none;
    background: linear-gradient(135deg, #14b8a6, #0ea5e9);
    color: white;
    font-weight: 600;
    transition: all 0.3s ease;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(14,165,233,0.3);
}
.tube-wrap {
    display: flex;
    justify-content: center;
    height: 350px;
    padding-top: 20px;
}
.tube-glass {
    width: 80px;
    height: 300px;
    border: 4px solid #64748b;
    border-top: none;
    border-radius: 0 0 40px 40px;
    position: relative;
    overflow: hidden;
    background: rgba(15, 23, 42, 0.16);
    box-shadow: inset 0 0 15px rgba(0,0,0,0.25);
    backdrop-filter: blur(3px);
}
.tube-liquid {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    transition: height 1.2s ease, background 1.2s ease;
}
.precipitate-layer {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 60px;
    box-shadow: inset 0 2px 5px rgba(0,0,0,0.2);
}
.cloudy-layer {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(to bottom, rgba(255,255,255,0.85), rgba(241,245,249,0.95));
}
.bubble-fx {
    position: absolute;
    background: rgba(0,0,0,0.15);
    border-radius: 50%;
    width: 8px;
    height: 8px;
    animation: floatUp 1.8s infinite ease-in;
}
@keyframes floatUp {
    0% { bottom: 0px; opacity: 1; }
    100% { bottom: 250px; opacity: 0; }
}
/* Menyesuaikan style tabs agar lebih mirip dengan gambar referensimu */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}
.stTabs [data-baseweb="tab"] {
    height: 50px;
    background-color: #f1f5f9;
    border-radius: 8px 8px 0px 0px;
    padding: 10px 20px;
    font-weight: 600;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #0f766e, #14b8a6);
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. FUNGSI HELPER & DATABASE
# ==============================================================================
def force_rerun():
    if hasattr(st, 'rerun'):
        st.rerun()
    elif hasattr(st, 'experimental_rerun'):
        st.experimental_rerun()

def render_tube(tinggi, warna_larutan, efek, warna_endapan=None):
    e_html = ""
    if efek == "precipitate":
        bg_endapan = warna_endapan if warna_endapan else warna_larutan
        e_html = f"<div class='precipitate-layer' style='background: {bg_endapan}; border-top: 3.5px solid rgba(0, 0, 0, 0.25);'></div>"
    elif efek == "cloudy":
        e_html = "<div class='cloudy-layer'></div>"
    elif efek == "bubbles":
        e_html = "<div class='bubble-fx' style='left:20px;'></div><div class='bubble-fx' style='left:50px; animation-delay:0.5s;'></div>"
    return f"<div class='tube-wrap'><div class='tube-glass'><div class='tube-liquid' style='height:{tinggi}; background:{warna_larutan};'>{e_html}</div></div></div>"

reagen_colors = {
    "Uji Golongan Alkohol": "#f97316", 
    "Uji Oksidasi Alkohol": "#f97316", 
    "Uji Golongan Alkohol Tersier": "#f8fafc", 
    "Uji Golongan Alkohol Sekunder": "#f8fafc", 
    "Uji Golongan Alkanal/Aldehida (Bisulfit)": "#f8fafc", 
    "Uji Reduksi Golongan Alkanal (Fehling)": "#3b82f6", 
    "Uji Spesifik Golongan Alkanal (Schiff)": "#f8fafc",
    "Uji Golongan Metil Keton / Metil Karbinol": "#f8fafc",
    "Uji Golongan Ester": "#f8fafc",
    "Uji Golongan Asam Karboksilat": "#f8fafc"
}

flowchart_paths = {
    "Alkohol Primer": ["Uji Golongan Alkohol", "Uji Oksidasi Alkohol", "Uji Golongan Alkohol Sekunder"],
    "Alkohol Sekunder": ["Uji Golongan Alkohol", "Uji Oksidasi Alkohol", "Uji Golongan Alkohol Sekunder", "Uji Golongan Metil Keton / Metil Karbinol"],
    "Alkohol Tersier": ["Uji Golongan Alkohol", "Uji Oksidasi Alkohol", "Uji Golongan Alkohol Tersier"],
    "Aldehida (Alkanal)": ["Uji Golongan Alkohol", "Uji Golongan Alkanal/Aldehida (Bisulfit)", "Uji Reduksi Golongan Alkanal (Fehling)", "Uji Spesifik Golongan Alkanal (Schiff)"],
    "Keton (Alkanon)": ["Uji Golongan Alkohol", "Uji Golongan Alkanal/Aldehida (Bisulfit)", "Uji Reduksi Golongan Alkanal (Fehling)", "Uji Golongan Metil Keton / Metil Karbinol"],
    "Ester (Alkil Alkanoat)": ["Uji Golongan Alkohol", "Uji Golongan Alkanal/Aldehida (Bisulfit)", "Uji Golongan Ester"],
    "Asam Karboksilat": ["Uji Golongan Alkohol", "Uji Golongan Alkanal/Aldehida (Bisulfit)", "Uji Golongan Ester", "Uji Golongan Asam Karboksilat"],
    "Alkana / Hidrokarbon Jenuh": ["Uji Golongan Alkohol", "Uji Golongan Alkanal/Aldehida (Bisulfit)", "Uji Golongan Ester", "Uji Golongan Asam Karboksilat"]
}

database_reaksi = {
    "Alkohol Primer": {
        "Uji Golongan Alkohol": {"hasil": "(+) Merah Ceri", "reaksi": r"R-OH + [Ce(NO_3)_6]^{2-} \rightarrow [Ce(OR)(NO_3)_5]^{2-} + HNO_3", "alasan": "Gugus -OH bebas bereaksi membentuk senyawa kompleks koordinasi berwarna merah ceri.", "warna_akhir": "#ef4444", "efek": "none"},
        "Uji Oksidasi Alkohol": {"hasil": "(+) Hijau", "reaksi": r"3\ R-CH_2OH + 2\ CrO_3 + 3\ H_2SO_4 \rightarrow 3\ R-CHO + Cr_2(SO_4)_3 + 6\ H_2O", "alasan": "Gugus -OH dioksidasi menjadi aldehida, Kromium(VI) jingga tereduksi menjadi Kromium(III) hijau.", "warna_akhir": "#10b981", "efek": "none"},
        "Uji Golongan Alkohol Sekunder": {"hasil": "(-) Tetap Jingga", "reaksi": r"R-CH_2OH + HCl \xrightarrow{ZnCl_2} \text{Tidak ada reaksi}", "alasan": "Karbokation primer sangat tidak stabil sehingga tidak mampu bereaksi.", "warna_akhir": "#f97316", "efek": "none"}
    },
    "Alkohol Sekunder": {
        "Uji Golongan Alkohol": {"hasil": "(+) Merah Ceri", "reaksi": r"R-OH + [Ce(NO_3)_6]^{2-} \rightarrow [Ce(OR)(NO_3)_5]^{2-} + HNO_3", "alasan": "Ikatan koordinasi terbentuk dengan logam Cerium pusat.", "warna_akhir": "#ef4444", "efek": "none"},
        "Uji Oksidasi Alkohol": {"hasil": "(+) Hijau", "reaksi": r"3\ R_2CH-OH + 2\ CrO_3 + 3\ H_2SO_4 \rightarrow 3\ R_2C=O + Cr_2(SO_4)_3 + 6\ H_2O", "alasan": "Alkohol sekunder dioksidasi menjadi keton.", "warna_akhir": "#10b981", "efek": "none"},
        "Uji Golongan Alkohol Sekunder": {"hasil": "(+) Emulsi Putih", "reaksi": r"R_2CH-OH + HCl \xrightarrow{ZnCl_2} R_2CH-Cl \downarrow + H_2O", "alasan": "Karbokation sekunder menghasilkan alkil klorida setelah 5-10 menit.", "warna_akhir": "#e2e8f0", "efek": "cloudy"},
        "Uji Golongan Metil Keton / Metil Karbinol": {"hasil": "(+) Endapan Kuning", "reaksi": r"R-CH(OH)-CH_3 + 4\ I_2 + 6\ NaOH \rightarrow CHI_3 \downarrow + R-COONa + 5\ NaI + 5\ H_2O", "alasan": "Membentuk kristal iodoform berwarna kuning.", "warna_akhir": "#fef08a", "efek": "precipitate", "warna_endapan": "#facc15"}
    },
    "Alkohol Tersier": {
        "Uji Golongan Alkohol": {"hasil": "(+) Merah Ceri", "reaksi": r"R-OH + [Ce(NO_3)_6]^{2-} \rightarrow [Ce(OR)(NO_3)_5]^{2-} + HNO_3", "alasan": "Membentuk kompleks koordinasi berwarna merah.", "warna_akhir": "#ef4444", "efek": "none"},
        "Uji Oksidasi Alkohol": {"hasil": "(-) Tetap Jingga", "reaksi": r"R_3C-OH + CrO_3 \rightarrow \text{Tidak bereaksi}", "alasan": "Alkohol tersier tidak memiliki atom hidrogen alfa.", "warna_akhir": "#f97316", "efek": "none"},
        "Uji Golongan Alkohol Tersier": {"hasil": "(+) Emulsi Putih (Seketika)", "reaksi": r"R_3C-OH + HCl \xrightarrow{ZnCl_2} R_3C-Cl \downarrow + H_2O", "alasan": "Membentuk karbokation tersier yang sangat stabil seketika.", "warna_akhir": "#94a3b8", "efek": "cloudy"}
    },
    "Aldehida (Alkanal)": {
        "Uji Golongan Alkohol": {"hasil": "(-) Tetap Jingga", "reaksi": r"R-CHO + [Ce(NO_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}", "alasan": "Tidak memiliki gugus hidroksil (-OH) bebas.", "warna_akhir": "#f97316", "efek": "none"},
        "Uji Golongan Alkanal/Aldehida (Bisulfit)": {"hasil": "(+) Endapan Putih", "reaksi": r"R-CHO + NaHSO_3 \rightarrow R-CH(OH)SO_3Na \downarrow", "alasan": "Nukleofil bisulfit menyerang gugus karbonil.", "warna_akhir": "#cbd5e1", "efek": "precipitate", "warna_endapan": "#ffffff"},
        "Uji Reduksi Golongan Alkanal (Fehling)": {"hasil": "(+) Merah Bata", "reaksi": r"R-CHO + 2\ Cu^{2+} + 5\ OH^- \rightarrow R-COO^- + Cu_2O \downarrow + 3\ H_2O", "alasan": "Aldehida mereduksi kupri oksida menjadi tembaga(I) oksida.", "warna_akhir": "#3b82f6", "efek": "precipitate", "warna_endapan": "#b91c1c"},
        "Uji Spesifik Golongan Alkanal (Schiff)": {"hasil": "(+) Ungu / Magenta", "reaksi": r"\text{Aldehida} + \text{Pereaksi Schiff} \rightarrow \text{Kompleks Magenta}", "alasan": "Reaksi adisi spesifik menghasilkan warna ungu.", "warna_akhir": "#d946ef", "efek": "none"}
    },
    "Keton (Alkanon)": {
        "Uji Golongan Alkohol": {"hasil": "(-) Tetap Jingga", "reaksi": r"\text{Keton} + [Ce(NO_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}", "alasan": "Keton tidak memiliki gugus fungsi hidroksil.", "warna_akhir": "#f97316", "efek": "none"},
        "Uji Golongan Alkanal/Aldehida (Bisulfit)": {"hasil": "(+) Endapan Putih", "reaksi": r"CH_3-CO-CH_3 + NaHSO_3 \rightarrow (CH_3)_2C(OH)SO_3Na \downarrow", "alasan": "Keton suku rendah diadisi oleh bisulfit.", "warna_akhir": "#cbd5e1", "efek": "precipitate", "warna_endapan": "#ffffff"},
        "Uji Reduksi Golongan Alkanal (Fehling)": {"hasil": "(-) Tetap Biru", "reaksi": r"\text{Keton} + Cu^{2+} \rightarrow \text{Tidak bereaksi}", "alasan": "Keton tidak bersifat reduktor.", "warna_akhir": "#3b82f6", "efek": "none"},
        "Uji Golongan Metil Keton / Metil Karbinol": {"hasil": "(+) Endapan Kuning", "reaksi": r"R-CO-CH_3 + 3\ I_2 + 4\ NaOH \rightarrow CHI_3 \downarrow + R-COONa + 3\ NaI + 3\ H_2O", "alasan": "Metil keton membentuk endapan kuning iodoform.", "warna_akhir": "#fef08a", "efek": "precipitate", "warna_endapan": "#facc15"}
    },
    "Ester (Alkil Alkanoat)": {
        "Uji Golongan Alkohol": {"hasil": "(-) Tetap Jingga", "reaksi": r"\text{Ester} + [Ce(NO_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}", "alasan": "Tidak memiliki gugus hidroksil bebas.", "warna_akhir": "#f97316", "efek": "none"},
        "Uji Golongan Alkanal/Aldehida (Bisulfit)": {"hasil": "(-) Bening", "reaksi": r"\text{Ester} + NaHSO_3 \rightarrow \text{Tidak bereaksi}", "alasan": "Gugus ester stabil akibat efek resonansi.", "warna_akhir": "#f8fafc", "efek": "none"},
        "Uji Golongan Ester": {"hasil": "(+) Merah Violet", "reaksi": r"3\ R-CONHOH + FeCl_3 \rightarrow Fe(R-CONHO)_3 + 3\ HCl", "alasan": "Membentuk kompleks berwarna violet dengan besi(III).", "warna_akhir": "#c026d3", "efek": "none"}
    },
    "Asam Karboksilat": {
        "Uji Golongan Alkohol": {"hasil": "(-) Tetap Jingga", "reaksi": r"R-COOH + [Ce(NO_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}", "alasan": "Sifat nukleofil oksigen hidroksil ditarik oleh resonansi karbonil.", "warna_akhir": "#f97316", "efek": "none"},
        "Uji Golongan Alkanal/Aldehida (Bisulfit)": {"hasil": "(-) Bening", "reaksi": r"R-COOH + NaHSO_3 \rightarrow \text{Tidak bereaksi}", "alasan": "Tidak mengandung gugus aldehida atau keton.", "warna_akhir": "#f8fafc", "efek": "none"},
        "Uji Golongan Ester": {"hasil": "(-) Bening", "reaksi": r"R-COOH + NH_2OH + FeCl_3 \rightarrow \text{Tidak bereaksi}", "alasan": "Asam karboksilat bebas tidak membentuk hidroksamat pada kondisi ini.", "warna_akhir": "#f8fafc", "efek": "none"},
        "Uji Golongan Asam Karboksilat": {"hasil": "(+) Gelembung & Keruh", "reaksi": r"CO_2 + Ba(OH)_2 \rightarrow BaCO_3 \downarrow + H_2O", "alasan": "Menghasilkan gas CO2 yang mengeruhkan air barit.", "warna_akhir": "#f8fafc", "efek": "bubbles"}
    },
    "Alkana / Hidrokarbon Jenuh": {
        "Uji Golongan Alkohol": {"hasil": "(-) Tetap Jingga", "reaksi": r"\text{Alkana} + [Ce(NO_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}", "alasan": "Senyawa nonpolar inert.", "warna_akhir": "#f97316", "efek": "none"},
        "Uji Golongan Alkanal/Aldehida (Bisulfit)": {"hasil": "(-) Bening", "reaksi": r"\text{Alkana} + NaHSO_3 \rightarrow \text{Tidak bereaksi}", "alasan": "Tidak memiliki gugus fungsi karbonil.", "warna_akhir": "#f8fafc", "efek": "none"},
        "Uji Golongan Ester": {"hasil": "(-) Bening", "reaksi": r"\text{Alkana} + NH_2OH \rightarrow \text{Tidak bereaksi}", "alasan": "Tidak memiliki gugus fungsi ester.", "warna_akhir": "#f8fafc", "efek": "none"},
        "Uji Golongan Asam Karboksilat": {"hasil": "(-) Bening", "reaksi": r"\text{Alkana} + NaNaHCO_3 \rightarrow \text{Tidak bereaksi}", "alasan": "Hidrokarbon jenuh bersifat inert.", "warna_akhir": "#f8fafc", "efek": "none"}
    }
}

# Inisialisasi session state
if "test_started" not in st.session_state:
    st.session_state.test_started = False
if "current_step" not in st.session_state:
    st.session_state.current_step = 0
if "log_history" not in st.session_state:
    st.session_state.log_history = []
if "trigger_animation" not in st.session_state:
    st.session_state.trigger_animation = False

# ==============================================================================
# 4. SIDEBAR NAVIGASI
# ==============================================================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3022/3022607.png", width=75)
    st.title("OrganicChem v1.0")
    st.write("🔬 *E-Learning & Lab Simulator*")
    st.markdown("---")
    
    pilihan_halaman = st.sidebar.radio(
        "Navigasi Menu:",
        [
            "🏠 HALAMAN UTAMA", 
            "📘 BAB I. HIDROKARBON", 
            "📙 BAB II. ALKOHOL, ETER, DAN FENOL", 
            "📗 BAB III. ALDEHID DAN KETON", 
            "📕 BAB IV. ASAM KARBOKSILAT DAN DERIVATNYA", 
            "🔬 POST TEST"
        ]
    )
    st.markdown("---")
    st.caption("E-Learning Kimia Organik | © 2026")

# ==============================================================================
# 5. LOGIKA KONTEN TIAP HALAMAN
# ==============================================================================

if pilihan_halaman == "🏠 HALAMAN UTAMA":
    st.markdown("""
        <div class="banner-utama">
            <h1 style='color: white; margin-bottom: 5px; font-weight: 700;'>Eksplorasi Dunia Kimia Organik Tanpa Batas! 👋</h1>
            <p style='font-size: 1.2em; opacity: 0.95;'>Solusi cerdas belajar mandiri dan simulasi identifikasi gugus fungsi dalam satu platform.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("💡 Tentang Platform Ini")
    st.write("Kami hadir untuk menjembatani teori dan praktik. Platform ini dirancang khusus untuk membantu Anda memahami materi teoretis sekaligus memvisualisasikan reaksi uji kualitatif senyawa organik secara interaktif—kapan saja dan di mana saja, layaknya memiliki laboratorium pribadi.")
    st.markdown("---")
    
    st.markdown("### 📜 Petunjuk Penggunaan")
    p1, p2, p3 = st.columns(3)
    
    with p1:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; border-top: 5px solid #0f766e; box-shadow: 0 4px 6px rgba(0,0,0,0.05); min-height: 180px;">
            <h4 style="margin-top:0; color:#0f766e;">📖 Langkah 1: Pelajari</h4>
            <p style="font-size: 0.95em; color: #475569;">Buka <b>Menu Navigasi</b> di samping kiri. Pilih materi dari <b>BAB I hingga BAB IV</b> untuk membaca teori dasar, sifat fisik/kimia, dan persamaan reaksi.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with p2:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; border-top: 5px solid #14b8a6; box-shadow: 0 4px 6px rgba(0,0,0,0.05); min-height: 180px;">
            <h4 style="margin-top:0; color:#14b8a6;">🧪 Langkah 2: Simulasi</h4>
            <p style="font-size: 0.95em; color: #475569;">Masuk ke menu <b>🔬 POST TEST</b>. Di sana, kamu bisa memilih sampel misterius (<i>Blind Sample</i>) untuk menguji pemahaman analisismu secara langsung.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with p3:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; border-top: 5px solid #0ea5e9; box-shadow: 0 4px 6px rgba(0,0,0,0.05); min-height: 180px;">
            <h4 style="margin-top:0; color:#0ea5e9;">📊 Langkah 3: Amati</h4>
            <p style="font-size: 0.95em; color: #475569;">Klik tombol reaksi, amati perubahan visual pada <b>Visual Lab</b>, serta baca hasil evaluasi otomatis pada tab <b>Logbook & Analisis</b>.</p>
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# BAB I
# ------------------------------------------------------------------------------
elif pilihan_halaman == "📘 BAB I. HIDROKARBON":
    st.title("📘 BAB I. HIDROKARBON")
    st.write("---")
    
    tab_teori, tab_reaksi, tab_visual = st.tabs(["📖 Referensi Standar & Sifat", "📊 Analisis Parameter Reaksi", "📈 Visualisasi 2D"])
    
    with tab_teori:
        st.subheader("Landasan Teori Hidrokarbon")
        st.markdown("""
        Hidrokarbon adalah senyawa organik yang seluruh strukturnya hanya tersusun atas unsur karbon (C) dan hidrogen (H). Berdasarkan jenis ikatannya, dibagi menjadi alifatik (jenuh dan tidak jenuh) dan aromatik.
        
        #### **A. Sifat Fisika Hidrokarbon**
        * **Wujud Zat:** Suhu rendah ($C_1 - C_4$) berwujud gas, sedang ($C_5 - C_{17}$) cair, tinggi ($\ge C_{18}$) padat.
        * **Kelarutan:** Bersifat nonpolar, tidak larut dalam air. Larut dalam pelarut organik nonpolar ($CHCl_3$, eter).
        * **Titik Didih:** Meningkat seiring bertambahnya massa molekul (panjang rantai karbon). Rantai lurus memiliki titik didih lebih tinggi dari rantai bercabang.
        * **Densitas:** Lebih kecil daripada air.
        """)

    with tab_reaksi:
        st.subheader("Sifat Kimia & Reaksi Identifikasi")
        
        st.markdown("**1. Alkana (Hidrokarbon Jenuh)**")
        st.markdown("Sangat tidak reaktif (parafin). Bereaksi dengan halogen melalui substitusi radikal bebas dengan bantuan UV.")
        st.latex(r"\text{CH}_4 + \text{I}_2 \xrightarrow{\text{Sinar UV} / \Delta} \text{CH}_3\text{I} + \text{HI}")
        st.divider()
        
        st.markdown("**2. Alkena dan Alkuna (Hidrokarbon Tidak Jenuh)**")
        st.markdown("**Uji Adisi Iodium:** Mengadisi halogen seketika pada ikatan rangkap.")
        st.latex(r"\text{R-CH}=\text{CH-R} + \text{I}_2 \rightarrow \text{R-CH(I)-CH(I)-R}")
        st.markdown("**Uji Baeyer:** Dioksidasi oleh $KMnO_4$ menghasilkan senyawa glikol dan endapan cokelat $MnO_2$.")
        st.latex(r"3\text{CH}_2=\text{CH}_2 + 2\text{KMnO}_4 + 4\text{H}_2\text{O} \rightarrow 3\text{HO-CH}_2\text{-CH}_2\text{-OH} + 2\text{MnO}_2\downarrow + 2\text{KOH}")
        st.divider()
        
        st.markdown("**3. Benzena (Hidrokarbon Aromatik)**")
        st.markdown("Sangat stabil berkat delokalisasi elektron pi. Cenderung mengalami reaksi substitusi elektrofilik (contoh: Nitrasi).")
        st.latex(r"\text{C}_6\text{H}_6 + \text{HNO}_3 \xrightarrow{\text{H}_2\text{SO}_4\text{ pekat}} \text{C}_6\text{H}_5\text{NO}_2 + \text{H}_2\text{O}")

    with tab_visual:
        st.subheader("Ilustrasi 2D Mekanisme Reaksi")
        st.info("💡 **Tips:** Ganti tautan URL pada file Python dengan direktori gambar struktur ChemDraw/MarvinSketch milikmu.")
        
        st.markdown("#### Uji Adisi Iodium pada Etena")
        col1, col2, col3 = st.columns([2, 1, 2])
        with col1:
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Ethylene-2D.svg/120px-Ethylene-2D.svg.png", caption="Etena + I₂")
        with col2:
            st.markdown("<h1 style='text-align: center; color: #14b8a6; margin-top: 30px;'>➔</h1>", unsafe_allow_html=True)
        with col3:
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/1%2C2-Diiodoethane_Structural_Formula_V1.svg/200px-1%2C2-Diiodoethane_Structural_Formula_V1.svg.png", caption="1,2-diiodoetana")

# ------------------------------------------------------------------------------
# BAB II
# ------------------------------------------------------------------------------
elif pilihan_halaman == "📙 BAB II. ALKOHOL, ETER, DAN FENOL":
    st.title("📙 BAB II. ALKOHOL, ETER, DAN FENOL")
    st.write("---")
    
    tab_teori, tab_reaksi, tab_visual = st.tabs(["📖 Referensi Standar & Sifat", "📊 Analisis Parameter Reaksi", "📈 Visualisasi 2D"])

    with tab_teori:
        st.subheader("Sifat Fisika & Klasifikasi")
        st.markdown("""
        * **Alkohol ($R - OH$):** Turunan alkana dengan gugus hidroksil. Diklasifikasikan menjadi $1^\circ, 2^\circ, 3^\circ$. Mudah larut dalam air karena ikatan hidrogen.
        * **Eter ($R^1 - O - R^2$):** Isomer fungsional alkohol. Titik didih sangat rendah karena tidak ada ikatan hidrogen antar-molekul eter.
        * **Fenol ($C_6H_5OH$):** Gugus $-OH$ terikat langsung pada cincin benzena. Bersifat asam lemah.
        """)

    with tab_reaksi:
        st.subheader("Persamaan Reaksi Kimia")
        
        st.markdown("**1. Pereaksi Lucas ($HCl / ZnCl_2$)**")
        st.markdown("Membedakan alkohol berdasarkan kecepatan reaksi pembentukan alkil klorida ($3^\circ$ instan, $2^\circ$ lambat, $1^\circ$ tidak bereaksi).")
        st.latex(r"\text{R}_3\text{C-OH} + \text{HCl} \xrightarrow{\text{ZnCl}_2} \text{R}_3\text{C-Cl}\downarrow + \text{H}_2\text{O}")
        
        st.markdown("**2. Pereaksi Jones ($CrO_3 / H_2SO_4$)**")
        st.markdown("Oksidasi alkohol $1^\circ$ menjadi asam karboksilat, $2^\circ$ menjadi keton. Ditandai perubahan warna Jingga ➔ Hijau.")
        st.latex(r"\text{R-CH}_2\text{-OH} \xrightarrow{\text{CrO}_3/\text{H}_2\text{SO}_4} \text{R-COOH}")
        
        st.markdown("**3. Uji Iodoform**")
        st.markdown("Khusus alkohol dengan gugus metil alfa. Menghasilkan endapan kuning iodoform ($CHI_3$).")
        st.latex(r"\text{R-CH(OH)-CH}_3 + 4\text{I}_2 + 6\text{NaOH} \rightarrow \text{R-COONa} + \text{CHI}_3\downarrow + 5\text{NaI} + 5\text{H}_2\text{O}")
        
        st.markdown("**4. Fenol: Uji $FeCl_3$**")
        st.markdown("Membentuk senyawa kompleks ungu tua.")
        st.latex(r"6\text{C}_6\text{H}_5\text{OH} + \text{FeCl}_3 \rightarrow [\text{Fe(OC}_6\text{H}_5)_6]^{3-} + 3\text{H}^+ + 3\text{Cl}^-")

    with tab_visual:
        st.subheader("Ilustrasi 2D Mekanisme Reaksi")
        st.markdown("#### Pembentukan Kompleks Fenol dengan Besi(III)")
        col1, col2, col3 = st.columns([2, 1, 2])
        with col1:
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Phenol_chemical_structure.png/120px-Phenol_chemical_structure.png", caption="Fenol + FeCl₃ (Kuning Pucat)")
        with col2:
            st.markdown("<h1 style='text-align: center; color: #14b8a6; margin-top: 30px;'>➔</h1>", unsafe_allow_html=True)
        with col3:
            st.markdown("<div style='height: 120px; background: #4c1d95; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;'>[Kompleks Fe-Fenoksida]³⁻<br>(Ungu Tua)</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# BAB III
# ------------------------------------------------------------------------------
elif pilihan_halaman == "📗 BAB III. ALDEHID DAN KETON":
    st.title("📗 BAB III. ALDEHID DAN KETON")
    st.write("---")
    
    tab_teori, tab_reaksi, tab_visual = st.tabs(["📖 Referensi Standar & Sifat", "📊 Analisis Parameter Reaksi", "📈 Visualisasi 2D"])

    with tab_teori:
        st.subheader("Sifat Fisika & Klasifikasi")
        st.markdown("""
        Senyawa karbonil. Aldehida ($R-CHO$) memiliki minimal satu H pada C karbonil, sedangkan keton ($R-CO-R'$) mengikat dua gugus alkil. Aldehida cenderung memiliki aroma buah-buahan, sedangkan keton suku rendah (aseton) memiliki aroma pelarut organik yang khas.
        """)

    with tab_reaksi:
        st.subheader("Reaksi Diferensiasi (Daya Reduksi)")
        
        st.markdown("**1. Uji Tollens (Cermin Perak)**")
        st.markdown("Aldehida mereduksi ion perak beramoniak menjadi endapan cermin perak murni di dinding tabung.")
        st.latex(r"\text{R-CHO} + 2[\text{Ag(NH}_3)_2]^+ + 3\text{OH}^- \rightarrow \text{R-COO}^- + 2\text{Ag}\downarrow + 4\text{NH}_3 + 2\text{H}_2\text{O}")
        
        st.markdown("**2. Uji Fehling / Benedict**")
        st.markdown("Aldehida mereduksi $Cu^{2+}$ basa menjadi endapan merah bata $Cu_2O$. Keton tidak bereaksi.")
        st.latex(r"\text{R-CHO} + 2\text{Cu}^{2+} + 5\text{OH}^- \rightarrow \text{R-COO}^- + \text{Cu}_2\text{O}\downarrow + 3\text{H}_2\text{O}")
        
        st.markdown("**3. Adisi Natrium Bisulfit ($NaHSO_3$)**")
        st.markdown("Reaksi adisi nukleofilik menghasilkan senyawa padat putih kristalin.")
        st.latex(r"\text{R-CHO} + \text{NaHSO}_3 \rightarrow \text{R-CH(OH)-SO}_3\text{Na}\downarrow")

    with tab_visual:
        st.subheader("Ilustrasi 2D Mekanisme Reaksi")
        st.markdown("#### Oksidasi Aldehida (Uji Fehling)")
        col1, col2, col3 = st.columns([2, 1, 2])
        with col1:
            st.markdown("<div style='height: 120px; background: #3b82f6; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;'>Aldehida + Cu²⁺<br>(Larutan Biru)</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<h1 style='text-align: center; color: #14b8a6; margin-top: 30px;'>➔</h1>", unsafe_allow_html=True)
        with col3:
            st.markdown("<div style='height: 120px; background: #b91c1c; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;'>Asam Karboksilat + Cu₂O<br>(Endapan Merah Bata)</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# BAB IV
# ------------------------------------------------------------------------------
elif pilihan_halaman == "📕 BAB IV. ASAM KARBOKSILAT DAN DERIVATNYA":
    st.title("📕 BAB IV. ASAM KARBOKSILAT DAN DERIVATNYA")
    st.write("---")
    
    tab_teori, tab_reaksi, tab_visual = st.tabs(["📖 Referensi Standar & Sifat", "📊 Analisis Parameter Reaksi", "📈 Visualisasi 2D"])

    with tab_teori:
        st.subheader("Sifat Fisika & Klasifikasi")
        st.markdown("""
        Asam karboksilat memiliki gugus ($-COOH$). Rantai pendek larut dalam air membentuk ikatan hidrogen kuat (dimer). Derivatnya (seperti ester, amida, asil halida) terbentuk dari substitusi gugus $-OH$.
        """)

    with tab_reaksi:
        st.subheader("Persamaan Reaksi Kimia")
        
        st.markdown("**1. Reaksi dengan Basa Lemah ($NaHCO_3$)**")
        st.markdown("Membedakan karboksilat dengan fenol. Menghasilkan effervescence (gelembung gas $CO_2$).")
        st.latex(r"\text{R-COOH} + \text{NaHCO}_3 \rightarrow \text{R-COONa} + \text{H}_2\text{O} + \text{CO}_2\uparrow")
        
        st.markdown("**2. Esterifikasi Fischer**")
        st.markdown("Kondensasi asam karboksilat dan alkohol dibantu $H_2SO_4$ menghasilkan ester beraroma wangi.")
        st.latex(r"\text{R-COOH} + \text{R'-OH} \xrightarrow{\text{H}_2\text{SO}_4, \Delta} \text{R-COOR'} + \text{H}_2\text{O}")
        
        st.markdown("**3. Uji Asam Hidroksamat (Identifikasi Ester)**")
        st.markdown("Ester direaksikan dengan hidroksilamin, lalu ditambahkan $FeCl_3$ membentuk kompleks ungu.")
        st.latex(r"\text{R-COOR'} + \text{NH}_2\text{OH} \rightarrow \text{R-CONH-OH} + \text{R'-OH}")
        st.latex(r"3\text{R-CONH-OH} + \text{FeCl}_3 \rightarrow \text{Fe(R-CONHO)}_3 + 3\text{HCl}")

    with tab_visual:
        st.subheader("Ilustrasi 2D Mekanisme Reaksi")
        st.markdown("#### Reaksi Asam Karboksilat dengan Bikarbonat")
        col1, col2, col3 = st.columns([2, 1, 2])
        with col1:
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Acetic_acid_flat_structure.svg/120px-Acetic_acid_flat_structure.svg.png", caption="Asam Asetat + NaHCO₃")
        with col2:
            st.markdown("<h1 style='text-align: center; color: #14b8a6; margin-top: 30px;'>➔</h1>", unsafe_allow_html=True)
        with col3:
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Carbon_dioxide_2D.svg/120px-Carbon_dioxide_2D.svg.png", caption="Natrium Asetat + H₂O + Gas CO₂ (Gelembung)")

# ------------------------------------------------------------------------------
# POST TEST
# ------------------------------------------------------------------------------
elif pilihan_halaman == "🔬 POST TEST":
    # Pastikan untuk mereset test_started jika tab lain diklik
    st.title("🔀 Asisten Identifikasi Cerdas (Step-by-Step)")
    st.write("Sistem ini mensimulasikan penelusuran Identifikasi Kualitatif langkah demi langkah. Tekan tombol Lanjut untuk melanjutkan ke tahap reaksi berikutnya.")

    if not st.session_state.test_started:
        st.divider()
        senyawa = st.selectbox("Pilih Golongan Senyawa yang Akan Diuji (Sebagai *Blind Sample*):", ["-- Pilih Senyawa --"] + list(flowchart_paths.keys()))
        if st.button("Mulai Identifikasi 🚀", type="primary"):
            if senyawa == "-- Pilih Senyawa --":
                st.warning("⚠️ Harap pilih komponen senyawa terlebih dahulu!")
            else:
                st.session_state.test_started = True
                st.session_state.senyawa_uji = senyawa
                st.session_state.current_step = 0
                st.session_state.log_history = []
                st.session_state.trigger_animation = True
                force_rerun()

    else:
        st.write("---")
        senyawa = st.session_state.senyawa_uji
        urutan = flowchart_paths[senyawa]

        col_visual, col_log = st.columns([1, 2.5])
        
        with col_visual:
            st.markdown("<h4 style='text-align: center;'>Visual Lab</h4>", unsafe_allow_html=True)
            tube_placeholder = st.empty() 
            status_placeholder = st.empty()
            
            st.write("")
            if st.button("⏹️ Stop & Pilih Reagen/Sampel Ulang", use_container_width=True, type="secondary"):
                st.session_state.test_started = False
                st.session_state.current_step = 0
                st.session_state.log_history = []
                st.session_state.trigger_animation = False
                force_rerun()
            
        with col_log:
            st.markdown("#### 📑 Logbook & Analisis Teoritis")
            log_container = st.container()

        with log_container:
            for log in st.session_state.log_history:
                if "(+)" in log["hasil"]:
                    st.success(f"**Tahap {log['step']}: {log['pereaksi']}** ➔ **{log['hasil']}**")
                    st.latex(log['reaksi'])
                    st.write(f"**Pembahasan:** {log['alasan']}")
                else:
                    st.error(f"**Tahap {log['step']}: {log['pereaksi']}** ➔ **{log['hasil']}**")
                    st.latex(log['reaksi'])
                    st.write(f"**Pembahasan:** {log['alasan']}")

        if st.session_state.trigger_animation and st.session_state.current_step < len(urutan):
            pereaksi = urutan[st.session_state.current_step]
            
            tube_placeholder.markdown(render_tube("30%", "#f1f5f9", "none"), unsafe_allow_html=True)
            status_placeholder.markdown(f"<div style='text-align:center;'><em>Menyiapkan sampel untuk {pereaksi}...</em></div>", unsafe_allow_html=True)
            time.sleep(1.0)
            
            warna_reagen = reagen_colors[pereaksi]
            tube_placeholder.markdown(render_tube("65%", warna_reagen, "none"), unsafe_allow_html=True)
            status_placeholder.markdown(f"<div style='text-align:center;'><em>Mereaksikan {pereaksi}...</em></div>", unsafe_allow_html=True)
            time.sleep(1.5)
            
            res = database_reaksi[senyawa][pereaksi]
            w_endapan = res.get("warna_endapan", None)
            tube_placeholder.markdown(render_tube("65%", res["warna_akhir"], res["efek"], warna_endapan=w_endapan), unsafe_allow_html=True)
            status_placeholder.markdown("<div style='text-align:center; font-weight:bold;'>Mengamati pengendapan & perubahan warna...</div>", unsafe_allow_html=True)
            time.sleep(1.2)
            
            st.session_state.log_history.append({
                "step": st.session_state.current_step + 1,
                "pereaksi": pereaksi,
                "hasil": res["hasil"],
                "reaksi": res["reaksi"],
                "alasan": res["alasan"]
            })
            
            st.session_state.current_step += 1
            st.session_state.trigger_animation = False
            force_rerun()

        elif not st.session_state.trigger_animation:
            if st.session_state.current_step > 0:
                last_pereaksi = urutan[st.session_state.current_step - 1]
                res = database_reaksi[senyawa][last_pereaksi]
                w_endapan = res.get("warna_endapan", None)
                tube_placeholder.markdown(render_tube("65%", res["warna_akhir"], res["efek"], warna_endapan=w_endapan), unsafe_allow_html=True)
            
            if st.session_state.current_step < len(urutan):
                next_pereaksi = urutan[st.session_state.current_step]
                status_placeholder.markdown("<div style='text-align:center; color:#475569;'>Menunggu konfirmasi data...</div>", unsafe_allow_html=True)
                
                with col_visual:
                    if st.button(f"Lanjutkan ke {next_pereaksi} ⏭️", use_container_width=True, type="primary"):
                        st.session_state.trigger_animation = True
                        force_rerun()
                        
            else:
                status_placeholder.markdown("<div style='text-align:center; font-weight:bold; color:#10b981;'>Rangkaian uji selesai!</div>", unsafe_allow_html=True)
                with log_container:
                    st.info(f"🎉 **KESIMPULAN AKHIR:** Sampel ini terbukti sah merupakan golongan **{senyawa.upper()}**.")
                
                with col_visual:
                    if st.button("🔄 Uji Golongan Senyawa Lain", use_container_width=True):
                        st.session_state.test_started = False
                        force_rerun()