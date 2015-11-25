def grade(tid, answer):
	if answer.find("all_hail_michy") != -1:
		return { "correct": True, "message": "Much sharp" }
	return { "correct": False, "message": "Nope try again. This problem isn't like the others . . . you need to sharpen your mind" }