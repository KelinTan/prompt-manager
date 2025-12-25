from datetime import datetime
import pytz
from datetime import timedelta


def format_cst_datetime(utc_datetime: datetime) -> datetime:
    """
    Format a utc time to a cst timezone datetime
    """
    cst_datetime = utc_datetime.astimezone(pytz.timezone("Asia/Shanghai")) + timedelta(
        hours=8
    )
    return cst_datetime
