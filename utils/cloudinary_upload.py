import cloudinary.uploader

def upload_image_to_cloudinary(file, property_id):
    """
    Upload image to Cloudinary inside property folder
    """
    result = cloudinary.uploader.upload(
        file,
        folder=f"properties/{property_id}",
        resource_type="image",
        use_filename=True,
        unique_filename=True,
        overwrite=False,
        transformation=[
            {"width": 1200, "height": 800, "crop": "limit"},
            {"quality": "auto"},
            {"fetch_format": "auto"}
        ]
    )

    return {
        "url": result["secure_url"],
        "public_id": result["public_id"]
    }
