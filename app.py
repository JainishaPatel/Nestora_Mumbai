from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_wtf import CSRFProtect
from utils import upload_image_to_cloudinary
from utils.cloudinary_config import *
import uuid
import json
import re
import os

from data import why_nestora, how_it_works, mumbai_areas
from models import (
    User, Property, 
    insert_property, read_property, browse_read_property, view_property_raw, view_property_with_owner_access,
    delete_property, update_property, view_user_properties, 
    insert_user, update_user_profile, update_user_password, get_user_by_email, update_last_login, 
    user_profile, save_reset_token, get_user_by_reset_token, clear_reset_token,
    admin_pending_properties, admin_verify_property, admin_reject_property
)
from middlewares import login_required, admin_required


# ------------------- Flask Setup -------------------
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or "dev_secret_key_for_testing"
csrf = CSRFProtect(app)

CLOUDINARY_DEFAULT_IMAGE = (
    f"https://res.cloudinary.com/"
    f"{os.getenv('CLOUDINARY_CLOUD_NAME')}/image/upload/"
    "w_800,h_600,c_fill,q_auto,f_auto/default_property.png"
)


# ------------------- HOME PAGE -------------------
@app.route('/')
def home():
    rows = read_property()  # fetches only latest 4 rows
    property_list = [Property(**row) for row in rows]

    return render_template(
        'index.html',
        properties=property_list,
        why_nestora=why_nestora,
        how_it_works=how_it_works
    )


# ------------------- BROWSE -------------------
@app.route('/browse')
def browse_houses():
    area = request.args.get("area")
    property_type = request.args.get("property_type")
    max_price = request.args.get("max_price")
    page = request.args.get("page", 1, type=int)
    per_page = 8

    rows, total = browse_read_property(area, property_type, max_price, page, per_page)

    if not rows:
        flash("No properties found for the selected filters.", "info")

    property_list = [Property(**row) for row in rows]

    total_pages = (total + per_page - 1) // per_page

    return render_template(
        'browse.html',
        areas=mumbai_areas,
        area=area,
        property_type=property_type,
        max_price=max_price,
        paginated_properties=property_list,
        page=page,
        total_pages=total_pages
    )


# ------------------- PROPERTY DETAILS -------------------
@app.route('/property/<id>')    # id is string (UUID)
def property_details(id):
    viewer_user_id = session.get("user_id")
    is_admin = session.get("is_admin", False)

    row = view_property_with_owner_access(property_id=id, viewer_user_id=viewer_user_id, is_admin=is_admin)
    
    if not row:
        flash("Property not found  or unavailable!", "danger")
        return redirect(url_for("browse_houses"))
    
    property_fields = [
        "id","user_id","title","area","direction","city","property_type",
        "bhk","furnishing","price","price_type","images",
        "floor","total_floors","carpet_area","bathrooms","toilet_type",
        "age_of_property","balcony","parking","lift","gas_pipeline",
        "water_supply","landmark","nearby_metro","nearby_school","nearby_hospital",
        "owner_type","deposit","maintenance_charge", "posted_on", "is_verified", "is_available"
    ]
        
    selected_property = Property(**{k: row[k] for k in property_fields if k in row})

    is_owner = viewer_user_id == row["user_id"]

    return render_template(
        'property_details.html', 
        property = selected_property, 
        property_owner = row, 
        is_owner = is_owner, 
        is_admin = is_admin
    )


# ------------------- CREATE PROPERTY -------------------         
@app.route('/create_property')
@login_required
def create_property():
    return render_template('create_property.html', areas=mumbai_areas)


