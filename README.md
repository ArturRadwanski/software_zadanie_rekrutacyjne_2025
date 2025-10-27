### Setup

Te same biblioteki:
```bash
pip install crccheck bitstruct pyyaml
```
Potem uruchamiamy kolejno:
```bash
python tcp_proxy.py
```

```bash
python tcp_simulator.py
```

```bash
python index.py
```
### Notka

Zrobiłem prosty interface do sterowania rakietą. Workflow wygląda następująco:
1.Wciskamy Fuel i czekamy aż rakieta zostanie zatankowana.
2.Wciskamy Start i czekamy aż rakieta bezpiecznie wyląduje.

Interfejs komunikuje się z serwerem nasłuchując w nieskończonej pętli, procesowanie odbywa się callbackach

100% kodu wykonane jest w pythonie i użyty framework to nice gui
