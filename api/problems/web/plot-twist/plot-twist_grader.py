def grade(tid, answer):
	if answer.find("remember_to_check_everywhere") != -1:
		return { "correct": True, "message": "Nice!" }
	return { "correct": False, "message": "Check EVERYWHERE . . ." }