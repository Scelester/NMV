import requests

def send_email():
    api_key = '89B1CAD4C46AC17690E272FCA21B778CF2049B26BE88579E252C9466207001F3771738F5D04DBCBA66E6333C4AD64248'
    url = 'https://api.elasticemail.com/v2/email/send'

    payload = {
        'apikey': api_key,
        'from': 'nabinpaudel664@gmail.com',  # Replace with your sender email
        'to': 'nabinpauudel664@gmail.com',     # Replace with recipient email
        'subject': 'Hello from Elastic Email',
        'bodyText': 'This is a test email sent using Elastic Email API.',
    }

    response = requests.post(url, data=payload)
    
    # Check the response from the API
    if response.status_code == 200:
        print('Email sent successfully!')
    else:
        print(f'Failed to send email. Status code: {response.status_code}')
        print('Response:', response.json())

# Example usage
send_email()
