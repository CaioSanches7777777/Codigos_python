import os
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from tkinter import filedialog, messagebox


# Definição da lógica da geração do relatório

# ==============================
# CONFIGURAÇÕES DO PDF
# ==============================
PAGE_WIDTH = 2480    # A4 em pixels (300 DPI)
PAGE_HEIGHT = 3508
MARGIN_X = 150
MARGIN_Y = 150
COLUMN_GAP = 100
ROW_GAP = 100

COLUMNS = 2
CELL_WIDTH = (PAGE_WIDTH - 2 * MARGIN_X - COLUMN_GAP) // 2
CELL_HEIGHT = 900

HEADER_SPACE = 300  # Espaço reservado para título e data


def create_pdf_from_images(image_paths, output_pdf, report_title, report_date):
    pages = []
    page = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), "white")
    draw = ImageDraw.Draw(page)

    # Fonte (usa padrão se não encontrar Arial)
    try:
        font_title = ImageFont.truetype("arial.ttf", 80)
        font_date = ImageFont.truetype("arial.ttf", 50)
    except:
        font_title = ImageFont.load_default()
        font_date = ImageFont.load_default()

    # ==============================
    # DESENHAR TÍTULO E DATA
    # ==============================
    draw.text((PAGE_WIDTH // 2, MARGIN_Y),
              report_title,
              font=font_title,
              fill="black",
              anchor="mm")

    draw.text((PAGE_WIDTH // 2, MARGIN_Y + 120),
              f"Data: {report_date}",
              font=font_date,
              fill="black",
              anchor="mm")

    # Linha separadora
    draw.line((MARGIN_X, MARGIN_Y + 200,
               PAGE_WIDTH - MARGIN_X, MARGIN_Y + 200),
              fill="black",
              width=5)

    x_positions = [
        MARGIN_X,
        MARGIN_X + CELL_WIDTH + COLUMN_GAP
    ]

    x_col = 0
    y = MARGIN_Y + HEADER_SPACE

    for img_path in image_paths:
        img = Image.open(img_path)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        img.thumbnail((CELL_WIDTH, CELL_HEIGHT))

        x = x_positions[x_col] + (CELL_WIDTH - img.width) // 2

        if y + img.height > PAGE_HEIGHT - MARGIN_Y:
            pages.append(page)
            page = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), "white")
            y = MARGIN_Y
            x_col = 0
            x = x_positions[x_col] + (CELL_WIDTH - img.width) // 2

        page.paste(img, (x, y))

        if x_col == 0:
            x_col = 1
        else:
            x_col = 0
            y += CELL_HEIGHT + ROW_GAP

    pages.append(page)

    pages[0].save(output_pdf, save_all=True, append_images=pages[1:])
    messagebox.showinfo("Sucesso", f"PDF criado com sucesso:\n{output_pdf}")


# ==============================
# INTERFACE GRÁFICA
# ==============================
def select_images():
    report_title = entry_title.get()
    report_date = entry_date.get()

    if not report_title or not report_date:
        messagebox.showerror("Erro", "Preencha o título e a data do relatório.")
        return

    files = filedialog.askopenfilenames(
        title="Selecione as imagens",
        filetypes=[("Imagens", "*.png *.jpg *.jpeg *.bmp *.tiff *.webp")]
    )

    if not files:
        return

    output_pdf = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF", "*.pdf")],
        title="Salvar PDF como"
    )

    if output_pdf:
        create_pdf_from_images(files, output_pdf, report_title, report_date)



# Definição da Interface do Usuário

# ==============================
# APP TKINTER
# ==============================
root = tk.Tk()
root.title("Imagens para PDF (2 colunas)")
root.geometry("500x300")

# Campo Título
tk.Label(root, text="Nome / Título do Relatório:", font=("Arial", 10)).pack(pady=(10, 0))
entry_title = tk.Entry(root, width=50)
entry_title.pack(pady=5)

# Campo Data
tk.Label(root, text="Data do Relatório:", font=("Arial", 10)).pack(pady=(10, 0))
entry_date = tk.Entry(root, width=50)
entry_date.pack(pady=5)

# Botão
btn = tk.Button(
    root,
    text="Selecionar imagens e gerar PDF",
    command=select_images,
    font=("Arial", 12),
    padx=20,
    pady=15
)

btn.pack(pady=20)

root.mainloop()
