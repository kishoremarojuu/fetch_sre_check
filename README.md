# fetch_sre_check


---

# Fetch SRE Take-Home Exercise (Python)

## Overview

This tool performs continuous availability monitoring of HTTP endpoints defined in a YAML config file. Every 15 seconds, it checks all endpoints concurrently and logs domain-level availability, considering both HTTP response codes and response time thresholds.

---

## 🔧 Requirements

- Python 3.8+
- Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run


```bash
python monitor.py --config config.yaml
```

3. The tool will:
    - Check all endpoints every 15 seconds
    - Log domain-level availability (ignoring ports)
    - Consider endpoints "available" **only if**:
        - Status code is `2xx`
        - Response time ≤ 500ms

## ✅ Availability Logic

- Status codes: `200–299` are considered successful
- Response times: must be ≤ 500ms
- Availability is **cumulative per domain**, based on number of successful checks vs. total

---

## 🛠️ What Was Improved

### 1. **Concurrency Added**
- ❌ *Original*: Blocking HTTP requests meant the loop could exceed 15 seconds if endpoints were slow.
- ✅ *Fixed*: Used `asyncio` + `httpx.AsyncClient` for concurrent requests to keep the loop within the 15-second window.

### 2. **Timeout Handling**
- ✅ *Implemented*: 500ms timeout using `httpx` to match performance criteria.

### 3. **Clean CLI & Error Handling**
- ✅ *Implemented*: Graceful shutdown on `Ctrl+C`, and helpful CLI errors if config is missing.

---

## 📦 File Structure

```
fetch_sre_check/
├── monitor.py            # Main runner
├── utils.py              # Shared helpers (requests, logging)
├── config.yaml           # Sample config
├── requirements.txt
└── README.md
```

---

## ✅ Sample Output

```text
--- Availability Report ---
google.com: 3/3 available (100.00%)
httpbin.org: 2/3 available (66.67%)
```

---
