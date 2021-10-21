from wit import Wit

client = Wit("KADJWIX3VLFUEXI6DD5GFNWMVWI6FZBV")


while True:
    message = str(input("Enter your message: "))
    resp = client.message(message)
    print(resp)


