# 🎙️ Translate Now --- Tradução em Tempo Real com Acessibilidade

## 📌 1. Resumo do Projeto

O **Translate Now (Traduzir Agora)** é uma aplicação desenvolvida como
entrega prática de um bootcamp de IA aplicada, cujo objetivo foi
implementar uma solução utilizando **Speech-to-Text**.

A aplicação captura áudio do microfone em tempo real, processa a fala
utilizando o modelo **Whisper**, converte o conteúdo em texto, traduz
automaticamente e disponibiliza o resultado de forma acessível,
incluindo integração com o **VLibras** para interpretação em Língua
Brasileira de Sinais.

### 🚀 Funcionalidades

-   Captura de áudio em tempo real.
-   Transcrição automática com Whisper.
-   Tradução automática com deep-translator.
-   Integração com VLibras (acessibilidade).
-   Interface gráfica com PyQt6.
-   Buffer inteligente de áudio para otimização de processamento.

------------------------------------------------------------------------

## ⚙️ 2. Configuração do VLibras

Repositório oficial: https://github.com/spbgovbr-vlibras

### 2.1 Instalar Node.js

Baixe a versão LTS: https://nodejs.org

Verifique:

``` bash
node -v
npm -v
```

### 2.2 Iniciar o servidor do widget

``` bash
cd translate-now/widget
node server.js
```

Servidor disponível em: http://localhost:8080

------------------------------------------------------------------------

## 🐍 3. Instalar Python 3

Requisitos: - Python 3.10+ - pip atualizado

Criar ambiente virtual:

``` bash
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

Instalar dependências:

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## ▶️ 4. Executar a Aplicação

Com o VLibras em execução:

``` bash
python main.py
```

A aplicação irá:

1.  Abrir a interface gráfica.
2.  Capturar o áudio do microfone.
3.  Processar blocos de áudio (\~2 segundos).
4.  Transcrever com Whisper.
5.  Traduzir automaticamente.
6.  Exibir texto e enviar ao VLibras.

------------------------------------------------------------------------

## 🔄 Fluxo da Aplicação

    Microfone → Captura → Buffer → Whisper → Texto → Tradução → Interface → VLibras

------------------------------------------------------------------------

## 📚 5. Considerações Finais

Projeto desenvolvido durante o bootcamp:

https://web.dio.me/track/bradesco-genai-dados

A parceria **DIO + Bradesco** proporcionou uma experiência prática com:

-   IA Generativa aplicada
-   Processamento de fala
-   Integração de tecnologias
-   Desenvolvimento com impacto em acessibilidade

------------------------------------------------------------------------

## 👨‍💻 Autor

**Leandro Monteiro** Analista de Sistemas \| Arquitetura de Software \|
IA Aplicada