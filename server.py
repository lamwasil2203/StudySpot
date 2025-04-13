from flask import Flask, url_for
from flask import render_template
from flask import request, jsonify

app = Flask(__name__)

id_counter = 11
# Replace the study_spots list in server.py with this expanded version
study_spots = [
    {
        "id": 1,
        "name": "Remi43 Flower & Coffee",
        "link": "/spot/Remi43",
        "time": "7 AM - 6 PM",
        "location": "810 2nd Ave, New York, NY 10017",
        "image": "https://www.passblue.com/wp-content/uploads/2021/10/Remi43-from-the-mezzanine-scaled.jpg",
        "description": "A cozy floral-themed café in Midtown offering a tranquil ambiance for studying or working remotely. With beautiful flower arrangements, a wide variety of unique coffee blends, and a peaceful vibe, it's the perfect spot for focused work or relaxing coffee breaks.",
        "capacity": "Plenty of seating, though it can get crowded.",
        "noise_level": "Quiet to moderate (light background music and casual conversations).",
        "wifi": "Fast and reliable.",
        "outlets": "Available near the seating area.",
        "related_topics": ["coffee", "quiet", "midtown", "floral", "cozy"]
     },
    {
        "id": 2,
        "name": "Brooklyn Public Library - Central Branch",
        "link": "/spot/bpl-central",
        "time": "9 AM - 9 PM Mon-Sat, 1 PM - 5 PM Sun",
        "location": "10 Grand Army Plaza, Brooklyn, NY 11238",
        "image": "https://www.archpaper.com/wp-content/uploads/2021/05/BPL_Business-Career-Center.jpg",
        "description": "This stunning limestone building offers various study spaces, from quiet reading rooms to collaborative areas. With its beautiful architecture and extensive resources, it's an excellent spot for serious studying across all subjects.",
        "capacity": "Very spacious with multiple study areas.",
        "noise_level": "Silent in designated quiet zones, low elsewhere.",
        "wifi": "Free and reliable.",
        "outlets": "Abundant throughout the building.",
        "related_topics": ["library", "quiet", "Brooklyn", "spacious", "architecture"]
     },
    {
        "id": 3,
        "name": "Think Coffee",
        "link": "/spot/think-coffee",
        "time": " 8 AM - 7PM",
        "location": "471 Broadway, New York, NY 10013",
        "image": "https://assets.benable.com/rec_object_photos/1916927/full_size/c1f7ba3ec09a4a185f66.jpeg",
        "description": "A cozy café with ethically sourced coffee, teas, and light bites. With locations across NYC, it's ideal for studying, working, or relaxing, while supporting sustainability and fair trade.",
        "capacity": "Plenty of seating but gets busy during the weekends.",
        "noise_level": "Moderate - conversations ",
        "wifi": "Free public Wi-Fi is available.",
        "outlets": "Limited - best to charge before coming.",
        "related_topics": ["coffee", "ethical", "moderate noise", "sustainable"]
    },
    {
        "id": 4,
        "name": "The Bean",
        "link": "/spot/the-bean",
        "time": "7 AM - 9 PM",
        "location": "31 3rd Ave, New York, NY 10003",
        "image": "https://ac766573303797d89c30.cdn6.editmysite.com/uploads/b/ac766573303797d89c309f11063ad83ab68895ff9a59b2a6ddb18be67f1a22d1/Bean_life_1609788253.jpg?width=2400&optimize=medium",
        "description": "A popular East Village coffee shop with a vibrant atmosphere. The Bean offers plenty of seating, strong coffee, and a lively environment. It's perfect for casual studying or group meetups where conversation is welcome.",
        "capacity": "Moderate to large seating area with tables and couches.",
        "noise_level": "Moderate (conversations and upbeat music).",
        "wifi": "Good but can slow during peak hours.",
        "outlets": "Limited - best to come with a charged battery.",
        "related_topics": ["coffee", "east village", "lively", "casual"]

    },
    {
        "id": 5,
        "name": "Butler Library",
        "link": "/spot/quiet-library",
        "time": "OPEN 24/7",
        "location": "Columbia University, 535 W 114th St",
        "image": "https://upload.wikimedia.org/wikipedia/commons/a/aa/Butler_Library_Columbia_University.jpg",
        "description": "A quiet, wood-paneled reading room with large desks, soft lighting, and a serious academic atmosphere. Ideal for focused study sessions.",
        "capacity": "Limited during midterms/finals, otherwise moderate.",
        "noise_level": "Silent",
        "wifi": "Fast and reliable.",
        "outlets": "Available. Might have difficulty if it is too crowded",
        "related_topics": ["library", "quiet", "academic", "24/7", "focused"]
    },
    {
        "id": 6,
        "name": "Ace Hotel Lobby",
        "link": "/spot/ace-hotel",
        "time": "Open 24/7 for guests, 8 AM - 11 PM for non-guests",
        "location": "20 W 29th St, New York, NY 10001",
        "image": "https://acehotel.com/new-york/wp-content/uploads/sites/9/2021/08/lobby-slider.jpg",
        "description": "The stylish lobby of the Ace Hotel features long communal tables, comfortable leather couches, and a hip atmosphere. Popular among creatives and remote workers, it offers a unique ambiance for productive work sessions with the bonus of great coffee from the attached Stumptown Coffee Roasters.",
        "capacity": "Large communal tables and couch seating.",
        "noise_level": "Low to moderate (ambient music and hushed conversations).",
        "wifi": "Free and fast.",
        "outlets": "Available at most tables.",
        "related_topics": ["hotel", "stylish", "communal", "creative", "coffee"]
    },
    {
        "id": 7,
        "name": "McNally Jackson Café",
        "link": "/spot/mcnally-jackson",
        "time": "10 AM - 10 PM",
        "location": "52 Prince St, New York, NY 10012",
        "image": "https://images.squarespace-cdn.com/content/v1/56719b227086d77cfd9e9c60/1453310315163-6DKH29HRDJI68DTQP9FU/01_McJ-overallstore.jpg",
        "description": "Attached to the beloved independent bookstore, this café offers a literary atmosphere perfect for studying. Surrounded by books and fellow readers, it's ideal for humanities students or anyone seeking inspiration from a cultured environment.",
        "capacity": "Limited seating - about 20 spots.",
        "noise_level": "Quiet (occasional book browsing and soft conversations).",
        "wifi": "Available with purchase.",
        "outlets": "Few - located along walls.",
        "related_topics": ["bookstore", "quiet", "literary", "cafe", "intimate"]
    },
    {
        "id": 8,
        "name": "Bobst Library",
        "link": "/spot/bobst-library",
        "time": "7 AM - 11 PM (varies by floor, some 24/7 for NYU students)",
        "location": "70 Washington Square S, New York, NY 10012",
        "image": "https://nyunews.com/wp-content/uploads/2023/08/IMG_0624.jpg",
        "description": "NYU's main library offers 12 floors of study space with incredible views of Washington Square Park. While primarily for NYU students, visitors can obtain day passes. With specialized study rooms, silent floors, and group work areas, it accommodates all study preferences.",
        "capacity": "Extensive - multiple floors of seating.",
        "noise_level": "Varies by floor (completely silent to conversation-friendly).",
        "wifi": "NYU network for students, guest access available.",
        "outlets": "Abundant throughout all floors.",
        "related_topics": ["library", "university", "views", "quiet", "spacious"]
    },
    {

        "id": 9,
        "name": "Blank Street Coffee",
        "link": "/spot/blank-street-coffee",
        "time": "6:30 AM - 8 PM",
        "location": "63 Spring Street, New York, NY 10012",
        "image": "https://res.cloudinary.com/blank-street/image/upload/w_1200,h_900,c_lfill,g_auto/DSC_03799_3dcad96a9f.webp?_a=BAMADKXu0.jpg",
        "description": "This minimalist micro-café emphasizes quality and efficiency in a compact space. With a streamlined menu focusing on exceptional coffee and a few specialty items, Blank Street offers a refreshing alternative to overwhelming coffee menus. Their tech-forward approach includes mobile ordering and contactless pickup options. Despite the small footprint, clever design creates a welcoming atmosphere with floor-to-ceiling windows bringing in natural light.",
        "capacity": "Limited but thoughtfully arranged seating with small tables and a standing bar.",
        "noise_level": "Moderate - busy but not overwhelming due to the small space.",
        "wifi": "Fast and free with purchase.",
        "outlets": "Available at the window bar and select seating areas.",
        "related_topics": ["coffee", "minimalist", "tech-forward", "compact", "modern"]
    },
    {
        "id": 10,
        "name": "Atrium at Lincoln Center",
        "link": "/spot/lincoln-center",
        "time": "8 AM - 10 PM",
        "location": "10 Lincoln Center Plaza, New York, NY 10023",
        "image": "https://i0.wp.com/yourevent.lincolncenter.org/wp-content/uploads/2021/07/hero-6.jpg?fit=1920%2C1080&ssl=1.jpg",
        "description": "This stunning public space features free Wi-Fi, ample seating, and a café. With its soaring ceilings, greenery, and natural light, it offers an inspiring atmosphere for studying. As a public space, no purchase is necessary to use the seating areas.",
        "capacity": "Very spacious with various seating options.",
        "noise_level": "Moderate (background conversations and occasional performances).",
        "wifi": "Free public Wi-Fi.",
        "outlets": "Limited - concentrated near specific seating areas.",
        "related_topics": ["public space", "spacious", "arts", "free", "light"]
    }
]

