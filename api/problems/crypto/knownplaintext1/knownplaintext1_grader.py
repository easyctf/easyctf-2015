def grade(tid, answer):
	if answer.find("w0w_d4t_h3x_th0") != -1:
		return { "correct": True, "message": "Good job!" }
	return { "correct": False, "message": "Nope. Try again." }