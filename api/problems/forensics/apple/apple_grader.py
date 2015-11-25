def grade(tid, answer):
	if answer.find("w0w_much_appl3s") != -1:
		return { "correct": True, "message": "Great job!" }
	return { "correct": False, "message": "Wikipedia: Steganography" }