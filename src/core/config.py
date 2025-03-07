# config.py

class FlaskAppConfig:
    """
    Info: 
        Has App and Database related configurations
    """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///todo.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True  # Optional: Set to False in production

    


context_variables={
    "social_links":
        {
        "LinkedIn":"https://www.linkedin.com/in/yogeshvperumal/",
        "GitHub":"https://github.com/yogesh-codes"
        }
    ,

    "sample":
        {
        "s1":23,
        "s2":25
        }

}