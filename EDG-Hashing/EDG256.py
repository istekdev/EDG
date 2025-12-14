def rotr(a, b):
    return ((a >> b) | (a << (32 - b))) & 0xFFFFFFFF

def choose(a, b, c):
    return (a & b) ^ (~a & c)

def major(a, b, c):
    return (a & b) ^ (a & c) ^ (b & c)

def theta(inp):
  lanes = [int.from_bytes(inp[l:l+4], "big") for l in range(0, 32, 4)]
  parity = 0
  for l in lanes:
      parity ^= l
  rot = rotr(parity, 1) ^ rotr(parity, 8)
  return [(l ^ rot) & 0xFFFFFFFF for l in lanes]

def pi(inp):
  pi = [(c * 3) % 8 for c in range(8)]
  lanes = [int.from_bytes(inp[l:l+4], "big") for l in range(0, 32, 4)]
  lanes = [lanes[p] for p in pi]
  return b"".join(l.to_bytes(4, "big") for l in lanes)

def rho(inp):
  rho = [2, 5, 11, 17, 23, 29, 31, 19]
  lanes = [int.from_bytes(inp[l:l+4], "big") for l in range(0, 32, 4)]
  lanes = [rotr(lanes[i], rho[i] % 32) for i in range(8)]
  return b"".join(l.to_bytes(4, "big") for l in lanes)

def chi(inp):
  return [(inp[l] ^ (~inp[(l+1)%8] & inp[(l+2)%8])) & 0xFFFFFFFF for l in range(8)]

def edg256(payload):
  prime = 0xBB67AE85
  edg = int.from_bytes("EDG256".encode("utf-8"), "big")
  conglomerate = 0

  if len(payload) == 0:
    blob = b"\x00" * 16
  elif len(payload) < 16:
    blob = (payload * ((16 // len(payload)) + 1))[:16]
  else:
    blob = payload[:16]

  for p in range(0, 16, 8):
    chunks = payload[p:p+8]
    integer = int.from_bytes(chunks, "big")
    a = (integer >> 48) & 0xFFFF
    b = (integer >> 32) & 0xFFFF
    c = (integer >> 16) & 0xFFFF
    d = integer & 0xFFFF
    integer = choose(a, b, c) ^ major(b, c, d)
    conglomerate ^= (integer ^ edg ^ ((p+1) * prime))
    conglomerate &= (1 << 256) - 1
  lanes = []
  output = 0
  for rounds in range(128):
    RHO = rho(conglomerate.to_bytes(32, "big"))
    PI = pi(RHO)
    lanes = theta(PI)
    
    sig0 = [rotr(l, 2) ^ rotr(l, 13) ^ rotr(l, 22) for l in lanes]
    sig1 = [rotr(l, 6) ^ rotr(l, 11) ^ rotr(l, 25) for l in lanes]
    lanes = [s0 ^ s1 for s0, s1 in zip(sig0, sig1)]
    lanes = chi(lanes)
  output = int.from_bytes(b''.join(l.to_bytes(4, 'big') for l in lanes), 'big')
  output &= (1 << 256) - 1
  return output.to_bytes(32, "big")
