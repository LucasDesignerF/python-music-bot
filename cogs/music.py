import disnake
from disnake.ext import commands
import yt_dlp
import os

# Definir o caminho para o FFmpeg
FFMPEG_PATH = os.path.join(os.getcwd(), "bin", "ffmpeg.exe")

# Definir opções para yt-dlp
ydl_opts = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
}

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def search_youtube(self, query):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch:{query}", download=False)
                return info['entries'][0]
            except Exception as e:
                print(f"Erro ao buscar no YouTube: {e}")
                return None

    async def update_status(self, title):
        activity = disnake.Game(name=f"Ouvindo {title}")  # Alterado para "Ouvindo"
        await self.bot.change_presence(activity=activity)

    @commands.slash_command(description="Toca uma música pelo nome")
    async def play(self, inter: disnake.ApplicationCommandInteraction, query: str):
        await inter.response.send_message(f"Buscando: {query}...")

        song_info = await self.search_youtube(query)

        if song_info is None:
            await inter.followup.send("Não foi possível encontrar a música.")
            return

        url = song_info['url']
        title = song_info['title']
        await inter.followup.send(f"🎵 Música encontrada: {title}")

        # Conectar ao canal de voz
        if not inter.author.voice:
            await inter.followup.send("Você precisa estar em um canal de voz para usar este comando.", ephemeral=True)
            return

        voice_channel = inter.author.voice.channel
        if inter.guild.voice_client is None:
            await voice_channel.connect()

        voice_client = inter.guild.voice_client

        # Tocar a música em streaming
        try:
            ffmpeg_options = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn'
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                audio_url = info['formats'][0]['url']

            source = disnake.FFmpegPCMAudio(audio_url, **ffmpeg_options, executable=FFMPEG_PATH)
            voice_client.play(source)

            await self.update_status(title)  # Atualizar status com o título da música
            await inter.followup.send(f"Tocando agora: {title}")
        except Exception as e:
            await inter.followup.send(f"Ocorreu um erro ao tentar tocar a música: {str(e)}")

    @commands.slash_command(description="Limpa a pasta de músicas temporárias")
    async def clear_temp(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_message("Essa função não é mais necessária, pois não estamos salvando arquivos temporariamente.")

    @commands.slash_command(description="Mostra o tamanho da pasta de músicas temporárias")
    async def infolder(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_message("Essa função não é mais necessária, pois não estamos salvando arquivos temporariamente.")

    @commands.slash_command(description="Toca um áudio local")
    async def test_local_audio(self, inter: disnake.ApplicationCommandInteraction, filename: str):
        await inter.response.send_message(f"Tentando tocar o áudio: {filename}...")

        if not inter.author.voice:
            await inter.followup.send("Você precisa estar em um canal de voz para usar este comando.", ephemeral=True)
            return

        voice_channel = inter.author.voice.channel
        if inter.guild.voice_client is None:
            await voice_channel.connect()

        voice_client = inter.guild.voice_client

        try:
            # Verifique se o arquivo existe
            mp3_filepath = os.path.join(os.getcwd(), filename)  # Presume que o arquivo está na raiz do bot
            if not os.path.isfile(mp3_filepath):
                await inter.followup.send(f"O arquivo {filename} não foi encontrado.")
                return
            
            source = disnake.FFmpegPCMAudio(mp3_filepath, executable=FFMPEG_PATH)
            voice_client.play(source)
            await self.update_status(filename)  # Atualizar status com o nome do arquivo
            await inter.followup.send(f"Tocando áudio local: {filename}")
        except Exception as e:
            await inter.followup.send(f"Ocorreu um erro ao tentar tocar o áudio: {str(e)}")

    @commands.slash_command(description="Pausa a música atual")
    async def pause(self, inter: disnake.ApplicationCommandInteraction):
        voice_client = inter.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.pause()
            await inter.response.send_message("Música pausada.")
        else:
            await inter.response.send_message("Nenhuma música está tocando.")

    @commands.slash_command(description="Resuma a música atual")
    async def resume(self, inter: disnake.ApplicationCommandInteraction):
        voice_client = inter.guild.voice_client
        if voice_client and voice_client.is_paused():
            voice_client.resume()
            await inter.response.send_message("Música retomada.")
        else:
            await inter.response.send_message("Nenhuma música está pausada.")

    @commands.slash_command(description="Pule para a próxima música")
    async def skip(self, inter: disnake.ApplicationCommandInteraction):
        voice_client = inter.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await inter.response.send_message("Música pulada.")
        else:
            await inter.response.send_message("Nenhuma música está tocando para pular.")

    @commands.slash_command(description="Sai do canal de voz")
    async def leave(self, inter: disnake.ApplicationCommandInteraction):
        if inter.guild.voice_client:
            await inter.guild.voice_client.disconnect()
            await inter.response.send_message("Desconectado do canal de voz.")
        else:
            await inter.response.send_message("Eu não estou em nenhum canal de voz no momento.")

def setup(bot):
    bot.add_cog(Music(bot))
