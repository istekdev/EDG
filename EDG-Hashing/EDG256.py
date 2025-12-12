def rotr(x, n):
    return ((x >> n) | (x << (64 - n))) & 0xFFFFFFFFFFFFFFFF

def shuffle(anything):
  order = [5, 2, 7, 1, 6, 0, 4, 3]
  chunks = [anything[i:i+4] for i in range(0, 32, 4)]
  return b"".join(chunks[o] for o in order)

def edg256(input):
  edg = int.from_bytes("EDG".encode("utf-8"), "big")
  prime = 0x9E3779B185EBCA77
  if len(input) == 0:
    payload = b"\x00" * 64
  elif len(input) < 64:
    payload = (input * ((64 // len(input)) + 1))[:64]
  else:
    payload = input[:64]
  conglomerate = 0
  for p in range(0, 64, 8):
    chunks = payload[p:p+8]
    iChunk = int.from_bytes(chunks, "big")
    conglomerate ^= (iChunk ^ edg ^ ((p+1) * prime))
    conglomerate &= (1 << 256) - 1
  for r in range(8):
    cB = conglomerate.to_bytes(32, "big")
    shuffled = shuffle(cB)
    shuffleList = [int.from_bytes(shuffled[c:c+4], "big") for c in range(0, 32, 4)]
    mixed = []
    for s in shuffleList:
      rot = (rotr(shuffleList[(s+0)%8], 2) ^ rotr(shuffleList[(s+1)%8], 13) ^ rotr(shuffleList[(s+2)%8], 22)) ^ (rotr(shuffleList[(s+3)%8], 6) ^ rotr(shuffleList[(s+4)%8], 11) ^ rotr(shuffleList[(s+5)%8], 25))
      mixed.append(rot)
    output = 0
    for a, b in enumerate(mixed):
      output |= b << (32*(7-a))
      output &= (1 << 256) - 1
  return output.to_bytes(32, "big")
