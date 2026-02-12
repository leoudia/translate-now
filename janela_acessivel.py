import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtCore import QUrl
from PyQt6.QtCore import QObject, pyqtSignal

class AudioSignals(QObject):
    # Definimos os sinais que a interface vai "escutar"
    acessibilidade_recebida = pyqtSignal(str)
    traducao_recebida = pyqtSignal(str)

class JanelaAcessivel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tradutor em Tempo Real + Libras")
        self.setGeometry(100, 100, 1200, 600)
        self.setStyleSheet("background-color: #121212;") # Fundo escuro

        self.signals = AudioSignals()
        self.signals.acessibilidade_recebida.connect(self.view_accessibility)
        self.signals.traducao_recebida.connect(self.view_caption)

        # Layout Principal
        layout_principal = QHBoxLayout()

        # 1. Área do Texto Traduzido (Esquerda)
        self.label_traducao = QLabel("Aguardando áudio...")
        self.label_traducao.setStyleSheet("color: #00FF00; font-size: 24px; font-weight: bold; padding: 20px;")
        self.label_traducao.setWordWrap(True)
        layout_principal.addWidget(self.label_traducao, stretch=2)

        # 2. Área do Avatar VLibras (Direita)
        self.web_view = QWebEngineView()
        # Aqui você carregaria um HTML local que contém o script do VLibras
        # self.web_view.setHtml(html_com_vlibras)
        self.web_view.setUrl(QUrl("http://localhost:8080"))
        layout_principal.addWidget(self.web_view, stretch=1)

        container = QWidget()
        container.setLayout(layout_principal)
        self.setCentralWidget(container)

    def update_accessibility(self, texto):
        if texto:
            self.signals.acessibilidade_recebida.emit(texto)

    def update_caption(self, texto):
        if texto:
            self.signals.traducao_recebida.emit(texto)

    def view_accessibility(self, texto):
        try:
            self.web_view.page().runJavaScript(f"window.plugin.translate('{texto}');")
            print(f"[JanelaAcessivel] Enviando para VLibras: {texto}")
        except Exception as e:
            print(f"Erro ao atualizar acessibilidade: {e}")
    
    def view_caption(self, texto):
        try:
            self.label_traducao.setText(texto)
        except Exception as e:
            print(f"Erro ao atualizar legenda: {e}")

    def callback(self, result):
        if result is None:
            print("JavaScript executed with no return value or failed.")
        else:
            print(result)
