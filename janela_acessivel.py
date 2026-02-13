import sys

import queue
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtCore import QUrl
from PyQt6.QtCore import QObject, pyqtSignal
import threading

class AudioSignals(QObject):
    # Definimos os sinais que a interface vai "escutar"
    acessibilidade_recebida = pyqtSignal(str)
    traducao_recebida = pyqtSignal(str)


import asyncio
import time
from typing import List, Callable, Optional

class CaptionBuffer:
    def __init__(self, timeout: int, callback: Callable[[str], asyncio.Future]):
        self.timeout = timeout
        self.callback = callback
        self._words: List[str] = []
        self.queue = queue.Queue()
        self._last_flush_time = time.time()
        self._worker_task = threading.Thread(target=self.run, daemon=True)

        self.queue.put("")
        

    def add_word(self, word: str):
        """Apenas insere na fila. Zero processamento pesado aqui."""
        self.queue.put(word)

    def start(self):
        self._worker_task.start()
    
    def run(self):

        while True:
            if not self._words:
                self._last_flush_time = time.time()

            try:
                word = self.queue.get(timeout=self.timeout, block=True)
                self._words.append(word)
            except queue.Empty:
                continue;

            now = time.time()
            remaining = self.timeout - (now - self._last_flush_time)

            if remaining <= 0:
                self._flush()

    def _flush(self):
        if self._words:
            text = " ".join(self._words)
            self._words = []
            
            try:
                self.callback(text)
            except Exception as e:
                print(f"Erro no callback de legenda: {e}")
            
            self._last_flush_time = time.time()

    def stop(self):
        self._worker.cancel()

class JanelaAcessivel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tradutor em Tempo Real + Libras")
        self.setGeometry(100, 100, 1200, 600)
        self.setStyleSheet("background-color: #121212;") # Fundo escuro

        self.signals = AudioSignals()
        self.signals.acessibilidade_recebida.connect(self.view_accessibility)
        self.signals.traducao_recebida.connect(self.view_caption)

        self.buffer = CaptionBuffer(timeout=5, callback=self.send_buffered_caption)

        layout_principal = QHBoxLayout()

        self.label_traducao = QLabel("Aguardando áudio...")
        self.label_traducao.setStyleSheet("color: #00FF00; font-size: 24px; font-weight: bold; padding: 20px;")
        self.label_traducao.setWordWrap(True)
        layout_principal.addWidget(self.label_traducao, stretch=2)

        self.web_view = QWebEngineView()

        self.web_view.setUrl(QUrl("http://localhost:8080"))
        layout_principal.addWidget(self.web_view, stretch=1)

        container = QWidget()
        container.setLayout(layout_principal)
        self.setCentralWidget(container)

        self.buffer.start()

    def update_accessibility(self, texto):
        if texto:
            self.signals.acessibilidade_recebida.emit(texto)

    def update_caption(self, texto):
        if texto:
            self.buffer.add_word(texto)

    def send_buffered_caption(self, texto):
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
