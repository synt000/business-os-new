curl -X POST http://127.0.0 \
     -H "Content-Type: application/json" \
     -d '{
       "username": "admin",
       "email": "admin@test.com",
       "password": "Admin12345",
       "tenant_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
       "role": "admin"
     }'
