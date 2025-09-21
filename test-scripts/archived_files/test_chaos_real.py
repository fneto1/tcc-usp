#!/usr/bin/env python3
"""
Test real chaos engineering
"""
from chaos_real import real_chaos
import requests
import time

# Test scenario application
print("Testing real chaos scenarios...")
real_chaos.apply_scenario('medium_stress')

# Test request with real chaos
start = time.time()
try:
    response = real_chaos.add_chaos_to_request(requests.get, 'http://localhost:3000/health')
    print(f'Request completed in: {time.time()-start:.2f} seconds')
    print(f'Status: {response.status_code}')
except Exception as e:
    print(f'Error: {e}')
    print(f'Time elapsed: {time.time()-start:.2f} seconds')

# Clear chaos
real_chaos.clear_chaos()
print("Test completed!")