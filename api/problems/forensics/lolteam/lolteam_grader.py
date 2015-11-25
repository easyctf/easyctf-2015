def grade(tid, answer):
	if answer.find("no,_lolteam_is_not_an_admin_account") != -1:
		return { "correct": True, "message": "Great job!" }
	return { "correct": False, "message": "lol no" }