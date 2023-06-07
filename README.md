## rSentimentAnalysis


## 1.	Charakterystyka oprogramowania 
   * a. Nazwa skrócona: rSA 
   * b. Nazwa pełna: Reddit Sentiment Analysis 
   * c. Krótki opis z wskazaniem celów: rSA będzie to aplikacja umożliwiająca analizę sentymentu z serwisu www.reddit.com. Celem aplikacji jest umożliwienie użytkownikom łatwej analizy sentymentu komentarzy i postów na wszelkie tematy z naszego serwisu. Naszym motywem przewodnim jest jednak tematyka piłkarska więc funkcjonalność będzie miała optymalne zostosowanie dla fanatyków sportu.
## 2.	Prawa autorskie 
* a. Autorzy: Aplikacja zostanie stworzona przez Mikołaja Orzoł i Jakuba Gabryszewskiego. 
* b. Warunki licencyjne do oprogramowania wytworzonego przez grupę: Aplikacja jest objęta licencją open-source na warunkach MIT License.
## 3.	Specyfikacja wymagań 
 
| Identyfikator	| Nazwa |	Opis | Priorytet | Kategoria |
| --------------|-------|------|-----------|-----------|
| REQ-1	| Analiza sentymentu |	Aplikacja powinna umożliwiać analizę sentymentu komentarzy i postów z serwisu www.reddit.com	| 1 |	Funkcjonalne |
| REQ-2	| Prezentacja wyników |	Aplikacja powinna prezentować wyniki analizy sentymentu. | 1	| Funkcjonalne |
| REQ-3	| Integracja z serwisem |	Aplikacja powinna umożliwiać pobieranie komentarzy i postów z serwisu www.reddit.com |	1	| Funkcjonalne |
| REQ-4	| Wyświetlanie popularnych klubów	| Aplikacja powinna wyświetlać popularne kluby w formie przycisków które będą przenosić na odpowiednie subreddity. Ułatwi to działania użytkownika i pozwoli oszczędzić jego czas. |	2	| Funkcjonalne |
| REQ-5	| Obsługa błędów	| Aplikacja powinna wyświetlać czytelne komunikaty błędów w przypadku wystąpienia problemów z działaniem aplikacji. |	2	| Poza funkcjonalne |
| REQ-6	| Język interfejsu	| Aplikacja powinna mieć interfejs w języku angielskim. |	3	| User Interface |
| REQ-7 | Podział postu według kryteriów | Aplikacja powinna umożliwiać wyciągnięcie z tekstu paragrafów/tytułów lub zdjęć | 3 | Funkcjonalne |
 
## 4. Architektura rozwoju

| importy | Opis | Polecenie |
| ------- | ---- | --------- |
| Flask | moduł potrzebny do utworzenia aplikacji we frameworku flask | pip install Flask |
| render_template | moduł potrzebny do utworzenia szablonu html w innym pliku i katalogu | pip install template-render |
| request | moduł potrzebny do wysyłania żądań ze strony  | pip install requests |
| redirect | moduł potrzebny do przekierowania na inną stronę. Zmienia on w tym celuu adres url | pip install redirect-streams |
| send_from_directory | moduł potrzebny do pobierania zawartości z wybranego komponentu na sstronie | pip install Flask |
| TextBlob | moduł potrzebny do rozpoznania języka tekstu, przetworzenia i określenia jego sentymentu | pip install Flask |
| praw | moduł ułatwiający korzystanie z API reddita | pip install Flask |
