from log.logger import log
from threading import Thread
from typing import List, Optional




class ThreadManager:
    """Класс для управления потоками."""
    threads: List[Thread] = []

    def __init__(cls) -> None: raise Exception("Класс ThreadManager работает только в статическом режиме")

    @classmethod
    def add_thread(cls, target: Optional[callable] = None, *args, **kwargs) -> None:
        """Добавляет новый поток в список и запускает его."""
        thread = Thread(target=target, args=args, kwargs=kwargs)
        thread.start()
        cls.threads.append(thread)
        log.info("Добавлен новый поток. Текущее количество потоков: %d", cls.countthreads())

    @classmethod
    def remove_thread(cls) -> None:
        """Удаляет последний поток из списка, если он существует."""
        if cls.threads:
            thread = cls.threads.pop()
            thread.join()  # Ждем завершения потока перед удалением
            log.info("Удален последний поток. Текущее количество потоков: %d", cls.countthreads())
        else:
            log.warning("Попытка удалить поток из пустого списка.")

    @classmethod
    def countthreads(cls) -> int:
        """Возвращает количество активных потоков."""
        return len(cls.threads)

    @classmethod
    def __repr__(cls) -> str:
        return f"ThreadManager(threads={cls.countthreads()})"