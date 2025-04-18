import imaplib
import email
from email.header import decode_header
import os
import re

# Identifiants
username = "ca.sfr@maneoreseaux.com"
password = "ijnn asfl pkrm wbdj "
code_racine = "U512655"
download_base = "C:/Users/maryam/Downloads/teste"

# scanner les label
labels_to_check = ["INBOX", '"[Gmail]/Tous les messages"', "EST", "CENTRE EST", "IDF / NORD", "SUD EST"]

# Connexion
mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(username, password)
print("✅ Connexion réussie")

# Fonction pour lire et sauvegarder les pièces jointes
def traiter_mails(label):
    print(f"\n📂 Traitement du dossier/label : {label}")
    try:
        mail.select(label, readonly=True)
        status, messages = mail.search(None, f'(SUBJECT "{code_racine}")')

        if status != "OK":
            print(" Erreur lors de la recherche.")
            return

        email_ids = messages[0].split()
        print(f"🔍 {len(email_ids)} mail(s) trouvé(s) dans {label}")

        for num in email_ids:
            res, msg_data = mail.fetch(num, "(RFC822)")
            if res != "OK":
                print(" Erreur de récupération du mail.")
                continue

            msg = email.message_from_bytes(msg_data[0][1])
            subject = decode_header(msg["Subject"])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode()

            match = re.search(rf'({code_racine}-\d+)', subject)
            if not match:
                print(f" Aucun code complet trouvé dans : {subject}")
                continue

            code_complet = match.group(1)
            dossier_courant = os.path.join(download_base, code_complet)
            os.makedirs(dossier_courant, exist_ok=True)

            for part in msg.walk():
                if part.get_content_maintype() == "multipart":
                    continue
                if part.get("Content-Disposition") is None:
                    continue

                filename = part.get_filename()
                if filename:
                    filename = decode_header(filename)[0][0]
                    if isinstance(filename, bytes):
                        filename = filename.decode()

                    filepath = os.path.join(dossier_courant, filename)
                    if not os.path.exists(filepath):
                        with open(filepath, "wb") as f:
                            f.write(part.get_payload(decode=True))
                        print(f"📎 Pièce jointe enregistrée : {filepath}")
                    else:
                        print(f"✅ Déjà existante : {filepath}")
    except Exception as e:
        print(f" Erreur avec le label {label} : {str(e)}")

# Lancer la vérification pour chaque libellé
for lbl in labels_to_check:
    traiter_mails(lbl)

mail.logout()
print("\n✅ Téléchargement terminé.")
