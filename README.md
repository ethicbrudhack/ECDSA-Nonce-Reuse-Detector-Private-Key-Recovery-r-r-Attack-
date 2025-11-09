# ♻️ ECDSA Nonce Reuse Detector & Private Key Recovery (r₁ = r₂ Attack)

This script performs the **classic ECDSA key recovery attack** when two signatures share the **same nonce** (`k`) — revealed by identical `r` values.  
If two different messages (`z₁`, `z₂`) are signed using the same `k`, it becomes mathematically trivial to recover the private key `d`.

---

## ⚙️ Step-by-step overview

### 1️⃣ Load the ECDSA parameters

Two signatures are defined by `(r, s, z)` triplets:

```python
r1, s1, z1 = ...  # signature 1
r2, s2, z2 = ...  # signature 2
Both are derived from transactions signed with the same elliptic curve key.

2️⃣ Verify nonce reuse
if r1 == r2:
    ...
else:
    print("❌ Brak powtórzonego r – nie można odzyskać k.")


If both signatures share the same r, they used the same ephemeral key k.

🧮 3️⃣ Recover the nonce k

From ECDSA’s signing equation:

s ≡ k⁻¹ (z + r·d) (mod n)


Taking the difference of two equations where k is the same gives:

(s1 − s2) * k ≡ (z1 − z2)  (mod n)
⇒ k ≡ (z1 − z2) * (s1 − s2)⁻¹  (mod n)


The script implements exactly this:

delta_s = (s1 - s2) % n
delta_z = (z1 - z2) % n
k = (delta_z * inverse_mod(delta_s, n)) % n

🔑 4️⃣ Recover the private key d

Once k is known, ECDSA’s equation rearranges to:

d ≡ (s1 * k − z1) * r1⁻¹  (mod n)


This yields the true private key used to sign both messages.

📜 Output Example
✅ Znaleziono k: 0x17c2a5b3b8e9...
✅ Klucz prywatny d: 0x91af4c72c0bd...


If r₁ ≠ r₂, the script stops, as nonce reuse did not occur.

🔢 Visual flow
Input:
 (r₁, s₁, z₁)
 (r₂, s₂, z₂)

Check:
 if r₁ == r₂ → same k used!

Compute:
 Δs = (s₁ − s₂) mod n
 Δz = (z₁ − z₂) mod n
 k  = Δz * (Δs)⁻¹ mod n
 d  = (s₁ * k − z₁) * r₁⁻¹ mod n

🧠 Cryptographic context

Cause: Reusing the same nonce k for multiple signatures destroys ECDSA security.

Effect: The attacker can recover the private key with simple modular arithmetic.

Historical note: This vulnerability has caused multiple real-world Bitcoin and blockchain key leaks (2010–2013 era).

⚠️ Limitations

Works only when r₁ == r₂ (exact reuse of the same k).

Requires both message digests (z₁, z₂) and signature values (r₁, s₁, r₂, s₂).

If s₁ − s₂ ≡ 0 (mod n), the attack fails (non-invertible case).

⚖️ Ethical reminder

Use this code only for authorized audits, educational demos, or testing weak signing systems.
Never attempt to recover private keys from external or unauthorized data sources.

© 2025 — Author: [ethicbrudhack]

BTC donation address: bc1q4nyq7kr4nwq6zw35pg0zl0k9jmdmtmadlfvqhr
