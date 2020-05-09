#Alembic migrations
##Configuration
In order to create/run migrations, it is first needed to configure the database environment to which
the application will keep synced.
 
As base rule, make sure you set all the environment variables required in the config/settings
class. Most importantly, remember to set correctly the `database_url` variable, as it represents
the real database to which the migrations should be applied. 

##Create/apply migrations
Alembic is used to automate schema sync with the databases used. In order to keep in order the
database schema with respect to the app' models, first it is required to generate migration files, 
and then apply them to the database.
  
  For this, run this command to auto-generate migration files with the given message:
   
>`alembic revision --autogenerate -m "migration message"`

Afterwards, you may apply the changes (migrations) to the configured database with the following:

>`alembic upgrade head`