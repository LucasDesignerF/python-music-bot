import sys
import disnake
from disnake.ext import commands
import config
import os
import logging
import asyncio

# Configurar o logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Definir intents: todas as intents ativadas
intents = disnake.Intents.all()

# Configurar o bot
bot = commands.InteractionBot(intents=intents)

# Cogs que serão carregadas
initial_extensions = ['cogs.music']

# Emojis para feedback de log
CHECK_EMOJI = "✅"
ERROR_EMOJI = "❌"
MUSIC_EMOJI = "🎵"

# Evento quando o bot está pronto
@bot.event
async def on_ready():
    logger.info(f"{CHECK_EMOJI} Bot conectado como {bot.user}")
    logger.info(f"{MUSIC_EMOJI} Estou em {len(bot.guilds)} servidores!")

# Evento ao entrar em um novo servidor
@bot.event
async def on_guild_join(guild):
    logger.info(f"📥 Entrei no servidor: {guild.name} (ID: {guild.id})")

# Evento ao sair de um servidor
@bot.event
async def on_guild_remove(guild):
    logger.info(f"📤 Saí do servidor: {guild.name} (ID: {guild.id})")

# Carregar cogs
if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
            logger.info(f"{CHECK_EMOJI} Cog {extension} carregada com sucesso!")
        except Exception as e:
            logger.error(f"{ERROR_EMOJI} Erro ao carregar a cog {extension}: {e}")

# Comando administrativo para reiniciar o bot
@bot.slash_command(description="Reinicia o bot (administrador apenas)")
@commands.has_permissions(administrator=True)
async def restart(inter: disnake.ApplicationCommandInteraction):
    # Embed de confirmação
    embed = disnake.Embed(
        title="Confirmação de Reinício",
        description="Você tem certeza de que deseja reiniciar o bot?",
        color=disnake.Color.orange()
    )

    # Botões de confirmação
    buttons = [
        disnake.ui.Button(label="Reiniciar", style=disnake.ButtonStyle.danger, custom_id="confirm_restart"),
        disnake.ui.Button(label="Cancelar", style=disnake.ButtonStyle.secondary, custom_id="cancel_restart")
    ]

    # Enviar a embed com os botões
    await inter.response.send_message(embed=embed, components=buttons)

# Listener para os botões de confirmação
@bot.listen("on_button_click")
async def on_button_click(interaction: disnake.MessageInteraction):
    if interaction.component.custom_id == "confirm_restart":
        # Confirmação de reinício
        await interaction.response.edit_message(
            content="Reiniciando o bot em 5 segundos...",
            components=[]
        )
        await asyncio.sleep(5)
        os.execv(sys.executable, ['python'] + sys.argv)  # Reinicia o bot

    elif interaction.component.custom_id == "cancel_restart":
        # Cancelamento do reinício
        await interaction.response.edit_message(
            content="Reinício cancelado.",
            components=[]
        )

# Tratamento de erros globais
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Este comando não existe!")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Você não tem permissão para executar este comando.")
    else:
        await ctx.send(f"Ocorreu um erro: {str(error)}")
        logger.error(f"{ERROR_EMOJI} Ocorreu um erro: {str(error)}")

# Rodar o bot
bot.run(config.DISCORD_TOKEN)
