# MediaMastery

## Introdução

MediaMastery é uma ferramenta que permite baixar vídeos de youtube em formato .mp4; extrair os textos do vídeo; e gerar legendas em tamanhos variados (SM, MD ou LG) com timestamps.

## Instalação

### 0. Pré-requisitos

Para instalar e utilizar o yt-dlp do jeito que desejamos, é necessário ter o Python e o ffmpeg instalado. Para isso, siga as instruções abaixo:

### 1. Instalar o Python

Primeiro, você precisa ter o Python instalado. Para isso:

1. Baixe o instalador do Python [neste link](https://www.python.org/downloads/).
2. Durante a instalação, **marque a opção "Add Python to PATH"**.
3. Conclua a instalação e, em seguida, verifique a instalação no terminal:

- **Windows:**

  ```bash
  python --version
  ```

- **Linux/Mac:**

  ```zsh
  python3 --version
  ```

  Você deverá ver a versão do Python instalada.

### 2. Instalar o ffmpeg

O yt-dlp precisa do ffmpeg para baixar os vídeos. Para isso:

1. Abra o terminal ou prompt de comando na raiz deste repositório.
2. Instale o ffmpeg executando:

   - **Windows, usando o Chocolatey:**

     ```bash
     choco install ffmpeg
     ```

   - **Linux/Mac:**

     ```zsh
     brew install ffmpeg
     ```

### 3. Instalar Bibliotecas Necessárias

Para manter sua instalação organizada e evitar conflitos com instalações globais, é altamente recomendado o uso de um ambiente virtual. Siga as instruções abaixo para configurar o ambiente e instalar a biblioteca necessária:

#### a) Criação e Ativação do Ambiente Virtual

1. Abra o terminal ou prompt de comando na raiz deste repositório.
2. Crie um ambiente virtual executando:

   - **Windows:**

     ```bash
     python -m venv venv
     ```

   - **Linux/Mac:**

     ```zsh
     python3 -m venv venv
     ```

3. Ative o ambiente virtual (se funcionar, você verá escrito no seu terminal `(venv)`):

   - **Windows:**

     ```bash
     source venv/Scripts/activate
     ```

   - **Linux/Mac:**

     ```zsh
     source venv/bin/activate
     ```

#### b) Instalação do yt-dlp no Ambiente Virtual

Com o ambiente virtual ativado, instale a biblioteca utilizando o comando:

- **Windows:**

  ```bash
  python -m pip install yt-dlp
  ```

- **Linux/Mac:**

  ```zsh
  python3 -m pip install yt-dlp
  ```

#### c) Instalação do Whisper no Ambiente Virtual

Com o ambiente virtual ativado, instale a biblioteca utilizando o comando:

- **Windows:**

  ```bash
  python -m pip install git+https://github.com/openai/whisper.git
  ```

- **Linux/Mac:**

  ```zsh
  python3 -m pip install git+https://github.com/openai/whisper.git
  ```

## Execução

Para executar o MediaMastery, siga as instruções abaixo:

1. Abra o terminal ou prompt de comando na raiz deste repositório.
2. Ative o ambiente virtual se ainda não estiver ativo:

   - **Windows:**

     ```bash
     source venv/Scripts/activate
     ```

   - **Linux/Mac:**

     ```zsh
     source venv/bin/activate
      ```

3. Para baxar vídeos:

   - No arquivo `01-Downloader.py`, substitua o valor da variável `urls` pelos links dos vídeos que deseja baixar.
   - Execute o comando:

     - **Windows:**

       ```bash
       python 01-Downloader.py
       ```

     - **Linux/Mac:**

       ```zsh
       python3 01-Downloader.py
       ```

4. Para legendar:

   - Primeiro, certifique-se de que os vídeos foram baixados.
   - Execute o comando:

     - **Windows:**

       ```bash
       python 02-Legender.py
       ```

     - **Linux/Mac:**

       ```zsh
       python3 02-Legender.py
       ```

5. Para extrair textos:

   - Primeiro, certifique-se de que os vídeos foram baixados.
   - Execute o comando:

     - **Windows:**

       ```bash
       python 03-Texter.py
       ```

     - **Linux/Mac:**

       ```zsh
       python3 03-Texter.py
       ```

## Créditos

Desenvolvido por **Guga - :coffee:** e **Yasmin - :bubbles:**.
- https://github.com/Yasmim-Coimbra
- https://github.com/GugaS1lva