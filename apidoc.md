### API Documentation for Alarm Level Management

#### Overview
This document describes the APIs required for managing alarm levels, including token generation, retrieving alarm levels, and adding new alarm levels. All APIs require token validation and have a QPS limit of one request per minute.

### 1. Token Generation API

#### Endpoint
`POST /api/token`

#### Description
Generates a token that is valid for 6 hours.

#### Request
- **Headers:**
  - `Content-Type: application/json`
- **Body:**
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```

#### Response
- **Success:**
  - Status: `200 OK`
  - Body:
    ```json
    {
      "token": "your_generated_token",
      "expires_in": 21600
    }
    ```
- **Failure:**
  - Status: `401 Unauthorized`
  - Body:
    ```json
    {
      "error": "Invalid credentials"
    }
    ```

### 2. Get All Alarm Levels

#### Endpoint
`GET /api/alarm-levels`

#### Description
Retrieves all alarm levels in JSON format. Requires token validation.

#### Request
- **Headers:**
  - `Authorization: Bearer your_token`

#### Response
- **Success:**
  - Status: `200 OK`
  - Body:
    ```json
    {
      "alarm_levels": [
        {
          "id": 1,
          "level": "Low",
          "description": "Low severity alarm"
        },
        {
          "id": 2,
          "level": "Medium",
          "description": "Medium severity alarm"
        },
        ...
      ]
    }
    ```
- **Failure:**
  - Status: `401 Unauthorized`
  - Body:
    ```json
    {
      "error": "Invalid or expired token"
    }
    ```

### 3. Get Specific Alarm Level

#### Endpoint
`GET /api/alarm-levels/{id}`

#### Description
Retrieves the details of a specific alarm level by ID. Requires token validation.

#### Request
- **Headers:**
  - `Authorization: Bearer your_token`
- **Path Parameters:**
  - `id` (integer): The ID of the alarm level to retrieve.

#### Response
- **Success:**
  - Status: `200 OK`
  - Body:
    ```json
    {
      "id": 1,
      "level": "Low",
      "description": "Low severity alarm"
    }
    ```
- **Failure:**
  - Status: `401 Unauthorized`
  - Body:
    ```json
    {
      "error": "Invalid or expired token"
    }
    ```
  - Status: `404 Not Found`
  - Body:
    ```json
    {
      "error": "Alarm level not found"
    }
    ```

### 4. Add New Alarm Level

#### Endpoint
`POST /api/alarm-levels`

#### Description
Adds a new alarm level. Requires token validation.

#### Request
- **Headers:**
  - `Authorization: Bearer your_token`
  - `Content-Type: application/json`
- **Body:**
  ```json
  {
    "level": "High",
    "description": "High severity alarm"
  }
  ```

#### Response
- **Success:**
  - Status: `201 Created`
  - Body:
    ```json
    {
      "id": 3,
      "level": "High",
      "description": "High severity alarm"
    }
    ```
- **Failure:**
  - Status: `401 Unauthorized`
  - Body:
    ```json
    {
      "error": "Invalid or expired token"
    }
    ```

### 5. Update Alarm Level

#### Endpoint
`PUT /api/alarm-levels/{id}`

#### Description
Updates an existing alarm level by ID. Requires token validation.

#### Request
- **Headers:**
  - `Authorization: Bearer your_token`
  - `Content-Type: application/json`
- **Path Parameters:**
  - `id` (integer): The ID of the alarm level to update.
- **Body:**
  ```json
  {
    "level": "High",
    "description": "Updated high severity alarm"
  }
  ```
#### Response
- **Success:**
  - Status: `200 OK`
  - Body:
    ```json
    {
      "id": 3,
      "level": "High",
      "description": "Updated high severity alarm"
    }
    ```
- **Failure:**
  - Status: `401 Unauthorized`
  - Body:
    ```json
    {
      "error": "Invalid or expired token"
    }
    ```
  - Status: `404 Not Found`
  - Body:
    ```json
    {
      "error": "Alarm level not found"
    }
    ```

### 6. Delete Alarm Level

#### Endpoint
`DELETE /api/alarm-levels/{id}`

#### Description
Deletes an alarm level by ID. Requires token validation.

#### Request
- **Headers:**
  - `Authorization: Bearer your_token`
- **Path Parameters:**
  - `id` (integer): The ID of the alarm level to delete.

#### Response
- **Success:**
  - Status: `200 OK`
  - Body:
    ```json
    {
      "message": "Alarm level deleted successfully"
    }
    ```
- **Failure:**
  - Status: `401 Unauthorized`
  - Body:
    ```json
    {
      "error": "Invalid or expired token"
    }
    ```
  - Status: `404 Not Found`
  - Body:
    ```json
    {
      "error": "Alarm level not found"
    }
    ```

### 5. User and Token Management APIs

#### User Registration

##### Endpoint
`POST /api/users/register`

##### Description
Registers a new user.

##### Request
- **Headers:**
  - `Content-Type: application/json`
- **Body:**
  ```json
  {
    "username": "new_user",
    "password": "new_password"
  }
  ```

##### Response
- **Success:**
  - Status: `201 Created`
  - Body:
    ```json
    {
      "message": "User registered successfully"
    }
    ```
- **Failure:**
  - Status: `400 Bad Request`
  - Body:
    ```json
    {
      "error": "User already exists"
    }
    ```

#### User Login

##### Endpoint
`POST /api/users/login`

##### Description
Logs in a user and generates a token.

##### Request
- **Headers:**
  - `Content-Type: application/json`
- **Body:**
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```

