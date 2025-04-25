📄 Description du script – Téléchargement automatique des pièces jointes Gmail



Ce script Python permet de se connecter à une boîte mail Gmail via IMAP, de rechercher des mails contenant un code spécifique dans l’objet,


et de télécharger automatiquement les pièces jointes associées dans des dossiers nommés selon ce code.

🔧 Fonctionnalités principales :
Connexion sécurisée à Gmail avec imaplib via IMAP SSL.

Scan de plusieurs labels (dossiers) dans la boîte mail, définis dans la liste labels_to_check.

Pour chaque label :

Recherche des mails dont l’objet contient le code racine U512655.

Extraction du code complet au format U512655-XXXX depuis le sujet du mail.

Création automatique d’un dossier local pour ce code complet.

Téléchargement et sauvegarde de chaque pièce jointe du mail dans le dossier correspondant.

Évitement des doublons : les pièces jointes déjà présentes ne sont pas re-téléchargées.

Gestion des erreurs avec des messages explicites pour chaque étape.
