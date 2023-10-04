def test_root_is_404(client):
    """Dummy test."""
    response = client.get('/')
    assert response.status_code == 404

def test_explorer_is_200(client):
    """Other Dummy test."""
    response = client.get('/explorer')
    assert response.status_code == 200