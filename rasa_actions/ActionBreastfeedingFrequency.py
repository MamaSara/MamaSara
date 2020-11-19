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


class ActionBreastfeedingFrequency(Action):
    def name(self):
        return "action_breastfeeding_frequency"

    def run(self, dispatcher, tracker, domain):
        responses = read_responses()

        curr_iteration = tracker.get_slot("iteration_num")

        if int(curr_iteration) >= 4:
            dispatcher.utter_message(text="That's all I have on the subject.")
            return [Restarted()]

        return_message = responses["breastfeeding_frequency"][int(curr_iteration)]

        dispatcher.utter_message(
            text=return_message
        )
        return [SlotSet("iteration_num", str(int(curr_iteration) + 1))]