from aiogram.filters import Filter
from aiogram.types import Message
import asyncio

class MyFilter(Filter):

    def __and__(self, other: Filter) -> Filter:
        return CombinedFilter(self, other, operator='and')

    def __or__(self, other: Filter) -> Filter:
        return CombinedFilter(self, other, operator='or')


class CombinedFilter(Filter):

    def __init__(self, filter1: Filter, filter2: Filter, operator: str) -> None:

        self.filters = (filter1, filter2)
        self.operator = operator

    async def __call__(self, message: Message) -> bool:

        results = await asyncio.gather(*(filter_(message) for filter_ in self.filters))
        return all(results) if self.operator == 'and' else any(results)










 