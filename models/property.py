from utils import format_indian_currency
from dotenv import load_dotenv
import os
import json
load_dotenv()

CLOUDINARY_DEFAULT_IMAGE = (
    f"https://res.cloudinary.com/"
    f"{os.getenv('CLOUDINARY_CLOUD_NAME')}/image/upload/"
    "w_800,h_600,c_fill,q_auto,f_auto/default_property.png"
)

class Property:
    def __init__(
        self, 
        id,
        user_id, 
        title, area, direction, city, property_type, bhk, furnishing,
        price, price_type, images,
        
        # Property Info
        floor=None,
        total_floors=None,
        carpet_area=None,
        balcony=False,
        bathrooms=None,
        toilet_type=None,
        age_of_property=None,

        # Amenities
        parking=False,
        lift=False,
        water_supply=None,        # BMC / Borewell / Both
        gas_pipeline=False,

        # Location Extras
        landmark=None,
        nearby_metro=None,
        nearby_school=None,
        nearby_hospital=None,

        # Ownership & Legal
        owner_type=None,          # Owner / Agent
        deposit=None,
        maintenance_charge=None,
        posted_on=None,

        is_verified=None, 
        is_available=None,
    ):
        
        # Identity
        self.id = id 
        self.user_id = user_id

        # Basic Details
        self.title = title
        self.property_type = property_type  # Rent / Buy
        self.bhk = bhk

        # Location
        self.area = area
        self.direction = direction
        self.city = city
        
        # Price
        self.price = price
        self.formatted_price = format_indian_currency(price) 
        self.price_type = price_type   # per month / total

        # Property Info
        self.floor = floor
        self.total_floors = total_floors
        self.carpet_area = carpet_area
        self.bathrooms = bathrooms
        self.toilet_type = toilet_type
        self.furnishing = furnishing
        self.balcony = balcony
        self.age_of_property = age_of_property

        # Amenities
        self.parking = parking
        self.lift = lift
        self.water_supply = water_supply
        self.gas_pipeline = gas_pipeline

        # Location Extras
        self.landmark = landmark
        self.nearby_metro = nearby_metro
        self.nearby_school = nearby_school
        self.nearby_hospital = nearby_hospital

        #  Ownership & Legal
        self.owner_type = owner_type
        self.deposit = deposit
        self.maintenance_charge = maintenance_charge
        self.posted_on = posted_on
        
        # Media (Cloudinary ONLY)
        if isinstance(images, list) and images:
            # Already a list of Cloudinary URLs
            self.images = images

        elif isinstance(images, str):
            # JSON string from DB
            try:
                parsed = json.loads(images)
                if isinstance(parsed, list) and parsed:
                    self.images = parsed
                else:
                    self.images = [CLOUDINARY_DEFAULT_IMAGE]
            except json.JSONDecodeError:
                self.images = [CLOUDINARY_DEFAULT_IMAGE]

        else:
            # None / empty / unexpected
            self.images = [CLOUDINARY_DEFAULT_IMAGE]
        
        # Status & Trust
        self.is_verified = bool(is_verified) if is_verified is not None else False
        self.is_available = bool(is_available) if is_available is not None else True



    # ---------- Image Helpers (Cloudinary) ----------

    def _cloudinary_transform(self, image, transformation):
        """
        Apply Cloudinary transformation safely.
        Accepts either a URL string or a dict with 'url'.
        Always returns a URL string.
        """
        if not image:
            return ""

        # If image is a dict (Cloudinary metadata)
        if isinstance(image, dict):
            url = image.get("url", "")
        else:
            url = image

        # If not a Cloudinary upload URL, return as-is
        if "/upload/" not in url:
            return url

        # Prevent double transformation
        if "/upload/w_" in url:
            return url

        return url.replace(
            "/upload/",
            f"/upload/{transformation}/"
        )

    def cover_image(self):
        """
        Main image for cards / listings
        """
        return self._cloudinary_transform(
            self.images[0],
            "w_800,h_600,c_fill,q_auto,f_auto"
        )

    def all_images(self):
        """
        Images for detail page / gallery
        """
        return [
            self._cloudinary_transform(
                img,
                "w_1200,h_800,c_limit,q_auto,f_auto"
            )
            for img in self.images
        ]
