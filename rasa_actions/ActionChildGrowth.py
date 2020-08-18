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

# Gives info on breastfeeding frequency
class ActionHowToKnowIfChildIsGrowingWell(Action):
    def name(self):
        return "action_how_to_know_if_child_is_growing_well"

    def run(self, dispatcher, tracker, domain):
        responses = read_responses()

        return_message = responses["how_to_know_if_child_is_growing_well"][0]

        dispatcher.utter_message(
            text=return_message
        )
        return [Restarted()]