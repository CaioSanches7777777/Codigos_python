import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
from numba import njit

# ----------------------------
# Configurações
# ----------------------------
varX = -0.46095
varY = 0.5619925

base_iter = 80
max_iter_cap = 2000

# ----------------------------
# JULIA (NUMBA + SMOOTH)
# ----------------------------
@njit
def julia_compute(Z0_real, Z0_imag, cx, cy, max_iter):
    h, w = Z0_real.shape
    result = np.zeros((h, w))

    for i in range(h):
        for j in range(w):
            zr = Z0_real[i, j]
            zi = Z0_imag[i, j]
            n = 0

            while zr*zr + zi*zi <= 4.0 and n < max_iter:
                temp = zr*zr - zi*zi + cx
                zi = 2*zr*zi + cy
                zr = temp
                n += 1

            if n < max_iter:
                mod = np.sqrt(zr*zr + zi*zi)
                result[i, j] = n + 1 - np.log(np.log(mod))/np.log(2)
            else:
                result[i, j] = 0

    return result


# ----------------------------
# MANDELBROT (NUMBA + SMOOTH)
# ----------------------------
@njit
def mandelbrot_compute(xmin, xmax, ymin, ymax, w, h, max_iter):
    result = np.zeros((h, w))

    for i in range(h):
        for j in range(w):
            cr = xmin + (xmax - xmin) * j / w
            ci = ymin + (ymax - ymin) * i / h

            zr = 0.0
            zi = 0.0
            n = 0

            while zr*zr + zi*zi <= 4.0 and n < max_iter:
                temp = zr*zr - zi*zi + cr
                zi = 2*zr*zi + ci
                zr = temp
                n += 1

            if n < max_iter:
                mod = np.sqrt(zr*zr + zi*zi)
                result[i, j] = n + 1 - np.log(np.log(mod))/np.log(2)
            else:
                result[i, j] = 0

    return result


# ----------------------------
# Função de iteração dinâmica
# ----------------------------
def dynamic_iter(xmin, xmax):
    zoom = 3.5 / (xmax - xmin)
    it = int(base_iter * np.log10(zoom + 1))
    return min(max(it, base_iter), max_iter_cap)


# ----------------------------
# Setup Figura
# ----------------------------
fig, (ax_julia, ax_mandel) = plt.subplots(1, 2, figsize=(12, 6))
plt.subplots_adjust(bottom=0.25)

# Grid Julia fixo
width, height = 600, 600
x = np.linspace(-1.5, 1.5, width)
y = np.linspace(-1.5, 1.5, height)
X, Y = np.meshgrid(x, y)

# Julia inicial
julia_img = ax_julia.imshow(
    julia_compute(X, Y, varX, varY, base_iter),
    extent=(-1.5, 1.5, -1.5, 1.5),
    origin="lower",
    cmap="inferno"
)
ax_julia.set_title("Julia Set")

# Mandelbrot inicial
xmin, xmax = -2, 0.5
ymin, ymax = -1.25, 1.25

initial_iter = dynamic_iter(xmin, xmax)
initial_data = mandelbrot_compute(xmin, xmax, ymin, ymax, 600, 600, initial_iter)

mandel_img = ax_mandel.imshow(
    initial_data,
    extent=(xmin, xmax, ymin, ymax),
    origin="lower",
    cmap="inferno",
    vmin=0,
    vmax=initial_data.max()
)

ax_mandel.set_title("Mandelbrot (Zoom Inteligente)")
ax_mandel.set(xlim=(xmin, xmax), ylim=(ymin, ymax))



# Controle para evitar dupla atualização
updating = False

def update_mandel(ax):
    global updating
    if updating:
        return
    updating = True

    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()

    w, h = ax.patch.get_window_extent().size.round().astype(int)
    w = max(w, 200)
    h = max(h, 200)

    iters = dynamic_iter(xmin, xmax)

    data = mandelbrot_compute(xmin, xmax, ymin, ymax, w, h, iters)

    mandel_img.set_data(data)
    mandel_img.set_extent((xmin, xmax, ymin, ymax))

    ax.figure.canvas.draw_idle()
    updating = False


# Conectar apenas UMA vez
ax_mandel.callbacks.connect("xlim_changed", update_mandel)


point, = ax_mandel.plot(varX, varY, "cyan", marker="o")

# ----------------------------
# Atualizar Mandelbrot ao zoom
# ----------------------------
def update_mandel(ax):
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()

    w, h = ax.patch.get_window_extent().size.round().astype(int)
    w = max(w, 300)
    h = max(h, 300)

    iters = dynamic_iter(xmin, xmax)
    data = mandelbrot_compute(xmin, xmax, ymin, ymax, w, h, iters)

    mandel_img.set_data(data)
    mandel_img.set_extent((xmin, xmax, ymin, ymax))
    mandel_img.set_clim(vmin=0, vmax=data.max())

    ax.figure.canvas.draw_idle()


ax_mandel.callbacks.connect("xlim_changed", update_mandel)
ax_mandel.callbacks.connect("ylim_changed", update_mandel)

# ----------------------------
# Clique para escolher C
# ----------------------------
def on_click(event):
    global varX, varY
    if event.inaxes == ax_mandel:
        varX = event.xdata
        varY = event.ydata

        textbox_x.set_val(str(varX))
        textbox_y.set_val(str(varY))

        julia_img.set_data(
            julia_compute(X, Y, varX, varY, base_iter)
        )

        point.set_data([varX], [varY])
        fig.canvas.draw_idle()

fig.canvas.mpl_connect("button_press_event", on_click)

# ----------------------------
# TextBoxes
# ----------------------------
axbox_x = fig.add_axes([0.3, 0.1, 0.2, 0.05])
axbox_y = fig.add_axes([0.6, 0.1, 0.2, 0.05])

textbox_x = TextBox(axbox_x, "VarX", initial=str(varX))
textbox_y = TextBox(axbox_y, "VarY", initial=str(varY))

def submit(text):
    global varX, varY
    try:
        varX = float(textbox_x.text)
        varY = float(textbox_y.text)

        julia_img.set_data(
            julia_compute(X, Y, varX, varY, base_iter)
        )

        point.set_data([varX], [varY])
        fig.canvas.draw_idle()

    except ValueError:
        print("Digite valores numéricos válidos.")

textbox_x.on_submit(submit)
textbox_y.on_submit(submit)

plt.show()
