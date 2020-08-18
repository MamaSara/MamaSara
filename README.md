# Mama Sara

- Mama Sara is a voice-controlled virtual assistant which will provide information regarding the
 health and wellness of young children aged 0 to 2.

## Files
- **data/nlu.md** contains training examples for the NLU model  
- **data/stories.md** contains training stories for the Core model  
- **actions.py** contains some custom actions
- **config.yml** contains the model configuration
- **domain.yml** contains the domain of the assistant  
- **endpoints.yml** contains the webhook configuration for the custom action  
- **policy.py** contains a custom policy
- **run.py** contains code to train a Rasa model and use it to parse some text
- **responses.json** contains responses in JSON format

## Training

To train the bot, run
```
rasa train
```
This will store a zipped model file in `models/`.

## Testing

Start the action server

```
rasa run actions
```

Then to chat with the bot on the command line, run
```
rasa shell [--debug]
```

or to use the voice assistant, run
```
rasa run actions
rasa run -m models --endpoints endpoints.yml
python run.py
```
## Interactive Learning

Start the action server

```
rasa run actions
```

Then for interactive learning on the command line
```
rasa interactive -m models --endpoints endpoints.yml --skip-visualization 
```


Check out the [documentation](http://rasa.com/docs/rasa/user-guide/command-line-interface/).

# MamaSaraV1_PocketSphinx
