def grade(tid, answer):
	if answer.find("looks_like_my_robot_proof_protection_isn't_very_human_proof") != -1:
		return { "correct": True, "message": "Great idea!" }
	return { "correct": False, "message": "Nope, that's not quite right." }