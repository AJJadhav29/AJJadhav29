import json
from datetime import datetime

def load_agenda():
    with open("agenda.json", "r") as file:
        return json.load(file)

def find_session_by_keyword(keyword):
    agenda = load_agenda()
    keyword = keyword.lower()
    for session in agenda:
        if keyword in session["title"].lower():
            return session
    return None

def format_session_info(session):
    if not session:
        return "Sorry, I couldn't find a session matching that description."

    time_obj = datetime.fromisoformat(session["time"])
    formatted_time = time_obj.strftime("%A, %B %d at %I:%M %p")

    return f"""
**{session['title']}**  
👩‍💼 Speaker: {session['speaker']}  
🕘 Time: {formatted_time}  
📍 Location: {session['location']}  
🔗 [Join Link]({session['link']})
"""
