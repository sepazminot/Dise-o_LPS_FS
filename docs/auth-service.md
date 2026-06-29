# AuthService - Sistema de Autenticación (PRO-21)

## Visión General

El AuthService es un sistema de autenticación basado en JWT RS256 implementado como un servicio gRPC. Proporciona funcionalidades completas de gestión de usuarios y autenticación, incluyendo registro, login, renovación de tokens, validación y gestión de perfiles.

**Características principales:**
- Autenticación basada en JWT RS256 (asimétrica)
- Gestión de tokens de acceso y refresh
- Roles y permisos (Admin, Teacher, Student)
- Hashing de contraseñas con bcrypt
- Interfaz gRPC para comunicación entre servicios
- Soporte para PostgreSQL como base de datos

## Arquitectura

```
┌─────────────┐
│   Cliente   │
│  (Frontend) │
└──────┬──────┘
       │ gRPC
       ↓
┌─────────────────────────────────────┐
│      AuthGrpcService (gRPC)        │
│  ┌──────────────────────────────┐  │
│  │   AuthService (Application) │  │
│  │  - Register                 │  │
│  │  - Login                    │  │
│  │  - RefreshToken             │  │
│  │  - ValidateToken            │  │
│  │  - GetProfile               │  │
│  │  - ChangePassword           │  │
│  └──────────────┬───────────────┘  │
└─────────────────┼──────────────────┘
                  │
        ┌─────────┴─────────┐
        ↓                   ↓
┌───────────────┐   ┌───────────────┐
│ UserRepository│   │  JWTAdapter   │
│  (PostgreSQL) │   │   (RS256)     │
└───────────────┘   └───────────────┘
```

**Flujo de autenticación:**

1. **Register/Login:**
   - Cliente → gRPC → AuthService → UserRepository (DB)
   - AuthService → JWTAdapter → Generar tokens
   - Retornar tokens al cliente

2. **ValidateToken:**
   - Cliente → gRPC → AuthService con access_token
   - AuthService → JWTAdapter → Validar firma
   - AuthService → UserRepository → Obtener usuario
   - Retornar usuario y permisos

3. **RefreshToken:**
   - Cliente → gRPC → AuthService con refresh_token
   - AuthService → JWTAdapter → Validar refresh_token
   - Generar nuevo par de tokens
   - Retornar nuevos tokens

## Configuración (Environment Variables)

| Variable | Descripción | Requerido | Valor por defecto | Comportamiento si no se configura |
|----------|-------------|-----------|-------------------|----------------------------------|
| `JWT_PRIVATE_KEY_PATH` | Ruta al archivo de clave privada RSA | No | (generado en runtime) | Genera clave temporal (NO para producción) |
| `JWT_PUBLIC_KEY_PATH` | Ruta al archivo de clave pública RSA | No | (generado en runtime) | Genera clave temporal (NO para producción) |
| `JWT_ALGORITHM` | Algoritmo de firma JWT | No | RS256 | Usa RS256 |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Tiempo de expiración del access token (minutos) | No | 30 | 30 minutos |
| `JWT_REFRESH_TOKEN_EXPIRE_DAYS` | Tiempo de expiración del refresh token (días) | No | 7 | 7 días |
| `JWT_ISSUER` | Emisor del token | No | educational-devops | educational-devops |
| `JWT_AUDIENCE` | Audiencia del token | No | educational-api | educational-api |
| `DATABASE_URL` | URL de conexión a PostgreSQL | Sí | - | Error de conexión |
| `GRPC_HOST` | Host del servidor gRPC | No | 0.0.0.0 | 0.0.0.0 |
| `GRPC_PORT` | Puerto del servidor gRPC | No | 50051 | 50051 |

**Ejemplo de archivo `.env`:**
```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/educational

# JWT RS256
JWT_PRIVATE_KEY_PATH=/path/to/private.pem
JWT_PUBLIC_KEY_PATH=/path/to/public.pem
JWT_ALGORITHM=RS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
JWT_ISSUER=educational-devops
JWT_AUDIENCE=educational-api

# gRPC
GRPC_HOST=0.0.0.0
GRPC_PORT=50051
```

## Guía de Integración (API Reference)

### Métodos gRPC expuestos

