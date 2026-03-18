# Instructions pour pousser le code vers GitHub

## 📋 Pré-requis

Git n'est pas installé sur votre système. Vous avez deux options :

---

## ✅ Option 1 : Installer Git (Recommandé)

### 1. Télécharger et installer Git
- Téléchargez Git depuis : https://git-scm.com/download/win
- Installez-le avec les options par défaut
- Redémarrez votre terminal PowerShell après l'installation

### 2. Configurer Git (première fois)
```powershell
git config --global user.name "Votre Nom"
git config --global user.email "votre.email@example.com"
```

### 3. Initialiser et pousser vers GitHub
```powershell
# Vérifier que Git est installé
git --version

# Ajouter le remote GitHub
git remote add origin https://github.com/hachokake/ma-pharmacie-.git

# Ajouter tous les fichiers
git add .

# Créer le premier commit
git commit -m "Initial commit - Système de gestion de pharmacie"

# Renommer la branche en main (si nécessaire)
git branch -M main

# Pousser vers GitHub
git push -u origin main
```

---

## ✅ Option 2 : Utiliser GitHub Desktop (Plus facile)

### 1. Télécharger GitHub Desktop
- Téléchargez depuis : https://desktop.github.com/
- Installez et connectez-vous avec votre compte GitHub

### 2. Ajouter votre projet
1. Ouvrez GitHub Desktop
2. File → Add Local Repository
3. Sélectionnez le dossier : `C:\Users\Ir. HACHOKAKE\Desktop\PHARMACIE - APK`
4. Cliquez sur "create a repository" si demandé

### 3. Publier sur GitHub
1. Cliquez sur "Publish repository"
2. Nom : `ma-pharmacie-`
3. Décochez "Keep this code private" si vous voulez le rendre public
4. Cliquez sur "Publish Repository"

---

## 📝 Fichiers importants créés

- ✅ `.gitignore` : Fichier pour exclure les fichiers sensibles et temporaires
  - Exclut `db.sqlite3` (base de données)
  - Exclut `__pycache__` et fichiers Python compilés
  - Exclut les logs et fichiers temporaires
  - Exclut les dossiers media avec photos

---

## ⚠️ Informations importantes

### Fichiers qui NE seront PAS envoyés sur GitHub (pour votre sécurité) :
- ❌ `db.sqlite3` - Base de données
- ❌ Fichiers `__pycache__/`
- ❌ Logs
- ❌ Photos des employés dans media/
- ❌ Fichiers `.env` (si vous en créez)

### Ce qui SERA envoyé :
- ✅ Tout le code source Python
- ✅ Templates HTML
- ✅ Configuration Django
- ✅ Requirements.txt
- ✅ Documentation
- ✅ Scripts batch et Python

---

## 🔒 Recommandations de sécurité

Avant de pousser vers GitHub :

1. **Vérifiez settings.py** - Ne mettez pas de clés secrètes
2. **Base de données** - Ne committez jamais `db.sqlite3`
3. **Variables sensibles** - Utilisez des variables d'environnement
4. **Mot de passe GitHub** - Utilisez un token d'accès personnel

---

## 🆘 Besoin d'aide ?

Si vous rencontrez des problèmes :
1. Vérifiez que Git est bien installé : `git --version`
2. Vérifiez que vous êtes dans le bon dossier
3. Utilisez GitHub Desktop pour une approche plus visuelle
