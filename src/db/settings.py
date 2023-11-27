class Index:
    tagsFullText = "TagsFulltext"
    statementsFullText = "StatementsFulltext"


class Constraint:
    statementId = "StatementId"
    tagId = "TagId"
    connectionId = "ConnectionId"
    username = "Username"


URI: str  # connection string
AUTH: tuple[str, str]  # username, password
DATABASE: str  # instance name


def pass_settings(uri, auth, database):
    global URI, AUTH, DATABASE
    URI = uri
    AUTH = auth
    DATABASE = database
