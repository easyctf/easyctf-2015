def grade(tid, answer):
	if answer.find("just_playing_h1de_and_seek_lel") != -1:
		return { "correct": True, "message": "Nice job!" }
	return { "correct": False, "message": "Nope, try again!" }