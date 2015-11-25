def grade(tid, answer):
	if answer.find("bad_encrypt_is_v_bad") != -1:
		return { "correct": True, "message": "Good job!" }
	return { "correct": False, "message": "Nope. Try again." }