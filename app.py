"""
IVORY IMMO — app.py v4
Fonctionnalités : Auth admin, Upload images, Email (Flask-Mail), API REST, SQLite
"""

from flask import (Flask, render_template, request, jsonify,
                   redirect, url_for, session, flash)
from flask_mail import Mail, Message as MailMessage
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import sqlite3, os, uuid

# ══════════════════════════════════════════════════════════
# CONFIGURATION
# ══════════════════════════════════════════════════════════
app = Flask(__name__)

app.config.update(
    SECRET_KEY = os.environ.get("SECRET_KEY", "ivoryimmo-secret-change-in-prod"),

    # ── Upload images ──────────────────────────────────────
    UPLOAD_FOLDER  = os.path.join(os.path.dirname(__file__), "static", "uploads"),
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024,   # 5 Mo max par fichier
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"},

    # ── Flask-Mail ─────────────────────────────────────────
    # → Remplacer par vos vraies valeurs ou définir en variables d'environnement
    MAIL_SERVER   = os.environ.get("MAIL_SERVER",   "smtp.gmail.com"),
    MAIL_PORT     = int(os.environ.get("MAIL_PORT", 587)),
    MAIL_USE_TLS  = True,
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "votre.email@gmail.com"),
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "votre_mot_de_passe_app"),
    MAIL_DEFAULT_SENDER = ("IvoryImmo", os.environ.get("MAIL_USERNAME", "votre.email@gmail.com")),
)

mail    = Mail(app)
DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


