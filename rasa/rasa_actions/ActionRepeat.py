class ActionRepeat(Action):
def name(self) -> Text:
    return "action_repeat"

def run(self, dispatcher, tracker, domain):
    if len(tracker.events) >= 3:
        dispatcher.utter_message(tracker.events[-3].get('text'))
    return [UserUtteranceReverted()]
