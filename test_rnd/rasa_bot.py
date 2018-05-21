from rasa_nlu.converters import load_data
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer

training_data = load_data('data/demo_rasa.json')
trainer = Trainer(RasaNLUConfig("nlu_model_config.json"))
trainer.train(training_data)
model_directory = trainer.persist('models/nlu/', fixed_model_name="current")

from rasa_nlu.model import Metadata, Interpreter
interpreter = Interpreter.load(model_directory)
json = interpreter.parse("hello")
print(json)