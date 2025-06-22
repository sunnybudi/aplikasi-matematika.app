import streamlit as st

# SET CONFIG HARUS PALING ATAS
st.set_page_config(page_title="Aplikasi Matematika Industri", layout="centered")

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import sympy as sp
import math

# =========================
# SIDEBAR - PETUNJUK
# =========================
st.sidebar.title("\U0001F4D8 Petunjuk Penggunaan")
st.sidebar.markdown("""
Aplikasi ini memiliki 5 model matematika industri:

1. **Optimasi Produksi**
2. **Model Persediaan EOQ**  
3. **Model Antrian (M/M/1)**  
4. **Model Lain** 
5. **Turunan Parsial** 

Masukkan data sesuai tab. Hasil & grafik akan muncul secara otomatis.
""")

# =========================
# TAB UTAMA
# =========================
st.title("\U0001F4CA Aplikasi Matematika Terapan")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1. Optimasi Produksi",
    "2. Model Persediaan (EOQ)",
    "3. Model Antrian (M/M/1)",
    "4. Model Lain",
    "5. Turunan Parsial"
])

# ================================================
# TAB 1: Optimasi Produksi (Linear Programming)
# ================================================

with tab1:
    st.header("1️⃣ Optimasi Produksi (Linear Programming)")
    st.markdown("""
    ### 🔧 Studi Kasus
    PT Kreasi Untung Indonesia yang merupakan sebuah perusahaan furnitur memproduksi **Meja (X)** dan **Kursi (Y)**. 
    Untuk mengetahui berapa banyak penjualan dan keuntungan pada hasil produksi, pemiliknya menggunakan perhitungan 
    matematika dengan rumus:
    """)

    st.latex(r"Z = c₁X + c₂Y")
    st.markdown("### 📘 Keterangan Notasi Model Optimasi Produksi:")
    st.markdown(r"""
    - $Z$  = Total biaya atau total keuntungan  
    - $c₁$ = Biaya atau keuntungan per unit X  
    - $c₂$ = Biaya atau keuntungan per unit Y  
    - $X$  = Jumlah unit produk (misal: Meja)  
    - $Y$  = Jumlah unit produk (misal: Kursi)
    """)

    # ===============================
    # Input Harga dan Keuntungan
    # ===============================
    st.markdown("### Harga Jual dan Keuntungan per Unit")
    col1, col2= st.columns(2)
    with col1:
        x = st.number_input("Jumlah Produksi Meja (X)", value=0)
        laba_meja = st.number_input("Keuntungan per Meja (c₁)", value=0)
        harga_meja = st.number_input("Harga Jual Meja", value=0)
    with col2:
        y = st.number_input("Jumlah Produksi Kursi (Y)", value=0)
        laba_kursi = st.number_input("Keuntungan per Kursi (c₂)", value=0)
        harga_kursi = st.number_input("Harga Jual Kursi", value=0)

    if all([laba_meja, laba_kursi, x, y]):
        Z = laba_meja * x + laba_kursi * y
    
        st.subheader("🧮 Perhitungan Berdasarkan Input")
        st.latex(rf"""
        \begin{{align*}}
        Z &= c_1 \cdot X + c_2 \cdot Y \\
          &= {laba_meja} \cdot {x} + {laba_kursi} \cdot {y} \\
          &= {Z:,.0f}
        \end{{align*}}
        """)

    # Hitung biaya produksi dari selisih harga dan keuntungan
    biaya_meja = harga_meja - laba_meja
    biaya_kursi = harga_kursi - laba_kursi
    
    # ===============================
    # Fungsi Format Rupiah
    # ===============================
    def format_rupiah(nilai):
        return f"Rp {nilai:,.0f}".replace(",", ".")

    # ===============================
    # Perhitungan Fungsi Tujuan Z
    # ===============================
    z1 = laba_meja * x + laba_kursi *y
    z2 = laba_meja * x
    z3 = laba_kursi * y

    st.markdown("### 🔎 Hasil Fungsi Tujuan Z:")
    st.write(f"Z({x}, {y}) = {format_rupiah(z1)}")
    st.write(f"Z({x}, 0) = {format_rupiah(z2)}")
    st.write(f"Z(0, {y}) = {format_rupiah(z3)}")

    z_opt = max(z1, z2, z3)
    if z_opt == z2:
        solusi = f"(0, {x})"
    elif z_opt == z3:
        solusi = f"({y}, 0)"
    else:
        solusi = "(0, 0)"

    # ===============================
    # Total Penjualan dan Keuntungan
    # ===============================
    st.markdown("### 💰 Ringkasan Total Penjualan")

    total_penjualan_meja = harga_meja * x
    total_penjualan_kursi = harga_kursi * y
    total_penjualan = total_penjualan_meja + total_penjualan_kursi

    st.write(f"🪑 Penjualan Meja (X): {format_rupiah(total_penjualan_meja)}")
    st.write(f"🪑 Penjualan Kursi (Y): {format_rupiah(total_penjualan_kursi)}")
    st.write(f"📊 Total Penjualan: {format_rupiah(total_penjualan)}")

    # ===============================
    # Total Biaya Produksi & Laba Bersih
    # ===============================
    st.markdown("### 🧾 Total Keuntungan Bersih")

    total_biaya_meja = biaya_meja * x
    total_biaya_kursi = biaya_kursi * y
    total_biaya_produksi = total_biaya_meja + total_biaya_kursi

    total_laba_meja = laba_meja * x
    total_laba_kursi = laba_kursi * y
    total_keuntungan_bersih = total_laba_meja + total_laba_kursi

    st.write(f"🔹 Keuntungan Meja (X): {format_rupiah(z2)}")
    st.write(f"🔹 Keuntungan Kursi (Y): {format_rupiah(z3)}")
    st.write(f"✅ Total Keuntungan Bersih: {format_rupiah(z2 + z3)}")

    # ===============================
    # Grafik Perbandingan (Diagram Batang Vertikal)
    # ===============================
    st.markdown("### 📊 Diagram Perbandingan Penjualan dan Keuntungan")
    
    # Data per kategori
    kategori = ['Meja (X)', 'Kursi (Y)', 'Total']
    penjualan = [total_penjualan_meja, total_penjualan_kursi, total_penjualan]
    keuntungan = [total_laba_meja, total_laba_kursi, total_keuntungan_bersih]
    
    # Grafik
    x_pos = np.arange(len(kategori))
    width = 0.35
    fig2, ax2 = plt.subplots()
    
    # Buat batang grafik
    bar1 = ax2.bar(x_pos - width/2, keuntungan, width=width, color='skyblue', label='Keuntungan')
    bar2 = ax2.bar(x_pos + width/2, penjualan, width=width, color='lightgreen', label='Penjualan')
    
    # Gabungan semua nilai untuk menentukan batas Y
    values = penjualan + keuntungan
    max_val = max(values)
    ax2.set_ylim(0, max_val * 1.3)  # Ruang ekstra di atas grafik
    
    # Label angka tetap (tidak menempel batang)
    for bars in [bar1, bar2]:
        for bar in bars:
            value = bar.get_height()
            text = f"{value:,.0f}".replace(",", ".")
            ax2.text(
                bar.get_x() + bar.get_width() / 2,
                value + (max_val * 0.03),  # Jarak 3% dari tinggi maksimal
                text,
                ha='center', va='bottom',
                fontsize=10,
                color='black',
                fontweight='bold'
            )
    
    # Pengaturan axis dan label
    ax2.set_ylabel("Rupiah", fontsize=10)
    ax2.set_xlabel("Kategori Produk", fontsize=10)
    ax2.set_title("Perbandingan Penjualan dan Keuntungan", fontsize=12)
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(kategori, fontsize=10)
    ax2.legend(fontsize=10)
    
    # Format angka di sumbu Y
    ax2.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'.replace(",", ".")))
    
    plt.tight_layout()
    st.pyplot(fig2)

