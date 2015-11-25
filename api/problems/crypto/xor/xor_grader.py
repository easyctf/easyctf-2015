def grade(tid, answer):
	if answer.find("yo_dawg_i_heard_you_liked_xor") != -1:
		return { "correct": True, "message": "So I put an XOR in your XOR so you could XOR while you XOR." }
	return { "correct": False, "message": "Nope. Try again." }