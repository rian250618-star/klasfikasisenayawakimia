import streamlit as st
from senyawa_data import senyawa_data
import random

st.set_page_config(
    page_title="Klasifikasi 100 Senyawa Kimia",
    page_icon="🧪",
    layout="wide"
)

BADGE_COLORS = {
    "korosif": "#dc3545",
    "mudah terbakar": "#fd7e14",
    "eksplosif": "#d63384",
    "beracun": "#6f42c1",
    "toksik": "#6f42c1",
    "karsinogen": "#6f42c1",
    "oksidator": "#0d6efd",
    "iritasi": "#ffc107",
    "tidak berbahaya": "#198754",
    "lingkungan": "#20c997",
}

SIMBOL_ICONS = {
    "korosif": "⚠️",
    "mudah terbakar": "🔥",
    "beracun": "☠️",
    "toksik": "☠️",
    "karsinogen": "⚠️",
    "oksidator": "💥",
    "iritasi": "❗",
    "tidak berbahaya": "✅",
    "eksplosif": "💢",
    "lingkungan": "🌍",
}

CATEGORIES = [
    ("Semua", ""),
    ("✅ Tidak Berbahaya", "tidak berbahaya"),
    ("☠️ Beracun", "beracun, toksik, karsinogen"),
    ("⚠️ Korosif", "korosif"),
    ("🔥 Mudah Terbakar", "mudah terbakar, eksplosif"),
    ("💥 Oksidator", "oksidator"),
    ("❗ Iritasi", "iritasi"),
    ("🌍 Lingkungan", "lingkungan"),
]

CHIP_PRIORITY = [
    "tidak berbahaya",
    "eksplosif",
    "sangat mudah terbakar",
    "mudah terbakar",
    "beracun, toksik, karsinogen",
    "oksidator",
    "korosif",
    "iritasi",
    "lingkungan",
]

HAZARD_MAP = [
    ("tidak berbahaya", "Tidak Berbahaya", "#198754", "✅"),
    ("sangat mudah terbakar", "Sangat Mudah Terbakar", "#dc3545", "🔥"),
    ("mudah terbakar", "Mudah Terbakar", "#fd7e14", "🔥"),
    ("karsinogen", "Karsinogen", "#6f42c1", "⚠️"),
    ("beracun", "Beracun", "#6f42c1", "☠️"),
    ("toksik", "Toksik", "#6f42c1", "☠️"),
    ("korosif", "Korosif", "#dc3545", "⚠️"),
    ("oksidator", "Oksidator", "#0d6efd", "💥"),
    ("eksplosif", "Eksplosif", "#d63384", "💢"),
    ("iritasi", "Iritasi", "#ffc107", "❗"),
    ("lingkungan", "Lingkungan", "#20c997", "🌍"),
    ("berbahaya", "Berbahaya", "#6c757d", "⚠️"),
]

def assign_category(simbol):
    s = simbol.lower()
    for group in CHIP_PRIORITY:
        keywords = [k.strip() for k in group.split(",")]
        for kw in keywords:
            if kw in s:
                for label, _ in CATEGORIES:
                    if label == "Semua":
                        continue
                    if kw in label.lower():
                        return label
                return group
    return "Lainnya"

def parse_hazards(simbol):
    s = simbol.lower()
    found = []
    for keyword, label, color, icon in HAZARD_MAP:
        if keyword in s:
            found.append((label, color, icon))
    if not found:
        found.append((simbol, "#6c757d", "🏷️"))
    return found

def render_hazard_diamonds(simbol):
    hazards = parse_hazards(simbol)
    parts = []
    for label, color, icon in hazards:
        parts.append(
            f'<div class="hazard-diamond" style="background-color:{color}">'
            f'<div class="hazard-inner"><span class="hazard-icon">{icon}</span>'
            f'<span class="hazard-label">{label}</span></div></div>'
        )
    return '<div class="hazard-row">' + "".join(parts) + "</div>"

