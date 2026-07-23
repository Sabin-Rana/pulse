import time
import httpx


def check_url(url: str) -> dict:
    start = time.perf_counter()
    try:
        response = httpx.get(url, timeout=5.0)
        latency_ms = round((time.perf_counter() - start) * 1000, 1)
        return {
            "url": url,
            "ok": response.status_code == 200,
            "status": response.status_code,
            "latency_ms": latency_ms,
        }
    except httpx.RequestError as exc:
        latency_ms = round((time.perf_counter() - start) * 1000, 1)
        return {"url": url, "ok": False, "error": str(exc), "latency_ms": latency_ms}


if __name__ == "__main__":
    print(check_url("http://localhost:8000/healthz"))
