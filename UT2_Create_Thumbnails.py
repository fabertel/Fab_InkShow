import os
from PIL import Image

def create_thumbnails(thumbnail_size=(512, 512)):
    # Define paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    script_folder = os.path.dirname(os.path.abspath(__file__))
    images_folder = os.path.join(BASE_DIR, "static", "images", "Projects")  # ← cambia se serve
    thumbnails_folder = os.path.join(images_folder, "thumbnails")  # ✅ Save in /static/images/thumbnails/

    # Create the "thumbnails" folder if it doesn't exist
    if not os.path.exists(thumbnails_folder):
        os.makedirs(thumbnails_folder)

    # ✅ Clean existing thumbnails
    for file in os.listdir(thumbnails_folder):
        file_path = os.path.join(thumbnails_folder, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

    # ✅ Generate thumbnails from images in /static/images/
    for file in os.listdir(images_folder):
        file_path = os.path.join(images_folder, file)

        # Check if the file is an image
        if os.path.isfile(file_path) and file.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif")):
            try:
                with Image.open(file_path) as img:
                    img.thumbnail(thumbnail_size)

                    # ✅ Save the thumbnail in /static/images/thumbnails/
                    base_name, ext = os.path.splitext(file)
                    thumbnail_name = f"{base_name}_TH{ext}"
                    thumbnail_path = os.path.join(thumbnails_folder, thumbnail_name)
                    img.save(thumbnail_path)

                    print(f"✅ Thumbnail created: {thumbnail_path}")
            except Exception as e:
                print(f"❌ Error processing {file_path}: {e}")

# Run the function
create_thumbnails()
