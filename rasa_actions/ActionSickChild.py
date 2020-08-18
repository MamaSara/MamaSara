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

# Responds with treatment info based on diagnostic info for ill child.
class ActionSickChild(Action):
    def name(self):
        return "action_sick_child"

    def run(self, dispatcher, tracker, domain):
        responses = read_responses()

        # get age from slot and convert "eight" to 8
        months_old = int(word_to_digits(tracker.get_slot('months_old')))
        print(months_old)

        days_sick = int(word_to_digits(tracker.get_slot('days_sick')))
        print(days_sick)

        symptoms = tracker.get_slot('symptom')
        print(symptoms)
        if type(symptoms) == list:
            return_message = ""
            for symptom in symptoms:
                return_message += responses["illness_information"][symptom] + " "
        else:
            return_message = responses["illness_information"][symptoms]

        dispatcher.utter_message(
            text=return_message
        )
        return [Restarted()]