import streamlit as st
import mysql.connector
from streamlit_option_menu import option_menu
import pandas as pd

# Fungsi koneksi database


def koneksi():
    db = mysql.connector.connect(
        host="localhost", user="root", password="", database="db_kampus"
    )
    return db

# Menu Aplikasi

with st.sidebar:

    menu = option_menu(
        menu_title="Menu Aplikasi",
        options=[
            "Tambah Data",
            "Daftar Data",
            "Cari Data",
            "Kelola Data",
            "Hapus Data"
            ],
        icons=[
            "plus-circle",
            "table",
            "search",
            "database-gear",
            "trash"
            ],
        default_index=0,
    )

# Tambah Data Mahasiswa

if menu == "Tambah Data":

    # Input Data Mahasiswa

    st.title("Aplikasi Input Data Mahasiswa")
    st.subheader("Tambah Data Mahasiswa")

    nim = st.text_input("NIM")
    nama = st.text_input("Nama Mahasiswa")
    prodi = st.selectbox(
        "Program Jurusan",
        [
            "",
            "Sistem Informasi",
            "Teknik Informatika",
            "Teknologi Informasi",
            "Ilmu Komunikasi",
            "Ilmu Pemerintahan",
        ],
    )
    semester = st.number_input("Semester:", min_value=1, max_value=14, step=1)
    ipk = st.number_input("IPK", min_value=0.0, max_value=4.0, step=0.01)

    # Menyimpan data

    if st.button("Simpan Data"):
        db = koneksi()
        cursor = db.cursor()

        # Perintah query untuk memasukkan data ke dalam tabel database

        sql = """
            INSERT INTO mahasiswa
            (nim, nama, ipk, semester, prodi)
            VALUE (%s, %s, %s, %s, %s)
        """

        nilai = (nim, nama, ipk, semester, prodi)

        cursor.execute(sql, nilai)

        db.commit()

        cursor.close()
        db.close()

        st.success("Data Mahasiswa Berhasil Disimpan")

# Daftar Mahasiswa

elif menu == "Daftar Data":

    st.title("Data Mahasiswa")

    # Perintah untuk menampilkan data dari database

    st.subheader("Daftar data mahasiswa yang telah ditambahkan")
    db = koneksi()

    # query untuk menampilkan semua data yang ada di dalam tabel mahasisw

    query = "SELECT * FROM MAHASISWA"

    data = pd.read_sql(query, db)

    st.dataframe(data)
    db.close()

# Cari Data Mahasiswa

elif menu == "Cari Data":
    st.title("Cari Data Mahasiswa")

    cari = st.text_input("Masukkan NIM atau nama mahasiswa")
    
    if st.button("Cari Mahasiswa"):
        db = koneksi()
        cursor = db.cursor()

        sql = """
            SELECT * FROM mahasiswa
            where nim LIKE %s OR nama LIKE %s
        """

        nilai = ("%" + cari + "%", "%" + cari + "%")

        cursor.execute(sql, nilai)
        hasil = cursor.fetchall()

        if hasil:
            data = pd.DataFrame(
                hasil,
                columns=[i[0] for i in cursor.description]
            )
            st.success("Mahasiswa berhasil ditemukan")
            st.dataframe(
                data, 
                use_container_width=True,
                hide_index=True)
        else:
            st.warning("Mahasiswa belum ditemukan")

        cursor.close()
        db.close()

# Kelola Data

elif menu == "Kelola Data":
    st.title("Edit Data Mahasiswa")

    db = koneksi()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM mahasiswa")

    data = cursor.fetchall()

    if data:

        # mahasiswa dapat memilih data siapa yang mau dirubah berdasarkan ID
        pilihan = st.selectbox(
            "Pilih Mahasiswa",
            data,
            format_func= lambda x: str(x[1]) + " - " + str(x[2])
        )

        id_mahasiswa  = pilihan[0]

        st.write("### Form edit mahasiswa")

        # Mengambil data lama
        nim = st.text_input("NIM", value=pilihan[1])
        nama = st.text_input("Nama", value=pilihan[2])

        ipk = st.number_input(
            "IPK",
            min_value=0.0,
            max_value=4.0,
            value=float(pilihan[3]),
            step=0.01
        )

        semester = st.number_input(
            "Semester",
            min_value=1,
            max_value=14,
            value=int(pilihan[4]),
            step=1
        )

        daftar_prodi = [
            "Sistem Informasi",
            "Teknik Informatika",
            "Teknologi Informasi"
        ]

        prodi_lama = pilihan[5]

        if prodi_lama not in daftar_prodi:
            daftar_prodi.append(prodi_lama)

        prodi = st.selectbox(
            "Program Studi",
            daftar_prodi,
            index=daftar_prodi.index(prodi_lama)
        )

        if st.button("Update Data"):

            sql = """
                UPDATE mahasiswa
                SET nim=%s, nama=%s, ipk=%s,
                    semester=%s, prodi=%s
                WHERE id_mahasiswa=%s
            """

            nilai = (
                nim, nama, ipk, semester, prodi, id_mahasiswa
            )

            cursor.execute(sql, nilai)
            db.commit()

            st.success("Data mahasiswa berhasil diperbarui!")

    else:
        st.warning("Belum ada data mahasiswa.")

    cursor.close()
    db.close()


# ==================================
# 7. HAPUS DATA MAHASISWA
# ==================================

elif menu == "Hapus Data":

    st.subheader("Hapus Data Mahasiswa")

    db = koneksi()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM mahasiswa")
    data = cursor.fetchall()

    if data:

        pilihan = st.selectbox(
            "Pilih Mahasiswa yang akan dihapus",
            data,
            format_func=lambda x: str(x[1]) + " - " + str(x[2])
        )

        st.write("Data yang akan dihapus:")
        st.write("NIM:", pilihan[1])
        st.write("Nama:", pilihan[2])

        if st.button("Hapus Data"):

            sql = "DELETE FROM mahasiswa WHERE id_mahasiswa=%s"

            cursor.execute(sql, (pilihan[0],))
            db.commit()

            st.success("Data mahasiswa berhasil dihapus!")

    else:
        st.warning("Belum ada data mahasiswa.")

    cursor.close()
    db.close()

        