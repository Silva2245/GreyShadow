# GreyShadow 🛡️

## Introduction
**GreyShadow** is a secure, peer-to-peer encrypted chat application designed for private communication and file sharing. Built with security at its core, it utilizes a **hybrid encryption model** (combining RSA and AES-GCM) to ensure that your messages and files remain confidential and untampered with during transmission.

The program operates using a unique "multi-tunnel" architecture. Instead of sending everything over one connection, it establishes four separate TCP tunnels:
*   **Tunnel 1 & 2:** Dedicated to outgoing and incoming text messages.
*   **Tunnel 3 & 4:** Dedicated to the secure transmission of files.

By separating these functions into different "tunnels," the application ensures a stable and organized flow of data between two users, regardless of whether you are sending a quick message or a large file.

---

## Features
- **🔐 High-Level Encryption:** Uses AES-GCM for data integrity and RSA for secure key exchange.
- **📂 Secure File Sharing:** Send files across the network with automated decryption on the receiving end.
- **💬 Real-time Messaging:** Dedicated threads handle incoming and outgoing text simultaneously.
- **🎨 Visual Interface:** Features color-coded console outputs for a better user experience.

---

## 🛠 Installation & Setup

### Prerequisites
Before running GreyShadow, ensure you have **Python 3.x** installed on your system.

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/GreyShadow-Arena.git
cd GreyShadow
```

### Step 2: Install Dependencies
The program requires several libraries to handle encryption, networking, and terminal styling. You can install them using `pip`:

```bash
pip install pycryptodome colorama psutil
```
*(Note: If you are using a specific environment, it is recommended to create a virtual environment first.)*

---

## 🚀 How to Run

To use GreyShadow, both participants must run the script. One person acts as the **Server** (the host) and the other as the **Client**.

### 1. Start the Server
The server hosts the connection. You must specify your name, the peer's name, and the ports to be used.

```bash
python GreyShadow.py -r server -yn "YourName" -on "PeerName" -ports 111,112,113,114
```

### 2. Start the Client
The client connects to the server's IP address. Replace `&lt;SERVER_IP&gt;` with the actual IP address of the person running the server.

```bash
python GreyShadow.py -r client -yn "YourName" -on "PeerName" -ip &lt;SERVER_IP&gt; -ports 111,112,113,114
```

### Command Arguments Reference:
| Flag | Description | Example |
|------|-------------|---------|
| `-r` | **Role**: Set as `server` or `client`. | `-r server` |
| `-yn` | **Your Name**: Your display name in the chat. | `-yn "Alice"` |
| `-on` | **Other Name**: The name of the person you are talking to. | `-on "Bob"` |
| `-ip` | **IP Address**: (Client only) The IP of the server. | `-ip 192.168.1.50` |
| `-ports` | **Ports**: Four ports for the four tunnels. | `-ports 111,112,113,114` |

---

## ⚠️ Important Notes for Users
*   **Network Connectivity:** Ensure that your firewall allows traffic on the ports specified (default: 111, 112, 113, 114).
*   **Key Security:** The current version uses a standard RSA handshake. For maximum security in a production environment, ensure you are running this over a trusted local network or a VPN.
*   **File Paths:** When sending files, the program will automatically create a `Files/` directory to store incoming data.

---

## 🛠 Development & Technical Details (For Contributors)
The system is built on three main layers:
1.  **Encryptor Layer:** Handles RSA key exchange and AES-GCM encryption for both text and files.
2.  **Connector Layer:** Manages the raw TCP socket connections across four distinct threads.
3.  **ChatPool Layer:** Orchestrates the logic of sending/receiving messages and handling file streams.

---

*Disclaimer: This project is intended for educational purposes to demonstrate cryptographic principles and multi-threaded networking.*
