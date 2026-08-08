import time
import httpx


def check_url(url: str) -> dict:
    start = time.perf_counter()
    try:
        response = httpx.get(url, timeout=5.0)
        latency_ms = round((time.perf_counter() - start) * 1000, 1)
        return {
            "url": url,
            "ok": response.status_code < 400,
            "status_code": response.status_code,
            "latency_ms": latency_ms,
        }
    except httpx.RequestError as exc:
        latency_ms = round((time.perf_counter() - start) * 1000, 1)
        return {
            "url": url,
            "ok": False,
            "status_code": None,
            "latency_ms": latency_ms,
            "error": str(exc),
        }


if __name__ == "__main__":
    sites = ["https://www.google.com", "https://www.facebook.com", "https://broken.sabinrana.xyz"]
    for url in sites:
        result = check_url(url)
        print(result)