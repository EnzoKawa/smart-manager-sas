from flask import Flask, render_template, request, session, redirect, url_for
import os  # Ajoutez ceci pour gérer les chemins de fichiers

import firebase_admin
from firebase_admin import credentials, auth

app = Flask(__name__)
app.secret_key = 'votre_clé_secrète'

# Obtenez le chemin absolu du répertoire contenant ce fichier
root_dir = os.path.dirname(os.path.abspath(__file__))

# Initialisez Firebase avec le fichier de configuration
cred = credentials.Certificate(os.path.join(root_dir, 'psc-manager-firebase-adminsdk.json'))
firebase_admin.initialize_app(cred)

# Page d'accueil de connexion
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        email = request.form['email']
        password = request.form['password']

        try:
            # Vérifier l'authentification de l'utilisateur avec Firebase
            user = auth.get_user_by_email(email)
            if user:
                # Authentification réussie
                session['email'] = email
                return redirect(url_for('dashboard'))
        except firebase_admin.auth.AuthError:
            # Afficher un message d'erreur si l'authentification échoue
            error = 'Adresse e-mail ou mot de passe incorrect'
            return render_template('login.html', error=error)

    # Afficher le formulaire de connexion
    return render_template('login.html')

# Tableau de bord protégé par l'authentification
@app.route('/dashboard')
def dashboard():
    # Vérifier si l'utilisateur est connecté
    if 'email' in session:
        # Afficher le tableau de bord
        return render_template('dashboard.html', email=session['email'])
    else:
        # Rediriger vers la page de connexion si l'utilisateur n'est pas connecté
        return redirect(url_for('login'))

# Déconnexion de l'utilisateur
@app.route('/logout')
def logout():
    # Supprimer l'adresse e-mail de l'utilisateur de la session
    session.pop('email', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')