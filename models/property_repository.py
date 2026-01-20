from models import db_connection
import json
import uuid



# ---------------- INSERT PROPERTY ----------------
def insert_property(property):
    """
    Inserts a new property into the database.
    Images are stored as a JSON string (list of dicts with url & public_id).
    """
    db = db_connection()
    cursor = db.cursor()

    sql = """
    INSERT INTO properties(
        id, user_id,
        title, area, direction, city, property_type,
        bhk, furnishing, price, price_type, images,
        floor, total_floors, carpet_area, bathrooms, toilet_type, age_of_property,
        balcony, parking,  lift, gas_pipeline,
        water_supply, landmark,
        nearby_metro, nearby_school, nearby_hospital,
        owner_type, deposit, maintenance_charge
    ) VALUES (
        %s, %s, 
        %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, 
        %s, %s, 
        %s, %s, %s, 
        %s, %s, %s
    )  
    """
    values = (
        property.id, property.user_id,
        property.title, property.area, property.direction, property.city, property.property_type,
        property.bhk, property.furnishing, property.price, property.price_type, 
        json.dumps(property.images),
        property.floor, property.total_floors, property.carpet_area, 
        property.bathrooms, property.toilet_type, property.age_of_property,
        int(property.balcony or 0), 
        int(property.parking or 0),  
        int(property.lift or 0), 
        int(property.gas_pipeline or 0),
        property.water_supply, property.landmark,
        property.nearby_metro, property.nearby_school, property.nearby_hospital,
        property.owner_type, property.deposit, property.maintenance_charge
    )

    cursor.execute(sql, values)

    db.commit()
    cursor.close()
    db.close()



# ---------------- READ LATEST PROPERTIES ----------------
def read_property():
    """
    Fetches the latest 4 verified and available properties for homepage display.
    """
    db = db_connection()
    cursor = db.cursor(dictionary=True)
    sql = """
        SELECT id, user_id, title, area, direction, city,
               property_type, bhk, furnishing,
               price, price_type, images
        FROM properties
        WHERE is_verified = 1 AND is_available = 1
        ORDER BY posted_on DESC
        LIMIT 4
    """
    cursor.execute(sql)
    rows = cursor.fetchall()

    cursor.close()
    db.close()

    return rows



# ---------------- BROWSE PROPERTIES ----------------
def browse_read_property(area, property_type, max_price, page, per_page):
    """
    Fetch paginated properties based on filters: area, property_type, max_price.
    Returns rows and total count for pagination.
    """
    offset = (page - 1) * per_page

    db = db_connection()
    cursor = db.cursor(dictionary=True)

    # Build dynamic WHERE clause
    conditions = ["is_verified = 1", "is_available = 1"]  # Only active properties
    values = []

    if area:
        conditions.append("area = %s")
        values.append(area)
    
    if property_type:
        conditions.append("property_type = %s")
        values.append(property_type)
   
    if max_price:
        conditions.append("price <= %s")
        values.append(max_price)

    where_sql = " WHERE " + " AND ".join(conditions)   # sql = WHERE is_verified = 1 AND is_available = 1 AND area = %s AND property_type = %s AND price <= %s

    # 1) DATA QUERY / Fetch paginated data
    data_sql = f"""
        SELECT id, user_id, title, area, direction, city,
               property_type, bhk, furnishing,
               price, price_type, images
        FROM properties
        {where_sql}
        ORDER BY posted_on DESC
        LIMIT %s OFFSET %s
    """

    data_values = values + [per_page, offset]   # data_values = [area, property_type, max_price, per_page, offset]
    cursor.execute(data_sql, tuple(data_values))
    rows = cursor.fetchall()

    # 2) COUNT QUERY / Fetch total count for pagination
    count_sql = f"""
        SELECT COUNT(*) AS total
        FROM properties
        {where_sql}
    """
    cursor.execute(count_sql, tuple(values))
    total = cursor.fetchone()["total"]

    cursor.close()
    db.close()

    return rows, total



def view_property_raw(id):
    db = db_connection()
    cursor = db.cursor(dictionary=True)

    sql = "SELECT * FROM properties WHERE id = %s"
    cursor.execute(sql, (id,))
    row = cursor.fetchone()

    cursor.close()
    db.close()
    return row



