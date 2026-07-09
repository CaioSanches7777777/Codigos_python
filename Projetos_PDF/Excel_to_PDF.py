import openpyxl
import tkinter as tk
from tkinter import filedialog, messagebox

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

# ======================================================
# GERAÇÃO DO PDF
# ======================================================

def create_pdf_from_sheet(sheet, output_pdf, report_title, report_date):

    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=A4,
        leftMargin=30,
        rightMargin=30,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER

    normal_style = styles["Normal"]
    normal_style.alignment = TA_CENTER

    elements = []

    # -----------------------------
    # Título
    # -----------------------------

    elements.append(
        Paragraph(report_title, title_style)
    )

    elements.append(
        Paragraph(f"Date: {report_date}", normal_style)
    )

    elements.append(Spacer(1, 20))

    # -----------------------------
    # Lê a planilha
    # -----------------------------

    table_data = []

    for row in sheet.iter_rows(values_only=True):

        table_data.append([
            "" if value is None else str(value)
            for value in row
        ])

    # -----------------------------
    # Cria tabela
    # -----------------------------

    table = Table(table_data, repeatRows=1)

    table.setStyle(TableStyle([

        # Cabeçalho
        ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),

        # Corpo
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 9),

        ('GRID', (0,0), (-1,-1), 0.5, colors.black),

        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),

        ('BOTTOMPADDING', (0,0), (-1,0), 8),

        ('ROWBACKGROUNDS',
         (0,1),
         (-1,-1),
         [colors.white, colors.beige])

    ]))

    elements.append(table)

    # -----------------------------
    # Salva PDF
    # -----------------------------

    doc.build(elements)

    messagebox.showinfo(
        "Success",
        f"PDF created:\n{output_pdf}"
    )


# ======================================================
# INTERFACE
# ======================================================

def select_info():

    report_title = entry_title.get()
    report_date = entry_date.get()

    if not report_title or not report_date:
        messagebox.showerror(
            "Error",
            "Give the report a title and a date."
        )
        return

    file = filedialog.askopenfilename(
        title="Select Excel file",
        filetypes=[("Excel Workbook", "*.xlsx")]
    )

    if not file:
        return

    workbook = openpyxl.load_workbook(file)

    sheet = workbook.active

    output_pdf = filedialog.asksaveasfilename(
        title="Save PDF",
        defaultextension=".pdf",
        filetypes=[("PDF", "*.pdf")]
    )

    if not output_pdf:
        return

    create_pdf_from_sheet(
        sheet,
        output_pdf,
        report_title,
        report_date
    )


# ======================================================
# TKINTER
# ======================================================

root = tk.Tk()

root.title("Excel to PDF Report")

root.geometry("500x300")

# Título

tk.Label(
    root,
    text="Report Title:"
).pack(pady=(15,5))

entry_title = tk.Entry(root, width=50)

entry_title.pack()

# Data

tk.Label(
    root,
    text="Report Date:"
).pack(pady=(15,5))

entry_date = tk.Entry(root, width=50)

entry_date.pack()

# Botão

btn = tk.Button(

    root,

    text="Select Excel File",

    command=select_info,

    padx=15,

    pady=10,

    font=("Arial",11)

)

btn.pack(pady=25)

root.mainloop()
