
import json

class ASVABSessionManager:
    def __init__(self):
        self.sessions = {}

    def start_session(self, user_id, mode="practice", section=None, sim_number=None):
        key = f"{user_id}-{mode}-{section or sim_number}"
        self.sessions[key] = {
            "mode": mode,
            "section": section,
            "sim_number": sim_number,
            "index": 0,
            "score": 0,
            "answers": []
        }
        return f"Session started for {mode} - {section or sim_number}"

    def save_answer(self, user_id, mode, section_or_sim, answer, correct):
        key = f"{user_id}-{mode}-{section_or_sim}"
        session = self.sessions.get(key)
        if not session:
            return "No active session"
        session["answers"].append(answer)
        if answer == correct:
            session["score"] += 1
        session["index"] += 1
        return session

    def get_session(self, user_id, mode, section_or_sim):
        key = f"{user_id}-{mode}-{section_or_sim}"
        return self.sessions.get(key, "No active session")

    def pause_session(self, user_id, mode, section_or_sim):
        return f"Session paused: {user_id}-{mode}-{section_or_sim}"

    def stop_session(self, user_id, mode, section_or_sim):
        key = f"{user_id}-{mode}-{section_or_sim}"
        return self.sessions.pop(key, "No active session to stop")

# Global instance
asvab_sessions = ASVABSessionManager()
