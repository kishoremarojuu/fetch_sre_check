import httpx
from urllib.parse import urlparse
import time

def extract_domain(url):
    return urlparse(url).hostname

async def check_endpoint(endpoint, availability):
    url = endpoint["url"]
    method = endpoint.get("method", "GET").upper()
    headers = endpoint.get("headers", {})
    body = endpoint.get("body", None)
    domain = extract_domain(url)

    start = time.perf_counter()
    try:
        async with httpx.AsyncClient(timeout=0.5) as client:
            response = await client.request(method, url, headers=headers, content=body)
            duration = (time.perf_counter() - start) * 1000  # in ms

            is_up = 200 <= response.status_code <= 299 and duration <= 500
    except Exception:
        is_up = False

    if domain not in availability:
        availability[domain] = {"total": 0, "success": 0}

    availability[domain]["total"] += 1
    availability[domain]["success"] += int(is_up)

def log_availability(availability):
    print("\n--- Availability Report ---")
    for domain, stats in availability.items():
        success = stats["success"]
        total = stats["total"]
        percent = (success / total) * 100
        print(f"{domain}: {success}/{total} available ({percent:.2f}%)")
