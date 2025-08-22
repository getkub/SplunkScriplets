export CLOUD_PROVIDER=gcp
export GCP_KMS_KEY=ansible-master-key
export GCP_KMS_KEYRING=ansible-keyring
export GCP_KMS_LOCATION=global
export GCP_PROJECT=my-gcp-project
export GCP_ENC_FILE=/etc/ansible/keys/ansible-vault.gcp.enc

ansible-playbook site.yml --vault-password-file ./vault-pass.py
