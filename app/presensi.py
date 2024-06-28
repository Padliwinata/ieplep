import datetime
import os
from datetime import timedelta

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


def number_to_excel_column(n):
    """Convert a number to an Excel-style column (0 -> A, 1 -> B, ..., 26 -> AA, etc.)."""
    column = ""
    n += 1  # Adjust for zero-based index
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        column = chr(65 + remainder) + column
    return column


def generate_input_tanggal(num_kelas: int, kelas: str):
    list_tanggal = []
    for i in range(num_kelas):
        list_tanggal.append(st.date_input(label=f"Tanggal Mulai Praktikum {kelas}-{str(i+1).zfill(2)}", key=f'tanggal_{i}'))
    return list_tanggal


def coordinates_to_excel(x, y):
    """Convert zero-based row and column numbers to Excel-style coordinates."""
    column = number_to_excel_column(y)
    return f"{column}{x + 1}"  # Adjust for zero-based index


def create_modul(sheet, wb, start_date: datetime.datetime, tp: bool, test_awal: bool, test_akhir: bool, modul: int):
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

    extra = 4 + tp + test_awal + test_akhir
    koor = (modul - 1) * extra + 4
    start_date += timedelta(days=(modul-1) * 7)

    sheet.merge_range(0, koor, 0, koor + extra - 1, f"MODUL {modul}", header_format)
    # if modul == 1:
    sheet.merge_range(1, koor, 1, koor + extra - 1, f"{start_date.strftime('%d/%m/%Y')}", cell_format=header_format)
    # else:
    # sheet.merge_range(1, koor, 1, koor + extra - 1, f"={coordinates_to_excel(1, koor-5)}+7", cell_format=date_format)
    sheet.write_string(2, koor, "KEHADIRAN ASPRAK", cell_format=header_format)
    sheet.write_string(2, koor + 1, "KEHADIRAN", cell_format=header_format)
    sheet.write_string(2, koor + 2, "EVIDENCE", cell_format=header_format)

    koor += 2
    if tp:
        sheet.write_string(2, koor + 1, "TP", cell_format=header_format)
        koor += 1

    if test_awal:
        sheet.write_string(2, koor + 1, "TES AWAL", cell_format=header_format)
        koor += 1

    if test_akhir:
        sheet.write_string(2, koor + 1, "TES AKHIR", cell_format=header_format)
        koor += 1

    sheet.write_string(2, koor + 1, "JURNAL", cell_format=header_format)
    sheet.write_string(2, koor + 1, "TOTAL NILAI", cell_format=header_format)


st.title("Presensi Generator")

nama_file = st.text_input(label="Nama File")
mk_angkatan = st.text_input(label="Prodi dan Angkatan")
modul = st.number_input(min_value=1, step=1, label="Jumlah Modul")
jumlah_kelas = st.number_input(min_value=1, step=1, label="Jumlah Kelas")
list_tanggal = generate_input_tanggal(jumlah_kelas, mk_angkatan)

# evidence = st.checkbox(label="Evidence")
tp = st.checkbox(label="TP")
test_awal = st.checkbox(label="Test Awal")
test_akhir = st.checkbox(label="Test Akhir")
# total_nilai = st.checkbox(label="Total Nilai")

workbook = xlsxwriter.Workbook(f"{nama_file}.xlsx")
worksheets = []
for i in range(int(jumlah_kelas)):
    worksheets.append(workbook.add_worksheet(f"{mk_angkatan}-{str(i+1).zfill(2)}"))

for worksheet in worksheets:
    add_base(worksheet, workbook)

for x in range(len(worksheets)):
    for i in range(modul):
        create_modul(worksheets[x], workbook, list_tanggal[x], tp, test_awal, test_akhir, i+1)

workbook.close()

with open(f"{nama_file}.xlsx", "rb") as file:
    st.download_button(label="Download", data=file.read(), file_name=f"{nama_file}.xlsx", mime='application/vnd.ms-excel')

os.remove(f"{nama_file}.xlsx")


