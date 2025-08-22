#!/usr/bin/env python3
import os, subprocess, sys, base64

# -------------------------------------------------------------------
# CONFIGURATION VIA ENVIRONMENT VARIABLES
# -------------------------------------------------------------------
# GCP
GCP_KEY_NAME     = os.getenv("GCP_KMS_KEY")       # e.g. ansible-master-key
GCP_KEYRING      = os.getenv("GCP_KMS_KEYRING")   # e.g. ansible-keyring
GCP_LOCATION     = os.getenv("GCP_KMS_LOCATION")  # e.g. global
GCP_PROJECT      = os.getenv("GCP_PROJECT")       # optional, use active project
GCP_ENC_FILE     = os.getenv("GCP_ENC_FILE", "ansible-vault.gcp.enc")

# AZURE
AZURE_KEY_NAME   = os.getenv("AZURE_KEY_NAME")    # e.g. ansible-master-key
AZURE_VAULT_NAME = os.getenv("AZURE_VAULT_NAME")  # e.g. ansible-vault-kv
AZURE_ENC_FILE   = os.getenv("AZURE_ENC_FILE", "ansible-vault.azure.enc")

# -------------------------------------------------------------------
def decrypt_gcp():
    cmd = [
        "gcloud", "kms", "decrypt",
        "--key", GCP_KEY_NAME,
        "--keyring", GCP_KEYRING,
        "--location", GCP_LOCATION,
        "--ciphertext-file", GCP_ENC_FILE,
        "--plaintext-file", "-"
    ]
    if GCP_PROJECT:
        cmd.extend(["--project", GCP_PROJECT])

    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout.strip()

def decrypt_azure():
    # Load ciphertext file and base64 encode for az CLI
    with open(AZURE_ENC_FILE, "rb") as f:
        ciphertext_b64 = base64.b64encode(f.read()).decode()

    cmd = [
        "az", "keyvault", "key", "decrypt",
        "--vault-name", AZURE_VAULT_NAME,
        "--name", AZURE_KEY_NAME,
        "--algorithm", "RSA-OAEP",
        "--value", ciphertext_b64,
        "--query", "result",
        "--output", "tsv"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout.strip()

def main():
    cloud = os.getenv("CLOUD_PROVIDER", "").lower()

    try:
        if cloud == "gcp" or (not cloud and os.path.exists(GCP_ENC_FILE)):
            if not (GCP_KEY_NAME and GCP_KEYRING and GCP_LOCATION):
                sys.stderr.write("❌ Missing GCP_* environment variables\n")
                sys.exit(1)
            key = decrypt_gcp()

        elif cloud == "azure" or (not cloud and os.path.exists(AZURE_ENC_FILE)):
            if not (AZURE_KEY_NAME and AZURE_VAULT_NAME):
                sys.stderr.write("❌ Missing AZURE_* environment variables\n")
                sys.exit(1)
            key = decrypt_azure()

        else:
            sys.stderr.write("❌ Could not detect cloud provider or missing encrypted file.\n")
            sys.exit(1)

    except subprocess.CalledProcessError as e:
        sys.stderr.write(f"❌ Decrypt failed: {e.stderr}\n")
        sys.exit(1)

    sys.stdout.write(key)

if __name__ == "__main__":
    main()
