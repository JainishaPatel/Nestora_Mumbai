from models import Property
from .users import u1, u2, u3
from utils import DEFAULT_IMAGES
import uuid

p1 = Property(
        id = str(uuid.uuid4()),
        user_id=u1.user_id,
        title="1 BHK Borivali East",
        area="Borivali",
        direction="East",
        city="Mumbai",
        property_type="Rent",
        bhk="1 BHK",
        furnishing="Semi-Furnished",
        price=22000,
        price_type="per month",
        images=[
            DEFAULT_IMAGES["image_1.png"],
            DEFAULT_IMAGES["image_2.png"],
            DEFAULT_IMAGES["image_3.png"],
            DEFAULT_IMAGES["image_4.png"],
        ],
        floor=3,
        total_floors=7,
        bathrooms=1,
        parking=True,
        lift=True,
        owner_type="Owner",
        deposit=60000
    )

p2 = Property(
        id = str(uuid.uuid4()),
        user_id=u1.user_id,
        title="2 BHK Andheri West",
        area="Andheri",
        direction="West",
        city="Mumbai",
        property_type="Rent",
        bhk="2 BHK",
        furnishing="Furnished",
        price=45000,
        price_type="per month",
        images=[
            DEFAULT_IMAGES["image_2.png"],
            DEFAULT_IMAGES["image_3.png"],
            DEFAULT_IMAGES["image_4.png"],
        ],
        floor=5,
        lift=True,
        water_supply="BMC",
        owner_type="Agent",
        deposit=120000
    )

p3 = Property(
        id = str(uuid.uuid4()),
        user_id=u1.user_id,
        title="3 BHK Powai Lake View",
        area="Powai",
        direction="East",
        city="Mumbai",
        property_type="Buy",
        bhk="3 BHK",
        furnishing="Unfurnished",
        price=18500000,
        price_type="total",
        images=[
            DEFAULT_IMAGES["image_3.png"],
            DEFAULT_IMAGES["image_4.png"],
            DEFAULT_IMAGES["image_1.png"],
        ],
        carpet_area=1200,
        balcony=True,
        parking=True,
        owner_type="Owner"
    )

p4 = Property(
        id = str(uuid.uuid4()),
        user_id=u1.user_id,
        title="1 RK Malad West",
        area="Malad",
        direction="West",
        city="Mumbai",
        property_type="Rent",
        bhk="1 RK",
        furnishing="Unfurnished",
        price=15000,
        price_type="per month",
        images=[
            DEFAULT_IMAGES["image_1.png"],
            DEFAULT_IMAGES["image_2.png"],
            DEFAULT_IMAGES["image_3.png"],
            DEFAULT_IMAGES["image_4.png"],
        ],
        floor=2,
        bathrooms=1,
        owner_type="Owner"
    )

p5 = Property(
        id = str(uuid.uuid4()),
        user_id=u1.user_id,
        title="2 BHK Goregaon East",
        area="Goregaon",
        direction="East",
        city="Mumbai",
        property_type="Rent",
        bhk="2 BHK",
        furnishing="Semi-Furnished",
        price=32000,
        price_type="per month",
        images=[
            DEFAULT_IMAGES["image_2.png"],
            DEFAULT_IMAGES["image_3.png"],
        ],
        parking=True,
        gas_pipeline=True,
        owner_type="Agent"
    )

p6 = Property(
        id = str(uuid.uuid4()),
        user_id=u2.user_id,
        title="Studio Apartment Bandra",
        area="Bandra",
        direction="West",
        city="Mumbai",
        property_type="Rent",
        bhk="Studio",
        furnishing="Furnished",
        price=38000,
        price_type="per month",
        images=[
            DEFAULT_IMAGES["image_1.png"],
            DEFAULT_IMAGES["image_2.png"],
            DEFAULT_IMAGES["image_3.png"],
            DEFAULT_IMAGES["image_4.png"],
        ],
        lift=True,
        nearby_metro="Bandra",
        owner_type="Owner"
    )

p7 = Property(
        id = str(uuid.uuid4()),
        user_id=u2.user_id,
        title="Luxury 4 BHK Juhu",
        area="Juhu",
        direction="West",
        city="Mumbai",
        property_type="Buy",
        bhk="4 BHK",
        furnishing="Furnished",
        price=65000000,
        price_type="total",
        images=[
            DEFAULT_IMAGES["default_property.png"],
            DEFAULT_IMAGES["image_4.png"],
        ],
        balcony=True,
        parking=True,
        owner_type="Agent"
    )

p8 = Property(
        id = str(uuid.uuid4()),
        user_id=u2.user_id,
        title="2 BHK Kandivali East",
        area="Kandivali",
        direction="East",
        city="Mumbai",
        property_type="Rent",
        bhk="2 BHK",
        furnishing="Unfurnished",
        price=27000,
        price_type="per month",
        images=[
            DEFAULT_IMAGES["default_property.png"],
            DEFAULT_IMAGES["image_3.png"],
        ],
        floor=6,
        lift=True,
        owner_type="Owner"
    )

p9 = Property(
        id = str(uuid.uuid4()),
        user_id=u2.user_id,
        title="1 BHK Chembur",
        area="Chembur",
        direction="East",
        city="Mumbai",
        property_type="Rent",
        bhk="1 BHK",
        furnishing="Semi-Furnished",
        price=25000,
        price_type="per month",
        images=[
            DEFAULT_IMAGES["default_property.png"],
            DEFAULT_IMAGES["image_1.png"],
        ],
        water_supply="Both",
        gas_pipeline=True,
        owner_type="Agent"
    )

p10 = Property(
        id = str(uuid.uuid4()),
        user_id=u2.user_id,
        title="3 BHK Thane West",
        area="Thane",
        direction="West",
        city="Mumbai",
        property_type="Buy",
        bhk="3 BHK",
        furnishing="Unfurnished",
        price=14500000,
        price_type="total",
        images=[
            DEFAULT_IMAGES["image_2.png"],
            DEFAULT_IMAGES["image_3.png"],
            DEFAULT_IMAGES["image_4.png"],
        ],
        carpet_area=980,
        owner_type="Owner"
    )

p11 = Property(
        id = str(uuid.uuid4()),
        user_id=u3.user_id,
        title="Affordable 1 BHK Mira Road",
        area="Mira Road",
        direction="East",
        city="Mumbai",
        property_type="Rent",
        bhk="1 BHK",
        furnishing="Unfurnished",
        price=18000,
        price_type="per month",
        images=[
            DEFAULT_IMAGES["default_property.png"],
            DEFAULT_IMAGES["image_3.png"],
        ],
        bathrooms=1,
        owner_type="Owner"
    )

p12 = Property(
        id = str(uuid.uuid4()),
        user_id=u3.user_id,
        title="Penthouse Lower Parel",
        area="Lower Parel",
        direction="West",
        city="Mumbai",
        property_type="Buy",
        bhk="4 BHK",
        furnishing="Furnished",
        price=82000000,
        price_type="total",
        images=[
            DEFAULT_IMAGES["image_2.png"],
            DEFAULT_IMAGES["image_3.png"],
            DEFAULT_IMAGES["image_4.png"],
        ],
        balcony=True,
        parking=True,
        lift=True,
        owner_type="Agent"
    )

properties = [p1, p2 , p3, p4, p5, p6, p7, p8, p9, p10, p11, p12]
