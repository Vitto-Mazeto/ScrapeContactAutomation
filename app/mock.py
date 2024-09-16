import random


def mock_google_search(query, num_results):
    return [f"https://example.com/{random.randint(1, 100000)}" for i in range(num_results)]

def mock_fetch_contacts(url):
    return {
        'site': url,
        'celular': [f"({random.randint(10, 99)}) {random.randint(90000, 99999)}-{random.randint(1000, 9999)}"],
        'email': [f"aaa{random.randint(1, 100000)}@example.com"]
    }