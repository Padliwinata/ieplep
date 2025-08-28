import datetime
from datetime import timedelta
import io

import streamlit as st
import xlsxwriter


def add_base(sheet, wb):
    header_format = wb.add_format({
        'bold': True,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#C6E0B4'
    })
    sheet.merge_range('A1:A3', 'NO.', header_format)
    sheet.merge_range('B1:B3', 'NIM', header_format)
    sheet.merge_range('C1:C3', 'NAMA', header_format)
    sheet.merge_range('D1:D3', 'KODE ASPRAK', header_format)

    sheet.set_column('A:A', 6)
    sheet.set_column('B:B', 14)
    sheet.set_column('C:C', 24)
    sheet.set_column('D:D', 14)
    sheet.freeze_panes(3, 0)


def number_to_excel_column(n: int) -> str:
    column = ""
    n += 1
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        column = chr(65 + remainder) + column
    return column


def coordinates_to_excel(x: int, y: int) -> str:
    column = number_to_excel_column(y)
    return f"{column}{x + 1}"


def generate_input_tanggal(num_kelas: int, kelas_label: str):
    list_tanggal = []
    today = datetime.date.today()
    for i in range(num_kelas):
        tgl = st.date_input(
            label=f"Tanggal Mulai Praktikum {kelas_label}-{str(i+1).zfill(2)}",
            key=f'tanggal_{kelas_label}_{i}',
            value=today
        )
        list_tanggal.append(datetime.datetime.combine(tgl, datetime.time.min))
    return list_tanggal


def create_modul(
    sheet,
    wb,
    start_date: datetime.datetime,
    tp: bool,
    test_awal: bool,
    test_akhir: bool,
    rate: bool,
    modul: int
):
    header_format = wb.add_format({
        'bold': True,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#C6E0B4'
    })
    date_format = wb.add_format({
        'bold': True,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#C6E0B4',
        'num_format': 'dd/mm/yyyy'
    })

    optional_cols = [
        ("TP", tp),
        ("JURNAL", test_awal),
        ("TES AKHIR", test_akhir),
        ("RATE", rate),
    ]
    selected_option_names = [name for name, on in optional_cols if on]
    num_option = len(selected_option_names)

    total_cols_this_module = 4 + num_option
    start_col = (modul - 1) * total_cols_this_module + 4
    modul_date = start_date + timedelta(days=(modul - 1) * 7)

    sheet.merge_range(0, start_col, 0, start_col + total_cols_this_module - 1, f"MODUL {modul}", header_format)
    sheet.merge_range(1, start_col, 1, start_col + total_cols_this_module - 1, modul_date.strftime('%d/%m/%Y'), header_format)

    col = start_col
    sheet.write_string(2, col, "KEHADIRAN ASPRAK", header_format); col += 1
    sheet.write_string(2, col, "KEHADIRAN", header_format);        col += 1
    sheet.write_string(2, col, "EVIDENCE", header_format);          col += 1

    for name in selected_option_names:
        sheet.write_string(2, col, name, header_format)
        col += 1

    sheet.write_string(2, col, "TOTAL NILAI", header_format)
    sheet.set_column(start_col, start_col + total_cols_this_module - 1, 14)


st.set_page_config(page_title="Presensi Generator", page_icon="📘", layout="wide")
st.title("Presensi Generator")

with st.sidebar:
    st.markdown("### Opsi File")
    nama_file = st.text_input(label="Nama File (tanpa .xlsx)", value="presensi")
    mk_angkatan = st.text_input(label="Prodi & Angkatan", value="TI-2022")
    modul = st.number_input(min_value=1, step=1, label="Jumlah Modul", value=8)
    jumlah_kelas = st.number_input(min_value=1, step=1, label="Jumlah Kelas", value=1)

st.markdown("### Tanggal Mulai per Kelas")
list_tanggal = generate_input_tanggal(int(jumlah_kelas), mk_angkatan)

st.markdown("### Opsi Kolom Opsional per Modul")
col1, col2, col3, col4 = st.columns(4)
with col1:
    tp = st.checkbox(label="TP", value=True)
with col2:
    test_awal = st.checkbox(label="JURNAL", value=True)
with col3:
    test_akhir = st.checkbox(label="TES AKHIR", value=True)
with col4:
    rate = st.checkbox(label="RATE", value=True)

st.markdown("---")

if st.button("Generate File Excel"):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})

    worksheets = []
    for i in range(int(jumlah_kelas)):
        ws_name = f"{mk_angkatan}-{str(i+1).zfill(2)}"
        worksheets.append(workbook.add_worksheet(ws_name))

    for ws in worksheets:
        add_base(ws, workbook)

    for idx_ws, ws in enumerate(worksheets):
        for i_modul in range(int(modul)):
            create_modul(
                ws,
                workbook,
                list_tanggal[idx_ws],
                tp=tp,
                test_awal=test_awal,
                test_akhir=test_akhir,
                rate=rate,
                modul=i_modul + 1
            )

    workbook.close()

    st.download_button(
        label=f"Download File Excel {nama_file}.xlsx",
        data=output.getvalue(),
        file_name=f"{nama_file}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.success("File berhasil dibuat!")
