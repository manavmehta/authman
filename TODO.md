# APIs needed for integration

* Get path based on username
	```
    payload:JWT -> including username
    response: access
    ```

* Get path based on org_id
	```
    payload:	org_id: int
    response: access
    ```

* Dependency:
  * SQL function to create path while adding a org


* GET `/auth/get-access-routes`
* GET `/auth/validate-access`

* `users/` (CRUD)
* `org/` (CRUD)

# Delegated:
    * Proper rollbacks for keycloak-DB sync
    * UUID for all DB  records
    * Error handling
    * Keycloak API status codes
    * Request and Response models