
# Discord Music Bot - By Rede Bots - Desenvolvido por Lucas Fortes

## Sumário

- [Descrição](#descrição)
- [Características](#características)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Comandos](#comandos)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Como Contribuir](#como-contribuir)
- [Licença](#licença)
- [Contato](#contato)

## Descrição

Este bot de música para Discord permite que os usuários reproduzam músicas diretamente de links do YouTube ou arquivos de áudio locais. Com uma interface de comando intuitiva, ele oferece funcionalidades como tocar, pausar, retomar e pular músicas, além de mostrar o status atual da música que está sendo reproduzida.

## Características

- Reproduz músicas a partir de links do YouTube.
- Suporte a arquivos de áudio locais.
- Controle total sobre a reprodução: pause, retome e pule músicas.
- Atualiza o status do bot com o título da música e thumbnail.
- Interface de comandos via Slash Commands.
- Log de eventos para monitoramento.

## Tecnologias Utilizadas

- **Python 3.8+**: Linguagem de programação.
- **Disnake**: Biblioteca para interação com a API do Discord.
- **yt-dlp**: Biblioteca para extração de áudio do YouTube.
- **FFmpeg**: Ferramenta para manipulação de áudio.
- **dotenv**: Gerenciamento de variáveis de ambiente.

## Pré-requisitos

Certifique-se de ter os seguintes pré-requisitos instalados:

- Python 3.8 ou superior.
- FFmpeg instalado e acessível no PATH do sistema.

## Instalação

1. Clone este repositório:

   ```bash
   git clone https://github.com/LucasDesignerF/python-music-bot.git
   cd python-music-bot
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):

   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows use: venv\Scripts\activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

## Configuração

1. Crie um arquivo `.env` na raiz do projeto e adicione seu token do Discord:

   ```plaintext
   DISCORD_TOKEN=seu_token_do_discord
   ```

2. Configure o caminho para o FFmpeg em `bin/ffmpeg.exe` ou ajuste o código para o local correto (a pasta bin nao foi adicionada ao projeto, devido ao tamanho dos binarios, portanto use os binarios de acordo com o sistema operacional que ira desenvolver o bot).

## Comandos

Os seguintes comandos estão disponíveis no bot:

| Comando             | Descrição                                   |
|---------------------|---------------------------------------------|
| `/play <query>`     | Toca uma música pelo nome.                 |
| `/pause`            | Pausa a música atual.                       |
| `/resume`           | Retoma a música pausada.                    |
| `/skip`             | Pula para a próxima música.                 |
| `/leave`            | Desconecta o bot do canal de voz.          |
| `/test_local_audio <filename>` | Toca um arquivo de áudio local.  |
| `/clear_temp`      | Limpa a pasta de músicas temporárias.      |
| `/infolder`        | Mostra o tamanho da pasta de músicas temporárias. |
| `/restart`         | Reinicia o bot (apenas para administradores). |

## Estrutura do Projeto

```
.
├── cogs
│   └── music.py         # Cog de música com comandos.
├── bin
│   └── ffmpeg.exe       # Executável do FFmpeg.
├── .env                  # Arquivo de configuração do ambiente.
├── requirements.txt      # Dependências do projeto.
└── main.py              # Ponto de entrada do bot.
```

## Como Contribuir

Contribuições são bem-vindas! Para contribuir:

1. Fork este repositório.
2. Crie uma branch para sua feature (`git checkout -b feature/nome-da-feature`).
3. Faça as alterações e adicione os arquivos (`git add .`).
4. Faça um commit (`git commit -m 'Adiciona nova feature'`).
5. Envie para o repositório remoto (`git push origin feature/nome-da-feature`).
6. Abra um Pull Request.

## Licença

Este projeto é licenciado sob a [MIT License](LICENSE).

## Contato

Para dúvidas ou sugestões, entre em contato:

- Nome: Lucas Fortes
- Discord: lrfortes
- Rede Bots: https://discord.gg/z5SkRN495p
