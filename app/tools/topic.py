class action:
    def __init__(self, *a, **kwa):
        pass
    def run():
        pass

class prompt_action():
    prompt: str
    action: action
    pass

class topic_layer():
    prompts: list[prompt_action]
    def respond(self, ask: str):
        for p in self.prompts:
            if p.prompt == ask:
                p.action.run()