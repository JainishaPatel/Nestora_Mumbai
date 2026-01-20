import os
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()

STATIC_DIR = "static/images"
CLOUD_FOLDER = "defaults"

images_list = []

for filename in os.listdir(STATIC_DIR):
    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        result = cloudinary.uploader.upload(
            os.path.join(STATIC_DIR, filename),
            folder=CLOUD_FOLDER,
            public_id=os.path.splitext(filename)[0],
            overwrite=True,
            resource_type="image"
        )

        images_list.append({
            "url": result["secure_url"],      # URL for front-end
            "public_id": result["public_id"]  # Cloudinary ID for delete/update
        })

        print("Uploaded:", filename)

# Now you can store images_list as JSON in your DB
import json
images_json = json.dumps(images_list)
print("Images JSON to store in DB:", images_json)
