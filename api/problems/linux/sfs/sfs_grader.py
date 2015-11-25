def grade(tid, answer):
	if answer.find("w0aw_stor1ng_fl4gs_in_pla1nt3xt_i5_s0oper_s3cure") != -1:
		return { "correct": True, "message": "Nice job!" }
	return { "correct": False, "message": "Nope, try again!" }