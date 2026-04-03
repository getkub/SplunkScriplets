# Goal

* Host (macOS)

  * Runs Ollama on LAN IP `192.168.4.42:11434`
  * Can SSH into VM `claw1`
  * Can access optional OpenClaw UI

* Guest (Arch Linux in UTM, IP `192.168.56.12`, hostname `claw1`)

  * Runs OpenClaw
  * Outbound network: ONLY allowed → host Ollama API
  * Inbound: SSH from host, optional OpenClaw UI port

---

# 1. UTM Network Setup

1. Open UTM → select VM → Edit → Network
2. Change network mode to **Host-Only**

   > This isolates VM from LAN and internet. Only host can reach VM.
3. Use subnet `192.168.56.0/24`
4. Guest VM will use static IP `192.168.56.12`

---

# 2. Configure Static IP in Arch Guest

Create or edit network file:

```
sudo nano /etc/systemd/network/20-wired.network
```

```
[Match]
Name=enp0s1

[Network]
Address=192.168.56.12/24
Gateway=192.168.56.1
DNS=192.168.56.1
```

Enable systemd-networkd:

```
sudo systemctl enable systemd-networkd
sudo systemctl restart systemd-networkd
```

Verify IP:

```
ip a
```

---

# 3. Update /etc/hosts

## Host macOS /etc/hosts:

```
192.168.56.12  claw1
192.168.56.10  ubuntu1
192.168.56.11  ubuntu2
192.168.4.42   myapp.local
```

## Guest Arch /etc/hosts:

```
192.168.4.42  ollama.local
```

---

# 4. Enable SSH (host → guest)

Install SSH server:

```
sudo pacman -S openssh
sudo systemctl enable sshd
sudo systemctl start sshd
```

Test from host macOS:

```
ssh user@claw1
```

---

# 5. Configure Ollama on macOS host

Run Ollama bound to all interfaces:

```
export OLLAMA_HOST=0.0.0.0
ollama serve
```

Test from guest VM:

```
curl http://ollama.local:11434/api/tags
```

---

# 6. Install OpenClaw in Guest VM

Install dependencies:

```
sudo pacman -S git python python-pip nodejs npm
```

Clone repository:

```
git clone https://github.com/<openclaw-repo>.git
cd openclaw
```

Create Python virtual environment:

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

# 7. Configure OpenClaw → Ollama

Set environment variables:

```
export OPENAI_BASE_URL=http://ollama.local:11434/v1
export OPENAI_API_KEY=ollama
export MODEL=gemma4
```

---

# 8. Optional Web UI

Install and run:

```
npm install
npm run dev
```

Access from host macOS:

```
http://claw1:3000
```

---

# 9. Firewall (strict isolation)

Install UFW:

```
sudo pacman -S ufw
```

Default deny all:

```
sudo ufw default deny outgoing
sudo ufw default deny incoming
```

Allow only necessary connections:

```
# Outbound → Ollama API only
sudo ufw allow out to 192.168.4.42 port 11434 proto tcp

# Inbound → SSH from host-only subnet
sudo ufw allow in from 192.168.56.0/24 to any port 22

# Inbound → OpenClaw UI (optional)
sudo ufw allow in 3000/tcp
```

Enable firewall:

```
sudo ufw enable
```

---

# 10. Verification

VM → Ollama API:

```
curl http://ollama.local:11434/api/tags
```

VM → Internet (should fail):

```
curl https://google.com
```

Host → VM SSH:

```
ssh user@claw1
```

Host → OpenClaw UI (optional):

```
http://claw1:3000
```

---

# 11. Optional Hardening

Create restricted user for OpenClaw:

```
sudo useradd -m claw
sudo passwd claw
su - claw
```

Limit OpenClaw to project directory:

```
mkdir ~/workspace
cd ~/workspace
```

Run OpenClaw inside this directory only.
