export CLOUD_PROVIDER=azure
export AZURE_KEY_NAME=ansible-master-key
export AZURE_VAULT_NAME=ansible-vault-kv
export AZURE_ENC_FILE=/etc/ansible/keys/ansible-vault.azure.enc

ansible-playbook site.yml --vault-password-file ./vault-pass.py
