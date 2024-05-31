# Números - El Bot de Discord para Adivinar Códigos 🕵️‍♂️

¡Bienvenido al desafío de Números! Este bot te trae un divertido minijuego para poner a prueba tu intuición y habilidades de deducción. 

## Para jugadores 🎲

**¿Cómo jugar?**

1. **Espera a que un administrador inicie el juego:** Solo los administradores del servidor pueden iniciar el juego usando el comando `/start`.
2. **Elige tu idioma (opcional):** Si quieres jugar en un idioma diferente al español (por defecto), usa el comando `/lang` y selecciona tu idioma preferido.
3. **Adivina el código:** Una vez iniciado el juego, escribe un número de 4 dígitos (entre 0001 y 9999) en el canal designado.
4. **Pistas y aciertos:** El bot te responderá con imágenes para indicarte si estás cerca o lejos de la solución. ¡Sigue intentando hasta que aciertes!
5. **¡El primero gana!** El primer jugador en adivinar el código secreto se llevará un premio de 5€.

## Para desarrolladores 🛠️

### 📂 Estructura del Proyecto

- `bot.py`: Lógica principal, eventos, comandos y gestión del juego.
- `config.py`: Configuración (token, imágenes, canal, código secreto, usuarios permitidos).
- `mensajes.py`: Diccionario con mensajes en diferentes idiomas.
- `idiomas_usuarios.json`: Almacena las preferencias de idioma.

### ⚙️ Componentes Clave

- **Comandos Slash:**
  - `/start`: Inicia el juego, reinicia el código secreto y borra las preferencias de idioma. (Solo para administradores)
  - `/lang`: Permite a los usuarios cambiar su idioma preferido.

- **Eventos:**
  - `on_ready`: Sincroniza comandos con Discord, carga preferencias de idioma y muestra un mensaje de confirmación en la consola.
  - `on_message`: Procesa los intentos de los usuarios, valida el código (4 dígitos, entre 0001 y 9999), verifica el idioma del usuario y envía respuestas (imagen de acierto o fallo).

- **Gestión de Idiomas:**
  - Soporta múltiples idiomas (definidos en `mensajes.py`).
  - Utiliza el idioma preferido del usuario (almacenado en `idiomas_usuarios.json`) o el predeterminado de Discord si no se ha seleccionado uno.

- **Persistencia de Datos:** Las preferencias de idioma se guardan en `idiomas_usuarios.json`.

### 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python 3.x
- **Librería:** discord.py (versión 2.0)
- **Almacenamiento de datos:** JSON
- **Expresiones regulares (Regex):** Para validar los códigos.
