gestures = [
    'UP',
    'DOWN',
    'LEFT',
    'RIGHT',
    'PULL',
    'PUSH',
    'CIRCLE CW',
    'CIRCLE CCW',
    'LOCK',
    'UNLOCK',
    'HELLO',
    'WAVE',
]


def to_vector(gesture):
    gesture_index = gestures.index(gesture)
    return [1 if i == gesture_index else 0 for i in range(len(gestures))]


def from_vector(vector):
    for i, el in enumerate(vector):
        if el > 0.6:
            return gestures[i]
    return None
