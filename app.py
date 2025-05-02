from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
from calendar import monthrange
from collections import defaultdict
import pyodbc

app = Flask(__name__)
app.secret_key = "secret_key"

def get_connection():
    return pyodbc.connect(
        'DRIVER={FreeTDS};'
        'SERVER=X;'
        'PORT=X;'
        'UID=X;'
        'PWD=X;'
        'DATABASE=X;'
        'TDS_Version=7.4;'
    )

def log_event(user_id, action, info=""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (user_id, action, info, timestamp) VALUES (?, ?, ?, ?)",
                   (user_id, action, info, datetime.now()))
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        user_id = request.form["id"]
        password = request.form["password"]
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, surname, role, blocked FROM users WHERE id = ? AND password = ?", (user_id, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            if user.blocked:
                message = "Account is blocked."
            else:
                session["id"] = user.id
                session["name"] = user.name
                session["surname"] = user.surname
                session["role"] = user.role
                log_event(user.id, "login")
                return redirect(url_for("dashboard"))
        else:
            message = "Invalid login credentials."
    return render_template("login.html", error=message)

@app.route("/logout")
def logout():
    if "id" in session:
        log_event(session["id"], "logout")
    session.clear()
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    if "id" not in session:
        return redirect(url_for("login"))
    if session["role"] == "admin":
        return render_template("admin_dashboard.html", user=session["name"])
    else:
        return redirect(url_for("activity"))

@app.route("/admin/users", methods=["GET"])
def admin_users():
    if "id" not in session or session["role"] != "admin":
        return redirect(url_for("login"))
    filter_text = request.args.get("filter", default="")
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT id, name, surname, role, blocked
        FROM users
        WHERE name LIKE ? OR surname LIKE ? OR role LIKE ?
    """
    like_filter = f"%{filter_text}%"
    cursor.execute(query, (like_filter, like_filter, like_filter))
    rows = cursor.fetchall()
    users = [{"id": r.id, "name": r.name, "surname": r.surname, "role": r.role, "blocked": r.blocked} for r in rows]
    conn.close()
    return render_template("admin_users.html", users=users, current_admin=session["id"], filter=filter_text)

@app.route("/admin/view_user/<user_id>")
def admin_view_user(user_id):
    if "id" not in session or session["role"] != "admin":
        return redirect(url_for("login"))
    return redirect(url_for("activity", user_id=user_id))

@app.route("/block_user/<user_id>")
def block_user(user_id):
    if "id" not in session or session["role"] != "admin" or user_id == str(session["id"]):
        return redirect(url_for("admin_users"))
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET blocked = 1 WHERE id = ?", (user_id,))
    log_event(session["id"], "block user", f"blocked user {user_id}")
    conn.commit()
    conn.close()
    return redirect(url_for("admin_users"))

@app.route("/unblock_user/<user_id>")
def unblock_user(user_id):
    if "id" not in session or session["role"] != "admin":
        return redirect(url_for("admin_users"))
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET blocked = 0 WHERE id = ?", (user_id,))
    log_event(session["id"], "unblock user", f"unblocked user {user_id}")
    conn.commit()
    conn.close()
    return redirect(url_for("admin_users"))

@app.route("/delete_user/<user_id>")
def delete_user(user_id):
    if "id" not in session or session["role"] != "admin" or user_id == str(session["id"]):
        return redirect(url_for("admin_users"))
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM logs WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    log_event(session["id"], "delete user", f"deleted user {user_id}")
    conn.commit()
    conn.close()
    return redirect(url_for("admin_users"))

@app.route("/activity", methods=["GET"])
def activity():
    if "id" not in session:
        return redirect(url_for("login"))

    user_id = session["id"]
    role = session["role"]

    selected_year = request.args.get("year", type=int)
    selected_month = request.args.get("month", type=int)

    now = datetime.now()
    if not selected_year:
        selected_year = now.year
    if not selected_month:
        selected_month = now.month

    conn = get_connection()
    cursor = conn.cursor()

    if role == "admin" and request.args.get("user_id"):
        target_user_id = request.args.get("user_id")
    else:
        target_user_id = user_id

    first_day = datetime(selected_year, selected_month, 1)
    last_day = datetime(selected_year, selected_month, monthrange(selected_year, selected_month)[1], 23, 59, 59)

    cursor.execute("""
        SELECT action, timestamp FROM logs
        WHERE user_id = ? AND timestamp BETWEEN ? AND ?
        ORDER BY timestamp ASC
    """, (target_user_id, first_day, last_day))
    records = cursor.fetchall()
    conn.close()

    days = defaultdict(list)

    for r in records:
        day = r.timestamp.date()
        days[day].append({"action": r.action, "time": r.timestamp.time()})

    days = dict(sorted(days.items()))

    return render_template("user_dashboard.html",
                           user=session["name"],
                           attendance_days=days,
                           selected_year=selected_year,
                           selected_month=selected_month,
                           is_admin=(role == "admin"),
                           target_user_id=target_user_id)

@app.route("/log_presence", methods=["POST"])
def log_presence():
    if "id" not in session:
        return redirect(url_for("login"))

    user_id = session["id"]

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT action FROM logs WHERE user_id = ? ORDER BY timestamp DESC", (user_id,))
    row = cursor.fetchone()
    last_action = row.action if row else None

    new_action = "exit" if last_action == "entry" else "entry"

    log_event(user_id, new_action)

    return redirect(url_for("dashboard"))

@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    if "id" not in session:
        return redirect(url_for("login"))
    message = ""
    if request.method == "POST":
        new_pass = request.form["new_password"]
        confirm_pass = request.form["confirm_password"]
        if new_pass != confirm_pass:
            message = "Passwords do not match."
        else:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET password = ? WHERE id = ?", (new_pass, session["id"]))
            log_event(session["id"], "password change")
            conn.commit()
            conn.close()
            return redirect(url_for("dashboard"))
    return render_template("change_password.html", error=message)

if __name__ == "__main__":
    app.run(debug=True)
