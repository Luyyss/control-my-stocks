from src.utils.database import database
from src.utils.defaults import variables as va

db = database(va['DATABASE'])
db.connect()
db.createTables()