# ---------------- SINGLE PROPERTY ACCESS (PUBLIC / OWNER / ADMIN) ----------------
def view_property_with_owner_access(property_id, viewer_user_id=None, is_admin=False):
    try:
        uuid_obj = uuid.UUID(property_id)
    except ValueError:
        return None

    db = db_connection()
    cursor = db.cursor(dictionary=True)

    if is_admin:
        sql = """
            SELECT p.*, u.name AS owner_name, u.email AS owner_email, u.phone AS owner_phone
            FROM properties p
            JOIN users u ON p.user_id = u.user_id
            WHERE p.id = %s
        """
        params = (str(uuid_obj),)

    else:
        sql = """
            SELECT p.*, u.name AS owner_name, u.email AS owner_email, u.phone AS owner_phone
            FROM properties p
            JOIN users u ON p.user_id = u.user_id
            WHERE p.id = %s
              AND p.is_available = 1
              AND (
                    p.is_verified = 1
                    OR p.user_id = %s
                  )
        """
        params = (str(uuid_obj), viewer_user_id)

    cursor.execute(sql, params)
    row = cursor.fetchone()

    if not row:
        cursor.close()
        db.close()
        return None

    if not is_admin:
        is_owner = viewer_user_id == row["user_id"]
        is_public_verified = row["is_verified"] == 1 and row["is_available"] == 1

        if not is_owner and not is_public_verified:
            row["owner_email"] = None
            row["owner_phone"] = None

    cursor.close()
    db.close()

    return row



# ---------------- DELETE PROPERTY (SOFT DELETE) ----------------
def delete_property(id, user_id):
    """
    Soft delete a property: mark as unavailable.
    Returns number of rows affected.
    """
    try:
        uuid_obj = uuid.UUID(id)
    except ValueError:
        return 0

    db = db_connection()
    cursor = db.cursor()

    sql = """
        UPDATE properties
        SET is_available = 0
        WHERE id = %s AND user_id = %s AND is_verified = 0
    """

    cursor.execute(sql, (str(uuid_obj), user_id))
    affected = cursor.rowcount

    db.commit()
    cursor.close()
    db.close()

    return affected



# ---------------- UPDATE PROPERTY ----------------
def update_property(property):
    """
    Update property details. Existing images are replaced with updated list.
    """
    db = db_connection()
    cursor = db.cursor()

    sql = """
        UPDATE properties
        SET title = %s, area = %s, direction = %s, city = %s, 
            property_type = %s, bhk = %s, furnishing = %s,
            price = %s, price_type = %s, images = %s,
            floor = %s, total_floors = %s, carpet_area = %s, balcony = %s, 
            bathrooms = %s,toilet_type = %s, age_of_property = %s,
            parking = %s, lift = %s, water_supply = %s, gas_pipeline = %s,
            landmark = %s, nearby_metro = %s, nearby_school = %s, nearby_hospital = %s,
            owner_type = %s, deposit = %s, maintenance_charge = %s
        WHERE id = %s AND user_id = %s AND is_verified = 0
    """ 
    values = (
        property.title, property.area, property.direction, property.city, 
        property.property_type, property.bhk, property.furnishing,
        property.price, property.price_type, json.dumps(property.images),
        property.floor, property.total_floors, property.carpet_area, int(property.balcony or 0), 
        property.bathrooms, property.toilet_type, property.age_of_property,
        int(property.parking or 0), int(property.lift or 0), property.water_supply, int(property.gas_pipeline or 0),
        property.landmark, property.nearby_metro, property.nearby_school, property.nearby_hospital,
        property.owner_type, property.deposit, property.maintenance_charge, 
        property.id, property.user_id
    )

    cursor.execute(sql, values)

    db.commit()
    cursor.close()
    db.close()



# ---------------- VIEW USER PROPERTIES ----------------
def view_user_properties(user_id):
    """
    Fetch all properties for a user, excluding soft-deleted ones.
    """
    db = db_connection()
    cursor = db.cursor(dictionary=True)

    sql = """
        SELECT * FROM properties 
        WHERE user_id = %s AND is_available = 1
        ORDER BY posted_on DESC
    """
    values = (user_id,)

    cursor.execute(sql, values)
    rows = cursor.fetchall()

    cursor.close()
    db.close()

    return rows



# ---------------- ADMIN: PENDING PROPERTIES ----------------
def admin_pending_properties():
    """
    Fetch all properties pending admin verification.
    Includes owner name and email via JOIN.
    """
    db = db_connection()
    cursor = db.cursor(dictionary=True)

    sql = """
        SELECT p.*, u.name AS owner_name, u.email AS owner_email
        FROM properties p
        JOIN users u ON p.user_id = u.user_id
        WHERE p.is_verified = 0 AND p.is_available = 1
        ORDER BY p.posted_on DESC
    """
    cursor.execute(sql)
    rows = cursor.fetchall()

    cursor.close()
    db.close()
    return rows



# ---------------- ADMIN: VERIFY PROPERTIES ----------------
def admin_verify_property(property_id):
    """
    Mark a property as verified by admin.
    """
    db = db_connection()
    cursor = db.cursor()

    sql = """
        UPDATE properties
        SET is_verified = 1
        WHERE id = %s AND is_available = 1
    """
    cursor.execute(sql, (property_id,))
    db.commit()

    cursor.close()
    db.close()