# =========================
# TAB 2: EOQ
# =========================
with tab2:
    st.header("📦 Model Persediaan EOQ")
    st.markdown("""
        ### 🔧 Studi Kasus
        PT Kreasi Untung Indonesia yang merupakan sebuah perusahaan furnitur memproduksi Meja dan Kursi. 
        Pihak manajemen ingin mengetahui berapa banyak lembar kayu yang sebaiknya dipesan pada setiap batch 
        order untuk menghemat biaya total persediaan.
        """)


    st.subheader("📐 Rumus-Rumus:")
    st.latex(r"""
    \begin{aligned}
    \textbf{EOQ} &= \sqrt{\frac{2DS}{H}} \\
    \textbf{N} &= \frac{D}{EOQ} \\
    \textbf{T} &= \frac{365}{\text{N}}
    \end{aligned}
    """)

    
    st.markdown("""Keterangan""")
    st.latex(f"""
    \\begin{{array}}{{lcl}}
    \\text{{EOQ}} & = & \\text{{Economic Order Quantity (jumlah pemesanan ekonomis)}} \\\\
    \\text{{D}}   & = & \\text{{Demand (jumlah kebutuhan / tuntutan barang per tahun)}} \\\\
    \\text{{S}}   & = & \\text{{Ordering Cost (biaya pemesanan per pesanan)}} \\\\
    \\text{{H}}   & = & \\text{{Holding Cost (biaya penyimpanan per unit per tahun)}} \\\\
    \\text{{N}}   & = & \\text{{Frekuensi pemesanan}} \\\\
    \\text{{T}}   & = & \\text{{Interval pemesanan}}
    \\end{{array}}
    """)
  
    D = st.number_input("📅 Permintaan Tahunan (D/unit)", value=0)
    S = st.number_input("🛒 Biaya Pemesanan per Order (S/Rp)", value=0)
    H = st.number_input("🏬 Biaya Penyimpanan per Unit per Tahun (H/Rp)", value=0)

    if D > 0 and S > 0 and H > 0:
        EOQ = math.sqrt((2 * D * S) / H)
        freq = D / EOQ
        cycle_days = 365 / freq

    if D > 0 and S > 0 and H > 0:
        try:
            EOQ = math.sqrt((2 * D * S) / H)
            N = D / EOQ
            T = 365 / N  # diasumsikan 1 tahun = 365 hari
    
            st.subheader("🧮 Perhitungan Berdasarkan Input")
            st.latex(rf"""
            \begin{{align*}}
            \text{{EOQ}} &= \sqrt{{\frac{{2DS}}{{H}}}} = \sqrt{{\frac{{2 \cdot {D} \cdot {S}}}{{{H}}}}} = \boxed{{\displaystyle {EOQ:.2f}}} \\
            N &= \frac{{D}}{{EOQ}} = \frac{{{D}}}{{{EOQ:.2f}}} = \boxed{{\displaystyle {N:.2f}}} \\
            T &= \frac{{365}}{{N}} = \frac{{365}}{{{N:.2f}}} = \boxed{{\displaystyle {T:.2f}}}~\text{{hari}}
            \end{{align*}}
            """)


 
        except:
            st.error("Pastikan semua input terisi dan nilai H ≠ 0")

        st.success(
            f"""
            EOQ: {EOQ:.2f} unit\\
            N: {freq:.2f} kali/tahun\\
            T: {cycle_days:.0f} hari
            """
        )

        st.markdown("### 📊 Diagram EOQ dan Permintaan Tahunan")
        fig, ax = plt.subplots()
        labels = ["Permintaan", "EOQ"]
        values = [D, EOQ]
        colors = ['red', 'green']
        
        bars = ax.bar(labels, values, color=colors)
        ax.set_ylabel("Jumlah Unit")
        ax.set_title("EOQ dan Permintaan Tahunan")
        
        # Tambahkan nilai di atas tiap batang
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,  # posisi tengah batang
                height + 0 * max(values),        # sedikit di atas batang
                f"{height:.2f}",                    # format angka
                ha='center', va='bottom', fontsize=10, fontweight='bold'
            )
        
        st.pyplot(fig)

