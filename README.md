# artifactory_api


portal username: alexeybeley
portal password: DGNHR$3@^7(*3)lmy!@2

api user: admin
api password: IAMwckGYQlRdz1g8Z0rRLA


#Usefull manual tests
Basic connectivity:
replace <> placeholders with real values:
```commandline
curl -u "<username>":"<password>" "https://alexeybeley.jfrog.io/artifactory/api/system/ping"
```


#`@connection_required` decorator
This allows to add any logic about the user connection status:
1) Access management
2) Logging 
etc.

#`@expose_api` decorator
Allows a developer by just adding this decorator above his function to make it automatically exposed in CLI.
All menus being added too.

