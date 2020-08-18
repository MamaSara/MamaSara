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

class ActionNutritionInformation(Action):
    def name(self):
        return "action_nutrition_information"

    def run(self, dispatcher, tracker, domain):
        responses = read_responses()

        # get age from slot and convert "eight" to 8
        months_old = int(word_to_digits(tracker.get_slot('months_old')))
        print(months_old)
        if months_old < 6:
            return_message = responses["nutrition_information"]['6']
        elif months_old < 9:
            return_message = responses["nutrition_information"]['9']
        elif months_old < 12:
            return_message = responses["nutrition_information"]['12']
        elif months_old < 24:
            return_message = responses["nutrition_information"]['24']

        dispatcher.utter_message(
            text=return_message
        )
        return [Restarted()]