top_spots = study_spots[:3]  # Slice the first 3

# ROUTES
@app.route('/')
def home():
    return render_template('home.html', spots=top_spots)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').strip()

    # If query is empty or contains only whitespace, return empty results
    if not query:
        return render_template('search.html', query='', results=[])

    # Perform case-insensitive search across multiple fields
    results = [
        item for item in study_spots
        if (query.lower() in item['name'].lower()
            or query.lower() in item['description'].lower()
            or any(query.lower() in str(topic).lower() for topic in item.get('related_topics', []))
            or query.lower() in item['location'].lower())
            or query.lower() in item['time'].lower()
            or query.lower() in item['capacity'].lower()
            or query.lower() in item['noise_level'].lower()
            or query.lower() in item['wifi'].lower()
            or query.lower() in item['outlets'].lower()
    ]

    return render_template('search.html', query=query, results=results, count=len(results))
@app.route('/view/<int:spot_id>')
def view_spot(spot_id):
    spot = next((s for s in study_spots if s["id"] == spot_id), None)
    if not spot:
        return "Spot not found", 404
    # Pass any search query to the view page
    query = request.args.get('q', '')
    return render_template('view.html', spot=spot, query=query)

@app.route('/add', methods=['GET', 'POST'])
def add_spot():
    return render_template('add.html')

