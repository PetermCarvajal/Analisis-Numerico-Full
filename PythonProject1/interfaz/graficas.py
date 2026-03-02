import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import tkinter as tk

def formatear_valor(valor):
    if valor is None or valor == '-' or valor == '--------':
        return valor
    if isinstance(valor, str):
        return valor
    try:
        val = float(valor)
        if val == 0.0:
            return "0.00000000"
        if abs(val) < 1e-4 or abs(val) >= 1e8:
            return f"{val:.8e}"
        else:
            return f"{val:.8f}"
    except (ValueError, TypeError):
        return str(valor)

class VisualizadorGrafico:
    def __init__(self, master):
        self.master = master
        # Fondo exacto de la ventana principal de la imagen (Azul marino oscuro)
        self.fig = plt.figure(figsize=(6, 6.5), dpi=100)
        self.fig.patch.set_facecolor('#1e1e2b')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.widget = self.canvas.get_tk_widget()
        self.widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.frame_toolbar = tk.Frame(self.master, bg='#1e1e2b')
        self.frame_toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame_toolbar)
        self.toolbar.config(background='#1e1e2b')
        for button in self.toolbar.winfo_children():
            button.config(background='#1e1e2b')
        self.toolbar.update()
        self.toolbar.pan()

        self.canvas.mpl_connect("scroll_event", self.zoom_rueda_raton)
        self.canvas.mpl_connect("motion_notify_event", self.on_hover)

        self.annot1 = None
        self.annot2 = None
        self.ax1 = None
        self.ax2 = None

    def zoom_rueda_raton(self, event):
        if event.inaxes is None or event.inaxes not in [self.ax1, self.ax2]: return
        escala = 1 / 1.2 if event.button == 'up' else 1.2
        ax = event.inaxes
        x_min, x_max = ax.get_xlim()
        y_min, y_max = ax.get_ylim()
        n_ancho, n_alto = (x_max - x_min) * escala, (y_max - y_min) * escala
        rx, ry = (event.xdata - x_min) / (x_max - x_min), (event.ydata - y_min) / (y_max - y_min)

        ax.set_xlim([event.xdata - n_ancho * rx, event.xdata + n_ancho * (1 - rx)])
        ax.set_ylim([event.ydata - n_alto * ry, event.ydata + n_alto * (1 - ry)])
        self.canvas.draw_idle()

    def on_hover(self, event):
        """Muestra tooltips al pasar el ratón."""
        if event.inaxes is None:
            es_visible = False
            if self.annot1 and self.annot1.get_visible():
                self.annot1.set_visible(False)
                es_visible = True
            if self.annot2 and self.annot2.get_visible():
                self.annot2.set_visible(False)
                es_visible = True
            if es_visible:
                self.canvas.draw_idle()
            return

        if event.inaxes == self.ax1 and self.annot1 is not None:
            self.annot1.xy = (event.xdata, event.ydata)
            self.annot1.set_text(f"x = {formatear_valor(event.xdata)}\nf(x) = {formatear_valor(event.ydata)}")
            self.annot1.set_visible(True)
            if self.annot2: self.annot2.set_visible(False)
            self.canvas.draw_idle()

        elif event.inaxes == self.ax2 and self.annot2 is not None:
            self.annot2.xy = (event.xdata, event.ydata)
            self.annot2.set_text(f"Iter = {event.xdata:.1f}\nErr = {formatear_valor(event.ydata)}")
            self.annot2.set_visible(True)
            if self.annot1: self.annot1.set_visible(False)
            self.canvas.draw_idle()

    def graficar_metodo(self, f, raiz, historial, titulo, mostrar_secantes=False, mostrar_tangentes=False,
                        mostrar_convergencia=False, mostrar_principal=True, historiales_multiples=None,
                        historial_secundario=None, nombre_metodo=""):
        self.fig.clf()
        self.ax1 = None
        self.ax2 = None

        tiene_conv = False
        errores_log = []
        iteraciones_n = []

        if historiales_multiples or historial_secundario:
            tiene_conv = mostrar_convergencia
        else:
            if historial:
                for iteracion in historial:
                    err = iteracion.get('error_absoluto', 0)
                    if err > 0:
                        errores_log.append(err)
                        iteraciones_n.append(iteracion.get('n', iteracion.get('iter', 0)))
            tiene_conv = mostrar_convergencia and len(errores_log) > 0

        if mostrar_principal and tiene_conv:
            gs = self.fig.add_gridspec(2, 1, height_ratios=[2, 1.2])
            self.ax1 = self.fig.add_subplot(gs[0])
            self.ax2 = self.fig.add_subplot(gs[1])
        elif mostrar_principal and not tiene_conv:
            self.ax1 = self.fig.add_subplot(111)
        elif not mostrar_principal and tiene_conv:
            self.ax2 = self.fig.add_subplot(111)
        else:
            self.canvas.draw()
            return self.master

        # --- PANEL SUPERIOR ---
        if self.ax1 is not None:
            # Fondo exacto interior del plot (Un poco más claro que el fondo general)
            self.ax1.set_facecolor('#242436')
            es_punto_fijo = "Punto Fijo" in nombre_metodo

            x_min, x_max = (0.0, 3.0) if es_punto_fijo else (raiz - 2.0, raiz + 2.0)
            x = np.linspace(x_min, x_max, 400)
            try:
                y = [f(val) for val in x]
            except:
                y = np.zeros_like(x)

            if es_punto_fijo:
                self.ax1.plot(x, x, color='#6272a4', linestyle='--', linewidth=1.2, label='y = x')
                self.ax1.plot(x, y, color='#8be9fd', linewidth=2.0, label='y = g(x)')
                self.ax1.axhline(0, color='#6272a4', linewidth=0.5, alpha=0.5)

                if historial and not historiales_multiples:
                    x0 = historial[0].get('c', 0)
                    cobweb_xs, cobweb_ys = [x0], [x0]
                    x_cur = x0
                    for it in historial:
                        gx = it.get('f(c)', 0)
                        cobweb_xs.extend([x_cur, x_cur, gx])
                        cobweb_ys.extend([x_cur, gx, gx])
                        x_cur = gx
                    self.ax1.plot(cobweb_xs, cobweb_ys, color='#ff79c6', linewidth=1.2, alpha=0.8, label='Cobweb')
                    self.ax1.scatter([x0], [x0], color='#50fa7b', zorder=6, s=70, label=f'x0={x0}')
            else:
                # Línea celeste principal como en la imagen
                self.ax1.plot(x, y, color='#6699ff', label='f(x)', linewidth=2.5)
                self.ax1.axhline(0, color='#4e4e6a', linewidth=1, linestyle='--')

            if historiales_multiples:
                colores_multi = ['#ff79c6', '#50fa7b', '#ffb86c', '#bd93f9', '#8be9fd']
                for i, (val_x0, hist) in enumerate(historiales_multiples.items()):
                    color = colores_multi[i % len(colores_multi)]
                    x_pts = [it.get('c', it.get('x_n', 0)) for it in hist]
                    y_pts = [it.get('f(c)', it.get('g_xn', 0)) for it in hist]
                    self.ax1.plot(x_pts, y_pts, marker='o', linestyle='-', color=color, alpha=0.8, label=f'x0={val_x0}')

            elif historial_secundario:
                cs1 = [rec.get('c', 0) for rec in historial]
                fcs1 = [rec.get('f(c)', 0) for rec in historial]
                self.ax1.scatter(cs1, fcs1, marker='x', s=60, color='#8be9fd', zorder=5, label='M. Principal')

                cs2 = [rec.get('c', 0) for rec in historial_secundario]
                fcs2 = [rec.get('f(c)', 0) for rec in historial_secundario]
                self.ax1.scatter(cs2, fcs2, marker='o', s=40, color='#ffb86c', zorder=4, alpha=0.7,
                                 label='M. Secundario')

            elif historial and not es_punto_fijo:
                for i, iteracion in enumerate(historial):
                    if i < 4:
                        x_n = iteracion.get('c', iteracion.get('x_n', 0))
                        f_n = iteracion.get('f(c)', iteracion.get('f(x_n)', 0))
                        if mostrar_tangentes:
                            df_n = iteracion.get('f_prima(c)', 0)
                            if df_n != 0:
                                y_tang = [df_n * (xv - x_n) + f_n for xv in x]
                                self.ax1.plot(x, y_tang, linestyle='-.', alpha=0.6, color="#ffb86c")
                                self.ax1.plot([x_n, x_n], [0, f_n], linestyle=':', color='#50fa7b', alpha=0.8)
                        elif mostrar_secantes:
                            x_n_1 = iteracion.get('x_n-1', 0)
                            f_n_1 = iteracion.get('f(x_n-1)', 0)
                            x_next = iteracion.get('x_n+1', 0)
                            # Puntos naranjas como en la imagen
                            self.ax1.plot([x_n_1, x_n, x_next], [f_n_1, f_n, 0], marker='o', markersize=6,
                                          linestyle='-', color='#ffb86c', alpha=0.9)

            # Estrella rosada/roja para la raíz
            self.ax1.plot(raiz, f(raiz) if not es_punto_fijo else raiz, marker='*', color='#ff5555', markersize=14,
                          label=f'Raíz: {formatear_valor(raiz)}', zorder=10)

            self.ax1.set_title(titulo, color='#c8c8d8', fontsize=11, fontweight='bold')
            self.ax1.tick_params(colors='#c8c8d8', labelsize=8)
            # Grid sutil
            self.ax1.grid(True, color='#3a3a50', linestyle=':', alpha=0.8)
            self.ax1.legend(loc='best', facecolor='#1e1e2b', edgecolor='#3a3a50', labelcolor='#c8c8d8', fontsize=8)

            # Tooltip 1
            self.annot1 = self.ax1.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                                            bbox=dict(boxstyle="round,pad=0.4", fc="#181825", ec="#7393ff", alpha=0.9),
                                            color="#e0e0e0", fontfamily="monospace", fontsize=9,
                                            arrowprops=dict(arrowstyle="->", color="#e0e0e0"))
            self.annot1.set_visible(False)

        # --- PANEL INFERIOR ---
        if self.ax2 is not None:
            self.ax2.set_facecolor('#242436')

            if historiales_multiples:
                colores_multi = ['#ff79c6', '#50fa7b', '#ffb86c', '#bd93f9', '#8be9fd']
                for i, (val_x0, hist) in enumerate(historiales_multiples.items()):
                    color = colores_multi[i % len(colores_multi)]
                    e_log = [it.get('error_absoluto', 0) for it in hist if it.get('error_absoluto', 0) > 0]
                    i_n = [it.get('n', it.get('iter', 0)) for it in hist if it.get('error_absoluto', 0) > 0]
                    self.ax2.plot(i_n, e_log, marker='s', color=color, linewidth=2, label=f'x0={val_x0}')

            elif historial_secundario:
                e1 = [it.get('error_absoluto', 0) for it in historial if it.get('error_absoluto', 0) > 0]
                n1 = [it.get('n', 0) for it in historial if it.get('error_absoluto', 0) > 0]
                self.ax2.plot(n1, e1, marker='s', color='#8be9fd', linewidth=2, label='M. Principal')

                e2 = [it.get('error_absoluto', 0) for it in historial_secundario if it.get('error_absoluto', 0) > 0]
                n2 = [it.get('n', 0) for it in historial_secundario if it.get('error_absoluto', 0) > 0]
                self.ax2.plot(n2, e2, marker='o', color='#ffb86c', linewidth=2, label='M. Secundario')

            else:
                # Línea verde de error como en la imagen
                self.ax2.plot(iteraciones_n, errores_log, marker='o', markersize=5, color='#a6e3a1', linewidth=2,
                              label='Error absoluto')
                for n_val, err_val in zip(iteraciones_n, errores_log):
                    self.ax2.annotate(f"{err_val:.1e}", (n_val, err_val), textcoords="offset points", xytext=(0, 8),
                                      ha='center', fontsize=7, color='#a0a0b0')

            self.ax2.set_yscale('log')
            self.ax2.set_title('Convergencia del Error Absoluto (escala log)', color='#c8c8d8', fontsize=10)
            self.ax2.set_ylabel('Error absoluto', color='#c8c8d8', fontsize=9)
            self.ax2.set_xlabel('Iteración n', color='#c8c8d8', fontsize=9)
            self.ax2.tick_params(colors='#c8c8d8', labelsize=8)
            self.ax2.legend(loc='best', facecolor='#1e1e2b', edgecolor='#3a3a50', labelcolor='#c8c8d8', fontsize=8)
            self.ax2.grid(True, which="both", color='#3a3a50', linestyle='-', alpha=0.5)

            # Tooltip 2
            self.annot2 = self.ax2.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                                            bbox=dict(boxstyle="round,pad=0.4", fc="#181825", ec="#a6e3a1", alpha=0.9),
                                            color="#e0e0e0", fontfamily="monospace", fontsize=9,
                                            arrowprops=dict(arrowstyle="->", color="#e0e0e0"))
            self.annot2.set_visible(False)

        self.fig.tight_layout(pad=2.0)
        self.canvas.draw()
        return self.master