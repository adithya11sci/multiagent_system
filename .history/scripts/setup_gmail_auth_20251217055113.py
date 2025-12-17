"""
Gmail OAuth Setup Script
Helps users authenticate with Gmail API
"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from config import settings


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def setup_gmail_auth(user_id: str = "default"):
    """
    Setup Gmail OAuth for a user
    
    Steps:
    1. User must have credentials.json from Google Cloud Console
    2. Run this script to authenticate
    3. Token will be saved for future use
    """
    print("=" * 60)
    print("Gmail OAuth Setup")
    print("=" * 60)
    print()
    
    # Check if credentials.json exists
    credentials_file = './credentials/credentials.json'
    
    if not os.path.exists(credentials_file):
        print("❌ Error: credentials.json not found!")
        print()
        print("To get credentials.json:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create a new project or select existing")
        print("3. Enable Gmail API")
        print("4. Create OAuth 2.0 credentials (Desktop app)")
        print("5. Download credentials and save as './credentials/credentials.json'")
        print()
        return False
    
    print("✅ Found credentials.json")
    print()
    
    # Check if token already exists
    token_path = f'./credentials/token_{user_id}.json'
    creds = None
    
    if os.path.exists(token_path):
        print(f"Found existing token for user: {user_id}")
        try:
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        except Exception as e:
            print(f"⚠️  Could not load existing token: {e}")
    
    # If no valid credentials, start OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token...")
            creds.refresh(Request())
        else:
            print("Starting OAuth flow...")
            print("A browser window will open for authentication.")
            print()
            
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file,
                SCOPES
            )
            creds = flow.run_local_server(port=8080)
        
        # Save token
        print(f"Saving token to {token_path}")
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    
    print()
    print("=" * 60)
    print("✅ Gmail OAuth setup complete!")
    print("=" * 60)
    print()
    print(f"Token saved for user: {user_id}")
    print("You can now use the Email Agent to access Gmail.")
    print()
    
    return True


def test_gmail_access(user_id: str = "default"):
    """Test Gmail access"""
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    
    token_path = f'./credentials/token_{user_id}.json'
    
    if not os.path.exists(token_path):
        print(f"❌ No token found for user: {user_id}")
        print("Run setup first: python scripts/setup_gmail_auth.py")
        return False
    
    try:
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        service = build('gmail', 'v1', credentials=creds)
        
        # Test by getting profile
        profile = service.users().getProfile(userId='me').execute()
        
        print("=" * 60)
        print("✅ Gmail Access Test Successful!")
        print("=" * 60)
        print(f"Email: {profile.get('emailAddress')}")
        print(f"Total Messages: {profile.get('messagesTotal')}")
        print(f"Total Threads: {profile.get('threadsTotal')}")
        print()
        
        return True
        
    except HttpError as error:
        print(f"❌ Gmail API Error: {error}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Setup Gmail OAuth')
    parser.add_argument('--user-id', default='default', help='User ID for token storage')
    parser.add_argument('--test', action='store_true', help='Test Gmail access after setup')
    
    args = parser.parse_args()
    
    # Ensure credentials directory exists
    os.makedirs('./credentials', exist_ok=True)
    
    # Run setup
    success = setup_gmail_auth(args.user_id)
    
    # Test if requested
    if success and args.test:
        print()
        test_gmail_access(args.user_id)
