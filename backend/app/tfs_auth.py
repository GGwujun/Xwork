"""
TFS Auth Module - OAuth/PAT Authentication for Azure DevOps / TFS.

This module provides:
1. PAT (Personal Access Token) authentication
2. OAuth 2.0 authentication flow for Azure DevOps
3. Token storage and management
4. Credential validation
"""

import os
import base64
import json
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from pydantic import BaseModel
from pathlib import Path

# --- Types ---

class TfsCredentials(BaseModel):
    """TFS/Azure DevOps credentials."""
    type: str  # "pat" or "oauth"
    organization: str
    pat: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_at: Optional[datetime] = None

class AuthResult(BaseModel):
    """Result of an authentication attempt."""
    success: bool
    message: str
    credentials: Optional[TfsCredentials] = None

# --- Token Storage ---

class TokenStorage:
    """
    Secure storage for TFS credentials.
    In production, use OS keychain (keyring library) or encrypted storage.
    """
    
    def __init__(self, storage_dir: Optional[str] = None):
        self.storage_dir = Path(storage_dir or os.path.expanduser("~/.forge"))
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.token_file = self.storage_dir / "tfs_credentials.json"
    
    def save(self, credentials: TfsCredentials) -> bool:
        """Save credentials to storage."""
        try:
            data = credentials.model_dump()
            # Convert datetime to ISO string
            if data.get("expires_at"):
                data["expires_at"] = data["expires_at"].isoformat()
            
            with open(self.token_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Failed to save credentials: {e}")
            return False
    
    def load(self) -> Optional[TfsCredentials]:
        """Load credentials from storage."""
        try:
            if not self.token_file.exists():
                return None
            
            with open(self.token_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Convert ISO string back to datetime
            if data.get("expires_at"):
                data["expires_at"] = datetime.fromisoformat(data["expires_at"])
            
            return TfsCredentials(**data)
        except Exception as e:
            print(f"Failed to load credentials: {e}")
            return None
    
    def clear(self) -> bool:
        """Clear stored credentials."""
        try:
            if self.token_file.exists():
                self.token_file.unlink()
            return True
        except Exception:
            return False

# --- TFS Auth Client ---

class TfsAuthClient:
    """
    Handles authentication with TFS/Azure DevOps.
    """
    
    # Azure DevOps OAuth endpoints
    OAUTH_AUTHORIZE_URL = "https://app.vssps.visualstudio.com/oauth2/authorize"
    OAUTH_TOKEN_URL = "https://app.vssps.visualstudio.com/oauth2/token"
    
    # OAuth app registration (set these via environment variables)
    CLIENT_ID = os.environ.get("AZURE_DEVOPS_CLIENT_ID", "")
    CLIENT_SECRET = os.environ.get("AZURE_DEVOPS_CLIENT_SECRET", "")
    REDIRECT_URI = os.environ.get("AZURE_DEVOPS_REDIRECT_URI", "http://localhost:8000/auth/callback")
    
    def __init__(self):
        self.storage = TokenStorage()
        self._cached_credentials: Optional[TfsCredentials] = None
    
    def get_current_credentials(self) -> Optional[TfsCredentials]:
        """Get currently stored credentials."""
        if self._cached_credentials:
            return self._cached_credentials
        self._cached_credentials = self.storage.load()
        return self._cached_credentials
    
    def is_authenticated(self) -> bool:
        """Check if we have valid credentials."""
        creds = self.get_current_credentials()
        if not creds:
            return False
        
        # For OAuth, check expiration
        if creds.type == "oauth" and creds.expires_at:
            if datetime.utcnow() >= creds.expires_at:
                return False
        
        # For PAT, just check if it exists
        if creds.type == "pat":
            return bool(creds.pat)
        
        return bool(creds.access_token)
    
    async def authenticate_with_pat(self, organization: str, pat: str) -> AuthResult:
        """
        Authenticate using a Personal Access Token.
        """
        if not pat or not organization:
            return AuthResult(
                success=False,
                message="Organization and PAT are required",
            )
        
        # Validate the PAT by making a test API call
        # In production, call: GET https://dev.azure.com/{org}/_apis/projects
        import httpx
        
        try:
            auth_header = base64.b64encode(f":{pat}".encode()).decode()
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://dev.azure.com/{organization}/_apis/projects?api-version=7.0",
                    headers={"Authorization": f"Basic {auth_header}"},
                    timeout=10.0,
                )
                
                if response.status_code == 200:
                    credentials = TfsCredentials(
                        type="pat",
                        organization=organization,
                        pat=pat,
                    )
                    self.storage.save(credentials)
                    self._cached_credentials = credentials
                    
                    return AuthResult(
                        success=True,
                        message=f"Successfully authenticated to {organization}",
                        credentials=credentials,
                    )
                elif response.status_code == 401:
                    return AuthResult(
                        success=False,
                        message="Invalid PAT or insufficient permissions",
                    )
                else:
                    return AuthResult(
                        success=False,
                        message=f"Authentication failed: {response.status_code}",
                    )
        except Exception as e:
            return AuthResult(
                success=False,
                message=f"Connection error: {str(e)}",
            )
    
    def get_oauth_authorize_url(self, organization: str, state: str = "") -> str:
        """
        Generate the OAuth authorization URL for user login.
        """
        from urllib.parse import urlencode
        
        params = {
            "client_id": self.CLIENT_ID,
            "response_type": "Assertion",
            "state": state or organization,
            "scope": "vso.work_full vso.code_full vso.build_execute",
            "redirect_uri": self.REDIRECT_URI,
        }
        
        return f"{self.OAUTH_AUTHORIZE_URL}?{urlencode(params)}"
    
    async def exchange_oauth_code(self, code: str, organization: str) -> AuthResult:
        """
        Exchange OAuth authorization code for access token.
        """
        import httpx
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.OAUTH_TOKEN_URL,
                    data={
                        "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
                        "client_assertion": self.CLIENT_SECRET,
                        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                        "assertion": code,
                        "redirect_uri": self.REDIRECT_URI,
                    },
                    timeout=15.0,
                )
                
                if response.status_code == 200:
                    token_data = response.json()
                    expires_in = token_data.get("expires_in", 3600)
                    
                    credentials = TfsCredentials(
                        type="oauth",
                        organization=organization,
                        access_token=token_data.get("access_token"),
                        refresh_token=token_data.get("refresh_token"),
                        expires_at=datetime.utcnow() + timedelta(seconds=expires_in),
                    )
                    self.storage.save(credentials)
                    self._cached_credentials = credentials
                    
                    return AuthResult(
                        success=True,
                        message="OAuth authentication successful",
                        credentials=credentials,
                    )
                else:
                    return AuthResult(
                        success=False,
                        message=f"Token exchange failed: {response.text}",
                    )
        except Exception as e:
            return AuthResult(
                success=False,
                message=f"OAuth error: {str(e)}",
            )
    
    async def refresh_oauth_token(self) -> AuthResult:
        """
        Refresh an expired OAuth token.
        """
        creds = self.get_current_credentials()
        if not creds or creds.type != "oauth" or not creds.refresh_token:
            return AuthResult(
                success=False,
                message="No refresh token available",
            )
        
        import httpx
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.OAUTH_TOKEN_URL,
                    data={
                        "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
                        "client_assertion": self.CLIENT_SECRET,
                        "grant_type": "refresh_token",
                        "refresh_token": creds.refresh_token,
                        "redirect_uri": self.REDIRECT_URI,
                    },
                    timeout=15.0,
                )
                
                if response.status_code == 200:
                    token_data = response.json()
                    expires_in = token_data.get("expires_in", 3600)
                    
                    creds.access_token = token_data.get("access_token")
                    creds.refresh_token = token_data.get("refresh_token", creds.refresh_token)
                    creds.expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
                    
                    self.storage.save(creds)
                    self._cached_credentials = creds
                    
                    return AuthResult(
                        success=True,
                        message="Token refreshed successfully",
                        credentials=creds,
                    )
                else:
                    return AuthResult(
                        success=False,
                        message=f"Token refresh failed: {response.text}",
                    )
        except Exception as e:
            return AuthResult(
                success=False,
                message=f"Refresh error: {str(e)}",
            )
    
    def logout(self) -> bool:
        """Clear stored credentials."""
        self._cached_credentials = None
        return self.storage.clear()
    
    def get_auth_header(self) -> Optional[str]:
        """Get the Authorization header value for API calls."""
        creds = self.get_current_credentials()
        if not creds:
            return None
        
        if creds.type == "pat" and creds.pat:
            auth_value = base64.b64encode(f":{creds.pat}".encode()).decode()
            return f"Basic {auth_value}"
        elif creds.type == "oauth" and creds.access_token:
            return f"Bearer {creds.access_token}"
        
        return None

# --- Global Instance ---

tfs_auth = TfsAuthClient()

# --- API Helpers ---

async def login_with_pat(organization: str, pat: str) -> Dict[str, Any]:
    """Login using PAT."""
    result = await tfs_auth.authenticate_with_pat(organization, pat)
    return result.model_dump()

async def get_oauth_url(organization: str) -> Dict[str, str]:
    """Get OAuth authorization URL."""
    url = tfs_auth.get_oauth_authorize_url(organization)
    return {"authorize_url": url, "organization": organization}

async def oauth_callback(code: str, organization: str) -> Dict[str, Any]:
    """Handle OAuth callback."""
    result = await tfs_auth.exchange_oauth_code(code, organization)
    return result.model_dump()

async def check_auth_status() -> Dict[str, Any]:
    """Check current authentication status."""
    return {
        "authenticated": tfs_auth.is_authenticated(),
        "credentials": tfs_auth.get_current_credentials().model_dump() if tfs_auth.get_current_credentials() else None,
    }

async def logout() -> Dict[str, bool]:
    """Logout and clear credentials."""
    success = tfs_auth.logout()
    return {"success": success}
