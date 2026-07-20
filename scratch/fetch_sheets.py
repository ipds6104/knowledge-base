import urllib.request
import csv
import io

url = "https://docs.google.com/spreadsheets/d/1q4Mt-oEaDfspqJ4O_6xXWKYQqC0evpwdcFr5qzPsHyM/export?format=csv&gid=0"

try:
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        print("Fetch successful. Preview first 500 chars:")
        print(html[:500])
        
        # Save to csv file
        with open("scratch/kcda_2025_monitoring.csv", "w", encoding="utf-8") as f:
            f.write(html)
            
except Exception as e:
    print("Error:", e)