# =========================
# TAB 3: Model Antrian (M/M/1)
# =========================
with tab3:
    st.header("3️⃣ Model Antrian (M/M/1)")
    st.markdown("""
        ### 🔧 Studi Kasus
        PT Kreasi Untung Indonesia yang merupakan sebuah perusahaan furnitur memproduksi Meja dan Kursi. 
        Perusahaan menginginkan semua aktivitas pembelian dialihkan ke website, maka dari itu diperlukan aplikasi
        untuk memantau proses pembelian di server web perusahaan.
    """)

    # Tampilkan Rumus Umum Sebelum Input
    st.subheader("📘 Rumus-Rumus Umum Model M/M/1")
    st.latex(r"""
    \begin{align*}
    \rho &= \frac{\lambda}{\mu} \\
    L &= \frac{\lambda}{\mu - \lambda} \\
    L_q &= \frac{\lambda^2}{\mu(\mu - \lambda)} \\
    W &= \frac{1}{\mu - \lambda} \\
    W_q &= \frac{\lambda}{\mu(\mu - \lambda)} \\
    P_0 &= 1 - \rho
    \end{align*}
    """)

    st.markdown("**📘 Keterangan Simbol Model M/M/1**")
    st.latex(r"""
    \begin{array}{rcl}
    \lambda & : & \text{Tingkat kedatangan pelanggan per satuan waktu (misalnya per jam)} \\
    \mu & : & \text{Tingkat pelayanan pelanggan per satuan waktu} \\
    \rho & : & \text{Utilisasi server, yaitu } \rho = \frac{\lambda}{\mu} \\
    L & : & \text{Rata-rata jumlah pelanggan dalam sistem (antrian + dilayani)} \\
    L_q & : & \text{Rata-rata jumlah pelanggan dalam antrian} \\
    W & : & \text{Waktu rata-rata pelanggan berada dalam sistem} \\
    W_q & : & \text{Waktu rata-rata pelanggan dalam antrian} \\
    P_0 & : & \text{Probabilitas sistem kosong (tidak ada pelanggan)} \\
    P_n & : & \text{Probabilitas terdapat } n \text{ pelanggan dalam sistem}
    \end{array}
    """)





    # Input parameter
    col1, col2 = st.columns(2)
    with col1:
        lambd = st.number_input("📥 Tingkat Kedatangan (λ) - pelanggan/jam", min_value=0, value=0)
    with col2:
        mu = st.number_input("⚙️ Tingkat Pelayanan (μ) - pelanggan/jam", min_value=0, value=0)

    if lambd >= mu:
        st.error("⚠️ Sistem tidak stabil (λ ≥ μ). Harap pastikan λ < μ.")
    else:
        # Perhitungan
        rho = lambd / mu
        L = lambd / (mu - lambd)
        Lq = (lambd ** 2) / (mu * (mu - lambd))
        W = 1 / (mu - lambd)
        Wq = lambd / (mu * (mu - lambd))
        P0 = 1 - rho

        # Tampilkan Rumus Dengan Nilai
        st.subheader("🧮 Perhitungan Berdasarkan Input")
        st.latex(rf"""
        \begin{{align*}}
        \rho &= \frac{{\lambda}}{{\mu}} = \frac{{{lambd}}}{{{mu}}} = {rho:.3f} \\
        L &= \frac{{\lambda}}{{\mu - \lambda}} = \frac{{{lambd}}}{{{mu - lambd}}} = {L:.3f} \\
        L_q &= \frac{{\lambda^2}}{{\mu(\mu - \lambda)}} = \frac{{{lambd}^2}}{{{mu}({mu - lambd})}} = {Lq:.3f} \\
        W &= \frac{{1}}{{\mu - \lambda}} = \frac{{1}}{{{mu - lambd}}} = {W:.3f} \\
        W_q &= \frac{{\lambda}}{{\mu(\mu - \lambda)}} = \frac{{{lambd}}}{{{mu}({mu - lambd})}} = {Wq:.3f} \\
        P_0 &= 1 - \rho = 1 - {rho:.3f} = {P0:.3f}
        \end{{align*}}
        """)

        # Grafik Ringkasan
        st.subheader("📊 Grafik Ringkasan")
        labels = ["ρ", "L", "Lq", "W", "Wq"]
        values = [rho, L, Lq, W, Wq]

        fig, ax = plt.subplots()
        bars = ax.bar(labels, values, color=['skyblue', 'orange', 'green', 'salmon', 'violet'])
        ax.set_ylim(0, max(values) * 1.2)
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f"{height:.2f}", xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom')
        ax.set_title("Ringkasan Parameter Antrian M/M/1")
        ax.set_ylabel("Nilai")
        st.pyplot(fig)

        # Hasil Perhitungan Teks
        st.subheader("📈 Hasil Perhitungan")
        st.markdown(f"""
        - **Tingkat Utilisasi (ρ):** {rho:.3f}
        - **Rata-rata pelanggan dalam sistem (L):** {L:.3f}
        - **Rata-rata dalam antrean (Lq):** {Lq:.3f}
        - **Waktu dalam sistem (W):** {W:.3f} jam ≈ {W*60:.0f} menit
        - **Waktu tunggu dalam antrean (Wq):** {Wq:.3f} jam ≈ {Wq*60:.0f} menit
        - **Probabilitas sistem kosong (P₀):** {P0:.3f}
        """)

        # Grafik Distribusi Pn
        st.subheader("📉 Distribusi Probabilitas Pn (Pelanggan ke-n)")
        n_vals = np.arange(0, 20)
        Pn_vals = (1 - rho) * rho ** n_vals

        fig2, ax2 = plt.subplots()
        ax2.bar(n_vals, Pn_vals, color='cornflowerblue')
        ax2.set_xlabel("n (jumlah pelanggan)")
        ax2.set_ylabel("P(n)")
        ax2.set_title("Distribusi Probabilitas Pelanggan dalam Sistem")
        st.pyplot(fig2)

