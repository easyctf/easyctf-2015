def grade(tid, answer):
	if answer.find("this_is_aperture_and_we_talk_too_much") != -1:
		return { "correct": True, "message": "Good job." }
	return { "correct": False, "message": "Nope. Try again." }