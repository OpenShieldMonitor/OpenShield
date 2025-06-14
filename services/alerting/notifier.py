from win10toast_click import ToastNotifier
import webbrowser

notifier = ToastNotifier()

def mostrar_alerta_windows(producto, version, severidad, cve_id=None, enlace=None):
    titulo = "🔒 Alerta de Seguridad Detectada"
    mensaje = f"{producto} v{version} - Severidad: {severidad}"
    enlace_final = enlace or f"https://nvd.nist.gov/vuln/detail/{cve_id}" if cve_id else None

    print(f"🔔 Notificación: {mensaje}")
    if enlace_final:
        print(f"🔗 CVE: {enlace_final}")

    notifier.show_toast(
        titulo,
        f"{mensaje}\n{cve_id}\nHaz clic para más detalles...",
        duration=10,
        callback_on_click=lambda: webbrowser.open(enlace_final) if enlace_final else None
    )
