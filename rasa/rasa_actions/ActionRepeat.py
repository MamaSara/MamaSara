from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Action
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import (
    SlotSet,
    UserUtteranceReverted,
    Restarted,
    ConversationPaused,
    EventType,
)


class ActionRepeat(Action):
    def name(self) -> Text:
        return "action_repeat"

    def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_ignore_count = 2
        count = 0
        tracker_list = []
        print("repeating action")
        while user_ignore_count > 0:
            event = tracker.events[count].get('event')
            if event == 'user':
                user_ignore_count = user_ignore_count - 1
            if event == 'bot':
                tracker_list.append(tracker.events[count])
            count = count - 1

        i = len(tracker_list) - 1
        while i >= 0:
            data = tracker_list[i].get('data')
            if data:
                if "buttons" in data:
                    dispatcher.utter_message(text=tracker_list[i].get('text'), buttons=data["buttons"])
                else:
                    dispatcher.utter_message(text=tracker_list[i].get('text'))
            i -= 1

        return []
