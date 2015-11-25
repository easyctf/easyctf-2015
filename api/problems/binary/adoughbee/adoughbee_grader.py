import ctypes

def grade(tid, answer):
	answer = answer.strip("easyctf{").strip("}")
	answer = answer.upper()
	if len(answer) != 25:
		return { "correct": False, "message": "Did you not read the question? The serial is 25 characters long." }
	email = "evil@anomat.cf"
	x = 0x1337
	for i in range(len(email)):
		x ^= ord(email[i])
	y = 0xdeadfa11
	for i in range(0, 25, 5):
		y ^= int(answer[i:i+5], 36) * x
		y = ctypes.c_uint(y).value
	result = x ^ y
	result = ctypes.c_uint(result).value
	if result == 0xfad499e1:
		return { "correct": True, "message": "Nice." }
	# if answer.find("19UFLAD2DRU4AXGUEV9R8GD2I") != -1:
		# return { "correct": True, "message": "Nice." }
	return { "correct": False, "message": "Nope, try again!" }