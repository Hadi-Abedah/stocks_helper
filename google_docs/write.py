def write(line):
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from pathlib import Path
    script_path = Path(__file__).resolve().parent
    # Path to the service account JSON key file
    SERVICE_ACCOUNT_FILE = script_path / "python-docs-433001-1a40e64e3f61.json"

    # Define the scope for Google Docs and Drive API
    SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']

    # Authenticate and create the service object
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('docs', 'v1', credentials=credentials)

    # Document ID (replace with your actual document ID)
    DOCUMENT_ID = '1Z4RC4yN1omK6-yUJarf0uOY3MS4S70-R1iWlC15gRsU'
    line = line + '\n'

    # Define the requests to update the document
    requests = [
        {
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': line
            }
        }
    ]

    # Execute the requests to update the document
    result = service.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': requests}).execute()

    print('Updated document with ID: {0}'.format(DOCUMENT_ID))
