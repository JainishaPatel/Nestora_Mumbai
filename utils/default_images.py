import os

CLOUD = os.getenv("CLOUDINARY_CLOUD_NAME")

BASE = (
    f"https://res.cloudinary.com/{CLOUD}/image/upload/"
    "w_1200,h_800,c_limit,q_auto,f_auto"
)

DEFAULT_IMAGES = {
    "default_property.png": {"url": f"{BASE}/defaults/default_property.png", "public_id": "defaults/default_property"},
    "image_1.png": {"url": f"{BASE}/defaults/image_1.png", "public_id": "defaults/image_1"},
    "image_2.png": {"url": f"{BASE}/defaults/image_2.png", "public_id": "defaults/image_2"},
    "image_3.png": {"url": f"{BASE}/defaults/image_3.png", "public_id": "defaults/image_3"},
    "image_4.png": {"url": f"{BASE}/defaults/image_4.png", "public_id": "defaults/image_4"},
}
