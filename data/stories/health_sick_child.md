## sick - one illness
* sick_child
    - illness_diagnostic_info_form
    - form{"name": "illness_diagnostic_info_form"}
    - form{"name": null}
    - action_sick_child

## sick child - multiple illnesses
* sick_child{"symptom": ["headache", "coughing"]}
    - illness_diagnostic_info_form
    - form{"name": "illness_diagnostic_info_form"}
    - slot{"symptom": ["headache", "coughing"]}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_sick_child