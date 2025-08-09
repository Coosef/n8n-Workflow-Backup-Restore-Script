📦 n8n Workflow Backup & Restore Script
Bu Python scripti, n8n otomasyon platformundaki tüm workflow'ları JSON formatında yedeklemek (export) ve gerektiğinde geri yüklemek (import) için geliştirilmiştir.

✨ Özellikler
Tüm workflow’ları toplu olarak yedekler

Otomatik dosya isimlendirme: Workflow adı, ID’si ve zaman damgası ile kaydeder

Geri yükleme desteği: Daha önce yedeklenen JSON dosyalarını toplu olarak n8n’e geri yükler

ID çakışmalarını önleme: Import sırasında workflow ID’si otomatik temizlenir

Kolay kullanım: Menü üzerinden export/import seçeneği yapılabilir

📂 Klasör Yapısı
pgsql
Kopyala
Düzenle
n8n_backup.py
n8n_workflows_backup/
    workflowName_ID_timestamp.json
🔧 Gereksinimler
Python 3.x

requests kütüphanesi (pip install requests)

n8n API erişimi ve API key (HTTPS üzerinden çalışmalıdır)

🚀 Kullanım
bash
Kopyala
Düzenle
python n8n_backup.py
Ardından:

1 → Workflow'ları yedekler

2 → JSON dosyalarını geri yükler

⚠️ Notlar
API anahtarınızın yetkili olması gerekir

Yedekler n8n_workflows_backup klasöründe saklanır

HTTPS zorunludur, HTTP bağlantılar desteklenmez

