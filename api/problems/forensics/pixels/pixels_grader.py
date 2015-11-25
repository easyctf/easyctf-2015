def grade(tid, answer):
	if answer.find("pretty_pixel_math") != -1:
		return { "correct": True, "message": "Great job!" }
	return { "correct": False, "message": "Try again!" }