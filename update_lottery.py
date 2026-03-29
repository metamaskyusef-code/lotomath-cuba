import re
from datetime import datetime

def update_lottery():
    # --- CONFIGURACIÓN DE LOS NUEVOS NÚMEROS ---
    # Aquí es donde pondrás los resultados del día
    nuevos_nums = [3, 8, 2] 
    fecha_hoy = datetime.now().strftime("%m/%d")
    momento = "Noche" # Puede ser "Noche" o "Mediodía"

    # 1. Leer el archivo index.html
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print("Error: No se encontró index.html")
        return

    # 2. EL PATRÓN (La brújula)
    # Este patrón busca 'pick3fl: {' seguido de 'results: ['
    patron = r"(pick3fl:\{.*?results:\[)(.*?)(\])"

    def reemplazar(match):
        prefix = match.group(1) # Parte inicial: pick3fl:{...results:[
        # Creamos el nuevo registro con el formato exacto de tu JS
        nuevo_item = f"{{date:'{fecha_hoy}', time:'{momento}', nums:{nuevos_nums}}}"
        
        # Recuperamos los resultados viejos y los limpiamos
        viejos = match.group(2).split('},')
        # Reconstruimos la lista manteniendo máximo 10 resultados para que la web no pese
        viejos_limpios = [v.strip() + '}' if not v.strip().endswith('}') else v.strip() for v in viejos if v.strip()]
        
        # Unimos el nuevo con los anteriores
        nueva_lista = nuevo_item + ", " + ", ".join(viejos_limpios[:9])
        return prefix + nueva_lista + "]"

    # 3. Aplicar el cambio con Regex (el "patrón")
    nuevo_html = re.sub(patron, reemplazar, content, flags=re.DOTALL)

    # 4. Guardar los cambios
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(nuevo_html)
    
    print(f"✅ Éxito: Se actualizó Pick 3 con {nuevos_nums}")

if __name__ == "__main__":
    update_lottery()
