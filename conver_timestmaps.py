timestamps = [
    '5:18 — Tekma I, Team A vs Team B: "Welcome to today\'s match between Team A and Team B! The atmosphere is electric as we kick off this exciting encounter."',
    '10:15 — PRILOŽNOST: "Here comes Žan, with a spectacular dribble across the entire court! He\'s running out of energy, but what a run that was! Just couldn\'t find the finish."',
    '12:55 — GOL: "Goal in the dying moments for Team B! Hamzo finds the net, securing a win in a dramatic fashion. What a climax to this game!"',
    '14:20 — Tekma II, Team B vs Team C: "And we\'re onto the next game, with Team B carrying their momentum against Team C. Let\'s see how this unfolds."',
    '22:45 — Tekma III, Team A vs Team C: "The third game begins with Team A looking to bounce back against Team C. The stakes are high!"',
    '26:23 — PRILOŽNOST: "Matija makes a daring dribble into the corner. He passes to Aleksander... Oh, but the finish is just not there!"',
    '27:45 — GOL: "Team C scores a beautifully worked goal! Tazzo with the finish and Nick with the assist. That\'s textbook teamwork!"',
    '29:48 — GOL: "Mark for Team A responds with a goal after incredible dribbling by Matija. This match is full of twists!"',
    '31:20 — Tekma IV, Team A vs Team B: "The second encounter between Team A and Team B begins. The rivalry intensifies!"',
    '37:45 — GOL (Tim): "Tim scores for Team A after a deflection. Sometimes, luck is all you need!"',
    '38:45 — GOL (Aleksander): "Aleksander with a cool finish for Team A, following a splitting pass from Matija. These guys are on fire!"',
    '39:10 — PRILOŽNOST: "A 4v1 chance for Team A, but they can\'t capitalize! Such moments can turn games, and they\'ve missed it."',
    '40:14 — Tekma V, Team B vs Team C: "We\'re now into the second encounter between Team B and Team C. The competition is heating up!"',
    '41:43 — Izbijanje NM: "A crucial clearance by Nick, denying Argentim a scoring opportunity. That was close!"',
    '46:20 — GREAT GOL: "What a phenomenal volley by Matic for Team B! Žetko had no chance. The crowd goes wild!"',
    '48:50 — Tekma VI, Team A vs Team C: "Team A faces off against Team C in the next match. The energy is palpable!"',
    '51:43 — GOL: "Aleksander finishes a brilliant chance for Team A, with Mark assisting. Their teamwork is impeccable!"',
    '55:10 — POŠKODBA: "A pause as Davor from Team C is injured. We hope it\'s not too serious. The game takes a brief halt."',
    '56:38 — GOL: "Nick executes a beautiful volley off the crossbar for Team B, assisted by Žetko. What a goal!"',
    '57:39 — Tekma VII, Team B vs Team A: "Team B and Team A are back at it. The rivalry is intense, and the fans are fully engaged."',
    '57:51 — PRILOŽNOST: "Matija intercepts in the midfield but fails to convert. These missed opportunities might haunt them later."',
    '59:05 — GOL (Filip): "Filip scores for Team A after a deflection, with Aleksander providing some brilliant dribbling on the left. Luck is on their side!"',
    '1:02:03 — PRILOŽNOST: "Matija again in the action, but his pass to Filip isn\'t on target. Team A needs to capitalize on these moments."',
    '1:02:15 — GOL: "Hamzo scores from a tough angle for Team B! They\'re showing resilience and skill in equal measure."',
    '1:04:41 — GOL: "Team A\'s Matija scores uncontested after a well-worked set-piece, assisted by Filip. They\'re back in it!"',
    '1:06:46 — Tekma VIII, Team B vs Team C: "And we\'re off with Team B and Team C again. The pace has not dropped one bit."',
    '1:13:29 — Nice Dribbling: "Matic shows off his skills with some fine dribbling, getting the ball through the legs. The crowd appreciates the flair!"',
    '1:15:28 — GOL: "Argentim intercepts a pass from Samuel and scores a perfect lob for Team C. What a way to seize the moment!"',
    '1:16:10 — Tekma IX, Team A vs Team C: "We\'re into the next match with Team A and Team C. The intensity is not letting up."',
    '1:17:48 — PODAJA: "A great pass from Matija, but Mark is just unlucky not to score. The precision was there, but not the luck."',
    '1:18:10 — "Faul" nad Žetkotom: "High tension here! Team C calls for a foul, but VAR shows Matija was first. Play continues with no foul."',
    '1:20:28 - PODAJA: "Erik delivers a nice pass, but Argentim can\'t capitalize. Team C needs to make these chances count."',
    '1:20:55 — GOL: "Argentim, for Team C, finds the net after a pass from Tazzo. Teamwork makes the dream work!"',
    '1:22:08 — GOL: "Team A fights back! Žan carries the ball, Mark finds Aleksander, who converts. They\'re not giving up!"',
    '1:24:15 — GOL: "Argentim seals the win for Team C with another top-corner goal from a corner. They\'re asserting dominance!"',
    '1:27:30 — Tekma X, Last Game, Team A vs Team C: "We\'re into the last game of the day, Team A versus Team C. It\'s been a rollercoaster of a match!"',
    '1:28:25 — GOL: "Žetko for Team A scores after some nice passing with Kristjan. Beautiful teamwork on display!"',
    '1:28:54 — PRILOŽNOST: "A chance to equalize for Team A! Filip finds himself clear, but the shot isn\'t accurate enough."',
    '1:35:09 — GOL: "Team C scores a goal from a counterattack! Argentim scores 1v1 after a pass from Hamzo. Clinical finish!"',
    '1:35:25 — Žan Scores: "Žan for Team A responds with a fantastic solo run and goal. What a response!"',
    '1:36:52 — Piša Žan: "And in a delightful display of skill, Žan gets the ball through legs with some nice dribbling. The fans are loving it!"'
]


def convert_to_seconds(timestamp):
    parts = timestamp.split(':')
    if len(parts) == 3:
        hours, minutes, seconds = map(int, parts)
        return hours * 3600 + minutes * 60 + seconds
    elif len(parts) == 2:
        minutes, seconds = map(int, parts)
        return minutes * 60 + seconds
    else:
        return 0

def process_timestamps_corrected(timestamps):
    results = []
    for timestamp in timestamps:
        # Splitting the string into time and description parts
        parts = timestamp.split(' — ')
        if len(parts) == 2:
            time, description = parts
            time_in_seconds = convert_to_seconds(time)

            # Further split the description to separate the event type and associated name (if any)
            event_parts = description.split(' (')
            event_type = event_parts[0]
            event_name = event_parts[1][:-1] if len(event_parts) > 1 else ""

            results.append({"timestamp": time_in_seconds, "eventType": event_type, "name": event_name})
    return results

processed_timestamps = process_timestamps(timestamps)