def grade(tid, answer):
	if answer.find("can_y0u_put_4ll_the_pieces_2gether") != -1 or answer.find("can_y0u_put_411_the_pieces_2gether") != -1 or answer.find("can_yOu_put_the_pieces_411_2gether") != -1 or answer.find("can_y0u_put_the_pieces_411_2gether") != -1 or answer.find("can_you_put_the_pieces_411_2gether") != -1:
		return { "correct": True, "message": "Great job!" }
	return { "correct": False, "message": "Try again..." }