import sys
import time
import threading

class Spinner:
    def __init__(self, mensaje="Analizando sistema..."):
        self.mensaje = mensaje
        self._stop_event = threading.Event()
        self._spinner_cycle = ['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏']
        self._thread = threading.Thread(target=self._spin)

    def _spin(self):
        idx = 0
        while not self._stop_event.is_set():
            spinner = self._spinner_cycle[idx % len(self._spinner_cycle)]
            sys.stdout.write(f"  \r{spinner} {self.mensaje}")
            sys.stdout.flush()
            time.sleep(0.1)
            idx += 1
        sys.stdout.write("\n\r✅ Análisis completado.\n")
        sys.stdout.flush()

    def start(self):
        self._stop_event.clear()
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        self._thread.join()
