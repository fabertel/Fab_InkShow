import os

# 🔧 Inserisci qui il path della cartella da pulire
FOLDER_PATH = "/home/fabio/code/Fab_InkShow/static/videos/"

def clean_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            # Rimuove file tipo ":Zone.Identifier"
            if ":Zone.Identifier" in filename:
                full_path = os.path.join(root, filename)
                try:
                    os.remove(full_path)
                    print(f"Deleted: {full_path}")
                except Exception as e:
                    print(f"Error deleting {full_path}: {e}")
                continue

            # Rinomina file con spazi → underscore
            if " " in filename:
                old_path = os.path.join(root, filename)
                new_filename = filename.replace(" ", "_")
                new_path = os.path.join(root, new_filename)
                try:
                    os.rename(old_path, new_path)
                    print(f"Renamed: {old_path} → {new_path}")
                except Exception as e:
                    print(f"Error renaming {old_path}: {e}")

if __name__ == "__main__":
    clean_folder(FOLDER_PATH)
