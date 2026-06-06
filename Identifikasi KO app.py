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
# 2. CUSTOM CSS
# ==============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@400;500;600;700&display=swap');

.stApp {
    background: linear-gradient(135deg, #f0f9ff, #f8fafc);
    font-family: 'DM Sans', sans-serif;
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
.kotak-analisis {
    border-left: 6px solid #14b8a6;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
    background: linear-gradient(135deg, #f0fdfa, #ecfeff);
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
.stButton > button {
    border-radius: 12px;
    border: none;
    background: linear-gradient(135deg, #14b8a6, #0ea5e9);
    color: white;
    font-weight: 600;
    transition: all 0.3s ease;
    font-family: 'DM Sans', sans-serif;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(14,165,233,0.3);
}

/* Lab Illustration Styles */
.lab-container {
    background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    border-radius: 16px;
    padding: 20px 15px;
    margin-bottom: 15px;
    position: relative;
    overflow: hidden;
    min-height: 380px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
}
.lab-title {
    font-family: 'Space Mono', monospace;
    color: #94a3b8;
    font-size: 0.7em;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 12px;
    text-align: center;
}
.lab-bench {
    background: linear-gradient(180deg, #334155, #1e293b);
    border-radius: 8px;
    padding: 15px;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: flex-end;
    gap: 20px;
    min-height: 200px;
    position: relative;
    border-top: 3px solid #475569;
}
.tube-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
}
.tube-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.6em;
    color: #94a3b8;
    text-align: center;
    max-width: 80px;
    word-wrap: break-word;
}
.tube-glass {
    width: 70px;
    height: 180px;
    border: 3px solid #64748b;
    border-top: none;
    border-radius: 0 0 35px 35px;
    position: relative;
    overflow: hidden;
    background: rgba(15, 23, 42, 0.3);
    box-shadow: inset 0 0 20px rgba(0,0,0,0.4), 2px 0 6px rgba(100,116,139,0.2);
}
.tube-glass::before {
    content: '';
    position: absolute;
    top: 0;
    left: 8px;
    width: 12px;
    height: 100%;
    background: linear-gradient(90deg, rgba(255,255,255,0.12), transparent);
    border-radius: 0 0 10px 10px;
    pointer-events: none;
    z-index: 10;
}
.tube-liquid {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    transition: height 1.3s cubic-bezier(0.4,0,0.2,1), background 1.3s ease;
}
.tube-stopper {
    width: 76px;
    height: 12px;
    background: linear-gradient(180deg, #94a3b8, #64748b);
    border-radius: 3px 3px 0 0;
    box-shadow: 0 -2px 4px rgba(0,0,0,0.3);
}
.precipitate-layer {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 55px;
    border-top: 2.5px solid rgba(0,0,0,0.2);
}
.cloudy-layer {
    position: absolute;
    top: 0; bottom: 0; left: 0; right: 0;
    background: linear-gradient(to bottom, rgba(255,255,255,0.75), rgba(241,245,249,0.9));
}
.bubble-fx {
    position: absolute;
    background: rgba(255,255,255,0.2);
    border-radius: 50%;
    width: 7px; height: 7px;
    animation: floatUp 2s infinite ease-in;
}
.bubble-fx:nth-child(2) { left: 30px; animation-delay: 0.6s; width: 5px; height: 5px; }
.bubble-fx:nth-child(3) { left: 50px; animation-delay: 1.1s; width: 9px; height: 9px; }
@keyframes floatUp {
    0% { bottom: 5px; opacity: 0.8; }
    100% { bottom: 160px; opacity: 0; }
}
.glow-effect {
    box-shadow: 0 0 25px var(--glow-color, rgba(255,100,100,0.4)), inset 0 0 20px rgba(0,0,0,0.3);
}
.lab-status {
    font-family: 'Space Mono', monospace;
    font-size: 0.68em;
    color: #64748b;
    text-align: center;
    padding: 8px 12px;
    background: rgba(15,23,42,0.5);
    border-radius: 8px;
    border: 1px solid #334155;
    margin-top: 10px;
    width: 100%;
}
.lab-status.active {
    color: #34d399;
    border-color: #065f46;
    background: rgba(6,78,59,0.3);
}
.result-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75em;
    font-weight: 700;
    font-family: 'Space Mono', monospace;
    margin-top: 8px;
}
.result-pos { background: rgba(52,211,153,0.15); color: #34d399; border: 1px solid #065f46; }
.result-neg { background: rgba(251,113,133,0.15); color: #fb7185; border: 1px solid #881337; }

/* Step control buttons */
.step-btn-row {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-top: 10px;
}
.reagent-tag {
    text-align: center;
    font-weight: bold;
    font-family: 'Space Mono', monospace;
    font-size: 0.75em;
    background: rgba(20,184,166,0.15);
    color: #2dd4bf;
    padding: 6px 12px;
    border-radius: 8px;
    margin-bottom: 10px;
    border: 1px solid #0d9488;
    letter-spacing: 0.5px;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. HELPER FUNCTIONS & DATABASE
# ==============================================================================
def force_rerun():
    if hasattr(st, 'rerun'):
        st.rerun()
    elif hasattr(st, 'experimental_rerun'):
        st.experimental_rerun()

def render_tube_2d(tinggi_pct, warna_larutan, efek, warna_endapan=None, label="Sampel", glow=False):
    """Render 2D tube illustration as HTML."""
    e_html = ""
    if efek == "precipitate":
        bg_end = warna_endapan if warna_endapan else warna_larutan
        e_html = f"<div class='precipitate-layer' style='background:{bg_end};'></div>"
    elif efek == "cloudy":
        e_html = "<div class='cloudy-layer'></div>"
    elif efek == "bubbles":
        e_html = "<div class='bubble-fx' style='left:15px;'></div><div class='bubble-fx'></div><div class='bubble-fx'></div>"

    glow_style = f"--glow-color:{warna_larutan}55;" if glow else ""
    glow_class = "glow-effect" if glow else ""
    height_px = int(180 * tinggi_pct / 100)

    return f"""
    <div class='tube-wrap'>
        <div class='tube-stopper'></div>
        <div class='tube-glass {glow_class}' style='{glow_style}'>
            <div class='tube-liquid' style='height:{height_px}px; background:{warna_larutan};'>{e_html}</div>
        </div>
        <div class='tube-label'>{label}</div>
    </div>
    """

def render_lab_scene(tubes_data, status_text="", status_active=False):
    """
    tubes_data: list of dicts: {tinggi, warna, efek, warna_endapan, label, glow}
    Renders the full dark lab bench scene.
    """
    tubes_html = ""
    for t in tubes_data:
        tubes_html += render_tube_2d(
            t.get("tinggi", 30),
            t.get("warna", "#1e3a5f"),
            t.get("efek", "none"),
            t.get("warna_endapan"),
            t.get("label", ""),
            t.get("glow", False)
        )

    status_class = "active" if status_active else ""
    status_html = f"<div class='lab-status {status_class}'>{status_text}</div>" if status_text else ""

    return f"""
    <div class='lab-container'>
        <div class='lab-title'>⬡ Virtual Lab — 2D Reaction View</div>
        <div class='lab-bench'>{tubes_html}</div>
        {status_html}
    </div>
    """

# ---- Data ----
reagen_colors = {
    "Uji Golongan Alkohol":                        "#f97316",
    "Uji Oksidasi Alkohol":                        "#f97316",
    "Uji Golongan Alkohol Tersier":                "#f8fafc",
    "Uji Golongan Alkohol Sekunder":               "#f8fafc",
    "Uji Golongan Alkanal/Aldehida (Bisulfit)":    "#f8fafc",
    "Uji Reduksi Golongan Alkanal (Fehling)":      "#3b82f6",
    "Uji Spesifik Golongan Alkanal (Schiff)":      "#f8fafc",
    "Uji Golongan Metil Keton / Metil Karbinol":   "#f8fafc",
    "Uji Golongan Ester":                          "#f8fafc",
    "Uji Golongan Asam Karboksilat":               "#f8fafc",
}

# Experiments for each chapter
bab_experiments = {
    "BAB I": {
        "Uji Adisi Iodium (Alkena)": {
            "steps": [
                {"label": "Awal (Kosong)", "tubes": [
                    {"tinggi": 0, "warna": "#1e293b", "efek": "none", "label": "Tabung"},
                ],"status": "Tabung kosong, siap diisi sampel."},
                {"label": "Masukkan Sampel Alkena", "tubes": [
                    {"tinggi": 45, "warna": "#e0f2fe", "efek": "none", "label": "Alkena (cair)", "glow": False},
                ], "status": "Sampel alkena dimasukkan ke tabung."},
                {"label": "Tambah I₂/CCl₄ (Cokelat)", "tubes": [
                    {"tinggi": 65, "warna": "#92400e", "efek": "none", "label": "I₂ + Alkena", "glow": True},
                ], "status": "Iodium berwarna cokelat ditambahkan..."},
                {"label": "Kocok — Amati Perubahan", "tubes": [
                    {"tinggi": 65, "warna": "#fef9c3", "efek": "none", "label": "Positif: Pudar", "glow": False},
                ], "status": "✔ POSITIF: Warna cokelat I₂ hilang → ikatan rangkap teradisi!"},
            ],
            "reaksi": r"\text{R-CH}=\text{CH-R} + \text{I}_2 \rightarrow \text{R-CH(I)-CH(I)-R}",
            "kesimpulan": "Warna iodium memudar menandakan ikatan rangkap (C=C) telah mengadisi I₂. Positif untuk alkena/alkuna."
        },
        "Uji Baeyer (KMnO₄)": {
            "steps": [
                {"label": "Awal (Kosong)", "tubes": [
                    {"tinggi": 0, "warna": "#1e293b", "efek": "none", "label": "Tabung"},
                ], "status": "Tabung kosong."},
                {"label": "Masukkan Sampel", "tubes": [
                    {"tinggi": 40, "warna": "#e0f2fe", "efek": "none", "label": "Sampel"},
                ], "status": "Sampel dimasukkan ke tabung reaksi."},
                {"label": "Tambah KMnO₄ (Ungu)", "tubes": [
                    {"tinggi": 65, "warna": "#7e22ce", "efek": "none", "label": "KMnO₄ ungu", "glow": True},
                ], "status": "Larutan KMnO₄ ungu ditambahkan..."},
                {"label": "Amati Perubahan", "tubes": [
                    {"tinggi": 65, "warna": "#92400e", "efek": "precipitate", "warna_endapan": "#451a03", "label": "MnO₂ cokelat", "glow": False},
                ], "status": "✔ POSITIF: Warna ungu hilang, muncul endapan cokelat MnO₂!"},
            ],
            "reaksi": r"3\text{CH}_2\!\!=\!\!\text{CH}_2 + 2\text{KMnO}_4 + 4\text{H}_2\text{O} \rightarrow 3\text{HOCH}_2\!\text{CH}_2\!\text{OH} + 2\text{MnO}_2\!\downarrow + 2\text{KOH}",
            "kesimpulan": "Warna ungu KMnO₄ hilang dan muncul endapan cokelat MnO₂ — membuktikan adanya ikatan tak jenuh (alkena/alkuna)."
        },
        "Uji Bakar Benzena (Jelaga)": {
            "steps": [
                {"label": "Awal", "tubes": [
                    {"tinggi": 0, "warna": "#1e293b", "efek": "none", "label": "Cawan"},
                ], "status": "Cawan porselin kosong, disiapkan untuk pembakaran."},
                {"label": "Teteskan Benzena", "tubes": [
                    {"tinggi": 30, "warna": "#f0fdf4", "efek": "none", "label": "Benzena"},
                ], "status": "Beberapa tetes benzena diletakkan di cawan porselin."},
                {"label": "Bakar dengan Api", "tubes": [
                    {"tinggi": 40, "warna": "#fbbf24", "efek": "bubbles", "label": "Api menyala", "glow": True},
                ], "status": "Membakar benzena dengan korek api..."},
                {"label": "Amati Jelaga", "tubes": [
                    {"tinggi": 55, "warna": "#1c1917", "efek": "bubbles", "label": "Jelaga hitam!", "glow": False},
                ], "status": "✔ POSITIF: Nyala berminyak dengan jelaga hitam tebal → senyawa aromatik!"},
            ],
            "reaksi": r"\text{C}_6\text{H}_6 + \text{O}_2 \rightarrow \text{C}_{(s)}\text{[jelaga]} + \text{CO} + \text{H}_2\text{O}",
            "kesimpulan": "Nyala api berminyak dan jelaga hitam tebal khas benzena disebabkan persentase karbon yang tinggi."
        },
    },
    "BAB II": {
        "Uji CAN — Alkohol vs Eter": {
            "steps": [
                {"label": "Awal (Kosong)", "tubes": [
                    {"tinggi": 0, "warna": "#1e293b", "efek": "none", "label": "Tabung A"},
                    {"tinggi": 0, "warna": "#1e293b", "efek": "none", "label": "Tabung B"},
                ], "status": "Dua tabung disiapkan untuk perbandingan."},
                {"label": "Masukkan Sampel", "tubes": [
                    {"tinggi": 40, "warna": "#dbeafe", "efek": "none", "label": "Alkohol"},
                    {"tinggi": 40, "warna": "#f0fdf4", "efek": "none", "label": "Eter"},
                ], "status": "Sampel alkohol (A) dan eter (B) dimasukkan."},
                {"label": "Tambah Pereaksi CAN (Jingga)", "tubes": [
                    {"tinggi": 65, "warna": "#f97316", "efek": "none", "label": "CAN + Alkohol", "glow": True},
                    {"tinggi": 65, "warna": "#f97316", "efek": "none", "label": "CAN + Eter"},
                ], "status": "Pereaksi CAN (jingga) ditambahkan ke kedua tabung..."},
                {"label": "Amati Perubahan", "tubes": [
                    {"tinggi": 65, "warna": "#ef4444", "efek": "none", "label": "→ Merah ceri!", "glow": True},
                    {"tinggi": 65, "warna": "#f97316", "efek": "none", "label": "→ Tetap jingga"},
                ], "status": "✔ Tabung A merah ceri (positif alkohol). Tabung B tetap jingga (negatif)."},
            ],
            "reaksi": r"\text{ROH} + [\text{Ce(NO}_3)_6]^{2-} \rightarrow [\text{Ce(OR)(NO}_3)_5]^{2-}\text{(Merah)} + \text{HNO}_3",
            "kesimpulan": "Alkohol bereaksi membentuk kompleks merah ceri. Eter tidak bereaksi (tidak punya -OH bebas)."
        },
        "Uji Lucas — Primer vs Sekunder vs Tersier": {
            "steps": [
                {"label": "Awal (Kosong)", "tubes": [
                    {"tinggi": 0, "warna": "#1e293b", "efek": "none", "label": "1°"},
                    {"tinggi": 0, "warna": "#1e293b", "efek": "none", "label": "2°"},
                    {"tinggi": 0, "warna": "#1e293b", "efek": "none", "label": "3°"},
                ], "status": "Tiga tabung disiapkan untuk ketiga jenis alkohol."},
                {"label": "Masukkan Sampel", "tubes": [
                    {"tinggi": 40, "warna": "#bfdbfe", "efek": "none", "label": "Alkohol 1°"},
                    {"tinggi": 40, "warna": "#bbf7d0", "efek": "none", "label": "Alkohol 2°"},
                    {"tinggi": 40, "warna": "#fde68a", "efek": "none", "label": "Alkohol 3°"},
                ], "status": "Sampel alkohol primer, sekunder, tersier dimasukkan."},
                {"label": "Tambah Pereaksi Lucas (HCl+ZnCl₂)", "tubes": [
                    {"tinggi": 60, "warna": "#bfdbfe", "efek": "none", "label": "1° + Lucas"},
                    {"tinggi": 60, "warna": "#bbf7d0", "efek": "none", "label": "2° + Lucas"},
                    {"tinggi": 60, "warna": "#fde68a", "efek": "none", "label": "3° + Lucas"},
                ], "status": "Pereaksi Lucas ditambahkan ke semua tabung. Menunggu reaksi..."},
                {"label": "Amati (5-10 menit)", "tubes": [
                    {"tinggi": 60, "warna": "#bfdbfe", "efek": "none", "label": "1°: Bening"},
                    {"tinggi": 60, "warna": "#e2e8f0", "efek": "cloudy", "label": "2°: Keruh", "glow": False},
                    {"tinggi": 60, "warna": "#94a3b8", "efek": "cloudy", "label": "3°: Keruh Sgt!", "glow": True},
                ], "status": "✔ 1°=bening, 2°=keruh lambat, 3°=keruh seketika → beda stabilitas karbokation!"},
            ],
            "reaksi": r"\text{R}_3\text{C-OH} + \text{HCl} \xrightarrow{\text{ZnCl}_2} \text{R}_3\text{C-Cl}\!\downarrow + \text{H}_2\text{O}",
            "kesimpulan": "Alkohol tersier bereaksi seketika (karbokation paling stabil), sekunder lambat, primer tidak bereaksi pada suhu kamar."
        },
        "Uji Jones — Oksidasi Alkohol": {
            "steps": [
                {"label": "Awal", "tubes": [
                    {"tinggi": 0, "warna": "#1e293b", "efek": "none", "label": "Tabung"},
                ], "status": "Tabung siap."},
                {"label": "Masukkan Alkohol", "tubes": [
                    {"tinggi": 40, "warna": "#dbeafe", "efek": "none", "label": "Alkohol"},
                ], "status": "Sampel alkohol dimasukkan."},
                {"label": "Tambah Pereaksi Jones (Jingga)", "tubes": [
                    {"tinggi": 65, "warna": "#f97316", "efek": "none", "label": "CrO₃ Jingga", "glow": True},
                ], "status": "CrO₃ dalam H₂SO₄ (jingga) ditambahkan..."},
                {"label": "Amati (Alkohol 1° atau 2°)", "tubes": [
                    {"tinggi": 65, "warna": "#10b981", "efek": "none", "label": "→ Hijau!", "glow": True},
                ], "status": "✔ POSITIF: Jingga → Hijau. Alkohol 1°/2° teroksidasi, Cr⁶⁺ → Cr³⁺."},
            ],
            "reaksi": r"3\text{R-CH}_2\text{OH} + 2\text{CrO}_3 + 3\text{H}_2\text{SO}_4 \rightarrow 3\text{R-CHO} + \text{Cr}_2(\text{SO}_4)_3 + 6\text{H}_2\text{O}",
            "kesimpulan": "Jingga → Hijau berarti positif (ada hidrogen alfa). Alkohol tersier tetap jingga karena tidak bisa dioksidasi."
        },
    },
    "BAB III": {
        "Uji Bisulfit (Aldehida vs Keton)": {
            "steps": [
                {"label": "Awal", "tubes": [
                    {"tinggi": 0, "warna": "#1e293b", "efek": "none", "label": "Aldehida"},
                    {"tinggi": 0, "warna": "#1e293b", "efek": "none", "label": "Keton"},
                ], "status": "Dua tabung disiapkan."},
                {"label": "Masukkan Sampel", "tubes": [
                    {"tinggi": 40, "warna": "#fef9c3", "efek": "none", "label": "Aldehida"},
                    {"tinggi": 40, "warna": "#f0fdf4", "efek": "none", "label": "Keton"},
                ], "status": "Sampel aldehida dan keton dimasukkan."},
                {"label": "Tambah NaHSO₃", "tubes": [
                    {"tinggi": 60, "warna": "#e2e8f0", "efek": "none", "label": "Bisulfit+Ald"},
                    {"tinggi": 60, "warna": "#e2e8f0", "efek": "none", "label": "Bisulfit+Ket"},
                ], "status": "Natrium bisulfit ditambahkan ke kedua tabung..."},
                {"label": "Amati Endapan", "tubes": [
                    {"tinggi": 65, "warna": "#e2e8f0", "efek": "precipitate", "warna_endapan": "#ffffff", "label": "Endapan Putih!", "glow": True},
                    {"tinggi": 65, "warna": "#f0fdf4", "efek": "none", "label": "Bening / sedikit"},
                ], "status": "✔ Aldehida → endapan putih jelas. Keton hanya sebagian kecil (atau nihil)."},
            ],
            "reaksi": r"\text{R-CHO} + \text{NaHSO}_3 \rightarrow \text{R-CH(OH)-SO}_3\text{Na}\!\downarrow",
            "kesimpulan": "Bisulfit mengadisi karbonil aldehida lebih mudah karena halangan sterik kecil, menghasilkan kristal putih."
        },
        "Uji Fehling (Aldehida vs Keton)": {
            "steps": [
                {"label": "Awal", "tubes": [
                    {"tinggi": 0, "warna": "#1e293b", "efek": "none", "label": "Aldehida"},
                    {"tinggi": 0, "warna": "#1e293b", "efek": "none", "label": "Keton"},
                ], "status": "Tabung disiapkan untuk uji diferensiasi."},
                {"label": "Masukkan Sampel", "tubes": [
                    {"tinggi": 40, "warna": "#fef9c3", "efek": "none", "label": "Aldehida"},
                    {"tinggi": 40, "warna": "#f0fdf4", "efek": "none", "label": "Keton"},
                ], "status": "Sampel dimasukkan."},
                {"label": "Tambah Larutan Fehling (Biru)", "tubes": [
                    {"tinggi": 65, "warna": "#3b82f6", "efek": "none", "label": "Fehling+Ald", "glow": True},
                    {"tinggi": 65, "warna": "#3b82f6", "efek": "none", "label": "Fehling+Ket"},
                ], "status": "Larutan Fehling biru ditambahkan, kemudian dipanaskan..."},
                {"label": "Panaskan & Amati", "tubes": [
                    {"tinggi": 65, "warna": "#3b82f6", "efek": "precipitate", "warna_endapan": "#b91c1c", "label": "Merah Bata!", "glow": True},
                    {"tinggi": 65, "warna": "#3b82f6", "efek": "none", "label": "→ Tetap Biru"},
                ], "status": "✔ Aldehida: endapan Cu₂O merah bata. Keton: tetap biru (bukan reduktor)."},
            ],
            "reaksi": r"\text{R-CHO} + 2\text{Cu}^{2+} + 5\text{OH}^- \rightarrow \text{R-COO}^- + \text{Cu}_2\text{O}\!\downarrow + 3\text{H}_2\text{O}",
            "kesimpulan": "Aldehida adalah reduktor kuat yang dapat mereduksi Cu²⁺ → Cu⁺ (Cu₂O merah bata). Keton tidak bisa."
        },
        "Uji Iodoform (Metil Keton)": {
            "steps": [
                {"label": "Awal", "tubes": [
                    {"tinggi": 0, "warna": "#1e293b", "efek": "none", "label": "Tabung"},
                ], "status": "Tabung siap untuk uji iodoform."},
                {"label": "Masukkan Metil Keton / Etanol", "tubes": [
                    {"tinggi": 40, "warna": "#f0fdf4", "efek": "none", "label": "Sampel"},
                ], "status": "Sampel dimasukkan."},
                {"label": "Tambah I₂ + NaOH", "tubes": [
                    {"tinggi": 60, "warna": "#92400e", "efek": "none", "label": "I₂/NaOH", "glow": True},
                ], "status": "Larutan I₂ dalam NaOH ditambahkan ke sampel..."},
                {"label": "Amati Endapan Kuning", "tubes": [
                    {"tinggi": 65, "warna": "#fef08a", "efek": "precipitate", "warna_endapan": "#facc15", "label": "CHI₃ Kuning!", "glow": True},
                ], "status": "✔ POSITIF: Endapan kuning kristal iodoform (CHI₃) berbau khas!"},
            ],
            "reaksi": r"\text{R-CO-CH}_3 + 3\text{I}_2 + 4\text{NaOH} \rightarrow \text{CHI}_3\!\downarrow + \text{R-COONa} + 3\text{NaI} + 3\text{H}_2\text{O}",
            "kesimpulan": "Gugus metil (CH₃) pada metil keton/etanol bereaksi dengan I₂/NaOH membentuk kristal kuning CHI₃ yang khas."
        },
    },
    "BAB IV": {
        "Uji NaHCO₃ — Asam Karboksilat": {
            "steps": [
                {"label": "Awal", "tubes": [
                    {"tinggi": 0, "warna": "#1e293b", "efek": "none", "label": "Tabung"},
                ], "status": "Tabung siap."},
                {"label": "Masukkan Sampel Asam Karboksilat", "tubes": [
                    {"tinggi": 40, "warna": "#fef3c7", "efek": "none", "label": "Asam Karboks."},
                ], "status": "Sampel asam karboksilat dimasukkan."},
                {"label": "Tambah NaHCO₃", "tubes": [
                    {"tinggi": 60, "warna": "#dbeafe", "efek": "none", "label": "NaHCO₃"},
                ], "status": "Natrium bikarbonat ditambahkan..."},
                {"label": "Amati Gas CO₂", "tubes": [
                    {"tinggi": 65, "warna": "#bfdbfe", "efek": "bubbles", "label": "CO₂ mendesau!", "glow": True},
                ], "status": "✔ POSITIF: Gelembung gas CO₂ terbentuk dengan deras (effervescence)!"},
            ],
            "reaksi": r"\text{R-COOH} + \text{NaHCO}_3 \rightarrow \text{R-COONa} + \text{H}_2\text{O} + \text{CO}_2\!\uparrow",
            "kesimpulan": "Asam karboksilat cukup asam untuk mendeprotonasi NaHCO₃ menghasilkan gas CO₂ yang membuktikan gugus -COOH."
        },
        "Uji Air Barit — Konfirmasi CO₂": {
            "steps": [
                {"label": "Awal", "tubes": [
                    {"tinggi": 0, "warna": "#1e293b", "efek": "none", "label": "Tabung Gas"},
                    {"tinggi": 40, "warna": "#f0fdf4", "efek": "none", "label": "Air Barit"},
                ], "status": "Tabung air barit disiapkan untuk menangkap CO₂."},
                {"label": "Hasilkan CO₂ dari Asam + NaHCO₃", "tubes": [
                    {"tinggi": 60, "warna": "#bfdbfe", "efek": "bubbles", "label": "CO₂ keluar", "glow": True},
                    {"tinggi": 40, "warna": "#f0fdf4", "efek": "none", "label": "Air Barit"},
                ], "status": "Gas CO₂ dialirkan ke dalam air barit Ba(OH)₂..."},
                {"label": "Amati Air Barit", "tubes": [
                    {"tinggi": 60, "warna": "#bfdbfe", "efek": "none", "label": "CO₂ sumber"},
                    {"tinggi": 60, "warna": "#f1f5f9", "efek": "precipitate", "warna_endapan": "#ffffff", "label": "BaCO₃ Keruh!", "glow": True},
                ], "status": "✔ POSITIF: Air barit menjadi keruh → terbentuk endapan BaCO₃ putih!"},
            ],
            "reaksi": r"\text{CO}_2 + \text{Ba(OH)}_2 \rightarrow \text{BaCO}_3\!\downarrow + \text{H}_2\text{O}",
            "kesimpulan": "Pengeruhan air barit oleh gas CO₂ mengkonfirmasi keberadaan gugus asam karboksilat dalam sampel."
        },
        "Uji Hidroksamat — Identifikasi Ester": {
            "steps": [
                {"label": "Awal", "tubes": [
                    {"tinggi": 0, "warna": "#1e293b", "efek": "none", "label": "Tabung"},
                ], "status": "Tabung siap untuk uji hidroksamat."},
                {"label": "Masukkan Sampel Ester", "tubes": [
                    {"tinggi": 40, "warna": "#f0fdf4", "efek": "none", "label": "Ester"},
                ], "status": "Sampel ester dimasukkan ke tabung."},
                {"label": "Tambah NH₂OH (Hidroksilamin)", "tubes": [
                    {"tinggi": 55, "warna": "#d1fae5", "efek": "none", "label": "Ester+NH₂OH"},
                ], "status": "Hidroksilamin membentuk asam hidroksamat dari ester..."},
                {"label": "Tambah FeCl₃ — Amati Warna", "tubes": [
                    {"tinggi": 65, "warna": "#c026d3", "efek": "none", "label": "Ungu Violet!", "glow": True},
                ], "status": "✔ POSITIF: Warna ungu/violet intens → kompleks Fe³⁺-hidroksamat terbentuk!"},
            ],
            "reaksi": r"3\text{R-COOR'} + \text{NH}_2\text{OH} \xrightarrow{\text{FeCl}_3} \text{Fe(R-CONHO)}_3\text{(Ungu)} + 3\text{HCl}",
            "kesimpulan": "Warna ungu menandakan terbentuknya kompleks besi(III)-hidroksamat. Khas dan spesifik untuk senyawa ester."
        },
    },
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
        "Uji Golongan Alkohol": {"hasil": "(+) Merah Ceri", "reaksi": r"R-OH + [Ce(NO_3)_6]^{2-} \rightarrow [Ce(OR)(NO_3)_5]^{2-} + HNO_3", "alasan": "Gugus -OH bebas bereaksi membentuk kompleks koordinasi merah ceri dengan ion Cerium(IV).", "warna_akhir": "#ef4444", "efek": "none"},
        "Uji Oksidasi Alkohol": {"hasil": "(+) Hijau", "reaksi": r"3\ R-CH_2OH + 2\ CrO_3 + 3\ H_2SO_4 \rightarrow 3\ R-CHO + Cr_2(SO_4)_3 + 6\ H_2O", "alasan": "Memiliki atom hidrogen alfa. Dioksidasi menjadi aldehida, Cr(VI) jingga → Cr(III) hijau.", "warna_akhir": "#10b981", "efek": "none"},
        "Uji Golongan Alkohol Sekunder": {"hasil": "(-) Tetap Jingga", "reaksi": r"R-CH_2OH + HCl \xrightarrow{ZnCl_2} \text{Tidak ada reaksi}", "alasan": "Karbokation primer sangat tidak stabil, tidak bereaksi dengan Lucas pada suhu kamar.", "warna_akhir": "#f97316", "efek": "none"}
    },
    "Alkohol Sekunder": {
        "Uji Golongan Alkohol": {"hasil": "(+) Merah Ceri", "reaksi": r"R-OH + [Ce(NO_3)_6]^{2-} \rightarrow [Ce(OR)(NO_3)_5]^{2-} + HNO_3", "alasan": "Gugus -OH sekunder membentuk kompleks koordinasi merah dengan Cerium(IV).", "warna_akhir": "#ef4444", "efek": "none"},
        "Uji Oksidasi Alkohol": {"hasil": "(+) Hijau", "reaksi": r"3\ R_2CH-OH + 2\ CrO_3 + 3\ H_2SO_4 \rightarrow 3\ R_2C=O + Cr_2(SO_4)_3 + 6\ H_2O", "alasan": "Alkohol sekunder dioksidasi menjadi keton, Cr(VI) jingga → Cr(III) hijau.", "warna_akhir": "#10b981", "efek": "none"},
        "Uji Golongan Alkohol Sekunder": {"hasil": "(+) Emulsi Putih", "reaksi": r"R_2CH-OH + HCl \xrightarrow{ZnCl_2} R_2CH-Cl \downarrow + H_2O", "alasan": "Karbokation sekunder stabil menengah, bereaksi dengan Lucas menghasilkan emulsi putih.", "warna_akhir": "#e2e8f0", "efek": "cloudy"},
        "Uji Golongan Metil Keton / Metil Karbinol": {"hasil": "(+) Endapan Kuning", "reaksi": r"R-CH(OH)-CH_3 + 4\ I_2 + 6\ NaOH \rightarrow CHI_3 \downarrow + R-COONa + 5\ NaI + 5\ H_2O", "alasan": "Struktur metil karbinol membentuk iodoform kuning.", "warna_akhir": "#fef08a", "efek": "precipitate", "warna_endapan": "#facc15"}
    },
    "Alkohol Tersier": {
        "Uji Golongan Alkohol": {"hasil": "(+) Merah Ceri", "reaksi": r"R-OH + [Ce(NO_3)_6]^{2-} \rightarrow [Ce(OR)(NO_3)_5]^{2-} + HNO_3", "alasan": "Memiliki gugus -OH bebas yang membentuk kompleks merah dengan CAN.", "warna_akhir": "#ef4444", "efek": "none"},
        "Uji Oksidasi Alkohol": {"hasil": "(-) Tetap Jingga", "reaksi": r"R_3C-OH + CrO_3 \rightarrow \text{Tidak bereaksi}", "alasan": "Tidak memiliki hidrogen alfa, tidak dapat dioksidasi.", "warna_akhir": "#f97316", "efek": "none"},
        "Uji Golongan Alkohol Tersier": {"hasil": "(+) Emulsi Putih (Seketika)", "reaksi": r"R_3C-OH + HCl \xrightarrow{ZnCl_2} R_3C-Cl \downarrow + H_2O", "alasan": "Karbokation tersier sangat stabil, reaksi berjalan instan membentuk emulsi putih.", "warna_akhir": "#94a3b8", "efek": "cloudy"}
    },
    "Aldehida (Alkanal)": {
        "Uji Golongan Alkohol": {"hasil": "(-) Tetap Jingga", "reaksi": r"R-CHO + [Ce(NO_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}", "alasan": "Aldehida tidak memiliki gugus -OH bebas.", "warna_akhir": "#f97316", "efek": "none"},
        "Uji Golongan Alkanal/Aldehida (Bisulfit)": {"hasil": "(+) Endapan Putih", "reaksi": r"R-CHO + NaHSO_3 \rightarrow R-CH(OH)SO_3Na \downarrow", "alasan": "Bisulfit mengadisi karbonil aldehida membentuk kristal putih.", "warna_akhir": "#cbd5e1", "efek": "precipitate", "warna_endapan": "#ffffff"},
        "Uji Reduksi Golongan Alkanal (Fehling)": {"hasil": "(+) Merah Bata", "reaksi": r"R-CHO + 2\ Cu^{2+} + 5\ OH^- \rightarrow R-COO^- + Cu_2O \downarrow + 3\ H_2O", "alasan": "Aldehida mereduksi Cu²⁺ menjadi Cu₂O merah bata.", "warna_akhir": "#3b82f6", "efek": "precipitate", "warna_endapan": "#b91c1c"},
        "Uji Spesifik Golongan Alkanal (Schiff)": {"hasil": "(+) Ungu / Magenta", "reaksi": r"\text{Aldehida} + \text{Pereaksi Schiff} \rightarrow \text{Kompleks Magenta}", "alasan": "Reaksi adisi spesifik mengembalikan warna p-rosanilin menjadi ungu.", "warna_akhir": "#d946ef", "efek": "none"}
    },
    "Keton (Alkanon)": {
        "Uji Golongan Alkohol": {"hasil": "(-) Tetap Jingga", "reaksi": r"\text{Keton} + [Ce(NO_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}", "alasan": "Keton tidak memiliki gugus hidroksil.", "warna_akhir": "#f97316", "efek": "none"},
        "Uji Golongan Alkanal/Aldehida (Bisulfit)": {"hasil": "(+) Endapan Putih", "reaksi": r"CH_3-CO-CH_3 + NaHSO_3 \rightarrow (CH_3)_2C(OH)SO_3Na \downarrow", "alasan": "Keton suku rendah masih bisa diadisi bisulfit membentuk endapan putih.", "warna_akhir": "#cbd5e1", "efek": "precipitate", "warna_endapan": "#ffffff"},
        "Uji Reduksi Golongan Alkanal (Fehling)": {"hasil": "(-) Tetap Biru", "reaksi": r"\text{Keton} + Cu^{2+} \rightarrow \text{Tidak bereaksi}", "alasan": "Keton bukan reduktor, tidak dapat mereduksi Cu²⁺.", "warna_akhir": "#3b82f6", "efek": "none"},
        "Uji Golongan Metil Keton / Metil Karbinol": {"hasil": "(+) Endapan Kuning", "reaksi": r"R-CO-CH_3 + 3\ I_2 + 4\ NaOH \rightarrow CHI_3 \downarrow + R-COONa + 3\ NaI + 3\ H_2O", "alasan": "Metil keton membentuk endapan kuning iodoform.", "warna_akhir": "#fef08a", "efek": "precipitate", "warna_endapan": "#facc15"}
    },
    "Ester (Alkil Alkanoat)": {
        "Uji Golongan Alkohol": {"hasil": "(-) Tetap Jingga", "reaksi": r"\text{Ester} + [Ce(NO_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}", "alasan": "Tidak memiliki gugus hidroksil bebas.", "warna_akhir": "#f97316", "efek": "none"},
        "Uji Golongan Alkanal/Aldehida (Bisulfit)": {"hasil": "(-) Bening", "reaksi": r"\text{Ester} + NaHSO_3 \rightarrow \text{Tidak bereaksi}", "alasan": "Gugus ester stabil akibat resonansi, tidak reaktif terhadap bisulfit.", "warna_akhir": "#f8fafc", "efek": "none"},
        "Uji Golongan Ester": {"hasil": "(+) Merah Violet", "reaksi": r"3\ R-CONHOH + FeCl_3 \rightarrow Fe(R-CONHO)_3 + 3\ HCl", "alasan": "Ester bereaksi dengan hidroksilamin membentuk asam hidroksamat yang kompleks violet.", "warna_akhir": "#c026d3", "efek": "none"}
    },
    "Asam Karboksilat": {
        "Uji Golongan Alkohol": {"hasil": "(-) Tetap Jingga", "reaksi": r"R-COOH + [Ce(NO_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}", "alasan": "Oksigen hidroksil tidak nukleofilik akibat resonansi karbonil.", "warna_akhir": "#f97316", "efek": "none"},
        "Uji Golongan Alkanal/Aldehida (Bisulfit)": {"hasil": "(-) Bening", "reaksi": r"R-COOH + NaHSO_3 \rightarrow \text{Tidak bereaksi}", "alasan": "Tidak mengandung aldehida atau keton.", "warna_akhir": "#f8fafc", "efek": "none"},
        "Uji Golongan Ester": {"hasil": "(-) Bening", "reaksi": r"R-COOH + NH_2OH + FeCl_3 \rightarrow \text{Tidak bereaksi}", "alasan": "Asam karboksilat bebas tidak membentuk hidroksamat pada kondisi ini.", "warna_akhir": "#f8fafc", "efek": "none"},
        "Uji Golongan Asam Karboksilat": {"hasil": "(+) Gelembung & Keruh", "reaksi": r"CO_2 + Ba(OH)_2 \rightarrow BaCO_3 \downarrow + H_2O", "alasan": "Asam mendonasikan proton ke bikarbonat menghasilkan CO₂ yang mengeruhkan air barit.", "warna_akhir": "#f8fafc", "efek": "bubbles"}
    },
    "Alkana / Hidrokarbon Jenuh": {
        "Uji Golongan Alkohol": {"hasil": "(-) Tetap Jingga", "reaksi": r"\text{Alkana} + [Ce(NO_3)_6]^{2-} \rightarrow \text{Tidak bereaksi}", "alasan": "Senyawa nonpolar inert.", "warna_akhir": "#f97316", "efek": "none"},
        "Uji Golongan Alkanal/Aldehida (Bisulfit)": {"hasil": "(-) Bening", "reaksi": r"\text{Alkana} + NaHSO_3 \rightarrow \text{Tidak bereaksi}", "alasan": "Tidak memiliki gugus karbonil.", "warna_akhir": "#f8fafc", "efek": "none"},
        "Uji Golongan Ester": {"hasil": "(-) Bening", "reaksi": r"\text{Alkana} + NH_2OH \rightarrow \text{Tidak bereaksi}", "alasan": "Tidak memiliki gugus ester.", "warna_akhir": "#f8fafc", "efek": "none"},
        "Uji Golongan Asam Karboksilat": {"hasil": "(-) Bening", "reaksi": r"\text{Alkana} + NaHCO_3 \rightarrow \text{Tidak bereaksi}", "alasan": "Hidrokarbon jenuh bersifat inert.", "warna_akhir": "#f8fafc", "efek": "none"}
    }
}

# ==============================================================================
# 4. SESSION STATE INITIALIZATION
# ==============================================================================
defaults = {
    "test_started": False, "current_step": 0,
    "log_history": [], "trigger_animation": False,
    "sub_bab_i": "A. Sifat Fisika Hidrokarbon",
    "sub_bab_ii": "A. Sifat Fisika & Klasifikasi",
    "sub_bab_iii": "A. Sifat Fisika",
    "sub_bab_iv": "A. Sifat Fisika",
    # For bab experiments
    "bab_exp_key": None, "bab_exp_step": 0, "bab_exp_started": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ==============================================================================
# 5. SIDEBAR
# ==============================================================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3022/3022607.png", width=75)
    st.title("OrganicChem v2.0")
    st.write("🔬 *E-Learning & Lab Simulator*")
    st.markdown("---")
    pilihan_halaman = st.sidebar.radio(
        "Navigasi Menu:",
        ["🏠 HALAMAN UTAMA",
         "📘 BAB I. HIDROKARBON",
         "📙 BAB II. ALKOHOL, ETER, DAN FENOL",
         "📗 BAB III. ALDEHID DAN KETON",
         "📕 BAB IV. ASAM KARBOKSILAT DAN DERIVATNYA",
         "🔬 POST TEST"]
    )
    st.markdown("---")
    st.caption("E-Learning Kimia Organik | © 2026")

# ==============================================================================
# 6. REUSABLE: BAB EXPERIMENT SIMULATOR
# ==============================================================================
def render_bab_experiment(bab_key):
    """Renders the 2D illustrated experiment for a chapter."""
    experiments = bab_experiments[bab_key]
    exp_names = list(experiments.keys())

    st.markdown("---")
    st.markdown("### 🧪 Simulasi Percobaan Interaktif")

    # Experiment selector
    selected_exp = st.selectbox("Pilih Percobaan:", exp_names, key=f"sel_{bab_key}")

    if st.session_state.bab_exp_key != selected_exp:
        st.session_state.bab_exp_key = selected_exp
        st.session_state.bab_exp_step = 0
        st.session_state.bab_exp_started = False

    exp = experiments[selected_exp]
    steps = exp["steps"]
    total_steps = len(steps)
    current = st.session_state.bab_exp_step

    col_tube, col_ctrl = st.columns([1, 1.8])

    with col_tube:
        step_data = steps[min(current, total_steps - 1)]
        is_last = (current == total_steps - 1)
        html = render_lab_scene(
            step_data["tubes"],
            step_data["status"],
            status_active=is_last
        )
        st.markdown(html, unsafe_allow_html=True)

        # Progress bar
        prog = current / (total_steps - 1) if total_steps > 1 else 1.0
        st.progress(prog, text=f"Tahap {current + 1} / {total_steps}")

    with col_ctrl:
        st.markdown(f"**📋 Percobaan:** {selected_exp}")
        st.markdown(f"**⚗️ Tahap saat ini:** *{step_data['label']}*")

        # Step buttons
        btn_cols = st.columns(2)
        with btn_cols[0]:
            if st.button("⏮ Kembali", disabled=(current == 0), use_container_width=True, key=f"back_{bab_key}"):
                st.session_state.bab_exp_step = max(0, current - 1)
                force_rerun()
        with btn_cols[1]:
            if current < total_steps - 1:
                label_next = steps[current + 1]["label"]
                if st.button(f"▶ {label_next}", use_container_width=True, key=f"next_{bab_key}", type="primary"):
                    st.session_state.bab_exp_step = current + 1
                    force_rerun()
            else:
                if st.button("🔄 Ulangi", use_container_width=True, key=f"reset_{bab_key}"):
                    st.session_state.bab_exp_step = 0
                    force_rerun()

        # Show all step navigation as chips
        st.markdown("**Lompat ke Tahap:**")
        chip_cols = st.columns(min(total_steps, 4))
        for i, s in enumerate(steps):
            col_idx = i % 4
            with chip_cols[col_idx]:
                btn_type = "primary" if i == current else "secondary"
                if st.button(f"{i+1}", key=f"chip_{bab_key}_{i}", use_container_width=True, type=btn_type):
                    st.session_state.bab_exp_step = i
                    force_rerun()

        st.markdown("---")
        # Reaction equation & conclusion
        if current == total_steps - 1:
            st.success("✅ Percobaan selesai! Berikut persamaan reaksinya:")
            st.latex(exp["reaksi"])
            st.info(f"**💡 Kesimpulan:** {exp['kesimpulan']}")
        else:
            st.markdown("*Persamaan reaksi akan ditampilkan setelah percobaan selesai.*")

# ==============================================================================
# 7. PAGE LOGIC
# ==============================================================================

if pilihan_halaman == "🏠 HALAMAN UTAMA":
    st.markdown("""
        <div class="banner-utama">
            <h1 style='color:white;margin-bottom:5px;font-weight:700;'>Eksplorasi Dunia Kimia Organik Tanpa Batas! 👋</h1>
            <p style='font-size:1.2em;opacity:0.95;'>Solusi cerdas belajar mandiri dan simulasi identifikasi gugus fungsi dalam satu platform.</p>
        </div>
    """, unsafe_allow_html=True)
    st.subheader("💡 Tentang Platform Ini")
    st.write("Kami hadir untuk menjembatani teori dan praktik. Platform ini membantu Anda memahami materi teoretis sekaligus memvisualisasikan reaksi uji kualitatif senyawa organik secara interaktif—kapan saja dan di mana saja.")
    st.markdown("---")
    st.markdown("### 📜 Petunjuk Penggunaan")
    p1, p2, p3 = st.columns(3)
    with p1:
        st.markdown("""<div style="background:white;padding:20px;border-radius:12px;border-top:5px solid #0f766e;box-shadow:0 4px 6px rgba(0,0,0,0.05);min-height:200px;">
            <h4 style="margin-top:0;color:#0f766e;">📖 Langkah 1: Pelajari</h4>
            <p style="font-size:0.95em;color:#475569;">Buka <b>Menu Navigasi</b> di samping kiri. Pilih materi dari <b>BAB I hingga BAB IV</b> untuk membaca teori dasar.</p>
        </div>""", unsafe_allow_html=True)
    with p2:
        st.markdown("""<div style="background:white;padding:20px;border-radius:12px;border-top:5px solid #14b8a6;box-shadow:0 4px 6px rgba(0,0,0,0.05);min-height:200px;">
            <h4 style="margin-top:0;color:#14b8a6;">🧪 Langkah 2: Simulasi Bab</h4>
            <p style="font-size:0.95em;color:#475569;">Di setiap BAB terdapat <b>Simulasi 2D Interaktif</b>. Tekan tombol tahap demi tahap untuk melihat reaksi secara visual.</p>
        </div>""", unsafe_allow_html=True)
    with p3:
        st.markdown("""<div style="background:white;padding:20px;border-radius:12px;border-top:5px solid #0ea5e9;box-shadow:0 4px 6px rgba(0,0,0,0.05);min-height:200px;">
            <h4 style="margin-top:0;color:#0ea5e9;">📊 Langkah 3: Post Test</h4>
            <p style="font-size:0.95em;color:#475569;">Masuk ke <b>🔬 POST TEST</b> untuk menguji identifikasi senyawa misterius (Blind Sample) secara lengkap.</p>
        </div>""", unsafe_allow_html=True)
    st.info("💡 **Baru!** Setiap BAB kini dilengkapi ilustrasi 2D tabung reaksi interaktif. Gunakan tombol ▶ untuk melanjutkan tiap tahap percobaan!")

elif pilihan_halaman == "📘 BAB I. HIDROKARBON":
    st.title("📘 BAB I. HIDROKARBON")
    st.write("---")
    st.write("**Pilih Sub-Bab Materi:**")
    btn_col1, btn_col2, _ = st.columns([1, 1, 2])
    with btn_col1:
        if st.button("A. Sifat Fisika Hidrokarbon", use_container_width=True):
            st.session_state.sub_bab_i = "A. Sifat Fisika Hidrokarbon"
    with btn_col2:
        if st.button("B. Sifat Kimia & Identifikasi", use_container_width=True):
            st.session_state.sub_bab_i = "B. Sifat Kimia & Reaksi Identifikasi"
    st.write("---")

    if st.session_state.sub_bab_i == "A. Sifat Fisika Hidrokarbon":
        st.markdown("""#### **A. Sifat Fisika Hidrokarbon**
Hidrokarbon adalah senyawa organik yang tersusun atas unsur karbon (C) dan hidrogen (H).
* **Wujud Zat:** $C_1-C_4$ berwujud gas; $C_5-C_{17}$ cair; $\ge C_{18}$ padat.
* **Kelarutan:** Nonpolar, tidak larut dalam air. Larut dalam pelarut organik nonpolar ($CHCl_3$, $CCl_4$, eter).
* **Titik Didih:** Meningkat seiring massa molekul. Rantai lurus > rantai bercabang.
* **Densitas:** Lebih kecil dari air, lapisan hidrokarbon selalu di atas.""")
    elif st.session_state.sub_bab_i == "B. Sifat Kimia & Reaksi Identifikasi":
        st.markdown("""#### **B. Sifat Kimia & Reaksi Identifikasi Hidrokarbon**
**1. Alkana** — Sangat tidak reaktif (parafin). Substitusi halogen dengan sinar UV berjalan lambat.
**2. Alkena/Alkuna** — Sangat reaktif karena ikatan rangkap, mudah diadisi.
**3. Benzena** — Inti stabil karena resonansi, cenderung substitusi elektrofilik.""")
        st.latex(r"\text{R-CH}=\text{CH-R} + \text{I}_2 \rightarrow \text{R-CH(I)-CH(I)-R}")
        st.latex(r"3\text{CH}_2=\text{CH}_2 + 2\text{KMnO}_4 + 4\text{H}_2\text{O} \rightarrow 3\text{HOCH}_2\text{CH}_2\text{OH} + 2\text{MnO}_2\downarrow + 2\text{KOH}")

    # 2D Lab Simulation
    render_bab_experiment("BAB I")

elif pilihan_halaman == "📙 BAB II. ALKOHOL, ETER, DAN FENOL":
    st.title("📙 BAB II. ALKOHOL, ETER, DAN FENOL")
    st.write("---")
    st.write("**Pilih Sub-Bab Materi:**")
    btn_col1, btn_col2, btn_col3, _ = st.columns([1.2, 1.2, 1.2, 1])
    with btn_col1:
        if st.button("A. Sifat Fisika & Klasifikasi", use_container_width=True):
            st.session_state.sub_bab_ii = "A. Sifat Fisika & Klasifikasi"
    with btn_col2:
        if st.button("B. Reaksi Alkohol & Eter", use_container_width=True):
            st.session_state.sub_bab_ii = "B. Reaksi Alkohol & Eter"
    with btn_col3:
        if st.button("C. Reaksi Kimia Fenol", use_container_width=True):
            st.session_state.sub_bab_ii = "C. Reaksi Kimia Fenol"
    st.write("---")

    if st.session_state.sub_bab_ii == "A. Sifat Fisika & Klasifikasi":
        st.markdown("""#### **A. Sifat Fisika & Klasifikasi**
* **Alkohol ($R-OH$):** Turunan alkana. Diklasifikasikan primer, sekunder, tersier. Suku rendah larut dalam air (ikatan hidrogen).
* **Eter ($R^1-O-R^2$):** Isomer fungsional alkohol. Titik didih lebih rendah dari alkohol.
* **Fenol ($C_6H_5OH$):** -OH langsung di cincin benzena. Bersifat asam lemah.""")
    elif st.session_state.sub_bab_ii == "B. Reaksi Alkohol & Eter":
        st.markdown("#### **B. Persamaan Reaksi Kimia Alkohol & Eter**")
        st.latex(r"\text{R}_3\text{C-OH} + \text{HCl} \xrightarrow{\text{ZnCl}_2} \text{R}_3\text{C-Cl}\downarrow + \text{H}_2\text{O}")
        st.latex(r"\text{R-CH}_2\text{-OH} \xrightarrow{\text{CrO}_3/\text{H}_2\text{SO}_4} \text{R-COOH}")
        st.latex(r"\text{ROH} + [\text{Ce(NO}_3)_6]^{2-} \rightarrow [\text{Ce(OR)(NO}_3)_5]^{2-}\text{(Merah)} + \text{HNO}_3")
    elif st.session_state.sub_bab_ii == "C. Reaksi Kimia Fenol":
        st.markdown("#### **C. Persamaan Reaksi Kimia Fenol**")
        st.latex(r"\text{C}_6\text{H}_5\text{OH} + \text{NaOH} \rightarrow \text{C}_6\text{H}_5\text{ONa} + \text{H}_2\text{O}")
        st.latex(r"6\text{C}_6\text{H}_5\text{OH} + \text{FeCl}_3 \rightarrow [\text{Fe(OC}_6\text{H}_5)_6]^{3-} + 3\text{H}^+ + 3\text{Cl}^-")
        st.latex(r"\text{C}_6\text{H}_5\text{OH} + 3\text{Br}_2 \rightarrow \text{C}_6\text{H}_2\text{Br}_3\text{OH}\downarrow + 3\text{HBr}")

    render_bab_experiment("BAB II")

elif pilihan_halaman == "📗 BAB III. ALDEHID DAN KETON":
    st.title("📗 BAB III. ALDEHID DAN KETON")
    st.write("---")
    st.write("**Pilih Sub-Bab Materi:**")
    btn_col1, btn_col2, btn_col3, _ = st.columns([1, 1.2, 1.5, 1])
    with btn_col1:
        if st.button("A. Sifat Fisika", use_container_width=True):
            st.session_state.sub_bab_iii = "A. Sifat Fisika"
    with btn_col2:
        if st.button("B. Reaksi Adisi Karbonil", use_container_width=True):
            st.session_state.sub_bab_iii = "B. Reaksi Adisi Karbonil"
    with btn_col3:
        if st.button("C. Reaksi Diferensiasi (Uji Reduksi)", use_container_width=True):
            st.session_state.sub_bab_iii = "C. Reaksi Diferensiasi (Uji Reduksi)"
    st.write("---")

    if st.session_state.sub_bab_iii == "A. Sifat Fisika":
        st.markdown("""#### **A. Sifat Fisika**
Aldehida ($R-CHO$) dan keton ($R-CO-R'$) adalah isomer fungsional dengan gugus karbonil ($C=O$).
Metanal berwujud gas. Keton suku rendah (aseton) berupa cairan encer yang mudah menguap.""")
    elif st.session_state.sub_bab_iii == "B. Reaksi Adisi Karbonil":
        st.markdown("#### **B. Reaksi Adisi Karbonil**")
        st.latex(r"\text{R-CHO} + \text{NaHSO}_3 \rightarrow \text{R-CH(OH)-SO}_3\text{Na}")
        st.latex(r"\text{R-CHO} + \text{R'OH} \xrightarrow{\text{HCl}} \text{R-CH(OH)(OR')}")
    elif st.session_state.sub_bab_iii == "C. Reaksi Diferensiasi (Uji Reduksi)":
        st.markdown("#### **C. Reaksi Diferensiasi (Uji Daya Reduksi Aldehida)**")
        st.latex(r"\text{R-CHO} + 2[\text{Ag(NH}_3)_2]^+ + 3\text{OH}^- \rightarrow \text{R-COO}^- + 2\text{Ag}\downarrow + 4\text{NH}_3 + 2\text{H}_2\text{O}")
        st.latex(r"\text{R-CHO} + 2\text{Cu}^{2+} + 5\text{OH}^- \rightarrow \text{R-COO}^- + \text{Cu}_2\text{O}\downarrow + 3\text{H}_2\text{O}")

    render_bab_experiment("BAB III")

elif pilihan_halaman == "📕 BAB IV. ASAM KARBOKSILAT DAN DERIVATNYA":
    st.title("📕 BAB IV. ASAM KARBOKSILAT DAN DERIVATNYA")
    st.write("---")
    st.write("**Pilih Sub-Bab Materi:**")
    btn_col1, btn_col2, btn_col3, _ = st.columns([1, 1.5, 1.5, 1])
    with btn_col1:
        if st.button("A. Sifat Fisika", use_container_width=True):
            st.session_state.sub_bab_iv = "A. Sifat Fisika"
    with btn_col2:
        if st.button("B. Reaksi Kimia Asam Karboksilat", use_container_width=True):
            st.session_state.sub_bab_iv = "B. Reaksi Kimia Asam Karboksilat"
    with btn_col3:
        if st.button("C. Identifikasi Derivat (Ester)", use_container_width=True):
            st.session_state.sub_bab_iv = "C. Identifikasi Derivat (Ester)"
    st.write("---")

    if st.session_state.sub_bab_iv == "A. Sifat Fisika":
        st.markdown("""#### **A. Sifat Fisika**
Asam karboksilat memiliki gugus $-COOH$. Rantai pendek ($C_1-C_4$) sangat larut dalam air karena ikatan hidrogen kuat.
Titik didih relatif tinggi, turun seiring bertambah panjang rantai nonpolar.""")
    elif st.session_state.sub_bab_iv == "B. Reaksi Kimia Asam Karboksilat":
        st.markdown("#### **B. Persamaan Reaksi Kimia Asam Karboksilat**")
        st.latex(r"\text{R-COOH} + \text{NaOH} \rightarrow \text{R-COONa} + \text{H}_2\text{O}")
        st.latex(r"\text{R-COOH} + \text{NaHCO}_3 \rightarrow \text{R-COONa} + \text{H}_2\text{O} + \text{CO}_2\uparrow")
        st.latex(r"\text{R-COOH} + \text{R'-OH} \xrightarrow{\text{H}_2\text{SO}_4,\Delta} \text{R-COOR'} + \text{H}_2\text{O}")
    elif st.session_state.sub_bab_iv == "C. Identifikasi Derivat (Ester)":
        st.markdown("#### **C. Persamaan Reaksi Identifikasi Ester (Uji Asam Hidroksamat)**")
        st.latex(r"\text{R-COOR'} + \text{NH}_2\text{OH} \rightarrow \text{R-CONH-OH} + \text{R'-OH}")
        st.latex(r"3\text{R-CONH-OH} + \text{FeCl}_3 \rightarrow \text{Fe(R-CONHO)}_3 + 3\text{HCl}")

    render_bab_experiment("BAB IV")

elif pilihan_halaman == "🔬 POST TEST":
    st.title("🔀 Asisten Identifikasi Cerdas (Step-by-Step)")
    st.write("Sistem ini mensimulasikan penelusuran identifikasi kualitatif langkah demi langkah.")

    if not st.session_state.test_started:
        st.divider()
        senyawa = st.selectbox("Pilih Golongan Senyawa yang Akan Diuji (*Blind Sample*):", ["-- Pilih Senyawa --"] + list(flowchart_paths.keys()))
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
            st.markdown("<h4 style='text-align:center;'>Visual Lab</h4>", unsafe_allow_html=True)
            reagent_tag_ph = st.empty()
            tube_ph = st.empty()
            status_ph = st.empty()
            st.write("")
            if st.button("⏹️ Stop & Pilih Ulang", use_container_width=True, type="secondary"):
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
                else:
                    st.error(f"**Tahap {log['step']}: {log['pereaksi']}** ➔ **{log['hasil']}**")
                st.latex(log['reaksi'])
                st.write(f"**Pembahasan:** {log['alasan']}")

        def make_post_tubes(warna, efek, warna_endapan=None, glow=False):
            return render_lab_scene(
                [{"tinggi": 65, "warna": warna, "efek": efek, "warna_endapan": warna_endapan, "label": "Sampel", "glow": glow}],
                "", False
            )

        if st.session_state.trigger_animation and st.session_state.current_step < len(urutan):
            pereaksi = urutan[st.session_state.current_step]
            reagent_tag_ph.markdown(f"<div class='reagent-tag'>🧪 Pereaksi: {pereaksi}</div>", unsafe_allow_html=True)

            tube_ph.markdown(make_post_tubes("#1e3a5f", "none"), unsafe_allow_html=True)
            status_ph.markdown("<div style='text-align:center;font-size:0.85em;color:#64748b;'>Menyiapkan sampel...</div>", unsafe_allow_html=True)
            time.sleep(0.8)

            warna_reagen = reagen_colors[pereaksi]
            tube_ph.markdown(make_post_tubes(warna_reagen, "none", glow=True), unsafe_allow_html=True)
            status_ph.markdown("<div style='text-align:center;font-size:0.85em;color:#64748b;'>Mereaksikan komponen...</div>", unsafe_allow_html=True)
            time.sleep(1.3)

            res = database_reaksi[senyawa][pereaksi]
            w_end = res.get("warna_endapan")
            tube_ph.markdown(make_post_tubes(res["warna_akhir"], res["efek"], w_end, glow=True), unsafe_allow_html=True)
            status_ph.markdown("<div style='text-align:center;font-size:0.85em;font-weight:bold;color:#34d399;'>Mengamati perubahan...</div>", unsafe_allow_html=True)
            time.sleep(1.0)

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
                last_p = urutan[st.session_state.current_step - 1]
                reagent_tag_ph.markdown(f"<div class='reagent-tag'>🧪 Pereaksi: {last_p}</div>", unsafe_allow_html=True)
                res = database_reaksi[senyawa][last_p]
                w_end = res.get("warna_endapan")
                tube_ph.markdown(make_post_tubes(res["warna_akhir"], res["efek"], w_end), unsafe_allow_html=True)

            if st.session_state.current_step < len(urutan):
                next_p = urutan[st.session_state.current_step]
                status_ph.markdown("<div style='text-align:center;color:#64748b;font-size:0.85em;'>Menunggu konfirmasi...</div>", unsafe_allow_html=True)
                with col_visual:
                    if st.button(f"Lanjutkan: {next_p} ⏭️", use_container_width=True, type="primary"):
                        st.session_state.trigger_animation = True
                        force_rerun()
            else:
                reagent_tag_ph.markdown("<div class='reagent-tag' style='background:rgba(52,211,153,0.15);color:#34d399;border-color:#065f46;'>🏁 Identifikasi Selesai</div>", unsafe_allow_html=True)
                status_ph.markdown("<div style='text-align:center;font-weight:bold;color:#34d399;'>✅ Rangkaian uji selesai!</div>", unsafe_allow_html=True)
                with log_container:
                    st.info(f"🎉 **KESIMPULAN:** Sampel terbukti merupakan golongan **{senyawa.upper()}**.")
                with col_visual:
                    if st.button("🔄 Uji Senyawa Lain", use_container_width=True):
                        st.session_state.test_started = False
                        force_rerun()
