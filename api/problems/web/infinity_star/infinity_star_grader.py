def grade(tid, answer):
	if answer.find("csrf_protection_would_probably_have_been_a_good_idea_:/") != -1:
		return { "correct": True, "message": "Indeed." }
	return { "correct": False, "message": "Nope, that's not quite right." }