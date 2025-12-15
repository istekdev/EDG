def edg64(input):
  tag = int.from_bytes("EDG64".encode("utf-8"), "big")
  if len(input) == 0:
    payload = b"\x00" * 16
  elif len(input) < 16:
    payload = (input * ((16 // len(input)) + 1))[:16]
  else:
    payload = input[:16]
  integer = (2**32) // int.from_bytes(input, "big") % 2**32
  return integer.to_bytes(8, "big")
