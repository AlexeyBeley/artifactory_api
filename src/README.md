# artifactory_api

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

* `CLIMenu.split_full_call_path`
   Recursively find the function to be called.
   1) Bonus: You can make a sub_menu function: e.g `packages list by_project` can be a function
      but `packages list` can be a function too.  

#Miscellanies
1) Dot (.) is a restricted char in api_menu name. Can be switched to anything else. e.g ->


#Usefull manual tests
Basic connectivity:
replace <> placeholders with real values:
```commandline
curl -u "<username>":"<password>" "https://alexeybeley.jfrog.io/artifactory/api/system/ping"
```

