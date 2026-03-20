import numpy as np
from ..utils.common import get_logger

logger = get_logger()

class OrderedCategoryEncoder:
    def __init__(self):
        self.categories_: list[str] = None
        self.category_map: dict[str: int] = None
        self.inverse_category_map: dict[int: str] = None

    def fit(self, ordered_categories: list[str]):
        self.categories_ = ordered_categories
        self.category_map = {category: i+1 for i, category in enumerate(ordered_categories)}
        self.inverse_category_map = {i+1: category for i, category in enumerate(ordered_categories)}


    def transform(self, values: list[str]) -> np.array:
        if set(values) - set(self.categories_):
            for value in values:
                logger.info(f"{value} was not in the fit data")
            raise ValueError("New category found, cannot transform")
        return np.array([self.category_map[value] for value in values])

    def inverse_transform(self, values: list[str]) -> np.array:
        return np.array([self.inverse_category_map[value] for value in values])
      