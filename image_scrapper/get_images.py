import json
import http.client

def get_images(conn, search: str, page: int, search_endgine: str = "google"):
    payload = json.dumps({
      "q": search,
      "num": 100,
      "engine": search_endgine,
      "page": page
    })
    headers = {
      'X-API-KEY': '802897edbf3f1097e617e2505394284b737ab10d',
      'Content-Type': 'application/json'
    }
    conn.request("POST", "/images", payload, headers)
    res = conn.getresponse()
    data = json.loads(res.read())
    images = data.get("images", [])

    image_links = [img.get("imageUrl") for img in images]

    return image_links
