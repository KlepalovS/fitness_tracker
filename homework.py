class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:0.3f} ч.; '
                f'Дистанция: {self.distance:0.3f} км; '
                f'Ср. скорость: {self.speed:0.3f} км/ч; '
                f'Потрачено ккал: {self.calories:0.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,  # число шагов при ходьбе и беге либо гребков — при плавани
                 duration: float,  # длительность тренировки;
                 weight: float,  # вес спортсмена
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.action * self.LEN_STEP / self.M_IN_KM) / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1: int = 18
    COEFF_CALORIE_2: int = 20

    def __init__(self,
                 action: int,  # число шагов при ходьбе и беге либо гребков — при плавани
                 duration: float,  # длительность тренировки;
                 weight: float,  # вес спортсмена
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (self.COEFF_CALORIE_1 * self.get_mean_speed() - self.COEFF_CALORIE_2) * self.weight / self.M_IN_KM * \
               (self.duration * 60)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,  # число шагов при ходьбе и беге либо гребков — при плавани
                 duration: float,  # длительность тренировки;
                 weight: float,  # вес спортсмена
                 height: float,  # рост спортсмена
                 ) -> None:
        self.height = height
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (0.035 * self.weight + (self.get_mean_speed() ** 2 // self.height) * 0.029 * self.weight) * \
               (self.duration * 60)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,  # число шагов при ходьбе и беге либо гребков — при плавани
                 duration: float,  # длительность тренировки;
                 weight: float,  # вес спортсмена
                 length_pool: float,  # длина бассейна в метрах;
                 count_pool: int  # сколько раз пользователь переплыл бассейн.
                 ) -> None:
        self.length_pool = length_pool
        self.count_pool = count_pool
        super().__init__(action, duration, weight)

    def get_mean_speed(self):
        '''Переопределяем рассчет средней скорости при плавании:.'''
        return self.length_pool * self.count_pool / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Переопределяем количество затраченных калорий."""
        return (self.get_mean_speed() + 1.1) * 2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    data_traning = {'SWM': Swimming,
                    'RUN': Running,
                    'WLK': SportsWalking
                    }
    return data_traning[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
