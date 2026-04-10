from django.http import JsonResponse
import random
import requests
from core.models import Event


def chatbot_response(request):
    msg = request.GET.get('msg', '').lower()
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    # =====================
    # BASIC RESPONSES
    # =====================

    if any(word in msg for word in ["hi", "hello", "hey"]):
        return JsonResponse({
            "reply": random.choice([
                "Hello 👋 Welcome to SevaSetu!",
                "Hey there! Ready to make an impact? 🚀",
                "Hi! How can I help you today 😊"
            ])
        })

    elif "certificate" in msg:
        return JsonResponse({"reply": "🎓 You will get certificate after seva!"})

    elif "badge" in msg:
        return JsonResponse({"reply": "🏆 Badges show your contribution level."})

    elif "points" in msg:
        return JsonResponse({"reply": "⭐ Earn points by joining events!"})

    elif "leaderboard" in msg:
        return JsonResponse({"reply": "🏆 Check leaderboard!"})

    # =====================
    # 📍 NEARBY FEATURE
    # =====================

    elif "nearby" in msg:

        if not (lat and lon):
            return JsonResponse({"reply": "📍 Please allow location access"})

        try:
            url = "https://nominatim.openstreetmap.org/reverse"
            params = {"format": "json", "lat": lat, "lon": lon}
            headers = {"User-Agent": "sevasetu-app"}

            res = requests.get(url, params=params, headers=headers, timeout=5)

            if res.status_code != 200:
                return JsonResponse({"reply": "⚠️ Location fetch failed"})

            data = res.json()
            address = data.get("address", {})

            # 🔥 ACCURATE LOCATION
            place = (
                address.get("amenity")
                or address.get("suburb")
                or address.get("village")
            )

            city = (
                address.get("city")
                or address.get("town")
                or address.get("county")
            )

            if not place:
                place = city or "your area"

            # 🔥 DB EVENTS
            events = Event.objects.filter(
                normalized_location__icontains=place.lower()
            )[:3]

            if events:
                event_list = ", ".join([e.title for e in events])
                return JsonResponse({
                    "reply": f"📍 Nearby in {place}: {event_list} 🚀"
                })
            else:
                return JsonResponse({
                    "reply": f"📍 No events found near {place} 😢"
                })

        except Exception as e:
            print("ERROR:", e)
            return JsonResponse({
                "reply": "⚠️ Location error"
            })

    # =====================
    # DEFAULT
    # =====================

    else:
        return JsonResponse({
            "reply": "Try: nearby seva, certificate, badge 😊"
        })