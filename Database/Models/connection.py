from bson import ObjectId


class Connection:
    """
    stm = statement
    """
    _id: ObjectId
    stm_start: int
    stm_stop: int
    stm_type: chr
    weight: float