##### Response
- **Success:**
  - Status: `200 OK`
  - Body:
    ```json
    {
      "token": "your_generated_token",
      "expires_in": 21600
    }
    ```
- **Failure:**
  - Status: `401 Unauthorized`
  - Body:
    ```json
    {
      "error": "Invalid credentials"
    }
    ```

#### User Deletion

##### Endpoint
`DELETE /api/users/{id}`

##### Description
Deletes a user by ID. Requires token validation.

##### Request
- **Headers:**
  - `Authorization: Bearer your_token`

##### Response
- **Success:**
  - Status: `200 OK`
  - Body:
    ```json
    {
      "message": "User deleted successfully"
    }
    ```

- **Failure:**
  - Status: `401 Unauthorized`
  - Body:
    ```json
    {
      "error": "Invalid or expired token"
    }
    ```
  - Status: `404 Not Found`
  - Body:
    ```json
    {
      "error": "User not found"
    }
    ```

#### Get All Users

##### Endpoint
`GET /api/users`

##### Description
Retrieves all users. Requires token validation.

##### Request
- **Headers:**
  - `Authorization: Bearer your_token`

##### Response
- **Success:**
  - Status: `200 OK`
  - Body:
    ```json
    {
      "users": [
        {
          "id": 1,
          "username": "user1"
        },
        {
          "id": 2,
          "username": "user2"
        },
        ...
      ]
    }
    ```
- **Failure:**
  - Status: `401 Unauthorized`
  - Body:
    ```json
    {
      "error": "Invalid or expired token"
    }
    ```

#### Get Specific User

##### Endpoint
`GET /api/users/{id}`

##### Description
Retrieves the details of a specific user by ID. Requires token validation.

##### Request
- **Headers:**
  - `Authorization: Bearer your_token`
- **Path Parameters:**
  - `id` (integer): The ID of the user to retrieve.

##### Response
- **Success:**
  - Status: `200 OK`
  - Body:
    ```json
    {
      "id": 1,
      "username": "user1"
    }
    ```
- **Failure:**
  - Status: `401 Unauthorized`
  - Body:
    ```json
    {
      "error": "Invalid or expired token"
    }
    ```
  - Status: `404 Not Found`
  - Body:
    ```json
    {
      "error": "User not found"
    }
    ```

#### Update User

##### Endpoint
`PUT /api/users/{id}`

##### Description
Updates an existing user by ID. Requires token validation.

##### Request
- **Headers:**
  - `Authorization: Bearer your_token`
  - `Content-Type: application/json`
- **Path Parameters:**
  - `id` (integer): The ID of the user to update.
- **Body:**
  ```json
  {
    "username": "updated_user",
    "password": "updated_password"
  }
  ```

##### Response
- **Success:**
  - Status: `200 OK`
  - Body:
    ```json
    {
      "id": 1,
      "username": "updated_user"
    }
    ```
- **Failure:**
  - Status: `401 Unauthorized`
  - Body:
    ```json
    {
      "error": "Invalid or expired token"
    }
    ```
  - Status: `404 Not Found`
  - Body:
    ```json
    {
      "error": "User not found"
    }
    ```

#### Token Validation

##### Endpoint
`GET /api/token/validate`

##### Description
Validates the token.

##### Request
- **Headers:**
  - `Authorization: Bearer your_token`

##### Response
- **Success:**
  - Status: `200 OK`
  - Body:
    ```json
    {
      "valid": true
    }
    ```
- **Failure:**
  - Status: `401 Unauthorized`
  - Body:
    ```json
    {
      "valid": false,
      "error": "Invalid or expired token"
    }
    ```

---

All endpoints adhere to a rate limit of one request per minute (QPS: 1). Ensure your client handles this limitation appropriately to avoid being rate-limited.