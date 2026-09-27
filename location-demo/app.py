from flask import Flask, render_template, request, jsonify
from urllib.request import Request, urlopen
from urllib.parse import urlencode
import json

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# REVERSE GEOCODING
# -----------------------------
@app.get("/reverse-geocode")
def reverse_geocode():

    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
        return jsonify({"error": "Coordinates missing"}), 400

    params = urlencode({
        "lat": lat,
        "lon": lon,
        "format": "jsonv2",
        "zoom": 18,
        "addressdetails": 1
    })

    url = "https://nominatim.openstreetmap.org/reverse?" + params

    req = Request(
        url,
        headers={
            "User-Agent": "LocalLocationDemo/1.0"
        }
    )

    try:

        with urlopen(req, timeout=10) as response:
            data = json.loads(
                response.read().decode("utf-8")
            )

        return jsonify({
            "display_name": data.get("display_name", ""),
            "address": data.get("address", {})
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# -----------------------------
# LOCATION SEARCH
# -----------------------------
@app.get("/search-location")
def search_location():

    query = request.args.get("q")

    if not query:
        return jsonify([])

    params = urlencode({
        "q": query,
        "format": "jsonv2",
        "limit": 5,
        "addressdetails": 1
    })

    url = "https://nominatim.openstreetmap.org/search?" + params

    req = Request(
        url,
        headers={
            "User-Agent": "LocalLocationDemo/1.0"
        }
    )

    try:

        with urlopen(req, timeout=10) as response:

            data = json.loads(
                response.read().decode("utf-8")
            )

        results = []

        for item in data:

            results.append({
                "lat": float(item["lat"]),
                "lon": float(item["lon"]),
                "name": item.get(
                    "display_name",
                    "Unknown location"
                )
            })

        return jsonify(results)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# -----------------------------
# REGISTRATION
# -----------------------------
@app.post("/register")
def register():

    data = request.json

    print("\n")
    print("=" * 50)
    print("        NEW REGISTRATION")
    print("=" * 50)

    print("Name      :", data.get("name"))
    print("Email     :", data.get("email"))
    print("Phone     :", data.get("phone"))
    print("Latitude  :", data.get("latitude"))
    print("Longitude :", data.get("longitude"))
    print("Address   :", data.get("address"))

    print("=" * 50)
    print()

    return jsonify({
        "success": True,
        "message": "Registration successful"
    })


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