@app.route('/features', methods=["POST"])
@login_required
def features():
    features_dict = {}
    features = [
        "id", "title", "area", "direction", "city", "property_type", "bhk", 
        "furnishing", "price", "price_type", "images", "owner_type", "floor", "total_floors", 
        "carpet_area", "bathrooms", "toilet_type", "age_of_property", 
        "balcony", "parking", "lift", "gas_pipeline", 
        "water_supply", "landmark", "nearby_metro", "nearby_school", "nearby_hospital", 
        "deposit", "maintenance_charge"
    ]

    for f in features:
        if f == "id":
            features_dict['id'] = str(uuid.uuid4())
        else:
            features_dict[f] = request.form.get(f) or None

    # Checkboxes
    amenities = ['balcony', 'parking', 'lift', 'gas_pipeline']
    for f in amenities:
        features_dict[f] = features_dict.get(f) == "on" # features_dict.get(key) -> return "on" ||| "on" == "on" ||| condition True ||| features_dict[key] = True

    # Integers
    int_keys = [
        "price", "floor", "total_floors", "carpet_area",
        "bathrooms", "age_of_property", "deposit", "maintenance_charge"
    ]

    for f in int_keys:
        raw_value = features_dict.get(f)

        if raw_value not in (None, ""):
            try:
                value = int(raw_value)
            except ValueError:
                flash(f"{f.replace('_', ' ').title()} must be a number.", "danger")
                return render_template(
                    "create_property.html",
                    areas=mumbai_areas,
                    form_data=features_dict
                )

            if value < 0:
                flash(f"{f.replace('_', ' ').title()} cannot be negative.", "danger")
                return render_template(
                    "create_property.html",
                    areas=mumbai_areas,
                    form_data=features_dict
                )

            features_dict[f] = value
        else:
            features_dict[f] = None


    # Images
    property_id = features_dict["id"]
    uploaded_images = request.files.getlist("images")
    image_list = [upload_image_to_cloudinary(img, property_id) for img in uploaded_images if img and img.filename]

    if not image_list:
        flash("At least one image is required", "danger")
        return redirect(url_for("create_property"))
    
    features_dict["images"] = image_list
    features_dict["user_id"] = session.get("user_id")

    new_property = Property(**features_dict)   # **kwargs  type(kwargs) = <class 'dict'>
    insert_property(new_property)

    flash("Property created successfully!", "success")

    return redirect(url_for("my_properties"))


# ------------------- DELETE PROPERTY -------------------  
@app.route('/property/delete/<id>', methods=["POST"])
@login_required
def delete_properties(id):
    rows_deleted = delete_property(id, user_id = session.get("user_id"))

    if rows_deleted == 0:
        flash("Property not found or unauthorized.", "danger")
    else:
        flash("Property deleted successfully!", "success")
    return redirect(url_for("my_properties"))
    

# ------------------- EDIT PROPERTY -------------------
@app.route('/edit_property/<id>')
@login_required
def edit_property(id):
    row = view_property_raw(id)

    if not row:
        flash("Property not found!", "danger")
        return redirect(url_for("browse_houses"))
    
    if row["user_id"] != session.get("user_id"):   
        flash("Unauthorized to edit this property.", "danger")
        return redirect(url_for("browse_houses"))
    
    selected_property = Property(**row)

    return render_template('edit_property.html', property = selected_property, areas=mumbai_areas)


# ------------------- UPDATE PROPERTY -------------------
@app.route('/updated_property/<id>', methods=["POST"])
@login_required
def updated_property(id):
    row = view_property_raw(id)

    if not row:
        flash("Property not found!", "danger")
        return redirect(url_for("browse_houses"))
     
    if row["user_id"] != session.get("user_id"):   
        flash("Unauthorized to edit this property.", "danger")
        return redirect(url_for("browse_houses"))
    
    property = Property(**row)

    # Update text fields
    text_fields = [
        "title", "area", "direction", "city", "property_type", "bhk",
        "furnishing", "price_type", "owner_type", "toilet_type",
        "water_supply", "landmark", "nearby_metro",
        "nearby_school", "nearby_hospital"
    ]
    for f in text_fields:
        f_value = request.form.get(f)
        if f_value is not None and f_value != "":
            setattr(property, f, f_value)
        # else → keep old value automatically

    # Update integer fields
    int_fields = [
        "price", "floor", "total_floors", "carpet_area",
        "bathrooms", "age_of_property", "deposit", "maintenance_charge"
    ]
   
    for f in int_fields:
        value = request.form.get(f)
        if value in (None, "", "None"):
            setattr(property, f, None)
        else:
            value = int(value)
            if value < 0:
                flash(f"{f.replace('_', ' ').title()} cannot be negative.", "danger")
                return redirect(url_for("edit_property", id=id))
            setattr(property, f, value)

    # Checkboxes
    checkbox_fields = ["balcony", "parking", "lift", "gas_pipeline"]
    for f in checkbox_fields:
        setattr(property, f, f in request.form)

    # ------------------ Handle images ------------------

    # 1) Existing images kept in the form / Existing images that user kept
    kept_images_raw = request.form.getlist("existing_images[]")
    kept_images = [json.loads(img) for img in kept_images_raw]

    # 2) Images removed by user
    removed_images = [img for img in property.images if img not in kept_images]

    # 3) Delete removed images from Cloudinary (skip default image)
    for img in removed_images:
        if isinstance(img, dict) and img.get("public_id") and not img["public_id"].startswith("defaults/"):
            try:
                cloudinary.uploader.destroy(img["public_id"])
            except Exception as e:
                print(f"Failed to delete {img['public_id']}: {e}")

    # 4) Newly uploaded images
    uploaded_images = request.files.getlist("images")
    new_images = []

    for img in uploaded_images:
        if img and img.filename:
            uploaded = upload_image_to_cloudinary(img, property.id)
            if uploaded:
                new_images.append(uploaded)

    # 5) Merge kept + new images
    property.images = kept_images + new_images

    # 6) Ensure at least one image (KEEP SCHEMA CONSISTENT)
    if not property.images:
        property.images = [{
            "url": CLOUDINARY_DEFAULT_IMAGE,
            "public_id": "defaults/default_property"
        }]

    # Save updates / changes 
    update_property(property)
    flash("Property updated successfully!", "success")
    return redirect(url_for("property_details", id = id))


