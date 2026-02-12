from audio_processador import AudioProcessador
from janela_acessivel import JanelaAcessivel
import threading
import sys
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = JanelaAcessivel()
    janela.show()

    audio = AudioProcessador()
    audio.register(janela)

    def on_close_event(event):
        audio.running = False
        event.accept()

    janela.closeEvent = on_close_event

    audio_thread = threading.Thread(target=audio.iniciar, daemon=True)
    audio_thread.start()

    sys.exit(app.exec())
