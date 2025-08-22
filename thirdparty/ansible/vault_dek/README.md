
---

### 🔑 Concept

* You create **one master data key (DEK)** that Ansible Vaults are encrypted with.
* That DEK is then **encrypted (“wrapped”) by each provider’s KMS**:

  * Wrapped copy in GCP KMS
  * Wrapped copy in Azure Key Vault
* You check in or distribute those wrapped blobs.

When running in:

* **GCP** → Ansible unlock script calls GCP KMS to unwrap DEK.
* **Azure** → unlock script calls Azure Key Vault to unwrap DEK.

The **plaintext DEK** that comes out is identical in both cases, so your Ansible Vault files decrypt the same way everywhere.

---

### 🖼 Example

#### 1. Generate a DEK

```bash
openssl rand -base64 32 > ansible-vault.key
```

#### 2. Encrypt (wrap) it in GCP

```bash
gcloud kms encrypt \
  --key my-key \
  --keyring my-keyring \
  --location global \
  --plaintext-file ansible-vault.key \
  --ciphertext-file ansible-vault.gcp.enc
```

#### 3. Encrypt (wrap) it in Azure

```bash
az keyvault key encrypt \
  --vault-name MyVault \
  --name MyKey \
  --algorithm RSA-OAEP \
  --value "$(base64 -w0 ansible-vault.key)" \
  --output-file ansible-vault.azure.enc
```

Now you have:

* `ansible-vault.gcp.enc`
* `ansible-vault.azure.enc`

Both represent the **same DEK**, just wrapped with each cloud’s own KMS key.

---

### 4. Ansible Unlock Scripts

* **GCP runner** → `vault-pass-gcp.py` calls GCP KMS decrypt on `ansible-vault.gcp.enc`.
* **Azure runner** → `vault-pass-azure.py` calls Azure Key Vault decrypt on `ansible-vault.azure.enc`.

Both scripts return the same plaintext DEK → Ansible Vault unlocks successfully.

---

### 🌍 Multi-cloud Reality

* Yes, each KMS is independent. They don’t “share” keys directly.
* But you only need **one DEK** — and you can “wrap” that DEK with as many KMS providers as you want.
* As long as each environment has its own wrapped copy + script, you’re safe.

---
