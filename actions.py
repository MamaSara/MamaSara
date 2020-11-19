######################################## ActionSickChild ################################################
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
#########################################################################################################

######################################## ActionRestarted ################################################
from rasa_sdk import Action
from rasa_sdk.events import (
    Restarted,
)

class ActionRestarted(Action):
    """ This is for restarting the chat"""

    def name(self):
        return "action_chat_restart"

    def run(self, dispatcher, tracker, domain):
        return [Restarted()]
#########################################################################################################

######################################## ActionKeepChildHealthy #########################################
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

class ActionKeepChildHealthy(Action):
    def name(self):
        return "action_keep_child_healthy"

    def run(self, dispatcher, tracker, domain):
        responses = read_responses()

        curr_iteration = tracker.get_slot("iteration_num")

        if int(curr_iteration) >= 6:
            dispatcher.utter_message(text="That's all I have on the subject.")
            return [Restarted()]

        return_message = responses["keep_child_healthy"][int(curr_iteration)]

        dispatcher.utter_message(
            text=return_message
        )
        return [SlotSet("iteration_num", str(int(curr_iteration) + 1))]
#########################################################################################################

######################################## ActionGetChildToEatMore ########################################
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

class ActionGetChildToEatMore(Action):
    def name(self):
        return "action_get_child_to_eat_more"

    def run(self, dispatcher, tracker, domain):
        responses = read_responses()

        curr_iteration = tracker.get_slot("iteration_num")

        if int(curr_iteration) >= 4:
            dispatcher.utter_message(text="That's all I have on the subject.")
            return [Restarted()]

        return_message = responses["get_child_to_eat_more"][int(curr_iteration)]

        dispatcher.utter_message(
            text=return_message
        )
        return [SlotSet("iteration_num", str(int(curr_iteration) + 1))]

#########################################################################################################

######################################## ActionGeneralNutrition #########################################
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

#########################################################################################################

######################################## ActionGeneralHealth ############################################
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
#########################################################################################################

######################################## ActionFeedSickChild ############################################
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

class ActionWhatToFeedSickChild(Action):
    def name(self):
        return "action_what_to_feed_sick_child"

    def run(self, dispatcher, tracker, domain):
        responses = read_responses()

        curr_iteration = tracker.get_slot("iteration_num")

        if int(curr_iteration) >= 2:
            dispatcher.utter_message(text="That's all I have on the subject.")
            return [Restarted()]

        return_message = responses["what_to_feed_sick_child"][int(curr_iteration)]

        dispatcher.utter_message(
            text=return_message
        )
        return [SlotSet("iteration_num", str(int(curr_iteration) + 1))]
#########################################################################################################

######################################## ActionFeedingForGrowth #########################################
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
class ActionFeedingForGrowth(Action):
    def name(self):
        return "action_feeding_child_for_growth"

    def run(self, dispatcher, tracker, domain):
        responses = read_responses()

        curr_iteration = tracker.get_slot("iteration_num")

        if int(curr_iteration) >= 4:
            dispatcher.utter_message(text="That's all I have on the subject.")
            return [Restarted()]

        return_message = responses["feeding_child_for_growth"][int(curr_iteration)]

        dispatcher.utter_message(
            text=return_message
        )
        return [SlotSet("iteration_num", str(int(curr_iteration) + 1))]
#########################################################################################################

######################################## ActionDefaultFallback ##########################################
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

# Currently just restarts conversation when unsure of input.
# Will need to provide more robust fallback response.
class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List["Event"]:

        # Fallback caused by TwoStageFallbackPolicy
        if (
            len(tracker.events) >= 4
            and tracker.events[-4].get("name") == "action_default_ask_affirmation"
        ):

            dispatcher.utter_template("utter_restart_with_button", tracker)

            return [Restarted()]

        # Fallback caused by Core
        else:
            dispatcher.utter_template("utter_default", tracker)
            return [UserUtteranceReverted()]
#########################################################################################################

######################################## ActionDefaultAskAffirmation ####################################
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
#########################################################################################################

######################################## ActionChildGrowth ##############################################
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
#########################################################################################################

######################################## ActionBreastFeedingFrequency ###################################
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
#########################################################################################################

######################################## FormGeneralHealth ##############################################
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

class FormGeneralHealth(FormAction):
    """Form for resolving which response to return for a question about nutrition information"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "health_diagnostic_info_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return [
            "months_old",
            "health"
        ]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "months_old": self.from_entity(entity="months_old"),
            "health": self.from_entity(entity="health")
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        dispatcher.utter_message(text="thank you")
        return []
#########################################################################################################

######################################## FormIllnessDiagnosticInfo ######################################
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

class IllnessDiagnosticInfoForm(FormAction):
    """Form for resolving which response to return for a question about nutrition information"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "illness_diagnostic_info_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return [
            "months_old",
            "days_sick",
            "symptom"
        ]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "months_old": self.from_entity(entity="months_old"),
            "days_sick": self.from_entity(entity="days_sick"),
            "symptom": self.from_entity(entity="symptom")
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        dispatcher.utter_message(text="thank you")
        return []
#########################################################################################################

######################################## FormNutritionDiagnosticInfo ####################################
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

class NutritionDiagnosticInfoForm(FormAction):
    """Form for resolving which response to return for a question about nutrition information"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "nutrition_diagnostic_info_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["months_old"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "months_old": self.from_entity(entity="months_old")
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        dispatcher.utter_message(text="Thank you")
        return []

#########################################################################################################