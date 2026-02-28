# 🏠 IvoryImmo v4 — Projet complet

## 📁 Architecture finale

```
immo-site-v4/
├── app.py                        ← Serveur Flask principal
├── requirements.txt              ← Dépendances Python
├── Procfile                      ← Commande de démarrage (Render/Heroku)
├── render.yaml                   ← Config déploiement Render.com
├── .env.example                  ← Template variables d'environnement
├── .gitignore
│
├── templates/                    ← Pages HTML (Jinja2)
│   ├── index.html                ← Accueil
│   ├── services.html             ← Catalogue des biens
│   ├── equipe.html               ← Notre équipe
│   ├── contact.html              ← Formulaire de contact
│   └── admin/                   ← Pages d'administration (protégées)
│       ├── base.html             ← Layout partagé admin (sidebar)
│       ├── login.html            ← Page de connexion
│       ├── dashboard.html        ← Tableau de bord
│       ├── properties.html       ← Liste des biens
│       ├── property_form.html    ← Ajout / modification bien + upload image
│       ├── messages.html         ← Messages reçus
│       └── settings.html         ← Changer le mot de passe
│
└── static/
    ├── css/
    │   ├── style.css             ← Styles site public
    │   └── admin.css             ← Styles interface admin
    ├── js/
    │   ├── data.js               ← Données des propriétés
    │   └── shared.js             ← Navbar, Modal, Chatbot IvA, Favoris
    └── uploads/                  ← Images uploadées (ignorées par git)
        └── .gitkeep
```

---

## 🚀 Installation locale

```bash
# 1. Cloner / dézipper le projet
cd immo-site-v4

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer les variables d'environnement
cp .env.example .env
# → Ouvrez .env et remplissez vos valeurs (email, secret key...)

# 5. Lancer l'application
python app.py

# 6. Ouvrir dans le navigateur
# Site public  → http://localhost:5000
# Admin panel  → http://localhost:5000/admin
```

**Identifiants admin par défaut :**
| Champ    | Valeur          |
|----------|-----------------|
| Login    | `admin`         |
| Password | `ivoryimmo2025` |

⚠️ **Changez ce mot de passe dès votre première connexion** dans Admin → Paramètres.

---

## 📬 Configuration Email (Flask-Mail)

### Gmail (recommandé pour débuter)
1. Activez la **validation en deux étapes** sur votre compte Google
2. Allez sur [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Créez un "Mot de passe d'application" pour "Mail"
4. Copiez le code généré dans votre `.env` :

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=votre.email@gmail.com
MAIL_PASSWORD=xxxx xxxx xxxx xxxx
```

### Autres fournisseurs
| Service   | MAIL_SERVER           | MAIL_PORT |
|-----------|-----------------------|-----------|
| Gmail     | smtp.gmail.com        | 587       |
| SendGrid  | smtp.sendgrid.net     | 587       |
| Mailgun   | smtp.mailgun.org      | 587       |
| OVH       | ssl0.ovh.net          | 465       |

---

## 🌐 Déploiement sur Render.com (gratuit)

1. Créez un compte sur [render.com](https://render.com)
2. **New → Web Service → Connect a Git repository**
3. Sélectionnez votre repo GitHub contenant ce projet
4. Render détecte automatiquement le `Procfile`
5. Dans **Environment Variables**, ajoutez :
   - `SECRET_KEY` → une chaîne aléatoire longue
   - `MAIL_USERNAME` → votre email
   - `MAIL_PASSWORD` → votre mot de passe d'application
6. Cliquez **Deploy**
7. Votre site sera accessible sur `https://ivoryimmo.onrender.com`

### Déploiement sur Railway
```bash
npm install -g @railway/cli
railway login
railway init
railway up
```
Ajoutez les variables d'env dans le dashboard Railway.

### Déploiement sur Heroku
```bash
heroku create ivoryimmo
git push heroku main
heroku config:set SECRET_KEY=... MAIL_USERNAME=... MAIL_PASSWORD=...
heroku open
```

---

## ✨ Fonctionnalités complètes

### Site public
- ✅ 4 pages : Accueil, Nos Biens, Équipe, Contact
- ✅ Filtres avancés + recherche + tri + pagination
- ✅ Système de favoris (localStorage)
- ✅ Modal de détail au clic
- ✅ Chatbot IvA (15+ intentions)
- ✅ Design noir & or, responsive

### Admin (protégé par login)
- ✅ **Authentification** sécurisée (hash bcrypt)
- ✅ **Tableau de bord** avec statistiques
- ✅ **CRUD complet** des propriétés (ajouter, modifier, masquer, supprimer)
- ✅ **Upload d'images** avec drag & drop (PNG, JPG, WEBP, max 5 Mo)
- ✅ **Gestion des messages** avec lecture intégrée
- ✅ **Changement de mot de passe** sécurisé

### Email automatique
- ✅ Notification à l'agence à chaque message reçu
- ✅ Email de confirmation automatique envoyé au client
- ✅ Templates HTML élégants aux couleurs IvoryImmo

---

## 🔗 URLs du projet

| Page             | URL                          |
|------------------|------------------------------|
| Accueil          | `/`                          |
| Nos Biens        | `/services`                  |
| Équipe           | `/equipe`                    |
| Contact          | `/contact`                   |
| **Admin login**  | `/admin/login`               |
| **Dashboard**    | `/admin`                     |
| **Propriétés**   | `/admin/properties`          |
| **Messages**     | `/admin/messages`            |
| **Paramètres**   | `/admin/settings`            |
| API biens        | `/api/properties`            |