@app.route('/submit', methods=['POST'])
def submit():
    """Handle form submission via AJAX."""
    global id_counter

    data = request.json  # Get JSON data from AJAX request
    name = data.get("name", "").strip()
    location = data.get("location", "").strip()
    description = data.get("description", "").strip()
    capacity = data.get("capacity", "").strip()
    time = data.get("time", "").strip()
    image = data.get("image", "").strip()
    noise_level = data.get("noise_level", "").strip()
    wifi = data.get("wifi", "").strip()
    outlets = data.get("outlets", "").strip()

    # Optional related topics as array
    related_topics = data.get("related_topics", [])
    if isinstance(related_topics, str):
        # Convert comma-separated string to list
        related_topics = [topic.strip() for topic in related_topics.split(',') if topic.strip()]

    errors = {}

    # Validate input fields
    if not name:
        errors['name'] = "Study spot name is required."
    if not location:
        errors['location'] = "Location is required. Please enter a valid address."
    if not description:
        errors['description'] = "Please provide a short description of the study spot."
    if not capacity:
        errors['capacity'] = "Capacity must be provided (e.g., '10 people', 'plenty of seating')."
    if not time:
        errors['time'] = "Please specify the hours of operation (e.g., '8 AM – 10 PM')."
    if not image:
        errors[
            'image'] = "A valid image URL is required (must start with http:// or https:// and end in .jpg, .png, etc.)."
    elif not image.startswith("http://") and not image.startswith("https://"):
        errors['image'] = "Image URL must start with http:// or https://."
    elif not any(image.endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]):
        errors['image'] = "Image URL must end in .jpg, .jpeg, .png, .gif, or .webp."

    if not noise_level:
        errors['noise_level'] = "Please describe the typical noise level (e.g., 'quiet', 'moderate', 'loud')."
    if not wifi:
        errors['wifi'] = "Wifi info is required (e.g., 'fast', 'unreliable', 'not available')."
    if not outlets:
        errors['outlets'] = "Please describe outlet availability (e.g., 'plenty', 'few', 'none')."
    if not related_topics:
        errors[
            'related_topics'] = "Please enter related topics as a comma-separated list (e.g., 'quiet, coffee, campus')."
    elif isinstance(related_topics, str) and "," not in related_topics:
        errors['related_topics'] = "Enter at least two related topics, separated by commas."

    if errors:
        return jsonify({"success": False, "errors": errors}), 400

    # Create new entry
    new_spot = {
        "id": id_counter,
        "name": name,
        "location": location,
        "description": description,
        "capacity": capacity,
        "time": time,
        "image": image,
        "noise_level": noise_level,
        "wifi": wifi,
        "outlets": outlets,
        "related_topics": related_topics
    }

    study_spots.append(new_spot)
    id_counter += 1  # Increment ID

    return jsonify({"success": True, "id": new_spot["id"]}), 201

@app.route('/edit/<int:item_id>')
def edit_item(item_id):
    """Render the edit page with pre-filled data."""
    item = next((spot for spot in study_spots if spot["id"] == item_id), None)
    if not item:
        return "Item not found", 404
    display_item = dict(item)
    return render_template("edit.html", item=display_item)

@app.route('/update/<int:item_id>', methods=['POST'])
def update_item(item_id):
    """Handle updating the item with new data."""
    item = next((spot for spot in study_spots if spot["id"] == item_id), None)
    if not item:
        return jsonify({"success": False, "error": "Item not found"}), 404

    data = request.json

    # Process related topics if provided
    related_topics = data.get("related_topics", "")
    if isinstance(related_topics, str):
        related_topics = [topic.strip() for topic in related_topics.split(',') if topic.strip()]

    item.update({
        "name": data.get("name", "").strip(),
        "location": data.get("location", "").strip(),
        "description": data.get("description", "").strip(),
        "capacity": data.get("capacity", "").strip(),
        "time": data.get("time", "").strip(),
        "image": data.get("image", "").strip(),
        "noise_level": data.get("noise_level", "").strip(),
        "wifi": data.get("wifi", "").strip(),
        "outlets": data.get("outlets", "").strip(),
        "related_topics": related_topics
    })

    return jsonify({"success": True, "redirect": url_for('view_spot', spot_id=item_id)}), 200

if __name__ == '__main__':
   app.run(debug = True, port=5001)




