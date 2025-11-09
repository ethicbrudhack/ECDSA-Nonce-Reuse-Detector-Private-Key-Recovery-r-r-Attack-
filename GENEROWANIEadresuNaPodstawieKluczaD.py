from ecdsa.numbertheory import inverse_mod
from ecdsa.ecdsa import generator_secp256k1

# Stała dla secp256k1
n = generator_secp256k1.order()

# Dane dla transakcji 1
r1 = int("27c90531406bbf08bd6325b06fe0ac32e61a66f3d8b2762a7bf2ac6c13e76ddc", 16)
s1 = int("096ddba45472fe9cca48753e7ca89b70ef358badbd458e08ef77fc79a85d7ae8", 16)
z1 = int("af35ac2dfa66a276070a9876c1108a53744b8c1f0d2a339443e93c4f892dd82", 16)

# Dane dla transakcji 4
r2 = int("f676052e29ab14b5ea8a4515696edb2732ae765b4aee763e16a208e9f7753178", 16)
s2 = int("1ee030b36dba2a21fe236512668af824dcbb382a7a8aa962b3792ca6dc6a5efe", 16)
z2 = int("7d5a9d992a12716f248751b31a34d8c12ffcad27563a6f09da8fabb078299fd9", 16)

# Sprawdzamy, czy r1 == r2 (czy użyto tego samego k)
if r1 == r2:
    # Obliczamy k
    delta_s = (s1 - s2) % n
    delta_z = (z1 - z2) % n

    if delta_s != 0:
        k = (delta_z * inverse_mod(delta_s, n)) % n

        # Obliczamy klucz prywatny d
        d = ((s1 * k - z1) * inverse_mod(r1, n)) % n
        print(f"✅ Znaleziono k: {hex(k)}")
        print(f"✅ Klucz prywatny d: {hex(d)}")
    else:
        print("❌ Nie znaleziono zależności (delta_s = 0).")
else:
    print("❌ Brak powtórzonego r – nie można odzyskać k.")