#### 1. Register
Registra un nuevo usuario en el sistema.

**Request:**
```protobuf
message RegisterRequest {
  string email = 1;
  string password = 2;
  string full_name = 3;
  Role role = 4;  // ROLE_ADMIN, ROLE_TEACHER, ROLE_STUDENT
}
```

**Response:**
```protobuf
message RegisterResponse {
  User user = 1;
  string access_token = 2;
  string refresh_token = 3;
  int32 expires_in = 4;  // segundos
}
```

**Ejemplo de uso (Python):**
```python
import grpc
from app.interfaces.grpc import auth_pb2, auth_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub = auth_pb2_grpc.AuthServiceStub(channel)

request = auth_pb2.RegisterRequest(
    email="student@example.com",
    password="SecurePass123!",
    full_name="John Doe",
    role=auth_pb2.ROLE_STUDENT
)

response = stub.Register(request)
print(f"Access Token: {response.access_token}")
print(f"Refresh Token: {response.refresh_token}")
```

#### 2. Login
Autentica un usuario existente.

**Request:**
```protobuf
message LoginRequest {
  string email = 1;
  string password = 2;
}
```

**Response:**
```protobuf
message LoginResponse {
  User user = 1;
  string access_token = 2;
  string refresh_token = 3;
  int32 expires_in = 4;
}
```

**Ejemplo de uso:**
```python
request = auth_pb2.LoginRequest(
    email="student@example.com",
    password="SecurePass123!"
)
response = stub.Login(request)
```

#### 3. RefreshToken
Renueva el access token usando el refresh token.

**Request:**
```protobuf
message RefreshTokenRequest {
  string refresh_token = 1;
}
```

**Response:**
```protobuf
message RefreshTokenResponse {
  string access_token = 1;
  string refresh_token = 2;
  int32 expires_in = 3;
}
```

#### 4. ValidateToken
Valida un access token y retorna información del usuario y permisos.

**Request:**
```protobuf
message ValidateTokenRequest {
  string access_token = 1;
}
```

**Response:**
```protobuf
message ValidateTokenResponse {
  bool valid = 1;
  User user = 2;
  repeated string permissions = 3;
}
```

#### 5. GetProfile
Obtiene el perfil del usuario autenticado.

**Request:**
```protobuf
message GetProfileRequest {}
```

**Response:**
```protobuf
message GetProfileResponse {
  User user = 1;
}
```

**Nota:** Actualmente requiere contexto de autenticación (pendiente de implementar).

#### 6. ChangePassword
Cambia la contraseña del usuario autenticado.

**Request:**
```protobuf
message ChangePasswordRequest {
  string current_password = 1;
  string new_password = 2;
}
```

**Response:**
```protobuf
message ChangePasswordResponse {
  bool success = 1;
}
```

**Nota:** Actualmente requiere contexto de autenticación (pendiente de implementar).

## Requisitos de Seguridad

### Por qué RS256

**RS256 (RSA Signature with SHA-256)** es un algoritmo de firma asimétrica que proporciona:

1. **Separación de responsabilidades:** La clave privada se usa para firmar tokens (solo en el servidor), mientras que la clave pública se usa para validar tokens (puede distribuirse a otros servicios).
2. **Mayor seguridad:** Las claves asimétricas son más difíciles de comprometer que las simétricas (HS256).
3. **Escalabilidad:** Múltiples servicios pueden validar tokens sin tener acceso a la clave privada.
4. **Revocación más fácil:** Si la clave privada se compromete, solo es necesario rotar las claves sin afectar a los clientes.

### Gestión de Certificados

**Para desarrollo:**
- El sistema genera claves temporales en runtime si no se encuentran los archivos
- **NO usar en producción**

**Para producción:**
1. **Generar claves RSA:**
   ```bash
   # Generar clave privada (2048 bits)
   openssl genrsa -out private.pem 2048
   
   # Generar clave pública
   openssl rsa -in private.pem -pubout -out public.pem
   
   # Establecer permisos restrictivos
   chmod 600 private.pem
   chmod 644 public.pem
   ```

