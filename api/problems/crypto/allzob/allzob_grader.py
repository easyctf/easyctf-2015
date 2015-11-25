def grade(tid, answer):
	if answer.find("l0l_l3l_k1k_k3k_;p;") != -1:
		return { "correct": True, "message": "Good job!" }
	return { "correct": False, "message": "Nope. Try again." }