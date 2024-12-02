from log.logger import log
    
class Toggle:
    """Класс для управления состоянием бота (включено/выключено)."""
    _status: str = "Off"

    def __init__(cls) -> None: raise Exception("Класс Toggle работает только в статическом режиме")

    @classmethod
    def turn_on(cls) -> None:
        """Включает состояние."""
        if cls._status != "On":
            cls._status = "On"
            log.info("Состояние переключено на 'On'.")

    @classmethod
    def turn_off(cls) -> None:
        """Выключает состояние."""
        if cls._status != "Off":
            cls._status = "Off"
            log.info("Состояние переключено на 'Off'.")

    @classmethod
    def status(cls) -> str:
        """Возвращает статус."""
        log.info("Получение статуса бота.")
        return cls._status

    @classmethod
    def __repr__(cls) -> str:
        return f"Toggle(status={cls._status})"