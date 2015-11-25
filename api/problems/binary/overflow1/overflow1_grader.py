def grade(tid, answer):
	if answer.find("i_wish_everything_were_th1s_34sy") != -1:
		return { "correct": True, "message": "Nice." }
	return { "correct": False, "message": "Nope, try again!" }