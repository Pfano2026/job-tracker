import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "tracker.db")
STATUSES = ["applied", "interview", "offer", "rejected"]

app = Flask(__name__)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn, open(os.path.join(BASE, "schema.sql")) as f:
        conn.executescript(f.read())


init_db()


@app.route("/")
def index():
    sort = request.args.get("sort", "date")
    if sort == "status":
        order = ("CASE status WHEN 'applied' THEN 1 WHEN 'interview' THEN 2 "
                 "WHEN 'offer' THEN 3 ELSE 4 END, date_applied DESC")
    else:
        order = "date_applied DESC"
    conn = get_db()
    rows = conn.execute(f"SELECT * FROM applications ORDER BY {order}").fetchall()
    counts = {s: 0 for s in STATUSES}
    for r in conn.execute("SELECT status, COUNT(*) c FROM applications GROUP BY status"):
        counts[r["status"]] = r["c"]
    conn.close()
    return render_template("index.html", apps=rows, counts=counts,
                           statuses=STATUSES, sort=sort, total=sum(counts.values()))


@app.route("/add", methods=["POST"])
def add():
    company = request.form["company"].strip()
    role = request.form["role"].strip()
    date_applied = request.form["date_applied"]
    if company and role and date_applied:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO applications (company, role, date_applied) VALUES (?,?,?)",
                (company, role, date_applied))
    return redirect(url_for("index"))


@app.route("/update/<int:app_id>", methods=["POST"])
def update(app_id):
    status = request.form["status"]
    if status in STATUSES:
        with get_db() as conn:
            conn.execute("UPDATE applications SET status=? WHERE id=?", (status, app_id))
    return redirect(url_for("index", sort=request.args.get("sort", "date")))


@app.route("/delete/<int:app_id>", methods=["POST"])
def delete(app_id):
    with get_db() as conn:
        conn.execute("DELETE FROM applications WHERE id=?", (app_id,))
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