# ===================================
# TAB 4: Perhitungan untung dan rugi
# ===================================
with tab4:
    st.header("💱 Konversi Mata Uang untuk kalkulasi Untung dan Rugi")
    st.markdown("""
        ### 🔧 Studi Kasus
        PT Kreasi Untung Indonesia yang merupakan sebuah perusahaan furnitur memproduksi Meja dan Kursi. 
        Perusahaan saat ini memulai ekspand bisnis baru ke luar negeri. Karena itu perusahaan membutuhkan aplikasi
        matematika untuk menghitung untung dan rugi ketika mata uangnya dikonversikan.
    """)

    # Rumus-Rumus Umum
    st.markdown("### 📐 Rumus-Rumus Terkait")
    st.latex(r"""
    \begin{align*}
    \text{Konversi USD ke Rupiah:} &\quad \text{Harga Modal Rp} = \text{Harga USD} \times \text{Kurs} \\
    \text{Konversi Rupiah ke USD:} &\quad \text{Harga Modal USD} = \frac{\text{Harga Rp}}{\text{Kurs}} \\
    \text{Untung/Rugi:} &\quad \text{Selisih} = \text{Harga Jual} - \text{Harga Modal} \\
    \text{Persentase Untung/Rugi:} &\quad \frac{\text{Selisih}}{\text{Harga Modal}} \times 100
    \end{align*}
    """)

    # Keterangan Notasi
    st.markdown("### 📘 Keterangan Notasi")
    st.markdown(r"""
    - $Kurs$               = Nilai tukar Rupiah terhadap USD
    - $Harga Modal (USD)$  = Nilai modal barang dari luar negeri
    - $Harga Modal (Rp)$   = Nilai konversi ke mata uang lokal
    - $Harga Jual$         = Harga jual yang ditargetkan
    - $Untung/Rugi$        = Selisih harga jual - harga beli
    - $Persentase$         = (Selisih / Harga Beli) × 100
    """)

    colx1, colx2 = st.columns(2)
    with colx1:
        arah_konversi = st.selectbox("Arah Konversi Mata Uang", ["USD → Rupiah", "Rupiah → USD"])
    with colx2:
        default_kurs = 16000 if arah_konversi == "USD → Rupiah" else 1
        kurs = st.number_input("Kurs (Rp per USD)", min_value=0, step=100, value=default_kurs)

    col1, col2 = st.columns(2)
    if arah_konversi == "USD → Rupiah":
        with col1:
            harga_usd = st.number_input("Harga Modal (USD)", min_value=0, step=1)
        with col2:
            harga_jual_rp = st.number_input("Harga Jual (Rp)", min_value=0, step=1000)

        if harga_usd > 0 and harga_jual_rp > 0 and kurs > 0:
            harga_beli_rp = harga_usd * kurs
            selisih = harga_jual_rp - harga_beli_rp
            persen = (selisih / harga_beli_rp) * 100

            hasil_text = "Untung" if selisih > 0 else "Rugi"
            st.success(f"{hasil_text}: Rp {abs(selisih):,.2f} ({abs(persen):.2f}%)")

            st.subheader("🧮 Perhitungan")
            st.latex(rf"""
            \begin{{align*}}
            \text{{Harga Modal (Rp)}} &= {harga_usd} \times {kurs} = {harga_beli_rp:,.2f} \\
            \text{{{hasil_text}}} &= {harga_jual_rp:,.0f} - {harga_beli_rp:,.2f} = {selisih:,.2f} \\
            \text{{Persentase}} &= \frac{{{selisih:,.2f}}}{{{harga_beli_rp:,.2f}}} \times 100 = {persen:.2f}\%
            \end{{align*}}
            """)

            st.markdown("### 📊 Grafik Perbandingan Harga Modal vs Harga Jual (Rp)")
            fig, ax = plt.subplots(figsize=(6, 4))
            labels = ['Harga Modal (Rp)', 'Harga Jual (Rp)']
            values = [harga_beli_rp, harga_jual_rp]
            colors = ['orange', 'green' if selisih >= 0 else 'red']
            bars = ax.bar(labels, values, color=colors)
            max_val = max(values)
            ax.set_ylim(0, max_val * 1.15)

            for bar in bars:
                yval = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * max_val,
                        f"Rp {yval:,.2f}", ha='center', va='bottom', fontsize=10)

            ax.set_ylabel("Rupiah")
            ax.set_title("Perbandingan Harga Modal dan Harga Jual")
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'.replace(",", ".")))
            plt.tight_layout()
            st.pyplot(fig)

    else:  # Rupiah → USD
        with col1:
            harga_beli_rp = st.number_input("Harga Modal (Rp)", min_value=0, step=1000)
        with col2:
            harga_jual_usd = st.number_input("Harga Jual (USD)", min_value=0, step=1)

        if kurs > 0 and harga_beli_rp > 0 and harga_jual_usd > 0:
            harga_beli_usd = harga_beli_rp / kurs
            selisih_usd = harga_jual_usd - harga_beli_usd
            persen = (selisih_usd / harga_beli_usd) * 100

            hasil_text = "Untung" if selisih_usd > 0 else "Rugi"
            st.success(f"{hasil_text}: USD {abs(selisih_usd):,.2f} ({abs(persen):,.2f}%)")

            st.subheader("🧮 Perhitungan")
            st.latex(rf"""
            \begin{{align*}}
            \text{{Harga Modal (USD)}} &= \frac{{{harga_beli_rp:,.0f}}}{{{kurs:,.0f}}} = {harga_beli_usd:,.2f} \\
            \text{{{hasil_text}}} &= {harga_jual_usd:,.2f} - {harga_beli_usd:,.2f} = {selisih_usd:,.2f} \\
            \text{{Persentase}} &= \frac{{{selisih_usd:,.2f}}}{{{harga_beli_usd:,.2f}}} \times 100 = {persen:.2f}\%
            \end{{align*}}
            """)

            st.markdown("### 📊 Grafik Perbandingan Harga Modal vs Harga Jual (USD)")
            fig, ax = plt.subplots(figsize=(6, 4))
            labels = ['Harga Modal (USD)', 'Harga Jual (USD)']
            values = [harga_beli_usd, harga_jual_usd]
            colors = ['orange', 'green' if selisih_usd >= 0 else 'red']
            bars = ax.bar(labels, values, color=colors)
            max_val = max(values)
            ax.set_ylim(0, max(values) * 1.2)

            for bar in bars:
                yval = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * max_val,
                        f"USD {yval:,.2f}", ha='center', va='bottom', fontsize=10)

            ax.set_ylabel("USD")
            ax.set_title("Perbandingan Harga Modal dan Harga Jual")
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.2f}'))
            plt.tight_layout()
            st.pyplot(fig)