def get_badge_style(simbol):
    simbol_lower = simbol.lower()
    color = "#6c757d"
    icon = "🏷️"
    for key, clr in BADGE_COLORS.items():
        if key in simbol_lower:
            color = clr
            break
    for key, icn in SIMBOL_ICONS.items():
        if key in simbol_lower:
            icon = icn
            break
    return f'<span style="background-color:{color};color:white;padding:3px 10px;border-radius:10px;font-size:0.78rem;font-weight:600;white-space:nowrap">{icon} {simbol}</span>'

def render_detail_card(label, value, icon, color="#0d6efd", delay="0s"):
    st.markdown(
        f"""
        <div class="detail-card" style="animation-delay:{delay};background:white;border:1px solid #e0e0e0;border-radius:14px;
                    padding:18px 20px;border-left:5px solid {color};box-shadow:0 2px 8px rgba(0,0,0,0.05);height:100%">
            <div style="font-size:0.72rem;color:#6c757d;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:6px;font-weight:600">
                {icon} {label}
            </div>
            <div style="font-size:1.05rem;font-weight:600;color:#212529;word-wrap:break-word">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def filter_and_sort(query, category, sort_order):
    if query:
        q = query.lower()
        hasil = {n: d for n, d in senyawa_data.items()
                 if q in n.lower() or q in d["rumus"].lower()}
    else:
        hasil = dict(senyawa_data)

    if category and category != "Semua":
        hasil = {n: d for n, d in hasil.items() if assign_category(d["simbol_bahaya"]) == category}

    items = list(hasil.items())
    if sort_order == "A-Z":
        items.sort(key=lambda x: x[0].lower())
    else:
        items.sort(key=lambda x: x[0].lower(), reverse=True)
    return dict(items)

st.markdown("""
<style>
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    @keyframes slideDown {
        from { opacity: 0; max-height: 0; }
        to { opacity: 1; max-height: 800px; }
    }
    @keyframes glow {
        0% { box-shadow: 0 0 5px rgba(74,144,217,0.3); }
        50% { box-shadow: 0 0 20px rgba(74,144,217,0.5); }
        100% { box-shadow: 0 0 5px rgba(74,144,217,0.3); }
    }

    .main-header {
        background: linear-gradient(-45deg, #1e3a5f, #2d6a9f, #4a90d9, #2d6a9f, #1e3a5f);
        background-size: 400% 400%;
        animation: gradientShift 8s ease infinite;
        padding: 24px 32px;
        border-radius: 16px;
        margin-bottom: 24px;
        color: white;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
    }
    .main-header::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.05) 1px, transparent 1px);
        background-size: 30px 30px;
        pointer-events: none;
        animation: fadeIn 2s ease;
    }
    .main-header h1 {
        margin: 0;
        font-size: 1.8rem;
        font-weight: 700;
        position: relative;
        z-index: 1;
        animation: fadeInUp 0.6s ease;
    }
    .main-header p {
        margin: 4px 0 0 0;
        opacity: 0.85;
        font-size: 0.95rem;
        position: relative;
        z-index: 1;
        animation: fadeInUp 0.6s ease 0.1s both;
    }

    section[data-testid="stSidebar"] {
        background: #f8f9fa;
        animation: fadeIn 0.5s ease;
    }
    section[data-testid="stSidebar"] .stMarkdown h3 {
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #6c757d;
    }

    .detail-card {
        animation: fadeInUp 0.5s ease both;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .detail-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.1) !important;
    }

    div[data-testid="stRadio"] > label { display: none !important; }
    div[data-testid="stRadio"] div[role="radiogroup"] {
        max-height: 420px;
        overflow-y: auto;
        gap: 4px;
    }
    div[data-testid="stRadio"] div[role="radiogroup"]::-webkit-scrollbar { width: 4px; }
    div[data-testid="stRadio"] div[role="radiogroup"]::-webkit-scrollbar-thumb { background: #ccc; border-radius: 4px; }
    div[data-testid="stRadio"] div[role="radiogroup"] label {
        background: white;
        border: 1px solid #e8e8e8;
        border-radius: 10px;
        padding: 8px 12px !important;
        margin: 0;
        transition: all 0.25s ease;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
        display: flex !important;
        align-items: center;
        gap: 8px;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
        border-color: #4a90d9;
        box-shadow: 0 2px 12px rgba(74,144,217,0.18);
        transform: translateX(3px);
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label[data-checked="true"] {
        border-color: #4a90d9;
        background: #f0f7ff;
        box-shadow: 0 2px 12px rgba(74,144,217,0.25);
        animation: glow 1.5s ease-in-out infinite;
    }

    .footer {
        margin-top: 48px;
        padding: 16px 24px;
        background: #f8f9fa;
        border-radius: 12px;
        text-align: center;
        color: #6c757d;
        font-size: 0.85rem;
        border: 1px solid #e8e8e8;
        animation: fadeIn 0.8s ease;
    }
    .no-results {
        text-align: center;
        padding: 32px 16px;
        color: #6c757d;
        animation: fadeInUp 0.5s ease;
    }
    .no-results .big-icon { font-size: 3rem; margin-bottom: 8px; animation: pulse 2s ease infinite; }

    .compound-header {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        animation: fadeInUp 0.4s ease;
    }
    .compound-header h2 { margin: 0; font-size: 1.5rem; color: #1e3a5f; }

    .grid-card {
        background: white;
        border: 1px solid #e8e8e8;
        border-radius: 14px;
        padding: 16px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        cursor: pointer;
        animation: fadeInUp 0.5s ease both;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 6px;
    }
    .grid-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
        border-color: #4a90d9;
    }
    .grid-card:active {
        transform: translateY(-2px);
    }
    .grid-card .gc-name {
        font-weight: 700;
        font-size: 0.95rem;
        color: #212529;
        line-height: 1.3;
    }
    .grid-card .gc-formula {
        font-size: 0.8rem;
        color: #6c757d;
        font-family: monospace;
    }
    .grid-card .gc-badge {
        margin-top: 4px;
    }

    .grid-section-title {
        font-size: 0.85rem;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
        margin-bottom: 12px;
        margin-top: 8px;
        animation: fadeIn 0.5s ease;
    }

    .chip-btn {
        font-size: 0.75rem !important;
        padding: 2px 10px !important;
        border-radius: 20px !important;
        transition: all 0.25s ease !important;
    }
    .chip-btn:hover {
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .chip-active {
        box-shadow: 0 0 0 2px #4a90d9 !important;
        transform: scale(1.02);
    }

    .stButton button {
        transition: all 0.25s ease !important;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    .badge-row {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin: 6px 0;
    }

    .hazard-row {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        align-items: center;
        justify-content: center;
    }
    .hazard-diamond {
        width: 64px;
        height: 64px;
        transform: rotate(45deg);
        border-radius: 8px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.25);
        transition: all 0.3s ease;
        animation: fadeInUp 0.5s ease both;
        position: relative;
    }
    .hazard-diamond:hover {
        transform: rotate(45deg) scale(1.12);
        box-shadow: 0 5px 20px rgba(0,0,0,0.35);
    }
    .hazard-inner {
        transform: rotate(-45deg);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        line-height: 1.1;
    }
    .hazard-icon {
        font-size: 1.4rem;
    }
    .hazard-label {
        font-size: 0.45rem;
        color: white;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.3px;
        margin-top: 1px;
        text-align: center;
        max-width: 56px;
        line-height: 1.2;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🧪 Klasifikasi 100 Senyawa Kimia + Pencarian</h1>
    <p>Database keselamatan dan karakteristik 100 senyawa kimia laboratorium — Cari, filter, dan pelajari</p>
</div>
""", unsafe_allow_html=True)

if "filter_cat" not in st.session_state:
    st.session_state.filter_cat = "Semua"
if "sort_order" not in st.session_state:
    st.session_state.sort_order = "A-Z"
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "List"
if "selected" not in st.session_state:
    st.session_state.selected = list(senyawa_data.keys())[0]

col_sidebar, col_main = st.columns([0.32, 0.68], gap="large")

with col_sidebar:
    st.markdown("### 🔍 Pencarian")
    query = st.text_input(
        "Cari berdasarkan nama atau rumus",
        placeholder="Ketik nama atau rumus...",
        label_visibility="collapsed"
    ).strip()

    st.markdown("### 🏷️ Filter Kategori")
    chip_cols = st.columns(4)
    cat_labels = [c[0] for c in CATEGORIES]
    for i, label in enumerate(cat_labels):
        with chip_cols[i % 4]:
            is_active = st.session_state.filter_cat == label
            if st.button(
                label,
                key=f"chip_{label}",
                use_container_width=True,
                type="secondary" if not is_active else "primary"
            ):
                st.session_state.filter_cat = label

    st.markdown("### ⚙️ Pengaturan")
    col_s1, col_s2 = st.columns([1, 1])
    with col_s1:
        if st.button("📋 List", use_container_width=True,
                     type="primary" if st.session_state.view_mode == "List" else "secondary"):
            st.session_state.view_mode = "List"
    with col_s2:
        if st.button("🗂️ Grid", use_container_width=True,
                     type="primary" if st.session_state.view_mode == "Grid" else "secondary"):
            st.session_state.view_mode = "Grid"

    col_s3, col_s4 = st.columns([1, 1])
    with col_s3:
        sort_btn_label = "🔤 A-Z" if st.session_state.sort_order == "A-Z" else "🔤 Z-A"
        if st.button(sort_btn_label, use_container_width=True):
            st.session_state.sort_order = "Z-A" if st.session_state.sort_order == "A-Z" else "A-Z"
    with col_s4:
        if st.button("🎲 Acak", use_container_width=True):
            all_keys = list(senyawa_data.keys())
            st.session_state.selected = random.choice(all_keys)

    hasil = filter_and_sort(query, st.session_state.filter_cat, st.session_state.sort_order)

    if st.session_state.view_mode == "List":
        st.markdown("### 📋 Daftar Senyawa")
        st.markdown(
            f"<div style='font-size:0.78rem;color:#6c757d;margin-bottom:6px'>"
            f"{'Menampilkan ' + str(len(hasil)) + ' senyawa' if query or st.session_state.filter_cat != 'Semua' else 'Semua (100)'}</div>",
            unsafe_allow_html=True
        )

        if not hasil:
            st.markdown("""
            <div class="no-results">
                <div class="big-icon">🔬</div>
                <div style="font-size:1.1rem;font-weight:600;color:#495057">Senyawa tidak ditemukan</div>
                <div style="font-size:0.85rem;margin-top:4px">Coba kata kunci atau filter lain</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            nama_list = list(hasil.keys())
            prev_sel = st.session_state.selected
            if prev_sel not in nama_list:
                st.session_state.selected = nama_list[0]

            selected = st.radio(
                "Pilih senyawa",
                options=nama_list,
                format_func=lambda x: f"{x} ({hasil[x]['rumus']})",
                label_visibility="collapsed",
                index=nama_list.index(st.session_state.selected) if st.session_state.selected in nama_list else 0
            )
            st.session_state.selected = selected
    else:
        st.markdown(
            f"<div style='font-size:0.78rem;color:#6c757d;margin-bottom:6px'>"
            f"{'Menampilkan ' + str(len(hasil)) + ' senyawa' if query or st.session_state.filter_cat != 'Semua' else 'Semua (100)'}"
            f" — Klik card untuk lihat detail</div>",
            unsafe_allow_html=True
        )
        if not hasil:
            st.markdown("""
            <div class="no-results">
                <div class="big-icon">🔬</div>
                <div style="font-size:1.1rem;font-weight:600;color:#495057">Senyawa tidak ditemukan</div>
                <div style="font-size:0.85rem;margin-top:4px">Coba kata kunci atau filter lain</div>
            </div>
            """, unsafe_allow_html=True)

with col_main:
    selected_name = st.session_state.selected

    if st.session_state.view_mode == "List":
        if selected_name and selected_name in senyawa_data:
            data = senyawa_data[selected_name]
            hazard_html = render_hazard_diamonds(data["simbol_bahaya"])

            st.markdown(
                f"""
                <div class="compound-header">
                    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px">
                        <div>
                            <h2>{selected_name}</h2>
                            <div style="font-size:1rem;color:#6c757d;font-family:monospace;margin-top:2px">{data['rumus']}</div>
                        </div>
                        <div>{hazard_html}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            c1, c2, c3 = st.columns(3)
            with c1:
                render_detail_card("Wujud", data["wujud"], "💧", "#0d6efd", "0s")
            with c2:
                render_detail_card("Bau", data["bau"], "👃", "#198754", "0.1s")
            with c3:
                render_detail_card("Reaktivitas", data["reaktivitas"], "⚡", "#dc3545", "0.2s")

            c4, c5 = st.columns(2)
            with c4:
                hazards = parse_hazards(data["simbol_bahaya"])
                hazard_labels = ", ".join(h[0] for h in hazards)
                render_detail_card("Simbol Bahaya", hazard_labels, "⚠️", "#fd7e14", "0.3s")
            with c5:
                render_detail_card("Pengelolaan Limbah", data["pengelolaan_limbah"], "♻️", "#6f42c1", "0.4s")
        else:
            st.markdown("""
            <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:80px 20px;color:#6c757d;text-align:center">
                <div style="font-size:4rem;margin-bottom:16px">🧪</div>
                <div style="font-size:1.3rem;font-weight:600">Pilih senyawa dari daftar</div>
                <div style="font-size:0.9rem;margin-top:4px">Gunakan pencarian di sidebar untuk menemukan senyawa</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="grid-section-title">🗂️ Grid Senyawa</div>', unsafe_allow_html=True)

        if hasil:
            items = list(hasil.items())
            grid_cols = st.columns(4)
            for idx, (nama, data) in enumerate(items):
                with grid_cols[idx % 4]:
                    is_sel = st.session_state.get("selected") == nama
                    hazard_html = render_hazard_diamonds(data["simbol_bahaya"])
                    label = f"{nama}\n{data['rumus']}"
                    btn_type = "primary" if is_sel else "secondary"
                    if st.button(label, key=f"g{idx}", use_container_width=True, type=btn_type):
                        st.session_state.selected = nama
                    st.markdown(
                        f"<div style='text-align:center;margin-top:-8px;margin-bottom:8px'>{hazard_html}</div>",
                        unsafe_allow_html=True
                    )

            if selected_name and selected_name in senyawa_data:
                st.markdown("<hr style='margin:28px 0 20px 0'>", unsafe_allow_html=True)
                data = senyawa_data[selected_name]
                hazard_html = render_hazard_diamonds(data["simbol_bahaya"])

                st.markdown(
                    f"""
                    <div class="compound-header">
                        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px">
                            <div>
                                <h2>{selected_name}</h2>
                                <div style="font-size:1rem;color:#6c757d;font-family:monospace;margin-top:2px">{data['rumus']}</div>
                            </div>
                            <div>{hazard_html}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                c1, c2, c3 = st.columns(3)
                with c1:
                    render_detail_card("Wujud", data["wujud"], "💧", "#0d6efd", "0s")
                with c2:
                    render_detail_card("Bau", data["bau"], "👃", "#198754", "0.1s")
                with c3:
                    render_detail_card("Reaktivitas", data["reaktivitas"], "⚡", "#dc3545", "0.2s")

                c4, c5 = st.columns(2)
                with c4:
                    hazards = parse_hazards(data["simbol_bahaya"])
                    hazard_labels = ", ".join(h[0] for h in hazards)
                    render_detail_card("Simbol Bahaya", hazard_labels, "⚠️", "#fd7e14", "0.3s")
                with c5:
                    render_detail_card("Pengelolaan Limbah", data["pengelolaan_limbah"], "♻️", "#6f42c1", "0.4s")
        else:
            st.markdown("""
            <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:60px 20px;color:#6c757d;text-align:center">
                <div style="font-size:3rem;margin-bottom:12px">🔬</div>
                <div style="font-size:1.1rem;font-weight:600;color:#495057">Tidak ada hasil</div>
                <div style="font-size:0.85rem;margin-top:4px">Sesuaikan pencarian atau filter</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    <div style="font-weight:600;margin-bottom:4px">📚 Sumber Data</div>
    <div>Database karakteristik 100 senyawa kimia laboratorium — Data keselamatan, sifat fisika, dan penanganan limbah B3</div>
    <div style="margin-top:4px;font-size:0.78rem;opacity:0.7">© Klasifikasi Senyawa Kimia — Informasi untuk praktikum kimia dasar</div>
</div>
""", unsafe_allow_html=True)
