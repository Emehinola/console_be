from datetime import datetime

def isLessThan(time1: datetime, time2: datetime):
    if(time1.year < time2.year):
        return True
    elif time1.month < time2.month:
        return True
    elif time1.day < time2.day:
        return True
    
    return False


def isEqual(time1: datetime, time2: datetime):
    if((time1.year == time2.year) & (time1.month == time2.month) & (time1.day == time2.day)):
        return True
    
    return False