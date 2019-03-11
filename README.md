# Python Level UP
![logo kursu](https://raw.githubusercontent.com/daftcode/daftacademy-python_levelup-spring2019/master/logo.png)

## Plan zajęć
![Plan zajęć](https://raw.githubusercontent.com/daftcode/daftacademy-python_levelup-spring2019/master/logo.png)

## Materiały z zajęć
[https://github.com/daftcode/daftacademy-python_levelup-spring2019](https://github.com/daftcode/daftacademy-python_levelup-spring2019)

## Przygotowanie środowiska pracy przed zajęciami
### Instalacja Python 3.7
Żeby nie tracić czasu w trakcie warsztatu, zależałoby nam żebyście przyszli na zajęcia z zainstalowaną odpowiednią wersją Pythona. Poniżej opisana jest krótka instrukcja instalacji dla najpopularniejszych systemów operacyjnych. 

#### Windows
Wejdź na stronę [https://www.python.org/downloads/release/python-363/](https://www.python.org/downloads/release/python-372/) i pobierz odpowiedni instalator z sekcji `Files` - `Windows x86-64 executable installer` dla systemu 64-bitowego lub `Windows x86 executable installer` dla systemy 32-bitowego.

Uruchom pobrany instalator. Zaznacz opcję `Add Python 3.6 to PATH`, a następnie kliknij `Install Now`.
#### macOS
Wejdź na stronę [https://www.python.org/downloads/release/python-363/](https://www.python.org/downloads/release/python-372/) i pobierz odpowiedni instalator z sekcji `Files` - `Mac OS X 64-bit/32-bit installer`. Uruchom pobrany plik i dokończ instalację.
#### Linux
Istnieje duża szansa, że masz zainstalowanego odpowiedniego pythona na swoim komputerze. W celu sprawdzenia jaka wersja jest zainstalowana, wpisz w terminalu:
```bazaar
python3 --version
```
Jeżelu uzyskasz wynik `Python 3.7.x` - jesteś gotowy na zajęcia. W przypadku, gdy nie zostanie odnaleziona komenda `python3` lub zainstalowana będzie niższa wersja niż `Python 3.7`, należy podążać za kolejnymi krokami, zależnymi od systemu, który posiadasz.
##### Debian lub Ubuntu
Użyj w terminalu następującej komendy:
```bazaar
sudo apt-get install python3.7
```
Dla wersji Ubuntu starszych niż 16.10 powyższa komenda może nie zadziałać. W takiej sytuacji należy skorzystać z deadsnakes PPA:
```bazaar
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.7
```
##### Fedora (22+)
Użyj w terminalu następującej komendy:
```bazaar
sudo dnf install python3
```
Dla starszych wersji Fedory możesz dostać błąd mówiący o tym, że komenda `dnf` nie została znaleziona. W takiej sytuacji należy skorzystać z komendy `yum`.
##### openSUSE
Użyj w terminalu następującej komendy:
```bazaar
sudo zypper install python3
```
### Sprawdzenie, czy Python 3.7 jest zainstalowany
Wpisz w terminalu następującą komendę:
```bazaar
python3.7 --version
```
Jeżeli powyższa komenda zwróci wynik `Python 3.7.x` oznacza to, że masz zainstalowaną odpowiednią wersję Pythona.

Na Windowsie powyższa komenda może nie zadziałać. Wtedy należy użyć w `Wierszu polecenia`:
```bazaar
python --version
```
Powinno ono zwrócić wynik `Python 3.7.x`.
### Wybór edytora tekstu
Programowanie w Pythonie nie wymaga żadnych specjalistycznych narzędzi - wystarczy korzystać z edytora tekstu. Na zajęciach możesz korzystać z dowolnego edytora. Jeżeli nie wiesz co wybrać, polecamy Sublime Text [https://www.sublimetext.com/](https://www.sublimetext.com/).
