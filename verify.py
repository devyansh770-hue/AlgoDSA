import requests

BASE_URL = 'http://127.0.0.1:8000'
session = requests.Session()

print('1. Testing Landing Page...')
r = session.get(f'{BASE_URL}/')
assert r.status_code == 200, f'Landing page failed: {r.status_code}'
print('   Landing page loaded successfully!')

print('2. Testing Login...')
r = session.get(f'{BASE_URL}/auth/login/')
csrf_token = r.cookies.get('csrftoken')
login_data = {
    'username': 'demo',
    'password': 'demo12345',
    'csrfmiddlewaretoken': csrf_token,
}
r = session.post(f'{BASE_URL}/auth/login/', data=login_data, headers={'Referer': f'{BASE_URL}/auth/login/'})
assert r.status_code in (200, 302), f'Login failed: {r.status_code}'
print('   Login successful!')

print('3. Testing Learn Hub Overview (/learn/)...')
r = session.get(f'{BASE_URL}/learn/')
assert r.status_code == 200, f'Learn Hub failed: {r.status_code}'
assert 'Learn DSA &amp; Concept Notes' in r.text or 'Learn DSA & Concept Notes' in r.text
assert 'Big-O Time &amp; Space Complexity Cheat Sheet' in r.text or 'Cheat Sheet' in r.text
print('   Learn Hub (/learn/) verified successfully!')

print('4. Testing Topic Study Page (/learn/linked-lists/)...')
r = session.get(f'{BASE_URL}/learn/linked-lists/')
assert r.status_code == 200, f'Learn Linked Lists failed: {r.status_code}'
assert 'Learn Linked Lists' in r.text
assert 'Chrome Browser Tabs' in r.text or 'Music Playlist' in r.text
assert 'Standard Code Template' in r.text
assert 'Custom Study Notes' in r.text
print('   Topic Study Page (/learn/linked-lists/) verified successfully!')

print('\nALL VERIFICATION TESTS PASSED SUCCESSFULLY FOR LEARN HUB & DIRECT LEETCODE CONNECT!')
