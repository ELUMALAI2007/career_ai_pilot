"""
Dashboard View Unit Tests
"""

def test_dashboard_redirect_unauthenticated(client):
    """Unauthenticated users should be redirected to login page."""
    response = client.get('/dashboard/', follow_redirects=True)
    assert response.status_code == 200
    assert b'Sign In' in response.data
