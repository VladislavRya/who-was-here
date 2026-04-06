import os
import time

import redis
from flask import Flask, jsonify, request, send_from_directory

REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
LIST_KEY = "recent_visitors"
TTL_SECONDS = 60 * 60

app = Flask(__name__, static_folder="static")
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/api/visit", methods=["POST"])
def visit():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    if not name:
        return jsonify({"error": "Имя не может быть пустым"}), 400

    r.zadd(LIST_KEY, {name: time.time()})
    cutoff = time.time() - TTL_SECONDS
    r.zremrangebyscore(LIST_KEY, "-inf", cutoff)
    return jsonify({"ok": True, "name": name})


@app.route("/api/visitors")
def visitors():
    cutoff = time.time() - TTL_SECONDS
    r.zremrangebyscore(LIST_KEY, "-inf", cutoff)
    entries = r.zrevrangebyscore(LIST_KEY, "+inf", cutoff, withscores=True)
    result = [
        {"name": name, "time": time.strftime("%H:%M:%S", time.localtime(ts))}
        for name, ts in entries
    ]
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
