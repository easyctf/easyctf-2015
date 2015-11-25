import binascii

def compute(uinput):
	if len(uinput) > 32: return ""
	blen = 32
	n = blen - len(uinput) % blen
	if n == 0:
		n = blen
	pad = chr(n)
	ninput = uinput + pad * n
	r = ""
	for i in range(0, blen, 4):
		s = ninput[i:i+4]
		h = 0
		for j in range(len(s)):
			h = (h << 4) + ord(s[j])
			g = h & 4026531840
			if not(g == 0):
				h ^= g >> 24
			h &= ~g
		r += chr(h % 256)
	h = binascii.hexlify(bytes(r, 'Latin-1'))
	return h

def grade(tid, answer):
	if compute(answer) == compute("they_see_me_hashin_they_hatin"):
		return { "correct": True, "message": "They see me hashin' they hatin'" }
	return { "correct": False, "message": "Nope." }