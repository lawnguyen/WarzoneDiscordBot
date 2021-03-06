
class Message():

    def __init__(self, content, messageType, audio):
        self._messageTypes = [
            "cash_prompt", "loadout_cash_prompt", "checkpoint", "none"
        ]

        self._content = content
        self._messageType = messageType if messageType in self._messageTypes else "none"
        self._audio = audio

    @property
    def messageType(self):
        return self._messageType

    @property
    def content(self):
        return self._content

    @property
    def audio(self):
        return self._audio
