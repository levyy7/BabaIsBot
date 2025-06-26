from src.modules.memory.base_memory import BaseMemory


class LongTermMemory(BaseMemory):
    def get_property_meanings(self, property_names=None):
        return self.get(path='property_meanings', fields=property_names)

    def get_affordables(self, affordable_names=None):
        return self.get(path='affordables', fields=affordable_names)


    def set_property_meanings(self, property_meanings):
        self.set(path='property_meanings', value=property_meanings)

    def set_affordables(self, affordables):
        self.set(path='affordables', value=affordables)