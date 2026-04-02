# Goal

- Host (macOS)
  - Runs Ollama on fixed IP + port
  - Can SSH into VM
  - Can access optional OpenClaw UI

- Guest (Arch Linux in UTM)
  - Runs OpenClaw
  - Outbound network:
    - ONLY allowed → host Ollama API
  - Inbound:
    - SSH from host
    - Optional UI port

---

# 1. UTM Network (Host ↔ Guest only, fixed IP)

## Create isolated network (no router / no internet)

In UTM:

1. Open VM → Edit
2. Network:
   - Mode: **Shared Network**
   - Enable: **Isolate from host network** (important)

This creates a private subnet like:
- Host: `192.168.64.1`
- Guest: `192.168.64.x`

---

## Set static IP inside Arch

Edit network config:

```bash
sudo nano /etc/systemd/network/20-wired.network
````

```ini
[Match]
Name=enp0s1

[Network]
Address=192.168.64.2/24
Gateway=192.168.64.1
DNS=192.168.64.1
```

Enable systemd-networkd:

```bash
sudo systemctl enable systemd-networkd
sudo systemctl restart systemd-networkd
```

Verify:

```bash
ip a
```

---

# 2. Enable SSH (host → guest)

Install + enable:

```bash
sudo pacman -S openssh
sudo systemctl enable sshd
sudo systemctl start sshd
```

From macOS:

```bash
ssh user@192.168.64.2
```

---

# 3. Configure Ollama on macOS host

Run Ollama bound to all interfaces:

```bash
export OLLAMA_HOST=0.0.0.0
ollama serve
```

Host IP in this network:

```text
192.168.64.1
```

Test from VM:

```bash
curl http://192.168.64.1:11434/api/tags
```

---

# 4. Install OpenClaw

```bash
sudo pacman -S git python python-pip nodejs npm
```

```bash
git clone https://github.com/<openclaw-repo>.git
cd openclaw
```

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

# 5. Configure OpenClaw → Ollama

```bash
export OPENAI_BASE_URL=http://192.168.64.1:11434/v1
export OPENAI_API_KEY=ollama
export MODEL=gemma4
```

---

# 6. Optional Web UI

```bash
npm install
npm run dev
```

Access from macOS:

```text
http://192.168.64.2:3000
```

---

# 7. Firewall (strict isolation)

Install UFW:

```bash
sudo pacman -S ufw
```

Default deny:

```bash
sudo ufw default deny outgoing
sudo ufw default deny incoming
```

Allow outbound → Ollama only:

```bash
sudo ufw allow out to 192.168.64.1 port 11434 proto tcp
```

Allow inbound SSH:

```bash
sudo ufw allow in 22/tcp
```

Allow UI (optional):

```bash
sudo ufw allow in 3000/tcp
```

Enable firewall:

```bash
sudo ufw enable
```

---

# 8. Verification

Should work:

```bash
curl http://192.168.64.1:11434/api/tags
```

Should fail:

```bash
curl https://google.com
```

---

# 9. Optional Hardening

Create restricted user:

```bash
sudo useradd -m claw
sudo passwd claw
su - claw
```

Limit working directory:

```bash
mkdir ~/workspace
cd ~/workspace
```

Run OpenClaw only inside this directory.