# ---------------- ADMIN: REJECT PROPERTIES ----------------
def admin_reject_property(property_id):
    """
    Reject a property submission by marking it unavailable.
    """
    db = db_connection()
    cursor = db.cursor()

    sql = """
        UPDATE properties
        SET is_verified = 0, is_available = 0
        WHERE id = %s
    """
    cursor.execute(sql, (property_id,))
    db.commit()

    cursor.close()
    db.close()





# def delete_property(id, user_id):
#     import uuid

#     try:
#         uuid_obj = uuid.UUID(id)
#     except ValueError:
#         return 0
    
#     db = db_connection()
#     cursor = db.cursor()
    
#     sql = """
#         DELETE FROM properties
#         WHERE id = %s AND user_id = %s
#     """
#     values = (str(uuid_obj), user_id)

#     cursor.execute(sql, values)
#     rows_deleted = cursor.rowcount

#     db.commit()

#     cursor.close()
#     db.close()

#     return rows_deleted


# # ---------------- VIEW SINGLE PROPERTY ----------------
# def view_property(id):
#     """
#     Fetch a single property by ID.
#     Only available properties are returned (soft delete respected).
#     """
#     import uuid

#     try:
#         uuid_obj = uuid.UUID(id)
#     except ValueError:
#         return None

#     db = db_connection()
#     cursor = db.cursor(dictionary=True)

#     sql = """
#         SELECT *
#         FROM properties
#         WHERE id = %s AND is_verified = 1 AND is_available = 1 
#     """

#     cursor.execute(sql, (str(uuid_obj),))
#     row = cursor.fetchone()

#     cursor.close()
#     db.close()

#     return row



# # ---------------- USER: VIEW PROPERTY DETAILS EVEN IF NOT VERIFIED ----------------
# def view_property_for_user(property_id, user_id):
#     """
#     Owner can view their own property even if not verified.
#     Public users can only view verified & available properties.
#     """
#     import uuid

#     try:
#         uuid_obj = uuid.UUID(property_id)
#     except ValueError:
#         return None

#     db = db_connection()
#     cursor = db.cursor(dictionary=True)

#     sql = """
#         SELECT *
#         FROM properties
#         WHERE id = %s
#         AND is_available = 1
#         AND (
#             is_verified = 1
#             OR user_id = %s
#         )
#     """

#     cursor.execute(sql, (str(uuid_obj), user_id))
#     row = cursor.fetchone()

#     cursor.close()
#     db.close()

#     return row




# # ---------------- VIEW PROPERTY WITH OWNER INFO ----------------
# def view_property_with_owner(id):
#     """
#     Fetch a property along with owner details from users table.
#     Only returns available properties.
#     """
#     import uuid

#     try:
#         uuid_obj = uuid.UUID(id)
#     except ValueError:
#         return None
    
#     db = db_connection()
#     cursor = db.cursor(dictionary=True)

#     sql = """
#         SELECT 
#             p.*,
#             u.name AS owner_name,
#             u.email AS owner_email,
#             u.phone AS owner_phone
#         FROM properties p
#         JOIN users u ON p.user_id = u.user_id
#         WHERE p.id = %s AND p.is_verified = 1 AND p.is_available = 1  
#     """
#     values = (str(uuid_obj),)

#     cursor.execute(sql, values)

#     row = cursor.fetchone() # fetch single property with owner info

#     cursor.close()
#     db.close()

#     return row


# # ---------------- ADMIN: VIEW PENDING PROPERTY DETAILS ----------------
# def admin_can_view_property_with_owner(id):
#     """
#     Fetch a property along with owner details from users table.
#     Only returns available properties.
#     """
#     import uuid

#     try:
#         uuid_obj = uuid.UUID(id)
#     except ValueError:
#         return None
    
#     db = db_connection()
#     cursor = db.cursor(dictionary=True)

#     sql = """
#         SELECT 
#             p.*,
#             u.name AS owner_name,
#             u.email AS owner_email,
#             u.phone AS owner_phone
#         FROM properties p
#         JOIN users u ON p.user_id = u.user_id
#         WHERE p.id = %s   
#     """
#     values = (str(uuid_obj),)

#     cursor.execute(sql, values)

#     row = cursor.fetchone() # fetch single property with owner info

#     cursor.close()
#     db.close()

#     return row


# # ---------------- VIEW PENDING PROPERTY DETAILS WITHOUT OWNER DETAILS ----------------
# def view_property_raw(id):
#     db = db_connection()
#     cursor = db.cursor(dictionary=True)

#     sql = "SELECT * FROM properties WHERE id = %s"
#     cursor.execute(sql, (id,))
#     row = cursor.fetchone()

#     cursor.close()
#     db.close()
#     return row