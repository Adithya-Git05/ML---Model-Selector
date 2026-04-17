# AutoML Backend - User Authentication Microservice

A Python-based microservices authentication system with Flask, MongoDB, and JWT tokens.

## Architecture

```
API Gateway (Flask)
├── Auth Service (Register, Login, Verify Token, Refresh Token)
├── User Service (Get Profile, User Management)
└── Database Layer (MongoDB)
```

## Features

- **User Registration**: Create new user accounts with email verification
- **User Login**: Secure login with JWT token generation
- **Token Management**: Token verification and refresh capabilities
- **Password Security**: Bcrypt password hashing
- **Email Validation**: Built-in email format validation
- **Password Requirements**: Strong password enforcement (min 8 chars, uppercase, digits)
- **CORS Support**: Cross-origin resource sharing for frontend integration
- **MongoDB Integration**: Document-based user storage
- **Microservices Ready**: Scalable service-oriented architecture

## Project Structure

```
backend/
├── database/
│   └── connection.py          # MongoDB connection (Singleton pattern)
├── models/
│   ├── user.py               # User model
│   └── user_repository.py    # User database operations
├── services/
│   └── user_service.py       # Business logic (registration, login, etc.)
├── routes/
│   ├── auth_routes.py        # Authentication endpoints
│   └── user_routes.py        # User profile endpoints
├── utils/
│   └── auth_utils.py         # JWT and password utilities
├── app.py                     # Flask application setup
├── requirements.txt           # Python dependencies
└── .env                       # Environment variables
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- MongoDB (local or cloud instance)
- pip

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Edit `.env` file with your configuration:

```env
# MongoDB
MONGODB_URI=mongodb://localhost:27017
DB_NAME=automl_db

# JWT
JWT_SECRET_KEY=your_secret_key_here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Flask
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_flask_secret_key

# Services
API_GATEWAY_PORT=5000

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

### 3. Ensure MongoDB is Running

**Local MongoDB:**
```bash
mongod
```

**MongoDB Atlas (Cloud):**
Update MONGODB_URI in `.env`:
```
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
```

### 4. Run the Application

```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### Authentication Endpoints

#### 1. Register User
**POST** `/api/auth/register`

Request:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

Response:
```json
{
  "success": true,
  "message": "User registered successfully",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "email": "user@example.com",
    "created_at": "2024-04-17T10:30:00",
    "updated_at": "2024-04-17T10:30:00"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### 2. Login User
**POST** `/api/auth/login`

Request:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

Response:
```json
{
  "success": true,
  "message": "Login successful",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "email": "user@example.com",
    "created_at": "2024-04-17T10:30:00",
    "updated_at": "2024-04-17T10:30:00"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### 3. Verify Token
**POST** `/api/auth/verify-token`

Request:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

Response:
```json
{
  "success": true,
  "message": "Token is valid",
  "payload": {
    "user_id": "507f1f77bcf86cd799439011",
    "email": "user@example.com",
    "role": "user",
    "iat": 1713356723,
    "exp": 1713443123
  }
}
```

#### 4. Refresh Token
**POST** `/api/auth/refresh-token`

Request:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

Response:
```json
{
  "success": true,
  "message": "Token refreshed successfully",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### 5. Logout
**POST** `/api/auth/logout`

Headers:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Response:
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

### User Endpoints

#### 1. Get Current User Profile
**GET** `/api/users/profile`

Headers:
```
Authorization: Bearer <JWT_TOKEN>
```

Response:
```json
{
  "success": true,
  "message": "User found",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "user",
    "is_active": true,
    "created_at": "2024-04-17T10:30:00",
    "created_at": "2024-04-17T10:30:00",
    "updated_at": "2024-04-17T10:30:00
**GET** `/api/users/<user_id>`

Headers:
```
Authorization: Bearer <JWT_TOKEN>
```

Response:
```json
{
  "success": true,
  "message": "User found",
  "user": {...}
}
```

### Health Check
**GET** `/health`

Response:
```json
{
  "status": "healthy",
  "service": "API Gateway"
}
```

## Password Requirements

- Minimum 8 characters
- At least one uppercase letter
- At least one digit

**Valid Examples:**
- ✓ MyPassword123
- ✓ SecurePass999
- ✓ AutoML2024

**Invalid Examples:**
- ✗ short1
- ✗ nouppercase123
- ✗ NoDigitHere

## Database Schema

### Users Collection

```javascript
{
  _id: ObjectId,
  email: String (unique, lowercase),
  password_hash: String,
  first_name: String,
  last_name: String,
  role: String (default: "user"),
  is_active: Boolean (default: true),
  created_at: Date,
  updated_at: Date,
  last_login: Date (nullable)
}
```

## Error Handling

### Common Error Responses

**Invalid Credentials:**
```json
{
  "success": false,
  "message": "Invalid email or password"
}
```

**User Already Exists:**
```json
{
  "success": false,
  "message": "User with this email already exists"
}
```

**Invalid Token:**
```json
{
  "success": false,
  "message": "Token is missing"
}
```

**Server Error:**
```json
{
  "success": false,
  "message": "Internal server error"
}
```

## Security Features

1. **Password Hashing**: Bcrypt with 10 rounds
2. **JWT Token**: HS256 algorithm with configurable expiration
3. **CORS**: Restricted to configured origins
4. **Email Validation**: RFC 5322 compliant validation
5. **Input Validation**: Required field validation
6. **Error Handling**: Secure error messages

## Testing with cURL

### Register a User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123"
  }'
```

### Get Profile (with token)
```bash
curl -X GET http://localhost:5000/api/users/profile \
  -H "Authorization: Bearer <JWT_TOKEN>"
```

## Scalability & Microservices

This architecture is designed for horizontal scaling:

1. **Independent Services**: Each service can be deployed separately
2. **Database Isolation**: MongoDB collections for different domains
3. **Load Balancing**: Multiple instances behind a load balancer
4. **Service Discovery**: Ready for Kubernetes/Docker deployment
5. **API Gateway**: Single entry point for all services

### Future Enhancements

- [ ] Email verification/confirmation
- [ ] Password reset functionality
- [ ] Role-based access control (RBAC)
- [ ] OAuth 2.0 integration
- [ ] Two-factor authentication (2FA)
- [ ] Account lockout after failed attempts
- [ ] Audit logging
- [ ] Rate limiting
- [ ] API documentation (Swagger/OpenAPI)

## Troubleshooting

**MongoDB Connection Failed:**
- Ensure MongoDB is running
- Check MONGODB_URI in .env
- Verify network connectivity

**Invalid Token Error:**
- Token may have expired
- JWT_SECRET_KEY must match
- Check Authorization header format: `Bearer <token>`

**CORS Error:**
- Frontend URL must be in ALLOWED_ORIGINS
- Check .env CORS configuration

**Password Validation Error:**
- Ensure password meets requirements (8+ chars, uppercase, digit)

## License

MIT License

## Author

AutoML Backend Development Team
