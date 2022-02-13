import jwt
key = "secret"
encoded = jwt.encode({"some": "payload"},key)
print(jwt.decode("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiI1YWE5NmVjNy1mOTM2LTQzNTMtYTc1MC00Y2RmNWRjYWYzZDMiLCJleHAiOjE2MzExODc5NDd9.jzYGnHWWDucx3OxsIFoHI7xUQTUgpHfiriiBkevn7u8"))

