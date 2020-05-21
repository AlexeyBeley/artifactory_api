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

# For developer:
* `@connection_required`

   This decoratorallows to add any logic about the user connection status:
   1) Access management
   2) Logging 
   3) etc.

* `@expose_api`

   This decorator allows a developer by just adding this decorator above his function to:
   1) Mmake it automatically exposed in CLI.
   2) Add all submenus path.

#Miscellanies
1) Dot (.) is a restricted char in api_menu name. Can be switched to anything else. e.g ->
