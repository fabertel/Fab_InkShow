import os
import pandas as pd
from datetime import datetime
from PIL import Image
from math import gcd

# === Percorsi ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_folder = os.path.join(BASE_DIR, "static", "images", "DIGITAL")  # ← cambia se serve
output_excel = os.path.join(BASE_DIR, "gallery_json_digi.xlsx")

# === Parametri predefiniti ===
default_price = "EUR 55"
default_availability = "Available"
default_category = "digi"
default_medium = "Digitale"
default_tags = "auto"
default_description = "TODO"

def get_ratio(width, height):
    r = gcd(width, height)
    return f"{width // r}:{height // r}"

# === Estrai dati immagini ===
rows = []
for filename in sorted(os.listdir(image_folder)):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        filepath = os.path.join(image_folder, filename)
        created = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime("%Y-%m-%d %H:%M:%S")

        try:
            with Image.open(filepath) as img:
                w, h = img.size
                ratio = get_ratio(w, h)
        except:
            ratio = "?"

        name_no_ext = os.path.splitext(filename)[0]

        rows.append({
            "src": f"images/{filename}",
            "filename": filename,
            "title": name_no_ext,
            "description": default_description,
            "size": ratio,
            "price": default_price,
            "availability": default_availability,
            "category": default_category,
            "medium": default_medium,
            "tags": default_tags,
            "created_date": created
        })

# === Salva in Excel ===
df = pd.DataFrame(rows)
df.to_excel(output_excel, index=False)
print(f"✅ File creato: {output_excel}")
