# 🧾 Goal Architecture

```text
macOS (host)
 ├── Ollama (0.0.0.0:11434)
 └── SSH / browser → Arch VM

Arch Linux (UTM guest)
 ├── OpenClaw
 ├── (optional) web UI
 └── Firewall:
      ❌ block all outbound
      ✅ allow ONLY → host:11434
```

---

# ⚙️ 1. Prepare Arch VM (base setup)

Update system:

```bash
sudo pacman -Syu
```

Install essentials:

```bash
sudo pacman -S git python python-pip nodejs npm openssh ufw
```

Enable SSH (so host → guest works):

```bash
sudo systemctl enable sshd
sudo systemctl start sshd
```

Find VM IP:

```bash
ip a
```

👉 From macOS:

```bash
ssh user@<vm-ip>
```

---

# 🌐 2. Make Ollama accessible from host

On macOS:

```bash
export OLLAMA_HOST=0.0.0.0
ollama serve
```

Find host IP:

```bash
ipconfig getifaddr en0
```

Example:

```text
192.168.1.10
```

---

# 🔌 3. Test VM → host connectivity

Inside Arch VM:

```bash
curl http://192.168.1.10:11434/api/tags
```

✅ If this works → networking is correct

---

# 🤖 4. Install OpenClaw (generic setup)

> (Exact repo may vary depending on which OpenClaw fork you're using)

```bash
git clone https://github.com/<openclaw-repo>.git
cd openclaw
```

Create Python env:

```bash
python -m venv venv
source venv/bin/activate
```

Install deps:

```bash
pip install -r requirements.txt
```

---

# 🔗 5. Configure OpenClaw → Ollama

Set environment variables:

```bash
export OPENAI_BASE_URL=http://192.168.1.10:11434/v1
export OPENAI_API_KEY=ollama
export MODEL=gemma4
```

👉 This makes OpenClaw talk to:
**Ollama** on host

---

# 🖥️ 6. (Optional) Enable Web UI

If OpenClaw has a UI:

```bash
npm install
npm run dev
```

Then from macOS browser:

```text
http://<vm-ip>:3000
```

---

# 🔒 7. LOCK DOWN NETWORK (critical step)

Now we enforce:

> Guest → ONLY Ollama API
> Everything else blocked

---

## Enable firewall

```bash
sudo ufw default deny outgoing
sudo ufw default deny incoming
```

---

## Allow outbound → Ollama ONLY

```bash
sudo ufw allow out to 192.168.1.10 port 11434 proto tcp
```

---

## Allow inbound SSH (host → VM)

```bash
sudo ufw allow in 22/tcp
```

---

## (Optional) Allow Web UI

```bash
sudo ufw allow in 3000/tcp
```

---

## Enable firewall

```bash
sudo ufw enable
```

---

# 🧪 8. Verify isolation

### Should work:

```bash
curl http://192.168.1.10:11434/api/tags
```

### Should FAIL:

```bash
curl https://google.com
```

---

# 🔐 9. Extra hardening (recommended)

Run OpenClaw as non-root:

```bash
useradd -m claw
passwd claw
su - claw
```

Limit filesystem scope:

* only give it project directory
* avoid mounting host root

---

# 🧠 Notes on model choice

You’re using:

* **Gemma**

👉 It works, but for agents:

* weaker tool use
* worse planning

If things feel flaky, switch later.

---

# 🧾 Final Result

You now have:

* ✅ Host runs model (fast)
* ✅ VM runs agent (isolated)
* ✅ Host → VM access (SSH / UI)
* ✅ VM → ONLY Ollama API
* ❌ No internet from agent

---

# 💡 If you want next upgrades

I can help you:

* add a **proxy layer (stabilizes tool calling a LOT)**
* swap in a **better coding model for Ollama**
* or make a **one-command resettable VM snapshot workflow**

Just say 👍
