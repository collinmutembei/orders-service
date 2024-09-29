## Orders Service

### About
Orders service is REST API service that offers the following:

- OAuth2 authentication for customer using Keycloak as its IDP.
- Customers can update their phone number to receive order notification through SMS.
- Customers can create orders.
- Customers can view all their orders.
- Customers can retrieve details for a specific order by its id.

The API documentation is available at http://localhost:8000/docs

### Operations
To get the orders service running, follow these steps:
1. First start the IDP server
```bash
make start-keycloak-svc
```
  -  Once the server is running at http://localhost:8080, login with the default admin credentials
> username: admin  
> password: admin
  - Keycloak is preset to import a realm called `sso`, switch to it from the dropdown on the top left corner.
  - Navigate to clients and click on the `orders-service` client.
  - Click on the credentials tab then press the **Regenerate** button next to **Client Secret**.
  - Click the copy button on the client secret field.

2. Generate and configure the environment variables required
```bash
make env-file
```
This will generate a .env file at `./src/.env`, update the credentials for the following services
> *OPENID_CONNECT_CLIENT_SECRET* : paste the value copied from step 1  
> *AFRICASTALKING_USERNAME* : default is "sandbox", update with altenative credentials from [AT](https://account.africastalking.com)    
> *AFRICASTALKING_API_KEY* : update API key to accordingly for the username above  
> *KEYCLOAK_PUBLIC_KEY* : Retrieve from Keycloak, under sso's "Real Settings" > "Keys" tab > "Public key" button for **RS256**  
  - Configure all credential accordingly.
3. Start the orders service server
```bash
make start-orders-svc
```
- With everything configured correctly, you should be able to authenticate from the "Authorize" button on swagger UI at https://localhost:8000/docs by filling in the client secret.
- The Keycloak form that opens has a register button where you can create a new user from.
- Once a token is issued and redirected back to the documentation page, the API calls should return successfully without any errors.
- In the event that you experience an authentication error, make sure you have configured the correct "Client Secret" and "Keycloak Public Key" and restart the orders-service.
