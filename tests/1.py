class Counter:
    def __init__(self, value):
        self._value = value
        self._history = [value]
        self._change_count = 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value != self._value:
            self._history.append(value)
            self._change_count += 1
            self._value = value

    @property
    def history(self):
        return self._history

    @property
    def change_count(self):
        return self._change_count


counter = Counter(1)
print(counter.value)        # 1
print(counter.history)      # [1]
print(counter.change_count) # 0

counter.value = 2
counter.value = 2          # Не  должно изменить историю
counter.value = 3

print(f"\n{counter.history}")      #  [1, 2, 3]
print(counter.change_count) # 2