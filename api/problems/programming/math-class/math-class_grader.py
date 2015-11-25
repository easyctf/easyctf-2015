def grade(tid, answer):
	if answer.find("have_y0u_had_enough_of_math_in_sk0ol_yet") != -1:
		return { "correct": True, "message": "Nice job!" }
	return { "correct": False, "message": "If you're confused, read some tutorials :)" }