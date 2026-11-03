"""
quien-no-me-sigue
Mira quién no te sigue de vuelta en Instagram o TikTok
usando la descarga oficial de tus datos (sin iniciar sesión).
"""

import argparse
import csv
import json
import os
import zipfile


# ---------- Leer los archivos ----------

def es_archivo_util(nombre):
    """Devuelve True si el archivo es uno de los que nos interesan."""
    base = os.path.basename(nombre).lower()
    if not base.endswith(".json"):
        return False
    if base.startswith("followers") or base == "following.json":
        return True  # Instagram
    if base.startswith("user_data"):
        return True  # TikTok
    return False


def leer_jsons(ruta):
    """Lee los JSON que nos sirven de un .zip o de una carpeta."""
    archivos = {}

    if os.path.isfile(ruta) and zipfile.is_zipfile(ruta):
        with zipfile.ZipFile(ruta) as z:
            for nombre in z.namelist():
                if es_archivo_util(nombre):
                    with z.open(nombre) as f:
                        archivos[nombre] = json.load(f)

    elif os.path.isdir(ruta):
        for carpeta, _, ficheros in os.walk(ruta):
            for fichero in ficheros:
                completo = os.path.join(carpeta, fichero)
                if es_archivo_util(completo):
                    with open(completo, encoding="utf-8") as f:
                        archivos[completo] = json.load(f)

    elif os.path.isfile(ruta) and es_archivo_util(ruta):
        with open(ruta, encoding="utf-8") as f:
            archivos[ruta] = json.load(f)

    else:
        raise SystemExit(f"No encuentro '{ruta}'. Pon la ruta del .zip o de la carpeta.")

    return archivos


# ---------- Instagram ----------

def nombres_instagram(datos):
    """Saca los nombres de usuario de followers_X.json o following.json."""
    nombres = set()

    # following.json viene como {"relationships_following": [...]}
    if isinstance(datos, dict):
        lista = []
        for valor in datos.values():
            if isinstance(valor, list):
                lista += valor
    else:
        lista = datos

    for item in lista:
        if not isinstance(item, dict):
            continue
        for entrada in item.get("string_list_data", []):
            nombre = entrada.get("value") or item.get("title")
            # A veces solo viene el enlace al perfil
            if not nombre and entrada.get("href"):
                nombre = entrada["href"].rstrip("/").split("/")[-1]
            if nombre:
                nombres.add(nombre.lower())

    return nombres


# ---------- TikTok ----------

def agregar_tiktok(lista, destino):
    for persona in lista:
        if isinstance(persona, dict) and persona.get("UserName"):
            destino.add(persona["UserName"].lower())


def buscar_tiktok(datos, seguidores, seguidos):
    """Recorre el JSON de TikTok buscando las listas de seguidores y seguidos."""
    if isinstance(datos, dict):
        for clave, valor in datos.items():
            if clave == "FansList" and isinstance(valor, list):
                agregar_tiktok(valor, seguidores)
            elif clave == "Following" and isinstance(valor, list):
                agregar_tiktok(valor, seguidos)
            else:
                buscar_tiktok(valor, seguidores, seguidos)
    elif isinstance(datos, list):
        for valor in datos:
            buscar_tiktok(valor, seguidores, seguidos)


# ---------- Juntarlo todo ----------

def cargar_cuenta(ruta):
    """Devuelve (plataforma, seguidores, seguidos) de una exportación."""
    seguidores = set()
    seguidos = set()
    plataforma = None

    for nombre, datos in leer_jsons(ruta).items():
        base = os.path.basename(nombre).lower()
        if base.startswith("followers"):
            plataforma = "Instagram"
            seguidores |= nombres_instagram(datos)
        elif base == "following.json":
            plataforma = "Instagram"
            seguidos |= nombres_instagram(datos)
        elif base.startswith("user_data"):
            plataforma = "TikTok"
            buscar_tiktok(datos, seguidores, seguidos)

    if not seguidores and not seguidos:
        raise SystemExit(
            f"No he encontrado seguidores ni seguidos en '{ruta}'.\n"
            "Comprueba que descargaste los datos en formato JSON (no HTML)."
        )

    return plataforma, seguidores, seguidos


def mostrar(titulo, nombres):
    print(f"\n{titulo} ({len(nombres)})")
    print("-" * (len(titulo) + len(str(len(nombres))) + 3))
    if not nombres:
        print("  (nadie)")
    for nombre in sorted(nombres):
        print(f"  @{nombre}")


def guardar_csv(archivo, resultados):
    with open(archivo, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["categoria", "usuario"])
        for categoria, nombres in resultados.items():
            for nombre in sorted(nombres):
                escritor.writerow([categoria, nombre])
    print(f"\nResultados guardados en {archivo}")


def main():
    parser = argparse.ArgumentParser(
        description="Mira quién no te sigue de vuelta en Instagram o TikTok."
    )
    parser.add_argument("export", help="El .zip o la carpeta con tus datos descargados")
    parser.add_argument("--antes", help="Una exportación más antigua para ver quién te ha dejado de seguir")
    parser.add_argument("--csv", nargs="?", const="resultados.csv",
                        help="Guarda los resultados en un CSV (por defecto resultados.csv)")
    args = parser.parse_args()

    plataforma, seguidores, seguidos = cargar_cuenta(args.export)

    resultados = {
        "no_te_siguen": seguidos - seguidores,
        "no_sigues_tu": seguidores - seguidos,
        "mutuos": seguidores & seguidos,
    }

    if args.antes:
        _, seguidores_antes, _ = cargar_cuenta(args.antes)
        resultados["te_dejaron_de_seguir"] = seguidores_antes - seguidores
        resultados["nuevos_seguidores"] = seguidores - seguidores_antes

    print(f"\n=== quien-no-me-sigue | {plataforma} ===")
    print(f"Seguidores: {len(seguidores)}")
    print(f"Seguidos:   {len(seguidos)}")

    mostrar("No te siguen de vuelta", resultados["no_te_siguen"])
    mostrar("Te siguen pero tú no a ellos", resultados["no_sigues_tu"])
    print(f"\nMutuos: {len(resultados['mutuos'])}")

    if args.antes:
        mostrar("Te han dejado de seguir", resultados["te_dejaron_de_seguir"])
        mostrar("Seguidores nuevos", resultados["nuevos_seguidores"])

    if args.csv:
        guardar_csv(args.csv, resultados)


if __name__ == "__main__":
    main()
