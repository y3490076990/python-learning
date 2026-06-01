import requests

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNzgwMjg1NTk2fQ.FVtoM6509JpglGXzOlYabSGLofQLnVMTvo-RCnYyK2I"

r = requests.post(
      "http://127.0.0.1:8000/articles",
      json={"title": "Hello", "content": "World"},
      headers={"Authorization": f"Bearer {token}"}
  )
print(r.status_code)
print(r.json())