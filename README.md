# Quién no me sigue

**Descubre quién no te sigue de vuelta en Instagram y TikTok, sin dar tu contraseña.**

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Sin dependencias](https://img.shields.io/badge/dependencias-ninguna-brightgreen)
![Licencia MIT](https://img.shields.io/badge/licencia-MIT-lightgrey)

La mayoría de apps que hacen esto te piden iniciar sesión con tu cuenta. Eso es peligroso: te pueden robar la cuenta o Instagram te la puede bloquear por actividad rara.

**Esta herramienta funciona de otra forma:** usa el archivo con tus datos que te da la propia red social. Todo se hace en tu ordenador, sin internet y sin login.

---

## ¿Qué te dice?

- 👀 Quién **no te sigue de vuelta**
- 🙋 Quién te sigue pero **tú no a él**
- 🤝 Cuántos seguidores **mutuos** tienes
- 📉 Quién **te ha dejado de seguir** (comparando con una descarga anterior)
- 📈 Quién **te ha empezado a seguir**
- 💾 Opción de guardarlo todo en un **CSV** para abrirlo con Excel

---

## Cómo usarlo (en 3 pasos)

### 1. Descarga tus datos

<details>
<summary><b>📸 Instagram</b></summary>

1. Ve a **Configuración** → **Centro de cuentas** → **Tu información y permisos**
2. Entra en **Descargar tu información**
3. Elige **Parte de tu información** y marca solo **Seguidores y seguidos**
4. Muy importante: en formato elige **JSON** (no HTML)
5. Cuando te llegue el aviso, descarga el `.zip`

</details>

<details>
<summary><b>🎵 TikTok</b></summary>

1. Ve a tu **Perfil** → menú **☰** → **Ajustes y privacidad**
2. Entra en **Cuenta** → **Descargar tus datos**
3. En formato elige **JSON**
4. Pulsa **Solicitar datos**
5. Cuando esté listo, ve a la pestaña **Descargar datos** y bájate el archivo

</details>

> Los menús pueden cambiar un poco según la versión de la app. Si no lo encuentras, busca "descargar tus datos" en la configuración.

> ⏳ La descarga no es inmediata. Puede tardar desde unos minutos hasta un par de días.

### 2. Descarga el proyecto

```bash
git clone https://github.com/bgarciaa181/quien-no-me-sigue.git
cd quien-no-me-sigue
```

Solo necesitas tener **Python 3.8 o superior**. No hay que instalar nada más.

### 3. Ejecútalo

Pon el archivo que descargaste (`.zip` o carpeta) en la carpeta del proyecto y ejecuta:

```bash
python quien_no_me_sigue.py instagram.zip
```

¡Y listo! 🎉

---

## Ejemplo de resultado

```
=== quien-no-me-sigue | Instagram ===
Seguidores: 4
Seguidos:   4

No te siguen de vuelta (2)
--------------------------
  @exnovio99
  @famoso_oficial

Te siguen pero tú no a ellos (2)
--------------------------------
  @marta22
  @nuevo_fan

Mutuos: 2

Te han dejado de seguir (1)
---------------------------
  @el_que_se_fue
```

---

## Más opciones

| Quiero... | Comando |
|---|---|
| Ver mis resultados | `python quien_no_me_sigue.py instagram.zip` |
| Usar una carpeta en vez del zip | `python quien_no_me_sigue.py mi_carpeta/` |
| Ver quién me ha dejado de seguir | `python quien_no_me_sigue.py nuevo.zip --antes viejo.zip` |
| Guardarlo en un CSV | `python quien_no_me_sigue.py instagram.zip --csv` |
| Ver la ayuda | `python quien_no_me_sigue.py --help` |

💡 **Truco:** guarda cada descarga con la fecha (por ejemplo `instagram_2026-11.zip`). Así el mes que viene puedes compararlas y ver quién se ha ido.

---

## 🔒 Privacidad

- No pide usuario ni contraseña
- No se conecta a internet
- No envía tus datos a ningún sitio
- El código es corto y abierto, puedes leerlo entero en un rato

⚠️ **Ojo:** no subas tus `.zip` ni tus `.json` a GitHub. El archivo `.gitignore` del proyecto ya los ignora para que no se suban sin querer.

---

## Problemas comunes

**"No he encontrado seguidores ni seguidos"**
Seguramente descargaste los datos en formato HTML. Vuelve a pedirlos y elige **JSON**.

**"No encuentro el archivo"**
Revisa que el nombre está bien escrito y que estás en la carpeta correcta. Si el nombre tiene espacios, ponlo entre comillas: `python quien_no_me_sigue.py "mis datos.zip"`

**En Windows `python` no funciona**
Prueba con `py quien_no_me_sigue.py instagram.zip`

---

## Ideas para el futuro

- [ ] Versión web: arrastrar el zip y ver los resultados en el navegador
- [ ] Gráfica de cómo cambian tus seguidores con el tiempo
- [ ] Soporte para más redes sociales

¿Tienes alguna idea o encontraste un fallo? Abre un [issue](https://github.com/bgarciaa181/quien-no-me-sigue/issues) 🙌

---

## Autora

Hecho por **Bea García** ([@bgarciaa181](https://github.com/bgarciaa181)), estudiante de ASIR en Granada.

Si te ha servido, deja una ⭐ en el repo, ¡me ayuda mucho!

## Licencia

MIT. Puedes usarlo, cambiarlo y compartirlo libremente.