# ══════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def allowed_file(filename):
    return ("." in filename and
            filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"])

def login_required(f):
    """Décorateur : protège les routes admin."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_logged_in"):
            flash("Veuillez vous connecter pour accéder à l'administration.", "warning")
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated


# ══════════════════════════════════════════════════════════
# BASE DE DONNÉES
# ══════════════════════════════════════════════════════════

def init_db():
    conn = get_db(); c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS properties (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        title         TEXT NOT NULL,
        type          TEXT NOT NULL,        -- appartement | studio | villa
        location      TEXT NOT NULL,
        image         TEXT,                 -- URL externe ou chemin /static/uploads/...
        surface       TEXT,
        pieces        TEXT,
        etage         TEXT,
        parking       TEXT,
        description   TEXT,
        prix_location TEXT,
        prix_vente    TEXT,
        modes         TEXT NOT NULL,        -- "location" | "vente" | "location,vente"
        disponible    INTEGER DEFAULT 1,
        created_at    TEXT DEFAULT CURRENT_TIMESTAMP
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        nom        TEXT NOT NULL,
        email      TEXT NOT NULL,
        telephone  TEXT,
        objet      TEXT,
        type_bien  TEXT,
        message    TEXT NOT NULL,
        lu         INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")

    c.execute("""
    CREATE TABLE IF NOT EXISTS admin_users (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        username      TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at    TEXT DEFAULT CURRENT_TIMESTAMP
    )""")

    # Créer admin par défaut si aucun n'existe
    c.execute("SELECT COUNT(*) FROM admin_users")
    if c.fetchone()[0] == 0:
        c.execute(
            "INSERT INTO admin_users (username, password_hash) VALUES (?, ?)",
            ("admin", generate_password_hash("ivoryimmo2025"))
        )
        print("👤 Admin créé — login: admin / password: ivoryimmo2025")
        print("   ⚠️  Changez ce mot de passe dans l'interface admin !")

    # Données de démo
    c.execute("SELECT COUNT(*) FROM properties")
    if c.fetchone()[0] == 0:
        demo = [
            ("Appartement Luxe Cocody","appartement","Cocody, Abidjan",
             "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=700",
             "120 m²","4 pièces","3ème étage","1 place",
             "Magnifique appartement lumineux en plein cœur de Cocody. Vue dégagée, cuisine équipée, balcon spacieux. Résidence sécurisée avec gardien 24h/24.",
             "350 000 FCFA/mois","65 000 000 FCFA","location,vente"),
            ("Studio Moderne Plateau","studio","Le Plateau, Abidjan",
             "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=700",
             "35 m²","1 pièce","2ème étage","Non inclus",
             "Studio entièrement rénové, idéal pour jeune professionnel. Proche de toutes commodités.",
             "120 000 FCFA/mois","15 000 000 FCFA","location,vente"),
            ("Villa Prestige Riviera","villa","Riviera Golf, Abidjan",
             "https://images.unsplash.com/photo-1416331108676-a22ccb276e35?w=700",
             "450 m²","6 pièces","R+1","3 places",
             "Villa d'exception avec piscine privée, jardin tropical, salle de sport équipée.",
             "1 500 000 FCFA/mois","350 000 000 FCFA","location,vente"),
            ("Appartement Vue Mer Bassam","appartement","Grand-Bassam",
             "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=700",
             "80 m²","3 pièces","4ème étage","1 place",
             "Appartement avec vue imprenable sur l'océan Atlantique. Grande terrasse privatisée.",
             "280 000 FCFA/mois","45 000 000 FCFA","location,vente"),
            ("Studio Étudiant Deux-Plateaux","studio","Deux-Plateaux, Abidjan",
             "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=700",
             "28 m²","1 pièce","1er étage","Non inclus",
             "Studio fonctionnel proche des universités. Cuisine équipée, climatisation.",
             "80 000 FCFA/mois",None,"location"),
            ("Villa Contemporaine Angré","villa","Angré, Abidjan",
             "https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=700",
             "320 m²","5 pièces","R+1","2 places",
             "Villa de style contemporain avec matériaux nobles et architecture soignée.",
             None,"180 000 000 FCFA","vente"),
        ]
        c.executemany("""
            INSERT INTO properties (title,type,location,image,surface,pieces,etage,parking,
                                    description,prix_location,prix_vente,modes)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""", demo)

    conn.commit(); conn.close()
    print("✅ Base de données prête.")


# ══════════════════════════════════════════════════════════
# ROUTES PUBLIQUES
# ══════════════════════════════════════════════════════════

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/equipe")
def equipe():
    return render_template("equipe.html")

@app.route("/contact", methods=["GET"])
def contact_page():
    return render_template("contact.html")


# ── API REST ───────────────────────────────────────────────

@app.route("/api/properties")
def api_properties():
    type_f = request.args.get("type", "all")
    mode_f = request.args.get("mode", "all")
    search = request.args.get("q",    "").strip().lower()

    conn = get_db(); c = conn.cursor()
    sql    = "SELECT * FROM properties WHERE disponible=1"
    params = []
    if type_f != "all": sql += " AND type=?";  params.append(type_f)
    if mode_f != "all": sql += " AND modes LIKE ?"; params.append(f"%{mode_f}%")
    if search:
        sql += " AND (LOWER(title) LIKE ? OR LOWER(location) LIKE ?)";
        params += [f"%{search}%", f"%{search}%"]
    sql += " ORDER BY created_at DESC"
    rows = c.execute(sql, params).fetchall()
    conn.close()
    return jsonify([dict(r) | {"modes": r["modes"].split(",")} for r in rows])

@app.route("/api/properties/<int:pid>")
def api_property(pid):
    conn = get_db()
    row  = conn.execute("SELECT * FROM properties WHERE id=?", (pid,)).fetchone()
    conn.close()
    if not row: return jsonify({"error": "Introuvable"}), 404
    d = dict(row); d["modes"] = d["modes"].split(",")
    return jsonify(d)


# ── Formulaire contact ─────────────────────────────────────

@app.route("/contact", methods=["POST"])
def contact_post():
    nom       = request.form.get("nom",       "").strip()
    email     = request.form.get("email",     "").strip()
    telephone = request.form.get("telephone", "").strip()
    objet     = request.form.get("objet",     "")
    type_bien = request.form.get("type_bien", "")
    message   = request.form.get("message",   "").strip()

    if not nom or not email or not message:
        return jsonify({"success": False, "error": "Champs requis manquants"}), 400

    # Enregistrement en base
    conn = get_db()
    conn.execute(
        "INSERT INTO messages (nom, email, telephone, objet, type_bien, message) VALUES (?,?,?,?,?,?)",
        (nom, email, telephone, objet, type_bien, message))
    conn.commit(); conn.close()

    # ── Envoi email (notification à l'agence) ─────────────
    try:
        msg = MailMessage(
            subject=f"[IvoryImmo] Nouveau message — {objet or 'Contact général'}",
            recipients=[app.config["MAIL_USERNAME"]],
            html=f"""
            <div style="font-family:sans-serif;max-width:600px;margin:0 auto;
                        background:#141416;color:#e0e0e0;border-radius:12px;overflow:hidden">
              <div style="background:#C9A84C;padding:24px 30px">
                <h2 style="color:#0f0f0f;margin:0">🏠 IvoryImmo — Nouveau message</h2>
              </div>
              <div style="padding:28px 30px">
                <table style="width:100%;border-collapse:collapse">
                  <tr><td style="padding:8px 0;color:#888;width:140px">Nom</td>
                      <td style="padding:8px 0;font-weight:600">{nom}</td></tr>
                  <tr><td style="padding:8px 0;color:#888">Email</td>
                      <td style="padding:8px 0"><a href="mailto:{email}" style="color:#C9A84C">{email}</a></td></tr>
                  <tr><td style="padding:8px 0;color:#888">Téléphone</td>
                      <td style="padding:8px 0">{telephone or '—'}</td></tr>
                  <tr><td style="padding:8px 0;color:#888">Objet</td>
                      <td style="padding:8px 0">{objet or '—'}</td></tr>
                  <tr><td style="padding:8px 0;color:#888">Type de bien</td>
                      <td style="padding:8px 0">{type_bien or '—'}</td></tr>
                </table>
                <hr style="border:1px solid #333;margin:20px 0"/>
                <p style="color:#888;margin-bottom:8px">Message :</p>
                <p style="background:#1e1e22;padding:16px;border-radius:8px;
                           border-left:3px solid #C9A84C;line-height:1.6">{message}</p>
              </div>
              <div style="padding:16px 30px;background:#1e1e22;font-size:0.78rem;color:#555;text-align:center">
                IvoryImmo · Abidjan, Côte d'Ivoire
              </div>
            </div>"""
        )
        mail.send(msg)

        # Email de confirmation au client
        confirm = MailMessage(
            subject="IvoryImmo — Votre message a bien été reçu",
            recipients=[email],
            html=f"""
            <div style="font-family:sans-serif;max-width:600px;margin:0 auto;
                        background:#141416;color:#e0e0e0;border-radius:12px;overflow:hidden">
              <div style="background:#C9A84C;padding:24px 30px">
                <h2 style="color:#0f0f0f;margin:0">🏠 IvoryImmo</h2>
              </div>
              <div style="padding:28px 30px">
                <p>Bonjour <strong>{nom}</strong>,</p>
                <p>Nous avons bien reçu votre message et notre équipe vous répondra sous <strong>24h</strong>.</p>
                <p>En attendant, n'hésitez pas à consulter nos biens disponibles sur notre site.</p>
                <div style="margin:28px 0;text-align:center">
                  <a href="http://localhost:5000/services"
                     style="background:#C9A84C;color:#0f0f0f;padding:14px 32px;
                            border-radius:8px;text-decoration:none;font-weight:600">
                    Voir nos biens →
                  </a>
                </div>
                <hr style="border:1px solid #333;margin:20px 0"/>
                <p style="color:#888;font-size:0.85rem">
                  📞 +225 00 00 00 00 &nbsp;|&nbsp; ✉️ contact@ivoryimmo.ci<br/>
                  📍 Cocody Riviera, Abidjan
                </p>
              </div>
            </div>"""
        )
        mail.send(confirm)
    except Exception as e:
        print(f"⚠️  Email non envoyé : {e}")   # Ne bloque pas la réponse

    return jsonify({"success": True})


# ══════════════════════════════════════════════════════════
# ADMIN — AUTHENTIFICATION
# ══════════════════════════════════════════════════════════

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if session.get("admin_logged_in"):
        return redirect(url_for("admin_dashboard"))

    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        conn = get_db()
        user = conn.execute(
            "SELECT * FROM admin_users WHERE username=?", (username,)).fetchone()
        conn.close()
        if user and check_password_hash(user["password_hash"], password):
            session["admin_logged_in"] = True
            session["admin_username"]  = username
            return redirect(url_for("admin_dashboard"))
        error = "Identifiants incorrects."
    return render_template("admin/login.html", error=error)


@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("admin_login"))


# ══════════════════════════════════════════════════════════
# ADMIN — TABLEAU DE BORD
# ══════════════════════════════════════════════════════════

@app.route("/admin")
@login_required
def admin_dashboard():
    conn  = get_db()
    stats = {
        "properties": conn.execute("SELECT COUNT(*) FROM properties WHERE disponible=1").fetchone()[0],
        "messages":   conn.execute("SELECT COUNT(*) FROM messages").fetchone()[0],
        "unread":     conn.execute("SELECT COUNT(*) FROM messages WHERE lu=0").fetchone()[0],
        "vente":      conn.execute("SELECT COUNT(*) FROM properties WHERE modes LIKE '%vente%'").fetchone()[0],
        "location":   conn.execute("SELECT COUNT(*) FROM properties WHERE modes LIKE '%location%'").fetchone()[0],
    }
    recent_msgs  = conn.execute("SELECT * FROM messages  ORDER BY created_at DESC LIMIT 5").fetchall()
    recent_props = conn.execute("SELECT * FROM properties ORDER BY created_at DESC LIMIT 5").fetchall()
    conn.close()
    return render_template("admin/dashboard.html",
                           stats=stats,
                           recent_msgs=recent_msgs,
                           recent_props=recent_props)


# ══════════════════════════════════════════════════════════
# ADMIN — GESTION DES BIENS
# ══════════════════════════════════════════════════════════

@app.route("/admin/properties")
@login_required
def admin_properties():
    conn  = get_db()
    props = conn.execute("SELECT * FROM properties ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template("admin/properties.html", properties=props)


@app.route("/admin/properties/new", methods=["GET", "POST"])
@login_required
def admin_property_new():
    if request.method == "POST":
        return _save_property(None)
    return render_template("admin/property_form.html", prop=None, action="Ajouter")


@app.route("/admin/properties/<int:pid>/edit", methods=["GET", "POST"])
@login_required
def admin_property_edit(pid):
    conn = get_db()
    prop = conn.execute("SELECT * FROM properties WHERE id=?", (pid,)).fetchone()
    conn.close()
    if not prop: flash("Bien introuvable.", "error"); return redirect(url_for("admin_properties"))
    if request.method == "POST":
        return _save_property(pid)
    return render_template("admin/property_form.html", prop=prop, action="Modifier")


@app.route("/admin/properties/<int:pid>/toggle", methods=["POST"])
@login_required
def admin_property_toggle(pid):
    conn = get_db()
    conn.execute("UPDATE properties SET disponible = 1 - disponible WHERE id=?", (pid,))
    conn.commit(); conn.close()
    return redirect(url_for("admin_properties"))


@app.route("/admin/properties/<int:pid>/delete", methods=["POST"])
@login_required
def admin_property_delete(pid):
    conn = get_db()
    # Supprimer l'image locale si elle existe
    prop = conn.execute("SELECT image FROM properties WHERE id=?", (pid,)).fetchone()
    if prop and prop["image"] and prop["image"].startswith("/static/uploads/"):
        img_path = os.path.join(os.path.dirname(__file__), prop["image"].lstrip("/"))
        if os.path.exists(img_path):
            os.remove(img_path)
    conn.execute("DELETE FROM properties WHERE id=?", (pid,))
    conn.commit(); conn.close()
    flash("Bien supprimé.", "success")
    return redirect(url_for("admin_properties"))


def _save_property(pid):
    """Crée ou met à jour un bien (avec upload d'image)."""
    f = request.form

    # ── Gestion de l'image ─────────────────────────────────
    image_url = f.get("image_url", "").strip()   # URL externe existante
    file = request.files.get("image_file")

    if file and file.filename and allowed_file(file.filename):
        ext      = file.filename.rsplit(".", 1)[1].lower()
        filename = secure_filename(f"{uuid.uuid4().hex}.{ext}")
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(save_path)
        image_url = f"/static/uploads/{filename}"

    # Construire "modes"
    modes_list = request.form.getlist("modes")
    modes = ",".join(modes_list) if modes_list else "location"

    data = (
        f.get("title","").strip(),
        f.get("type","appartement"),
        f.get("location","").strip(),
        image_url or None,
        f.get("surface","").strip()  or None,
        f.get("pieces","").strip()   or None,
        f.get("etage","").strip()    or None,
        f.get("parking","").strip()  or None,
        f.get("description","").strip() or None,
        f.get("prix_location","").strip() or None,
        f.get("prix_vente","").strip()    or None,
        modes,
        1 if f.get("disponible") else 0,
    )

    conn = get_db()
    if pid is None:
        conn.execute("""
            INSERT INTO properties (title,type,location,image,surface,pieces,etage,parking,
                                    description,prix_location,prix_vente,modes,disponible)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", data)
        flash("Bien ajouté avec succès !", "success")
    else:
        conn.execute("""
            UPDATE properties SET title=?,type=?,location=?,image=?,surface=?,pieces=?,
            etage=?,parking=?,description=?,prix_location=?,prix_vente=?,modes=?,disponible=?
            WHERE id=?""", (*data, pid))
        flash("Bien modifié avec succès !", "success")
    conn.commit(); conn.close()
    return redirect(url_for("admin_properties"))


# ── Upload image standalone (drag & drop) ─────────────────

@app.route("/admin/upload", methods=["POST"])
@login_required
def admin_upload():
    file = request.files.get("file")
    if not file or not allowed_file(file.filename):
        return jsonify({"success": False, "error": "Fichier invalide"}), 400
    ext      = file.filename.rsplit(".", 1)[1].lower()
    filename = secure_filename(f"{uuid.uuid4().hex}.{ext}")
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    return jsonify({"success": True, "url": f"/static/uploads/{filename}"})


# ══════════════════════════════════════════════════════════
# ADMIN — MESSAGES
# ══════════════════════════════════════════════════════════

@app.route("/admin/messages")
@login_required
def admin_messages():
    conn  = get_db()
    msgs  = conn.execute("SELECT * FROM messages ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template("admin/messages.html", messages=msgs)


@app.route("/admin/messages/<int:mid>/read", methods=["POST"])
@login_required
def admin_message_read(mid):
    conn = get_db()
    conn.execute("UPDATE messages SET lu=1 WHERE id=?", (mid,))
    conn.commit(); conn.close()
    return redirect(url_for("admin_messages"))


@app.route("/admin/messages/<int:mid>/delete", methods=["POST"])
@login_required
def admin_message_delete(mid):
    conn = get_db()
    conn.execute("DELETE FROM messages WHERE id=?", (mid,))
    conn.commit(); conn.close()
    flash("Message supprimé.", "success")
    return redirect(url_for("admin_messages"))


# ══════════════════════════════════════════════════════════
# ADMIN — PARAMÈTRES (changer le mot de passe)
# ══════════════════════════════════════════════════════════

@app.route("/admin/settings", methods=["GET", "POST"])
@login_required
def admin_settings():
    msg = None
    if request.method == "POST":
        current  = request.form.get("current_password", "")
        new_pw   = request.form.get("new_password",     "")
        confirm  = request.form.get("confirm_password", "")
        username = session["admin_username"]

        conn = get_db()
        user = conn.execute("SELECT * FROM admin_users WHERE username=?", (username,)).fetchone()

        if not check_password_hash(user["password_hash"], current):
            msg = ("error", "Mot de passe actuel incorrect.")
        elif new_pw != confirm:
            msg = ("error", "Les nouveaux mots de passe ne correspondent pas.")
        elif len(new_pw) < 8:
            msg = ("error", "Le mot de passe doit contenir au moins 8 caractères.")
        else:
            conn.execute(
                "UPDATE admin_users SET password_hash=? WHERE username=?",
                (generate_password_hash(new_pw), username))
            conn.commit()
            msg = ("success", "Mot de passe modifié avec succès !")
        conn.close()

    return render_template("admin/settings.html", msg=msg)


# ══════════════════════════════════════════════════════════
# Initialiser la DB au démarrage (important pour Render/production)
with app.app_context():
    init_db()

if __name__ == "__main__":
    print("🏠 IvoryImmo v4  →  http://localhost:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)