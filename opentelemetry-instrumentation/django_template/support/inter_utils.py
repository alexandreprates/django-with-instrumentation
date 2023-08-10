from typing import Union


def retrieve_first_item_otherwise_itself(target: Union[str, Union[tuple, list]]):
    return target if isinstance(target, str) else target[0]
