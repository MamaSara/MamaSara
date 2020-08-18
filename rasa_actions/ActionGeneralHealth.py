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

import sys
sys.path.append('../')
from utils import read_responses, word_to_digits

class ActionGeneralHealth(Action):
    def name(self):
        return "action_general_health"

    def run(self, dispatcher, tracker, domain):
        responses = read_responses()

        months_old = int(word_to_digits(tracker.get_slot('months_old')))
        curr_iteration = tracker.get_slot("iteration_num")
        health = tracker.get_slot('health')

        if int(curr_iteration) > 2:
            dispatcher.utter_message(text="That's all I have on the subject.")
            return [Restarted()]

        if months_old < 15:
            return_message = responses["health_information"][health]["12"][int(curr_iteration)]
        else:
            return_message = responses["health_information"][health]["15"][int(curr_iteration)]

        dispatcher.utter_message(
            text=return_message
        )

        return [SlotSet("iteration_num", str(int(curr_iteration) + 1))]