# GreyShadow — Project Documentation

&gt; **GreyShadow** is an educational/CTF-style client-server encrypted chat application that demonstrates hybrid encryption (RSA + AES-GCM), multi-threaded socket communication, encrypted messaging, file transfer, and conversation logging.

---

## ⚠️ Important Disclaimer

This project is intended for **educational purposes only**. It contains intentional security weaknesses (hardcoded keys, MD5-based key derivation, fixed nonces) that are documented throughout the codebase to help learners understand what *not* to do in production systems. **Do not use this software for real-world secure communication.**

---

## 📋 Table of Contents

1. [Features](#-features)
2. [Architecture Overview](#-architecture-overview)
3. [Installation](#-installation)
   - [Prerequisites: Python](#prerequisites-python)
   - [Python Libraries (Dependencies)](#python-libraries-dependencies)
4. [Running the Program](#-running-the-program)
5. [Command-Line Arguments](#-command-line-arguments)
6. [How It Works](#-how-it-works)
7. [Project Structure](#-project-structure)
8. [Security Considerations](#-security-considerations)
9. [License / Credits](#-license--credits)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔐 **Hybrid Encryption** | RSA encrypts AES keys; AES-GCM provides authenticated encryption for data. |
| 🌐 **Multi-Tunnel Networking** | 4 parallel TCP "tunnels" (ports) handle simultaneous text chat and file transfers via threading. |
| 💬 **Encrypted Messaging** | Text messages are encrypted end-to-end using the hybrid scheme. |
| 📁 **Encrypted File Transfer** | Files are hybrid-encrypted before transmission and decrypted on receipt. |
| 📝 **Conversation Logging** | Messages can be persisted to XML files when enabled. |
| 🎨 **Colored CLI Interface** | Colorama provides readable, color-coded terminal output. |

---

## 🏗️ Architecture Overview

The application is split into two roles that must run simultaneously:

- **Server (role `1`)** — Listens for connections and accepts them.
- **Client (role `2`)** — Connects to the server's IP address.

### Class Hierarchy

```
Encryptor (Base)
├── ServerEncryptor(Encryptor)
│   └── ServerConnector(ServerEncryptor)
│       ├── ServerChatPool(ServerConnector)
│       │   └── ServerChatPool(ChatPool)  [orchestrates 4 threads]
│       └── PlayGround → home('1')
├── ClientEncryptor(Encryptor)
│   └── ClientConnector(ClientEncryptor)
│       ├── ClientChatPool(ClientConnector)
│       │   └── ClientChatPool(ChatPool)  [orchestrates 4 threads]
│       └── PlayGround → home('2')
├── Connector (Base)
└── ChatPool (Base)
```

### Key Components

| Component | Responsibility |
|-----------|----------------|
| `Encryptor` | Core cryptographic operations: AES-GCM encrypt/decrypt, hybrid file encryption. Hardcodes the shared RSA keypair. |
| `ServerEncryptor` | Server-side handshake logic; derives and RSA-encrypts handshake keys. |
| `ClientEncryptor` | Client-side handshake logic; RSA-decrypts received handshake keys. |
| `Connector` | Generic socket attributes (`self.c`, `self.OtherIP`). |
| `ServerConnector` | TCP server setup, port binding/listening/accepting, and encrypted handshake. |
| `ClientConnector` | TCP client connection to each configured port, then handshake. |
| `ChatPool` | Shared chat/file-transfer logic: message send/receive, file send/receive, conversation logging. |
| `ServerChatPool` / `ClientChatPool` | Role-specific orchestration of 4 background threads (tunnels). |
| `PlayGround` | Main orchestrator; dispatches to server or client flow based on role. |

---

## 📦 Installation

### Prerequisites: Python

Python must be installed before you can run this project. Follow the instructions for your operating system below.

#### Windows

1. Visit the official website: &lt;https://www.python.org/downloads/windows/&gt;
2. Click **Download Python** (choose the latest stable version).
3. Run the installer (`python-XX.X.x-amd64.exe`).
   - ⚠️ **Important:** Check the box that says **"Add Python to PATH"** during installation, or Python won't be accessible from your command line.
4. Open **Command Prompt** (press `Win + R`, type `cmd`, press Enter) and verify:
   ```bash
   python --version
   ```

#### Linux / macOS

Use your package manager to install Python:

```bash
# Ubuntu / Debian
sudo apt update
sudo apt install python3 python3-pip

# Fedora
sudo dnf install python3 python3-pip

# Arch Linux
sudo pacman -S python python-pip
```

Then verify the installation:

```bash
python3 --version
pip3 --version
```

&gt; **Note:** This project uses `python` in examples. If your system only provides `python3`, you can either use `python3` directly or create a symlink (`sudo ln -s /usr/bin/python3 /usr/local/bin/python`).

---

### Python Libraries (Dependencies)

After installing Python, install the required third-party libraries using **pip**.

#### Windows

Open Command Prompt and run:

```bash
pip install pycryptodome psutil colorama beautifulsoup4 rsa argparse
```

&gt; Note: `argparse` is part of the standard library and does not need to be installed. The above installs all external dependencies.

#### Linux / macOS

Open your terminal and run:

```bash
# Using pip3 (recommended)
pip3 install pycryptodome psutil colorama beautifulsoup4 rsa

# OR using python -m pip
python3 -m pip install pycryptodome psutil colorama beautifulsoup4 rsa
```

#### Verifying Installation

You can verify that all dependencies are installed correctly:

```bash
pip list | grep -E "pycryptodome|psutil|colorama|beautifulsoup|rsa"
```

---

## ▶️ Running the Program

### Step 1 — Start the Server

Open a terminal/command prompt and run:

```bash
python GreyShadow.py -r 1 -yn Server -on Client -ports 111,112,113,114
```

| Argument | Description |
|----------|-------------|
| `-r` | Role — use `1` for server. |
| `-yn` | Your name (server's display name). |
| `-on` | Other player's name (client's display name). |
| `-ports` | Comma-separated list of ports to bind: `111,112,113,114`. |

### Step 2 — Start the Client

Open a **second** terminal/command prompt and run:

```bash
python GreyShadow.py -r 2 -yn Client -on Server -ip &lt;SERVER_IP&gt; -ports 111,112,113,114
```

| Argument | Description |
|----------|-------------|
| `-r` | Role — use `2` for client. |
| `-yn` | Your name (client's display name). |
| `-on` | Other player's name (server's display name). |
| `-ip` | The server's IP address (replace `&lt;SERVER_IP&gt;` with the actual value). |
| `-ports` | Comma-separated list of ports to connect to. Must match the server's ports. |

&gt; **Tip:** To find your machine's local IP, run `python GreyShadow.py -v` or check via `ipconfig` (Windows) / `hostname -I` (Linux). If both machines are on the same network, you can also use `localhost`.

### Step 3 — Communicate

Once both terminals are running:

- **Text messages:** Type your message at the prompt and press Enter. The recipient will receive it encrypted.
- **File transfer:** Use `-f` to send a file (handled on Tunnel 3/4).
- **Exit:** Type `bye`, `disc`, or `exit` in any tunnel to stop that thread.

### Optional Flags

| Flag | Description |
|------|-------------|
| `-f &lt;file&gt;` | File to send (client side, encrypted file transfer). |
| `-mjk &lt;key&gt;` | Major key for handshake. |
| `-mnk &lt;key&gt;` | Minor key for handshake. |
| `-ip &lt;address&gt;` | Server IP address (client only). |
| `-ports &lt;list&gt;` | Comma-separated ports: `111,112,113,114`. |
| `-sc` | Save conversation to an XML file in the `Conversations/` folder. |
| `-v` | Verbose mode — prints additional diagnostic output (e.g., local IP). |

---

## 🔧 How It Works

### The Encryption Handshake

1. Both client and server share a **hardcoded RSA keypair** embedded in the source code.
2. During startup, each side derives an AES-GCM **minor key** (nonce) and **major key**.
3. These keys are RSA-encrypted into ciphers (`MinorCipher`, `MajorCipher`) and exchanged over the network.
4. Each side decrypts the received ciphers to recover the shared symmetric keys.
5. From then on, all data is encrypted with AES-GCM using those keys.

### The Four Tunnels (Ports)

| Tunnel | Port | Server Role | Client Role |
|--------|------|-------------|-------------|
| 1 | `port[0]` | Interactive input → sends text messages | Receives incoming text messages |
| 2 | `port[1]` | Receives incoming text messages | Interactive input → sends text messages |
| 3 | `port[2]` | Sends a file (`filee`) | Receives a file |
| 4 | `port[3]` | Receives a file | Sends a file |

Each tunnel runs as an independent background thread, allowing simultaneous bidirectional communication.

---

## 📁 Project Structure

```
GreyShadow/
├── GreyShadow.py          # Main application entry point
├── README.md              # This documentation
└── Conversations/         # Created at runtime when -sc is used (XML logs)
    └── &lt;Conversation&gt;.xml
```

---

## ⚠️ Security Considerations

This project is educational and intentionally contains security weaknesses. Learners should understand these flaws:

| Issue | Description |
|-------|-------------|
| 🔑 **Hardcoded RSA keys** | Keys are embedded in source; anyone with the file can decrypt all traffic. |
| 🧨 **MD5 for key derivation** | MD5 is cryptographically broken and unsuitable for key generation. |
| 🔁 **Fixed AES nonce** | A constant `MinorKey` reused across messages breaks GCM authentication and enables forgery. |
| 📂 **Fragile file handling** | `os.chdir()` to relative paths can corrupt the working directory; conversation logging overwrites content it just created. |
| 🔊 **No persistent listener loop** | The server binds/accepts once per port rather than continuously listening. |
| 🧱 **Fixed recv buffers** | 6000-byte buffers may truncate larger messages/files. |

&gt; These are documented deliberately so learners can study real-world vulnerabilities and understand secure alternatives.

---

## 📄 License / Credits

This is an educational/CTF-style demonstration project created for learning purposes. It is provided as-is without any warranty. Use responsibly and only in controlled, educational environments.

---
