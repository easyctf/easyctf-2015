def grade(tid, answer):
	if answer.find("bet_y0u_read_that_wiki_page") != -1:
		return { "correct": True, "message": "Nice job! You get an official art diploma from The Heischool of Failedxyz" }
	return { "correct": False, "message": "Nope! You clearly need to go to art school" }