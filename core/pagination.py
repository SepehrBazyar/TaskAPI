from starlette.datastructures import URL
from urllib.parse import urljoin
from math import ceil
from typing import Optional, List
from .base import ItemsPerPage
from .config import settings


class DBPagination:
    """Class Database Paginate Check Validate Pgae Number Returned Next and Previous"""

    def __init__(self, url: URL, total: int, paginations: ItemsPerPage):
        self.total = total
        self.size = paginations.itemsPerPage
        self.url = urljoin(settings.BASE_URL, url.path)
        self.maximum = max(ceil(self.total / self.size), 1)
        self.queries = url.remove_query_params(("page", "itemsPerPage")).query
        self.page = self.maximum if paginations.page == 0 else paginations.page

    @property
    def skip(self) -> int:
        """Returned the Number of Skipped Item for Offset in Database Results"""

        return self.size * (self.page - 1)

    async def is_valid_page(self) -> bool:
        """Check Page Number is Valid Between One and Maximum Page Number"""

        return 1 <= self.page <= self.maximum

    async def __get_query(self, page: int, itemsPerPage: int) -> str:
        """Generate Query Parameter Strings to Filtering Pagination Items"""

        params = f"?page={page}&itemsPerPage={itemsPerPage}"
        if self.queries:
            params += f"&{self.queries}"
        return params

    async def __get_url(self, page: int, itemsPerPage: int) -> str:
        """Generate a URL by Base URL and New Page & itemsPerPage Variables"""

        return urljoin(self.url, await self.__get_query(page, itemsPerPage))

    async def __has_previous(self) -> bool:
        """Check Page Number Greater than 1 to Has a Previous Page Returned Boolean"""

        return self.page > 1

    async def __has_next(self) -> bool:
        """Check Page Number Lower than Maximum to Has a Next Page Returned Boolean"""

        return self.page < self.maximum

    async def __get_previous(self) -> Optional[str]:
        """Check if Has a Previous Page Generate a URL Link to Access Pre Page"""

        if await self.__has_previous():
            return await self.__get_url(self.page - 1, self.size)

    async def __get_next(self) -> Optional[str]:
        """Check if Has a Next Page Generate a URL Link to Access Next Page"""

        if await self.__has_next():
            return await self.__get_url(self.page + 1, self.size)

    async def next_and_previous(self) -> List[Optional[str]]:
        """Returned the URL Links Next & Pre Pages if Exists Else Returned None"""

        next = await self.__get_next()
        previous = await self.__get_previous()
        return next, previous
