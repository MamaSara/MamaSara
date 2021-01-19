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

# Part of two-stage fallback policy. Currently will just restart conversation.
# Working on improving fallback response.
class ActionDefaultAskAffirmation(Action):
    """Asks for an affirmation of the intent if NLU threshold is not met."""

    def name(self) -> Text:
        return "action_default_ask_affirmation"

    def __init__(self) -> None:
        import pandas as pd

        # NOT IMPLEMENTED. Working on a means to resolve ambiguous input.
        self.intent_mappings = pd.read_csv("intent_description_mapping.csv")
        self.intent_mappings.fillna("", inplace=True)
        print("action_default_ask_affirmation")

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List["Event"]:

        intent_ranking = tracker.latest_message.get("intent_ranking", [])
        if len(intent_ranking) > 0:
            first_intent_names = intent_ranking[0].get("name", "")
        else:
            dispatcher.utter_message(text="let's restart.")
            dispatcher.utter_message(text="ask me a question.")
            return [Restarted()]

        print("ONE")
        # first_intent_names = [
        #     intent.get("name", "")
        #     for intent in intent_ranking
        #     if intent.get("name", "") != "out_of_scope"
        # ]

        # message_title = "Sorry, I'm not sure I've understood " "you correctly. Do you mean..."
        # print('TWO')
        # print(first_intent_names)
        # response = self.get_top_intent(first_intent_names)
        # dispatcher.utter_message(text=message_title)
        # print(response)
        # dispatcher.utter_message(text=response)

        message_title = "Could you repeat that?"
        dispatcher.utter_message(text=message_title)

        return [Restarted()]

    def get_top_intent(self, intent: Text) -> Text:
        utterance_query = self.intent_mappings.intent == intent

        utterances = self.intent_mappings[utterance_query].name[0]

        return utterances