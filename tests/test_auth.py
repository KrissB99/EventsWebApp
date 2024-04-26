def test_login_page(test_client):
    response = test_client.get('/auth/sign-in')
    assert response.status_code == 200
    
def test_register_page(test_client):
    response = test_client.get('/auth/sign-up')
    assert response.status_code == 200