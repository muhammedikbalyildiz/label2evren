# label2evren LLM Agent Tabanlı Object Detection Veri Seti Etiketleme Otomasyonu

## Giriş
Başlıca Savunma Sanayi Başkanlığı'nın geliştirdiği Evren platformu (https://evren.ssyz.org.tr/) için object detection modellerine özelleştirilmiş veri setlerini VOC standardıyla etiketleyip sisteme yükleme amaçlı düzenlenmiş otomasyon. Birkaç düzenlemeyle birlikte Evren platformu dışında da kullanılabilir.

**NOT:** Otomasyon veri setini güncelledikten sonra eski veriler silineceğinden, otomasyonu çalıştırmadan önce veri setinin güncel halinin versiyonlanması önerilir.


## Otomasyon

Otomasyon 3 agent, 1 MCP (Playwright MCP), 1 skill (playwright-mcp-tools), 2 Python scripti (detect_first_three.py ve detect_objects.py), 1 yerel görüntü işleme modelinden (rf-detr-xxlarge) oluşur.

### Agent-1
- Kullanıcı, agenta "start" yazar. Agent Playwright MCP kullanarak tarayıcıda https://evren.ssyz.org.tr/ adresini açar ve kullanıcının giriş yapıp Evren'deki veri seti linkini göndermesini bekler, kullanıcı giriş yaparken tarayıcıyı izlemez.
- Kullanıcı, agenta veri seti linkini (misalen https://evren.ssyz.org.tr/datasets/u41c639f9a604/drone-tespit-fork) gönderdikten sonra agent linke gidip veri setini .temp/ klasörüne indirir, veriyi normalize eder, veri seti ve etiketlemeyle ilgili gerekli bilgileri prompt halinde vererek Agent-2'yi çağırır.

### Agent-2
- Yerel görüntü işleme modelinin veri setinde tespit edebildiği nesneleri anlamak için detect_first_three.py scripti çalıştırılır, bu script veri setindeki ilk 3 resim dosyasını modele vererek nesneleri tanımasını ister.
- Agent, 3 resimde de ortak bulunan nesneleri veri setinde tanımlanmış sınıf isimleriyle karşılaştırır, aynı/benzer olanları eşleştirir ve buna göre detect_objects.py scriptini çalıştırır. Bu script, yerel görüntü işleme modelini tüm veri setinde gerekli sınıflar tanımlanmış helde kullanır ve VOC standardında etiketleme yaparak zipler.
- Agent, görüntü işleme modelinin çıkardığı veriyi kontrol eder, hata varsa düzeltir.

### Agent-1
- Agent-2'nin işi bitince etiketlenecek sınıf isimlerini prompt halinde vererek Agent-3'ü çağırır.

### Agent-3
- detect_objects.py scriptinin oluşturduğu zip'i açar, yerel görüntü işleme modelinin nesne çıkaramadığı resim dosyalarını kontrol eder, nesne bulursa etiketler.
- Tüm işi bitince dosyaları tekrardan VOC standardına göre zip'ler.

### Agent-1
- Eski veri setini silip, oluşturulan yeni veri setini sisteme yükler.
- Kullanıcıya rapor sunar, ardından artık kullanılmayacak olan .temp/ ve .playwright-mcp/ klasörlerinin içerini isteğe bağlı olarak siler.


## Benchmark

https://evren.ssyz.org.tr/datasets/u41c639f9a604/drone-tespit-fork veri setinde denendi.
- Tüm agentlara Qwen3.8 Flash Next Medium modeli verildi -> Toplam 600 veri, 7 hatalı etiketleme, 4 kısmi etiketleme, %98+ başarı oranı.
- Tüm agentlara Deepseek v4.1 Flash Medium modeli verildi -> Toplam 600 veri, 2 hatalı etiketleme, yaklaşık 10 kısmi etiketleme, %99 başarı oranı.


## Gereksinimler
- Evren hesabı
- Evren platformuna kaydedilmiş etiketsiz bir veri seti (veri setinin herkese açık olmaması önerilir)
- Veri setinde tanımlanmış sınıf(lar)
- Opencode veya alternatif bir harness
- Python3 & pip & requirements.txt dosyasındaki kütüphaneler
- 1 yerel görüntü işleme modeli (rf-detr-xxlarge, başka model kurulup ona göre scriptler yeniden yazılabilir veya scriptler iptal edilip tüm iş LLM'lere bırakılabilir)


## Kurulum

### 1. Python ortamı

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

> **GPU:** NVIDIA GPU kullanılacaksa PyTorch'un CUDA sürümününün `requirements.txt`'ten **önce** kurulması gerekir.
> Doğru komut [pytorch.org/get-started](https://pytorch.org/get-started/locally/) üzerinden alınır, ardından `pip install -r requirements.txt` ile devam edilir.

### 2. Modelin kurulumu

Model ağırlıkları `.roboflow/models/rf-detr-xxlarge.pth` (**~484 MB**, 507.831.201 bayt) `.gitignore` nedeniyle repoya alınmamıştır. Yani depoyu `git clone` ile alan birinin modeli ayrıca kurması gerekir.

Model yoksa ilk script çalıştırmasında modeli kütüphanenin kendisi indirir, MD5 doğrular ve `.roboflow/models/` altına yazar:

```bash
python3 detect_first_three.py -path ./gorseller
```

> İndirme her çalıştırmada tekrarlanmaz: dosya doğru MD5 ile yerindeyse kütüphane "already exists with correct MD5 hash" deyip geçer. MD5 tutmazsa dosyayı silip yeniden indirin. İlk indirme ~484 MB olduğu için biraz sürer.

### 3. Modelin konfigürasyonu

RF-DETR ağırlıkları `RF_HOME` değişkenindeki dizinde aranır. Bu, `.env` dosyasında tanımlıdır ve scriptler tarafından otomatik yüklenir; ayrı bir `export` gerekmez:

```bash
# .env
RF_HOME=.roboflow/models
```

Model path'i öncelik sırası:

1. Ortamda tanımlı `RF_HOME` (varsa `.env`'in üzerine yazmaz)
2. Repodaki `.env`
3. Kütüphane varsayılanı `~/.roboflow/models`

Tek seferlik geçersiz kılmak ya da farklı bir ağırlık dosyası kullanmak için `--weights` verilir:

```bash
python3 detect_objects.py -obj airplane -path ./gorseller -zip veri.zip
python3 detect_objects.py -obj airplane -path ./gorseller -w ./diger-model.pth
python3 detect_first_three.py -path ./gorseller -w ./diger-model.pth
```

Kurulumu doğrulamak için:

```bash
test -f .roboflow/models/rf-detr-xxlarge.pth && echo "model dosyası yerinde"
python3 -c "import rfdetr_plus; print('RF-DETR+ hazır:', rfdetr_plus.__version__)"
```


## Lisans

Bu depodaki Python scriptleri (`detect_objects.py`, `detect_first_three.py`), agent tanımları (`.opencode/agent/` içindeki `first-worker.md`, `second-worker.md`, `third-worker.md`) ve [README.md](README.md) dokümantasyonu — [MIT Lisansı](LICENSE) ile lisanslanmıştır. Bu lisans yalnızca yukarıda sayılan dosyaları kapsar; üçüncü taraf bileşenler kendi lisanslarına tabidir.

Yerel görüntü işleme modelinin ağırlıkları (`rf-detr-xxlarge.pth`) **bu lisansın kapsamı dışındadır** ve depoda bulundurulmaz ([.gitignore](.gitignore)).
