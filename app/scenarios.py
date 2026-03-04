from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Utterance:
    say: str
    pause_sec: int = 4  # time for the agent to respond

@dataclass
class Scenario:
    id: str
    title: str
    turns: List[Utterance]

def all_scenarios() -> Dict[str, Scenario]:
    scenarios = [
        Scenario(
            id="sched_simple",
            title="Simple appointment scheduling",
            turns=[
                Utterance("Hi, I’d like to schedule an appointment for knee pain.", 6),
                Utterance("Next week works. What times do you have available?", 6),
                Utterance("Morning is better. Could you book the earliest one?", 6),
                Utterance("Great, can you confirm the date and time again?", 5),
                Utterance("Thank you. That’s all.", 3),
            ],
        ),
        Scenario(
            id="reschedule",
            title="Reschedule appointment",
            turns=[
                Utterance("Hi, I have an appointment coming up and I need to reschedule it.", 6),
                Utterance("I’m not sure of the exact date. Can you look it up using my info?", 7),
                Utterance("Can we move it to the following week, any afternoon slot?", 7),
                Utterance("Please confirm the new appointment details.", 5),
                Utterance("Thanks.", 3),
            ],
        ),
        Scenario(
            id="cancel",
            title="Cancel appointment",
            turns=[
                Utterance("Hello, I need to cancel my appointment.", 6),
                Utterance("Yes, please cancel it. No reschedule right now.", 6),
                Utterance("Can you confirm it’s canceled?", 5),
                Utterance("Thanks.", 3),
            ],
        ),
        Scenario(
            id="refill",
            title="Medication refill request",
            turns=[
                Utterance("Hi, I’m calling to request a refill for my prescription.", 6),
                Utterance("It’s for pain medication I got after my last visit. Can you check what’s on file?", 7),
                Utterance("Yes, please send it to the same pharmacy as last time.", 7),
                Utterance("When will it be ready?", 5),
                Utterance("Thank you.", 3),
            ],
        ),
        Scenario(
            id="hours_location",
            title="Office hours and location questions",
            turns=[
                Utterance("Hi, what are your office hours this week?", 6),
                Utterance("Do you have a location near downtown? What’s the address?", 7),
                Utterance("Is parking available?", 5),
                Utterance("Thanks.", 3),
            ],
        ),
        Scenario(
            id="insurance",
            title="Insurance coverage question",
            turns=[
                Utterance("Hi, do you accept Blue Cross Blue Shield insurance?", 7),
                Utterance("If you’re not sure, can you tell me how I can verify coverage?", 7),
                Utterance("Okay, and do I need a referral?", 6),
                Utterance("Thank you.", 3),
            ],
        ),
        Scenario(
            id="edge_unclear",
            title="Mumbling / unclear + corrections",
            turns=[
                Utterance("Hi… uh… I need… an appointment… for my… ankle.", 7),
                Utterance("Sorry, I meant my right ankle. It started hurting yesterday.", 7),
                Utterance("I can do Friday or Monday. Which is available?", 7),
                Utterance("Please repeat the time. I didn’t catch that.", 6),
                Utterance("Thanks.", 3),
            ],
        ),
        Scenario(
            id="change_mind",
            title="Change mind mid-call",
            turns=[
                Utterance("Hi, I want to schedule an appointment for shoulder pain.", 6),
                Utterance("Actually—can we do knee pain instead? Sorry.", 7),
                Utterance("And… I may need imaging. Do you do X-rays there?", 7),
                Utterance("Ok book whatever is soonest.", 6),
                Utterance("Thanks.", 3),
            ],
        ),
        Scenario(
            id="after_hours",
            title="After-hours / urgent-ish",
            turns=[
                Utterance("Hi, it’s late but I wanted to see if you’re open right now.", 7),
                Utterance("If you’re closed, what should I do if pain gets worse tonight?", 8),
                Utterance("Okay. Then schedule me for the earliest available.", 7),
                Utterance("Thanks.", 3),
            ],
        ),
        Scenario(
            id="stress_long",
            title="Longer call + multiple questions",
            turns=[
                Utterance("Hi, I have a few questions and also want to book an appointment.", 7),
                Utterance("First, what are your hours and do you accept walk-ins?", 8),
                Utterance("Second, do you take Aetna? And do I need a referral?", 9),
                Utterance("Now, I’d like to schedule for back pain. Next week morning preferred.", 9),
                Utterance("Can you confirm everything we discussed?", 7),
                Utterance("Thanks.", 3),
            ],
        ),
    ]
    return {s.id: s for s in scenarios}