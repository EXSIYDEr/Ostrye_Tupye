class Item:
    def __init__(self, id, name, category, unit, quantity, min_limit, storage_place, status="Норма"):
        self.id = id
        self.name = name
        self.category = category
        self.unit = unit
        self.quantity = quantity
        self.min_limit = min_limit
        self.storage_place = storage_place

        # Автоматическая проверка статуса по минимальному запасу
        if self.quantity <= 0:
            self.status = "Отсутствует"
        elif self.quantity < self.min_limit:
            self.status = "Мало"
        else:
            self.status = status

    def to_dict(self):
        """Преобразование объекта класса в словарь (как на скриншоте 3)"""
        return {
            "id": f"{self.id:03d}",
            "name": self.name,
            "category": self.category,
            "unit": self.unit,
            "quantity": self.quantity,
            "min_limit": self.min_limit,
            "storage_place": self.storage_place,
            "status": self.status
        }


class User:
    def __init__(self, id, username, password, role="Администратор"):
        self.id = id
        self.username = username
        self.password = password
        self.role = role

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role
        }
