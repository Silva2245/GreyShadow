# GreyShadow.py — Technical Analysis Report

## 1. High-Level Overview

`GreyShadow.py` is a **peer-to-peer (P2P) encrypted chat and file-transfer application**. It's built around four conceptual layers:

| Layer | Class(es) | Responsibility |
|-------|-----------|----------------|
| Cryptography | `Encryptor`, `ServerEncryptor`, `ClientEncryptor` | RSA + AES-GCM encryption, key handling |
| Networking | `Connector`, `ServerConnector`, `ClientConnector` | TCP sockets and the handshake |
| Application | `ChatPool`, `ServerChatPool`, `ClientChatPool` | Chat loops ("tunnels") and file transfer |
| Orchestration | `PlayGround` + CLI parsing | Entry point, role selection, argument handling |

The stated goal — "no middle-point connection server so no one can know anything about the data" — is a **direct P2P design**: two peers connect to each other directly over TCP. There is no third-party relay server relaying your messages; traffic flows straight between the sender and receiver's machines. That part of the architecture matches your intent.

---

## 2. Class-by-Class Breakdown

### `Encryptor` (base class)

This holds all cryptographic logic.

**`__init__`** — Constructs a hardcoded RSA keypair:
- `self.puk` = RSA public key
- `self.pvk` = RSA private key

**`AESEncryptLayer(data)`** — Encrypts data using AES-GCM:
```python
aes = AES.new(self.MajorKey, AES.MODE_GCM, self.MinorKey)
cd, tag = aes.encrypt_and_digest(data)
return (cd, tag)
```
Returns a tuple of `(ciphertext, authentication_tag)`. GCM provides both confidentiality and integrity/authentication.

**`AESDecryptLayer(data, tag)`** — Reverses the above with `decrypt_and_verify()`, which also validates the tag (detects tampering).

**`EncryptFile(FileName, FileData)`** — Implements **hybrid encryption**, the correct approach for large data:
1. Encrypts the filename with RSA (`rsa.encrypt`)
2. Encrypts the file body with AES-GCM
3. Returns `[filename_cipher, filedata_cipher, tag]`

RSA can't encrypt large blobs efficiently, so it's used only to wrap a symmetric key — here applied directly to the filename (small). The bulk data uses fast AES. This is sound design.

**`DecryptFile(FileCipherList)`** — Reverses `EncryptFile`:
1. RSA-decrypts the filename with the private key
2. AES-GCM decrypts/verifies the body
3. Returns `(filename, filedata)`

---

### `ServerEncryptor(Encryptor)`

Adds server-side handshake logic.

**`ValidateMinorKey(key)`** — Checks that a "minor key" is exactly 12 characters long. (See Section 5 on why this matters.)

**`CraftMajorKey(key)`** — Derives the major key by hashing input with **MD5**:
```python
h = md5(key)
return h.hexdigest().encode('utf-8')
```

**`InitHandshakeKeys()`** — The interactive setup:
1. Prompts user for Major Key and Minor Key
2. Validates the minor key length
3. Encrypts both keys with RSA (`rsa.encrypt(..., self.puk)`) → `MinorCipher`, `MajorCipher`
4. Creates an AES-GCM cipher object (though this instance is largely unused — see Section 5)

**Why two "keys"?** The design splits the setup into a *major key* (the actual AES encryption key, derived from MD5 of user input) and a *minor key* (used as the GCM nonce). This separation is reasonable in concept.

---

### `ClientEncryptor(Encryptor)`

**`DeployHandshakeKeys()`** — The client counterpart:
1. RSA-decrypts the received ciphers with its private key (`rsa.decrypt(..., self.pvk)`)
2. Reconstructs `MinorKey`, `MajorKey`
3. Builds an AES-GCM cipher from them

This is a basic **asymmetric key exchange**: server sends encrypted keys, client decrypts them locally. No secrets are transmitted in the clear. Good conceptually — again, undermined by the hardcoded private key (Section 6).

---

### `Connector` and socket classes

**`Connector`** — Base class holding `self.c` (the list of sockets).

**`ServerConnector(Connector)`**:
- Creates a `ServerEncryptor`
- Calls `ServerConnect()` then `Handshake()`

