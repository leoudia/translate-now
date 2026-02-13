import whisper
import queue
import threading
import numpy as np
import sounddevice as sd

from tradutor import Tradutor

MODELO_WHISPER = "medium"  # Modelos disponíveis: tiny, base, small, medium, large
IDIOMA_ORIGEM = "pt"

class AudioDeviceManager:
    """Gerencia seleção e consulta dos dispositivos de áudio do sistema."""
    import sounddevice as sd

    @staticmethod
    def listar_dispositivos():
        print('Dispositivos de áudio disponíveis:')
        print(AudioDeviceManager.sd.query_devices())

    @staticmethod
    def get_default_input_device():
        default_device = AudioDeviceManager.sd.default.device[0]
        if default_device is not None and default_device >= 0:
            return default_device
        devices = AudioDeviceManager.sd.query_devices()
        for idx, dev in enumerate(devices):
            if dev['max_input_channels'] > 0:
                return idx
        raise RuntimeError('Nenhum microfone encontrado.')

    @staticmethod
    def get_default_output_device():
        default_device = AudioDeviceManager.sd.default.device[1]
        if default_device is not None and default_device >= 0:
            return default_device
        devices = AudioDeviceManager.sd.query_devices()
        for idx, dev in enumerate(devices):
            if dev['max_output_channels'] > 0:
                return idx
        raise RuntimeError('Nenhum alto-falante/fone encontrado.')

class Observable:
    def __init__(self):
        self._observers = []
        self.tradutor = Tradutor()

    def register(self, observer):
        self._observers.append(observer)
    def unregister(self, observer):
        self._observers.remove(observer)
    def notify(self, texto):
        print(f"[Observable] Notificando observadores com o texto: {texto}")
        for observer in self._observers:
            observer.update_accessibility(texto)
            observer.update_caption(self.tradutor.traduzir(texto))

class AudioProcessador(Observable):
    def __init__(self, device_in=None):
        super().__init__()
        self.model = whisper.load_model(MODELO_WHISPER)
        self.audio_queue = queue.Queue()
        self.running = True
        # Seleção automática do microfone se não informado
        self.device_in = device_in if device_in is not None else AudioDeviceManager.get_default_input_device()

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        #print(f"[AudioProcessador] Capturando áudio... (frames: {frames}), status: {status}, time: {time}")
        self.audio_queue.put(indata.copy())

    def processar_audio(self):
        print("--- Ouvindo... (Fale em Inglês) ---")
        fs = 16000  # taxa de amostragem
        min_duration = 2  # segundos
        min_samples = fs * min_duration
        audio_buffer = []
        samples_accum = 0
        while self.running:
            try:
                bloco = self.audio_queue.get(timeout=2, block=True)
                audio_buffer.append(bloco)
                samples_accum += bloco.shape[0]
                # Acumula até atingir o tempo mínimo
                if samples_accum >= min_samples:
                    audio_np = np.concatenate(audio_buffer).flatten().astype(np.float32)
                    result = self.model.transcribe(audio_np, language=IDIOMA_ORIGEM, fp16=False)
                    texto_original = result['text'].strip()
                    if texto_original:
                        self.notify(texto_original)
                    # Limpa buffer para próxima transcrição
                    audio_buffer = []
                    samples_accum = 0
            except queue.Empty:
                continue

    def iniciar(self):
        # Descobre o número de canais suportados pelo microfone selecionado
        info_in = sd.query_devices(self.device_in, 'input')
        canais_in = min(1, info_in['max_input_channels'])
        with sd.InputStream(callback=self.audio_callback, channels=canais_in, samplerate=16000, device=self.device_in):
            self.processar_audio()