def clean():
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from pathlib import Path
    
    script_dir = Path(__file__).resolve().parent
    # Path to the service account JSON key file
    SERVICE_ACCOUNT_FILE = script_dir / 'python-docs-433001-743c22c36e61.json'

    # Define the scope for Google Docs and Drive API
    SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']

    # Authenticate and create the service object
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('docs', 'v1', credentials=credentials)

    # Document ID (replace with your actual document ID)
    DOCUMENT_ID = '1Z4RC4yN1omK6-yUJarf0uOY3MS4S70-R1iWlC15gRsU'

    try:
        # Get the document's content
        document = service.documents().get(documentId=DOCUMENT_ID).execute()

        # Check if the document has content
        content = document.get('body').get('content', [])

        # If the document is empty, print a message and exit
        if len(content) <= 1:
            print("The document is empty. No content to delete.")
            return

        # Get the end index (total length of the document content)
        end_index = content[-1].get('endIndex', None)

        if end_index is None or end_index <= 1:
            print("The document is empty. No content to delete.")
            return

        # Define the request to delete the content range (remove all content)
        delete_request = {
            'deleteContentRange': {
                'range': {
                    'startIndex': 1,  # Start after the document start (index 1 to avoid removing the document title if present)
                    'endIndex': end_index - 1
                }
            }
        }

        # Execute the delete request to clear the document
        service.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': [delete_request]}).execute()
        print("Document content deleted successfully.")

    except Exception as e:
        print({"error": e})


if __name__ == "__main__":
    clean()
    print("the clean body is executed.")