2. **Almacenamiento seguro:**
   - **Nunca** commit las claves al repositorio
   - Usar secretos de Kubernetes / AWS Secrets Manager / Vault
   - Rotar claves regularmente (cada 90 días recomendado)
   - Usar variables de entorno o montajes de archivos seguros

3. **Rotación de claves:**
   - Implementar un sistema de `kid` (Key ID) en el payload JWT
   - Mantener múltiples pares de claves durante el período de transición
   - Invalidar tokens antiguos si es necesario

### Otras consideraciones de seguridad

- **Contraseñas:** Hashing con bcrypt (factor de costo 12 por defecto)
- **Tokens:** Access tokens de corta duración (30 min), refresh tokens de larga duración (7 días)
- **HTTPS:** Siempre usar TLS en producción para comunicación gRPC
- **Rate limiting:** Implementar límites de intentos de login
- **Auditoría:** Registrar eventos de autenticación para monitoreo

## Guía de Testing

### Prerequisites

```bash
# Instalar dependencias
cd backend
poetry install

# Configurar base de datos de pruebas
export DATABASE_URL=postgresql+asyncpg://test:test@localhost:5432/test_db
```

### Ejecutar tests

```bash
# Ejecutar todos los tests de auth
pytest tests/test_auth_service.py -v

# Ejecutar tests específicos
pytest tests/test_auth_service.py::test_register_user -v

# Ejecutar con coverage
pytest tests/test_auth_service.py --cov=app/application/auth_service --cov-report=html
```

### Tests implementados

1. **test_register_user:** Verifica registro exitoso de usuario
2. **test_register_duplicate_email:** Verifica que no se registren emails duplicados
3. **test_login_user:** Verifica login exitoso
4. **test_login_invalid_credentials:** Verifica fallo con credenciales inválidas
5. **test_refresh_token:** Verifica renovación de tokens
6. **test_validate_token:** Verifica validación de tokens
7. **test_validate_invalid_token:** Verifica rechazo de tokens inválidos
8. **test_get_profile:** Verifica obtención de perfil
9. **test_get_profile_not_found:** Verifica error cuando usuario no existe
10. **test_change_password:** Verifica cambio de contraseña
11. **test_change_password_wrong_current:** Verifica fallo con contraseña actual incorrecta
12. **test_jwt_adapter_create_token:** Verifica creación de tokens JWT
13. **test_jwt_adapter_validate_token:** Verifica validación de tokens JWT

### Setup de base de datos para tests

El archivo `tests/conftest.py` configura una base de datos temporal para los tests. Asegúrate de tener PostgreSQL ejecutándose:

```bash
# Docker
docker run -d --name test-postgres \
  -e POSTGRES_USER=test \
  -e POSTGRES_PASSWORD=test \
  -e POSTGRES_DB=test_db \
  -p 5432:5432 \
  postgres:15
```

### Tests de integración

Para probar el servicio gRPC completo:

```python
# test_integration.py
import grpc
from app.interfaces.grpc import auth_pb2, auth_pb2_grpc

def test_grpc_register():
    channel = grpc.insecure_channel('localhost:50051')
    stub = auth_pb2_grpc.AuthServiceStub(channel)
    
    request = auth_pb2.RegisterRequest(
        email="test@example.com",
        password="TestPass123!",
        full_name="Test User",
        role=auth_pb2.ROLE_STUDENT
    )
    
    response = stub.Register(request)
    assert response.access_token
    assert response.refresh_token
    assert response.user.email == "test@example.com"
```

## Troubleshooting

### Errores comunes

**Error: "Invalid token"**
- Verificar que el token no haya expirado
- Verificar que la clave pública coincida con la privada usada para firmar

**Error: "User not found"**
- Verificar que el usuario exista en la base de datos
- Verificar que el `user_id` en el token sea correcto

**Error: "Database connection failed"**
- Verificar que PostgreSQL esté ejecutándose
- Verificar la URL de conexión en `DATABASE_URL`

**Error: "Key generation failed"**
- Verificar permisos para escribir en el directorio de trabajo
- En producción, usar claves pre-generadas

## Referencias

- [gRPC Python Documentation](https://grpc.io/docs/languages/python/)
- [PyJWT Documentation](https://pyjwt.readthedocs.io/)
- [Protocol Buffers Guide](https://developers.google.com/protocol-buffers)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
