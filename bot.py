import discord
import re
import json
from discord import app_commands
from config import TOKEN, IMAGEN_ACIERTO, IMAGEN_FALLO, CANAL_ID, CODIGO_SECRETO, USUARIOS_PERMITIDOS
from mensajes import mensajes

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

# Archivo para guardar los idiomas
ARCHIVO_IDIOMAS = "idiomas_usuarios.json"

# Cargar idiomas al iniciar el bot
try:
    with open(ARCHIVO_IDIOMAS, "r") as f:
        idiomas_usuarios = json.load(f)
except FileNotFoundError:
    idiomas_usuarios = {}

# Variable para controlar si el juego está iniciado (declarada como global)
juego_iniciado = False 

@bot.event
async def on_ready():
    await tree.sync()
    print(f'Bot conectado como {bot.user.name}')

# Lista de idiomas soportados (obtenida dinámicamente desde mensajes.py)
IDIOMAS_SOPORTADOS = [
    app_commands.Choice(name=mensajes[lang]["nombre_idioma"], value=lang)
    for lang in mensajes.keys()
]

@tree.command(name="start", description="Iniciar el minijuego de adivinar el código")
async def start_game(interaction: discord.Interaction):
    global juego_iniciado  # Acceder a la variable global
    if interaction.user.id not in USUARIOS_PERMITIDOS:
        await interaction.response.send_message("No tienes permiso para iniciar el juego.", ephemeral=True)
        return

    if juego_iniciado:
        await interaction.response.send_message("El juego ya está en curso.", ephemeral=True)
        return

    juego_iniciado = True  # Marcar el juego como iniciado
    await interaction.response.send_message(mensajes["es"]["inicio"])  # Mensaje de inicio en español

@tree.command(name="lang", description="Cambiar tu idioma")
@app_commands.describe(idioma="Elige tu nuevo idioma")
@app_commands.choices(idioma=IDIOMAS_SOPORTADOS)
async def cambiar_idioma(interaction: discord.Interaction, idioma: app_commands.Choice[str]):
    idiomas_usuarios[str(interaction.user.id)] = idioma.value
    await interaction.response.send_message(mensajes[idioma.value]["confirmacion_idioma"])
    guardar_idiomas()

@bot.event
async def on_message(message: discord.Message):
    global juego_iniciado  # Declarar juego_iniciado como global aquí también

    if message.author == bot.user or message.author.bot:
        return

    if message.channel.id != CANAL_ID:
        return

    if message.content.startswith("/"):
        return

    # Si el mensaje es un código de 4 dígitos y el juego está iniciado
    if juego_iniciado and re.match(r'^\d{4}$', message.content):
        codigo = message.content

        # Obtener el idioma del usuario (usando preferred_locale o locale según el tipo de objeto)
        if isinstance(message.author, discord.Member):
            idioma = idiomas_usuarios.get(str(message.author.id), message.guild.preferred_locale)
        else:  # Si es un User
            try:
                idioma = str(message.author.locale).split('-')[0]
            except AttributeError:
                idioma = "es"

        # Corrección: Asegurar que el idioma esté en el diccionario mensajes
        if idioma not in mensajes:
            idioma = "es"  # Usar español como idioma por defecto si el idioma no está soportado

        if 1 <= int(codigo) <= 9999:
            if codigo == CODIGO_SECRETO:
                await message.reply(IMAGEN_ACIERTO)
                await message.channel.send(f"{message.author.mention} {mensajes[idioma]['victoria']}")
                # No borrar el idioma del usuario
                juego_iniciado = False  # Reiniciar el juego al ganar
            else:
                await message.reply(IMAGEN_FALLO)
        else:
            await message.reply(mensajes[idioma]["formato_incorrecto"])

def guardar_idiomas():
    with open(ARCHIVO_IDIOMAS, "w") as f:
        json.dump(idiomas_usuarios, f)

bot.run(TOKEN)
