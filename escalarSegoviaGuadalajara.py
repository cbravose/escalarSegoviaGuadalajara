
# Crear carpeta de salida si no existe
os.makedirs("salidas", exist_ok=True)

# Leer frases desde archivo .txt
with open("frases.txt", "r", encoding="utf-8") as f:
    frases = [line.strip() for line in f if line.strip()]

# Procesar cada frase
for i, frase in enumerate(frases, 1):
    doc = nlp(frase)

    # Extraer ubicaciones
    ubicaciones = [ent.text for ent in doc.ents if ent.label_ in ["LOC", "GPE"]]

    # Extraer información básica por búsqueda de palabras clave
    actividad = None
    problema = None
    causa = None
    efecto = None

    for token in doc:
        if "escalada" in token.text.lower():
            actividad = "escalada deportiva"
        elif "senderismo" in token.text.lower():
            actividad = "senderismo"

        if "problema" in token.lemma_ or "conflicto" in token.lemma_:
            problema = token.sent.text
        if "masificación" in token.text.lower() or "saturación" in token.text.lower():
            efecto = token.text
        if "publicar" in token.lemma_ or "difundir" in token.lemma_ or "cerrar" in token.lemma_:
            causa = token.sent.text

    resultado = {
        "frase_original": frase,
        "ubicaciones": ubicaciones,
        "actividad": actividad,
        "causa": causa,
        "problema": problema,
        "efecto": efecto
    }

    # Guardar resultado como archivo JSON individual
    output_path = f"salidas/frase_{i}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    print(f"✅ Procesado y guardado: {output_path}")
