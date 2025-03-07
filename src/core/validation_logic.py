def validate_and_clean_title(title):
    if not isinstance(title,str):

        raise ValueError(f"Expected:Title must be str. Obtained {title}:{type(title)}")
    
    if len(title)>225:
        raise ValueError("Title must not exceed 225 characters")

    title=title.strip()    
    return title

#if i only handle validity here, then the logic for how to HANDLe wrong values will
# be dealth by another func...
