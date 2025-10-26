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
Początek semestru, więc źle oceniłem ile czasu muszę poświęcić na nowe przedmioty przez weekend, więc troszkę brakło czasu
i kod jest messy i bez komentarzy (przepraszam kogokolwiek kto będzie to czytał)

Zrobiłem prosty interface do sterowania rakietą. Workflow wygląda następująco:
1.Wciskamy Fuel i czekamy aż rakieta zostanie zatankowana.
2.Wciskamy Start i czekamy aż rakieta bezpiecznie wyląduje.

100% kodu wykonane jest w pythonie i użyty framework to nice gui
Pozdrawiam Artur Radwański