**`ServerConnect()`** — Binds **four TCP sockets** on the server's own IP:
```python
s1.bind((myip, 111))   # Tunnel 1
s2.bind((myip, 112))   # Tunnel 2
s3.bind((myip, 113))   # Tunnel 3
s4.bind((myip, 114))   # Tunnel 4
```
It gets the local IP via `net_if_addrs()['Wi-Fi'][1].address` and listens for connections.

**`Handshake()` (server)** — Sends its encrypted keys to the client:
```python
self.c[0].send(self.en.MinorCipher)   # up to 6000 bytes
self.c[0].send(self.en.MajorCipher)   # up to 6000 bytes
recv = self.c[0].recv(6000)           # client's encrypted message
tag = self.c[0].recv(6000)            # client's auth tag
hndshake = self.en.AESDecryptLayer(recv, tag)
```

**`ClientConnector(Connector)`**:
- Prompts for target IP and port
- Calls `ClientConnect()` then `Handshake()`

**`ClientConnect()`** — Connects to **four ports on the server's IP**:
```python
c1.connect((self.ip, self.p))   # user-specified port (should be 111)
c2.connect((self.ip, 112))      # hardcoded
c3.connect((self.ip, 113))      # hardcoded
c4.connect((self.ip, 114))      # hardcoded
```

**`Handshake()` (client)** — Receives server's keys, decrypts them via `DeployHandshakeKeys()`, then encrypts a test message ("Welcome To GreyShadow Arena") and sends it back. This confirms both sides derived matching AES keys.

---

### `ChatPool` (base) + `ServerChatPool` / `ClientChatPool`

These implement the actual chat/file-transfer functionality using four "tunnels" (sockets).

**`GetFileData(FilePath)`** — Reads a file in binary mode and returns its bytes.
**`SaveFileData(FileName, FileData)`** — Writes to a `Files/` subdirectory (`os.chdir('Files')`).
**`SendTxtMsg(message, Connection)`** — Encrypts the message with AES-GCM, then encrypts the auth tag with RSA:
```python
cipherdata = self.cipher.AESEncryptLayer(...)   # (ciphertext, tag)
tag = rsa.encrypt(cipherdata[1], self.cipher.puk)  # wrap tag in RSA
Connection.send(cipherdata[0])                     # send ciphertext
Connection.send(tag)                               # send wrapped tag
```
**`RecvTxtMsg(Connection)`** — Reverses it: receives ciphertext and raw tag, decrypts the tag with the private key, then AES-decrypts.

&gt; Note on text messages: unlike files, here the **tag is RSA-wrapped** rather than sent in cleartext (as in `Handshake`). This is actually a *better* choice for short messages since it avoids sending the GCM tag openly. Good instinct there.

**`SendFile(FilePath, Connection)`** — Encrypts and streams the file across all cipher parts.
**`RecvFile(Connection)`** — Receives filename cipher, file data, and tag, then decrypts and saves.


**The four tunnels:**

- **Tunnel 1 / Tunnel 2** — Chat loop: one sends text (`input()`), the other receives and displays it.
- **Tunnel 3 / Tunnel 4** — File send/receive.

---

### `PlayGround` + CLI

**`home(role)`** — Routes based on role argument:
- `1/server/s/Server` → server mode
- `2/client/c/Client` → client mode

The bottom of the file sets up an `ArgumentParser` requiring `-r`, `-yn` (your name), `-on` (other's name), and optionally `-f` (file to send). This is standard CLI scaffolding.

---

## 3. How It Works End-to-End

1. **Server** starts, binds four TCP ports on its IP, waits for a client.
2. **Client** connects to the server's IP:port.
3. **Handshake:** Server sends RSA-encrypted keys → Client decrypts them with its private key and derives matching AES-GCM keys → Both confirm by exchanging an encrypted test message.
4. **Chat:** Text messages are AES-GCM encrypted (tag RSA-wrapped), sent over one tunnel, decrypted on the other end.
5. **Files:** Files use hybrid encryption — filename via RSA, body via AES-GCM — streamed across tunnels and saved to a `Files/` folder.

The intended flow is sound: it's a legitimate P2P encrypted messaging tool using proper hybrid crypto primitives (RSA for key exchange + AES-GCM for bulk data).

---

---

## 5. Summary Verdict

| Aspect | Status |
|--------|--------|
| Architecture (P2P, no relay) | ✅ Matches your goal |
| Hybrid RSA + AES-GCM approach | ✅ Correct primitives |
| Handshake key exchange concept | ✅ Sound idea |
