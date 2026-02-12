from deep_translator import GoogleTranslator

# Configurações

IDIOMA_ORIGEM = "pt"
IDIOMA_DESTINO = "en"

class Tradutor:

    def traduzir(self, texto_original):
        if texto_original:
            traducao = GoogleTranslator(source=IDIOMA_ORIGEM, target=IDIOMA_DESTINO).translate(texto_original)
            return traducao
        return None