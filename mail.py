import imaplib
import email
from email.header import decode_header
import os
import re

# Identifiants Gmail
EMAIL_ACCOUNT = ''
PASSWORD = 'qack gowc mayt uxau'

def download_attachments(mail, email_id, download_folder):
    # Télécharge les pièces jointes d'un e-mail
    status, msg_data = mail.fetch(email_id, "(RFC822)")
    if status == "OK":
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                for part in msg.walk():
                    # Si l'élément est une pièce jointe
                    if part.get_content_disposition() == "attachment":
                        filename = part.get_filename()
                        if filename:
                            filepath = os.path.join(download_folder, filename)
                            with open(filepath, "wb") as f:
                                f.write(part.get_payload(decode=True))
                            print(f"Pièce jointe téléchargée : {filepath}")

def search_email_by_project(mail, project_number, download_folder):
    try:
        # Critère de recherche flexible (en utilisant des expressions régulières pour capter la structure exacte)
        search_criteria = f'SUBJECT "Retour"'
        print(f"Recherche avec le critère : {search_criteria}")

        # Recherche dans le label "Retours terrain"
        status, messages = mail.search(None, search_criteria)

        if status == "OK":
            email_ids = messages[0].split()
            if email_ids:
                print(f"E-mails trouvés pour le projet {project_number} : {len(email_ids)}")
                for email_id in email_ids:
                    status, msg_data = mail.fetch(email_id, "(RFC822)")
                    if status == "OK":
                        for response_part in msg_data:
                            if isinstance(response_part, tuple):
                                msg = email.message_from_bytes(response_part[1])
                                subject = decode_header(msg["Subject"])[0][0]
                                if isinstance(subject, bytes):
                                    subject = subject.decode()
                                print(f"Sujet : {subject}")

                                # Vérification que le sujet contient "U{project_number}"
                                if re.search(rf'(_U{project_number}_)', subject):
                                    download_attachments(mail, email_id, download_folder)
            else:
                print(f"Aucun e-mail trouvé pour le projet {project_number}.")
        else:
            print(f"Erreur lors de la recherche : {status}")

    except Exception as e:
        print(f"Erreur lors de la recherche : {e}")

def main():
    try:
        # Connexion au serveur Gmail
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL_ACCOUNT, PASSWORD)

        # Sélectionnez le label "Retours terrain"
        label_name = "Retours terrain"
        status, _ = mail.select(f'"{label_name}"')  # Gestion des espaces dans le nom du label
        if status != "OK":
            print(f"Impossible de sélectionner le label : {label_name}")
            return

        # Créer un dossier pour les téléchargements
        download_folder = "downloaded_attachments"
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        # Demander le numéro de projet à rechercher
        project_number = input("Entrez le numéro de projet à rechercher (ex: 501147) : ")

        # Lancer la recherche et télécharger les e-mails
        search_email_by_project(mail, project_number, download_folder)

    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        # Déconnexion du serveur
        mail.logout()

if __name__ == "__main__":
    main()
