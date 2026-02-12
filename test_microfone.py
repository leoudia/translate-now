import sounddevice as sd
import numpy as np

def listar_dispositivos():
    print('Dispositivos de áudio disponíveis:')
    print(sd.query_devices())

def get_default_input_device():
    # Retorna o índice do microfone padrão do sistema
    default_device = sd.default.device[0]
    if default_device is not None and default_device >= 0:
        return default_device
    # Se não houver padrão, tenta encontrar o primeiro dispositivo de entrada disponível
    devices = sd.query_devices()
    for idx, dev in enumerate(devices):
        if dev['max_input_channels'] > 0:
            return idx
    raise RuntimeError('Nenhum microfone encontrado.')

def get_default_output_device():
    # Retorna o índice do alto-falante/fone padrão do sistema
    default_device = sd.default.device[1]
    if default_device is not None and default_device >= 0:
        return default_device
    # Se não houver padrão, tenta encontrar o primeiro dispositivo de saída disponível
    devices = sd.query_devices()
    for idx, dev in enumerate(devices):
        if dev['max_output_channels'] > 0:
            return idx
    raise RuntimeError('Nenhum alto-falante/fone encontrado.')

def testar_microfone(device_in=None, device_out=None):
    info_in = sd.query_devices(device_in, 'input')
    info_out = sd.query_devices(device_out, 'output') if device_out is not None else None
    fs = int(info_in['default_samplerate'])
    canais_in = info_in['max_input_channels']
    canais_out = info_out['max_output_channels'] if info_out else 2
    print(f'Gravando 3 segundos de áudio do microfone selecionado (sample rate: {fs}, canais: {canais_in})...')
    try:
        audio = sd.rec(int(3 * fs), samplerate=fs, channels=min(1, canais_in), dtype='float32', device=device_in)
        sd.wait()
        print(f'Reproduzindo o áudio gravado (canais de saída: {canais_out})...')
        sd.play(audio, fs, device=device_out)
        sd.wait()
        print('Teste concluído com sucesso!')
    except Exception as e:
        print('Erro ao acessar o microfone ou alto-falante:', e)

if __name__ == "__main__":
    listar_dispositivos()
    device_in = get_default_input_device()
    device_out = get_default_output_device()
    print(f'Usando microfone padrão (input): {device_in}')
    print(f'Usando saída padrão (output): {device_out}')
    testar_microfone(device_in=device_in, device_out=device_out)