# ------------------- MY PROPERTIES -------------------
@app.route('/my_properties')
@login_required
def my_properties():
    user_id = session.get("user_id")
    
    rows = view_user_properties(user_id)

    properties_list = [Property(**row) for row in rows]
       
    return render_template("my_properties.html", properties = properties_list)


# ------------------- AUTH ROUTES -------------------

# ------------------- SIGNUP -------------------
@app.route('/signup', methods=["GET", "POST"])
def signup():

    EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$'
    email = request.args.get("email")

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        # ---- Validation ----
        if not name:
            flash("Name is required!", "danger")
            return redirect(url_for("signup"))

        if not email or not re.match(EMAIL_REGEX, email.strip()):
            flash("Invalid email address!", "danger")
            return redirect(url_for("signup"))

        if not password or not re.match(PASSWORD_REGEX, password.strip()):
            flash("Password must be 8+ chars with uppercase, lowercase, number, special char.", "danger")
            return redirect(url_for("signup"))

        email = email.strip()

        # ---- Check existing user ----
        if get_user_by_email(email):
            flash("Email already registered!", "danger")
            return redirect(url_for("signup"))

        # ---- Create user ----
        user = User(
            user_id=str(uuid.uuid4()),
            name=name.strip(),
            email=email
        )
        user.set_password(password)

        insert_user(user)

        flash("Signup successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("auth/signup.html", email=email)


# ------------------- LOGIN -------------------
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = get_user_by_email(email)

        # Account not found
        if not user:
            flash("Account not found. Please sign up first.", "warning")
            return render_template("auth/login.html", show_signup_link=True, entered_email=email)

        # Incorrect password
        if not user.check_password(password):
            flash("Incorrect password. Please try again.", "danger")
            return redirect(url_for("login", next=request.args.get("next")))
        
        # Update last login
        user.update_last_login()
        update_last_login(user.user_id)

        # Set session
        session["user_id"] = user.user_id
        session["email"] = user.email
        session["is_admin"] = user.is_admin
        flash("Logged in successfully!", "success")

        # Redirect to intended page
        next_page = request.args.get("next")
        if next_page and next_page.startswith("/"):
            return redirect(next_page)

        return redirect(url_for("home"))

    return render_template("auth/login.html")


# ------------------- LOGOUT -------------------
@app.route('/logout')
@login_required
def logout():
    if "user_id" in session:
        session.clear()   # removes all session data
        flash("Logged out successfully", "success")
    else:
        flash("You are not logged in", "warning")
    return redirect(url_for("login"))


# ------------------- PROFILE -------------------
@app.route('/profile', methods=["GET", "POST"])
@login_required
def profile():
    user_info = user_profile(session.get("user_id"))
    
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        phone = (request.form.get("phone") or "").strip()
        update_user_profile(user_id = session.get("user_id"), name = name, phone = phone)
        flash("Profile updated successfully", "success")
        return redirect(url_for("profile"))
        
    return render_template("profile.html", user = user_info)


# ------------------- FORGOT PASSWORD -------------------
@app.route('/forgot_password', methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        user = get_user_by_email(email)

        if not user:
            flash("If the email exists, a reset link will be sent.", "info")
            return redirect(url_for("forgot_password"))

        # Generate secure token
        token = user.generate_reset_token(expiry_hours=1)

        # Save token in DB
        save_reset_token(user.user_id, user.reset_token, user.reset_expires)

        reset_link = url_for("reset_password", token=token, _external=True)

        # DEV ONLY
        print(f"[DEBUG][DEV][PASSWORD_RESET_LINK] -> {reset_link}")

        flash("Password reset link sent (check console in dev).", "success")
        return redirect(url_for("login"))

    return render_template("auth/forgot_password.html")


# ------------------- PASSWORD RESET -------------------
@app.route('/reset_password/<token>', methods=["GET", "POST"])
def reset_password(token):
    user = get_user_by_reset_token(token)

    if not user:
        flash("Invalid or expired password reset link.", "danger")
        return redirect(url_for("login"))

    if request.method == "POST":
        password = request.form.get("password")

        PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$'

        # 1) Check password strength
        if not password or not re.match(PASSWORD_REGEX, password):
            flash( "Password must contain uppercase, lowercase, number & special character.", "danger")
            return redirect(url_for("reset_password", token=token))

        # 2) Prevent reusing the old password
        if user.check_password(password):
            flash("You cannot reuse your previous password. Please choose a new one.", "danger")
            return redirect(url_for("reset_password", token=token))

        # 3) Save new password
        user.set_password(password)
        update_user_password(user)

        # 4) Clear the reset token
        clear_reset_token(user.user_id)

        flash("Password reset successful! You can now login.", "success")
        return redirect(url_for("login"))

    return render_template("auth/reset_password.html")


# ---------------- ADMIN: VIEW PENDING PROPERTIES ----------------
@app.route("/admin/properties")
@admin_required
def admin_properties():
    rows = admin_pending_properties()

    property_fields = [
        "id","user_id","title","area","direction","city","property_type",
        "bhk","furnishing","price","price_type","images",
        "floor","total_floors","carpet_area","bathrooms","toilet_type",
        "age_of_property","balcony","parking","lift","gas_pipeline",
        "water_supply","landmark","nearby_metro","nearby_school","nearby_hospital",
        "owner_type","deposit","maintenance_charge", "posted_on", "is_verified", "is_available"
    ]

    properties = []
    for row in rows:
        # Only pass Property fields to Property constructor
        prop = Property(**{k: row[k] for k in property_fields if k in row})
        # Attach owner info separately
        prop.owner_name = row.get("owner_name")
        prop.owner_email = row.get("owner_email")
        properties.append(prop)

    return render_template("admin/properties.html", properties=properties)


# ---------------- ADMIN: VIEW PENDING PROPERTY DETAILS ----------------
@app.route("/admin/property/<id>")
@admin_required
def admin_property_details(id):
    viewer_user_id = session.get("user_id")
    is_admin = session.get("is_admin", False)

    row = view_property_with_owner_access(property_id=id, viewer_user_id=viewer_user_id, is_admin=is_admin)
    
    if not row:
        flash("Property not found", "danger")
        return redirect(url_for("admin_properties"))
    
    property_fields = [
        "id","user_id","title","area","direction","city","property_type",
        "bhk","furnishing","price","price_type","images",
        "floor","total_floors","carpet_area","bathrooms","toilet_type",
        "age_of_property","balcony","parking","lift","gas_pipeline",
        "water_supply","landmark","nearby_metro","nearby_school","nearby_hospital",
        "owner_type","deposit","maintenance_charge", "posted_on", "is_verified", "is_available"
    ]
    
    property = Property(**{k: row[k] for k in property_fields if k in row})

    is_owner = viewer_user_id == row["user_id"]

    return render_template(
        "admin/property_details.html", 
        property = property, 
        property_owner = row,
        is_owner = is_owner,
        is_admin = is_admin
    )


# ---------------- ADMIN: VERIFY PROPERTY ----------------
@app.route("/admin/property/verify/<property_id>", methods=["POST"])
@admin_required
def verify_property(property_id):
    property_row = view_property_raw(property_id)
    if not property_row:
        flash("Property not found or already deleted.", "danger")
        return redirect(url_for("admin_properties"))

    admin_verify_property(property_id)
    flash(f"Property '{property_row.get('title', 'Unknown')}' verified successfully!", "success")
    return redirect(url_for("admin_properties"))


# ---------------- ADMIN: REJECT PROPERTY ----------------
@app.route("/admin/property/reject/<property_id>", methods=["POST"])
@admin_required
def reject_property(property_id):
    property_row = view_property_raw(property_id)
    if not property_row:
        flash("Property not found or already deleted.", "danger")
        return redirect(url_for("admin_properties"))

    admin_reject_property(property_id)
    flash(f"Property '{property_row.get('title', 'Unknown')}' rejected!", "warning")
    return redirect(url_for("admin_properties"))


# ------------------- ERROR HANDLERS -------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html"),404

@app.errorhandler(403)
def forbidden(e):
    return render_template("errors/403.html"), 403

@app.errorhandler(500)
def internal_error(e):
    return render_template("errors/500.html"), 500


# ------------------- RUN APP -------------------
if __name__ == "__main__":
    app.run(debug=True)