# =========================
# TAB 5: Turunan Parsial
# =========================
with tab5:
    st.header("4️⃣ Turunan Parsial")
    x, y = sp.symbols('x y')
    fungsi = st.text_input("Masukkan f(x, y):", "x**3 + y + y**2")

    try:
        f = sp.sympify(fungsi)
        fx = sp.diff(f, x)
        fy = sp.diff(f, y)
        x0 = st.number_input("x₀:", value=1.0)
        y0 = st.number_input("y₀:", value=2.0)

        f_val = f.subs({x: x0, y: y0})
        fx_val = fx.subs({x: x0, y: y0})
        fy_val = fy.subs({x: x0, y: y0})

        st.latex(rf"f(x, y) = {sp.latex(f)}")
        st.latex(rf"\frac{{\partial f}}{{\partial x}} = {sp.latex(fx)}")
        st.latex(rf"\frac{{\partial f}}{{\partial y}} = {sp.latex(fy)}")

        st.write(f"Nilai f: {f_val}, Gradien: ({fx_val}, {fy_val})")

        X, Y = np.meshgrid(np.linspace(x0-2, x0+2, 50), np.linspace(y0-2, y0+2, 50))
        f_np = sp.lambdify((x, y), f, 'numpy')
        Z = f_np(X, Y)
        Z_tangent = float(f_val) + float(fx_val)*(X - x0) + float(fy_val)*(Y - y0)

        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)
        ax.plot_surface(X, Y, Z_tangent, color='red', alpha=0.5)
        ax.set_title("f(x, y) dan Bidang Singgung di (x₀, y₀)")
        st.pyplot(fig)
    except:
        st.error("Fungsi tidak valid. Gunakan format Python: x**2 + y**2")
