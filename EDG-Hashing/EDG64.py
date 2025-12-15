def edg64(input):
  tag = int.from_bytes("EDG64".encode("utf-8"), "big")
  if len(input) == 0:
    payload = b"\x00" * 8
  elif len(input) < 8:
    payload = (input * ((16 // len(input)) + 1))[:8]
  else:
    payload = input[:8]
  integer = tag * int.from_bytes(input, "big")
  return integer.to_bytes(8, "big")
