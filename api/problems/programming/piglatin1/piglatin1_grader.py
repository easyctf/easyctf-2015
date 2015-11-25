def grade(tid, answer):
	if answer.find("atinl4y_easyyay_3noughyay_orfay_ayay_1gpay!") != -1:
		return { "correct": True, "message": "Awesome." }
	return { "correct": False, "message": "Dang it. That's not right." }