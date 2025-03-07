def validate_title(title):
    if not isinstance(title,str):
        raise ValueError("Title must be str")
    
    if len(title)>225:
        raise ValueError("Title must not exceed 225 characters")
    
    return True

#if i only handle validity here, then the logic for how to HANDLe wrong values will
# be dealth by another func...
