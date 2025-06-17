
# Django Project

A small Django Project using **Django Rest Framework (DRF)**, JWT-based authentication, **Celery with Redis** as a broker, and a Telegram Bot Webhook to fetch Username.

## Installation

### Clone the repository

```bash
git clone https://github.com/AmanDevelops/django-project.git
cd django-project
```

    
### Environment Variables

To run this project, you need to add the following environment variables to your .env file

``` bash
# Database Variables
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_database_name
POSTGRES_HOST=postgres-server
POSTGRES_PORT=5432

# Deployment Variables
DEPLOYMENT_URL=localhost

# Authentication
JWT_SIGNING_KEY=mysupersecretkey

# Email
SMTP_SERVER=smtp.domain.com
USER_EMAIL=your_email@domain.com
USER_PASSWORD=super_secret_email_password

# Celery Configuration
CELERY_BROKER_URL='redis://redis-server:6379/0'
```

> :warning: Do not change `POSTGRES_HOST` and `CELERY_BROKER_URL` if deployed using Docker


### Start the Project

``` bash
docker compose up -d
```

## Usage/Examples


### Public API Endpoint
``` bash
curl --location 'http://localhost:8000/'
```

#### Response

``` json
{
  "message": "Hello From AmanDevelops"
}
```

--- 

### Secure Endpoint

#### Unauthenticated Request

``` bash
curl --location 'http://localhost:8000/protected'
```
#### Response
``` json
{
  "detail": "Authentication credentials were not provided."
}
```

#### Obtain JWT Token

``` bash
curl --location 'http://localhost:8000/api/token/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "demo",
    "password": "demo@123" 
}'
```
> These demo credentials was Created during deployment, check `docker-compose.yaml`

#### Response

``` json
{
   "refresh": "<refresh-token>",
   "access": "<access-token>"
}
```

#### Re-Request Authenticated Endpoint with JWT Token

Copy the access token from the response above and include it in this request.

``` bash 
curl --location 'http://localhost:8000/protected' \
--header 'Authorization: Bearer <access-token>'
```

### Celery Service 

``` bash
curl --location http://localhost:8000/send_email?email=your_email
```

> If You have setup the email credentials in `.env` then you will receive an email shortly.


### Telegram Username Collection

A simple Telegram webhook is implemented to collect usernames when users send `/start` to your bot.

To use this, your app must be publicly accessible (e.g., via ngrok or deployment).

#### 🔧 Local Testing (Webhook Simulation)

To test it locally, we will simulate the webhook request sent by Telegram, which contains the following JSON data.

``` bash
curl --location 'http://localhost:8000/webhook' \
--header 'Content-Type: application/json' \
--data '{
   "update_id":12345678,
   "message":{
      "message_id":1,
      "from":{
         "id":"user_id",
         "is_bot":false,
         "first_name":"First_Name",
         "username":"demouser1234",
         "language_code":"en"
      },
      "chat":{
         "id":"user_id",
         "first_name":"First_Name",
         "username":"demouser1234",
         "type":"private"
      },
      "date":1750091614,
      "text":"/start",
      "entities":[
         {
            "offset":0,
            "length":6,
            "type":"bot_command"
         }
      ]
   }
}'
```

The username `demouser1234` will be stored in your database if the response code is `200`.

#### Deployment

Once deployed, you can setup the webhook by sending this request to Telegram API 

``` bash
curl --location 'https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook' \
--form 'url="https://example.com/webhook"'
```

#### Response 

``` json
{
    "ok": true,
    "result": true,
    "description": "Webhook was set"
}
```