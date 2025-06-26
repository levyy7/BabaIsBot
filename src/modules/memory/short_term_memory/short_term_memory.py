from src.modules.memory.base_memory import BaseMemory


class ShortTermMemory(BaseMemory):
    def get_state(self, fields=None):
        return self.get(path='state', fields=fields)

    def get_level(self, blocks=None):
        return self.get(path=['state','blocks'], fields=blocks)

    def get_rules(self, fields=None):
        return self.get(path='rules', fields=fields)


    def set_state(self, value):
        self.set(path='state', value=value)

    def set_rules(self, value):
        self.set(path='rules', value=value)