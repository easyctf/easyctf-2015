def grade(tid, answer):
	if answer.find("fl00r_d1visi0n") != -1:
		return { "correct": True, "message": "Niceeeeeee!" }
	return { "correct": False, "message": "Nope! Listen to your instincts . . ." }