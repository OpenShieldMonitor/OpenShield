from win10toast_click import ToastNotifier
import webbrowser


def abrir_cve_enlace(enlace_final):
    webbrowser.open(enlace_final)
    return 0  # ✅ IMPORTANTE: Retornar un entero para evitar errores por pantalla

notifier = ToastNotifier()

def mostrar_alerta_windows(producto, version, severidad, cve_id=None, enlace=None):
    titulo = "🔒 Alerta de Seguridad Detectada"
    mensaje = f"{producto} v{version} - Severidad: {severidad}"
    enlace_final = enlace or f"https://nvd.nist.gov/vuln/detail/{cve_id}" if cve_id else None

    print(f"\n┏━ 📢 Emitiendo notificación: {mensaje} 📢")
    if enlace_final:
        print(f"┗━ 🌐 NVD - CVE: {enlace_final}\n")

    notifier.show_toast(
        titulo,
        f"{mensaje}\n{cve_id}\nHaz clic para más detalles...",
        duration=10,
        callback_on_click=lambda: abrir_cve_enlace(enlace_final) if enlace_final else None
    )
