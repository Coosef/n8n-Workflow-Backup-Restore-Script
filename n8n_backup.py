import requests
import os
import json
from datetime import datetime
from urllib.parse import urljoin

# === AYARLAR ===
N8N_BASE_URL = 'https://n8n.yeb.one/'  # n8n adresin (HTTPS zorunlu)
API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3OTk4YjJmMi0zMTY3LTQ1ZDAtYTBlNi1hNDcxOTc4ZmJkM2MiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzUwODczNzY1fQ.tdV5ptxscWcCYOOOHmLkI_us76XdIabyyryw-wv8y5I'
OUTPUT_DIR = 'n8n_workflows_backup'

# === HEADER ===
HEADERS = {
    'X-N8N-API-KEY': API_KEY,
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0'
}

# === FONKSİYONLAR ===
def sanitize_filename(name):
    return "".join(c if c.isalnum() else "_" for c in name)

def backup_all_workflows():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    list_url = urljoin(N8N_BASE_URL, 'api/v1/workflows')
    response = requests.get(list_url, headers=HEADERS)

    if response.status_code != 200:
        print(f"❌ Workflow listesi alınamadı! HTTP {response.status_code}")
        print("Yanıt:", response.text)
        return

    workflows = response.json().get('data', [])
    print(f"🔍 {len(workflows)} workflow bulundu. Yedekleme başlatılıyor...\n")

    for wf in workflows:
        wf_id = wf['id']
        wf_name = sanitize_filename(wf['name'])
        export_url = urljoin(N8N_BASE_URL, f'api/v1/workflows/{wf_id}')

        export_resp = requests.get(export_url, headers=HEADERS)
        if export_resp.status_code == 200:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{wf_name}_{wf_id}_{timestamp}.json"
            filepath = os.path.join(OUTPUT_DIR, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_resp.json(), f, indent=2)
            print(f"✅ Export edildi: {filename}")
        else:
            print(f"❌ Workflow {wf_name} alınamadı! HTTP {export_resp.status_code}")
            print("Yanıt:", export_resp.text)

def import_workflows():
    import_folder = OUTPUT_DIR
    files = [f for f in os.listdir(import_folder) if f.endswith('.json')]

    if not files:
        print("📂 Import edilecek JSON dosyası bulunamadı.")
        return

    print(f"\n🔁 {len(files)} dosya içe aktarılacak...\n")

    for file in files:
        with open(os.path.join(import_folder, file), 'r', encoding='utf-8') as f:
            workflow_data = json.load(f)
            workflow_data.pop('id', None)  # ID çakışmalarını önle

            import_url = urljoin(N8N_BASE_URL, 'api/v1/workflows')
            response = requests.post(import_url, headers=HEADERS, json=workflow_data)

            if response.status_code == 201:
                print(f"✅ Import başarılı: {file}")
            else:
                print(f"❌ Import başarısız: {file} - HTTP {response.status_code}")
                print("Yanıt:", response.text)

# === ANA MENÜ ===
if __name__ == '__main__':
    print("\n🧩 n8n Workflow Yönetim Scripti")
    print("1 - Export (yedekle)")
    print("2 - Import (geri yükle)\n")
    secim = input("Seçiminiz (1/2): ").strip()

    if secim == '1':
        backup_all_workflows()
    elif secim == '2':
        import_workflows()
    else:
        print("❗ Geçersiz seçim yapıldı.")
