from better_profanity import profanity

NAME = "Neuron"

RESERVED_WORDS = [
    NAME,
    "out",
]

profanity.load_censor_words(RESERVED_WORDS)