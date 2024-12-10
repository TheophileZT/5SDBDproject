import os

def main():
    # Fetch the secret from the environment variable
    secret_value = os.environ.get('MY_SECRET_KEY')

    # Check if the secret is set
    if not secret_value:
        print("Error: The secret key is not set.")
        return

    # Mock action using the secret
    print("The secret key is successfully retrieved and can now be used for further operations.")

if __name__ == "__main__":
    main()
