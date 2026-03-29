import re
from datetime import datetime

def update_index():
    # 1. Configuración de los nuevos números (Esto lo puedes cambiar manual o automatizar)
    # Ejemplo: Florida Pick 3 Noche
    nuevos_nums = [1, 0, 2] 
    fecha_hoy = datetime.now().strftime("%m/%d")
    momento = "Noche" # o "Mediodía"

    # 2. Leer el archivo HTML
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print("Error: No se encontró index.html")
        return

    # 3. El PATRÓN (La brújula que te mencioné)
    # Busca la sección pick3fl -> results: [
    patron = r"(pick3fl:\{.*?results:\[)(.*?)(\])"

    def rotar_datos(match):
        prefix = match.group(1) # pick3fl:{...results:[
        datos_viejos = match.group(2) # Todo lo que está entre [ y ]
        
        # Creamos el nuevo registro
        nuevo_registro = f"{{date:'{fecha_hoy}', time:'{momento}', nums:{nuevos_nums}}}"
        
        # Limpiamos y cortamos para mantener solo los últimos 10 resultados (para que no pese)
        lista_viejos = datos_viejos.split('},')
        # Limpieza de espacios y comas
        lista_viejos = [v.strip() + '}' if not v.strip().endswith('}') else v.strip() for v in lista_viejos if v.strip()]
        
        # Unimos el nuevo con los mejores 9 antiguos
        nueva_lista = nuevo_registro + ", " + ", ".join(lista_viejos[:9])
        
        return prefix + nueva_lista + "]"

    # 4. Inyectar los datos
    nuevo_contenido = re.sub(patron, rotar_datos, content, flags=re.DOTALL)

    # 5. Guardar los cambios
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(nuevo_contenido)
    print(f"✅ Éxito: Se inyectó el resultado {nuevos_nums} en el histórico.")

if __name__ == "__main__":
    update_index()
