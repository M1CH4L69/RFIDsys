
Střední průmyslová škola elektrotechnická Ječná 

Počítačové systémy a sítě 

Praha 2, Ječná 30, 120 00 

 

 

 

 

 

 

 
 Docházkový systém s RFID a webovým rozhraním 

 

 

 

 

 

 

 

 
Michal Němec, C3b 

Počítačové systémy a sítě

 

​​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​​ 

 

Anotace 

Tato práce se zabývá návrhem a implementací docházkového systému využívajícího RFID technologii a webové rozhraní. Cílem projektu je vytvořit moderní, uživatelsky přívětivý systém pro evidenci příchodů a odchodů uživatelů s možností administrace uživatelů, správy hesel a přehledu docházky. 

 

Úvod 

Docházkové systémy jsou nezbytným nástrojem pro sledování docházky zaměstnanců, studentů či členů organizací. Cílem tohoto projektu bylo navrhnout a implementovat docházkový systém, který bude jednoduchý na používání, finančně dostupný a zároveň flexibilní z hlediska rozšiřitelnosti. 

Hlavními požadavky na systém bylo: 
Přihlašování pomocí RFID karet 
Správa uživatelů přes webové rozhraní 
Záznam přihlášení, odhlášení a dalších událostí do databáze 
Možnost změny hesla uživatelem 
Filtrace a přehledné zobrazování záznamů 
Pro projekt jsem využil programovací jazyk Python, framework Flask, databázi MS SQL Server, RFID čtečku kompatibilní s Raspberry Pi a webové technologie HTML/CSS. 

Konkurence: 
Na trhu existují komerční řešení docházkových systémů (Například: Docházka.cz, Alveno, Idemia), která však bývají drahá a uzavřená. 

Výhody mého řešení: 
Nízké pořizovací náklady (použití levného hardware jako Raspberry Pi a open-source softwaru) 
Přizpůsobitelnost a rozšiřitelnost dle konkrétních požadavků 
Bez licenčních poplatků za software 

Způsob propagace: 
Osobní prezentace ve školním prostředí 
Publikace na GitHubu 

Návratnost investic: 
Investice do hardware a vývoje se vrátí snížením nákladů oproti komerčním řešením a možností přizpůsobení systému bez dalších poplatků. 

Vývoj 
Použité technologie: 
Python (verze 3.11.2) 
Flask (webový framework) 
HTML/CSS (front-end) 
pyodbc + FreeTDS (připojení k MS SQL) 
MS SQL Server 
Raspberry Pi 5 
RFID čtečka (125kHz) 
RFID (karty a čipy 125kHz) 

Struktura programu: 
app.py – hlavní Flask aplikace (funkce, správa webu a DB) 
get_rfid_uid.py – skript pro aktualizaci DB 
HTML šablony – přihlašování, správa uživatelů, přehled docházky 
SQL databáze – tabulky users a logs 

Průběh vývoje: 
Vývoj začal návrhem databázové struktury a základního CRUD rozhraní pro uživatele. Postupně byl přidán modul pro čtení RFID UID a jeho propojení s webovou částí. V další fázi jsem implementoval logování událostí, správu uživatelů a možnost změny hesla. Celý projekt byl průběžně testován a iterativně vylepšován. 

Testování 
Testovací scénáře a výsledky: 
1. Registrace nového uživatele 
Úspěšné vytvoření účtu s RFID kartou a heslem 
2. Přihlášení RFID kartou 
Systém správně zaznamenal příchod/odchod 
3. Změna hesla uživatelem 
Heslo změněno, změna zaznamenána v logu 
4. Filtrace a zobrazení záznamů 
Filtrace dle jména a příjmení fungovala správně 
5. Nasazení aplikace 
Aplikace spuštěna na Raspberry Pi s připojením na vzdálený SQL server. Funkční přístup z webového rozhraní 
Výsledky testů byly úspěšné, všechny požadavky byly splněny 

Nasazení a spuštění 
Požadavky: 
Raspberry Pi s připojenou RFID čtečkou 
Připojení k MS SQL databázi 
Nainstalovaný Python a požadované knihovny (Flask, pyodbc) 

Postup: 
Spustit get_rfid_uid.py pro čtení karet 
Spustit Flask aplikaci app.py 
Přistoupit k webovému rozhraní přes prohlížeč 

(Všechny scripty se spustí po zapojení RaspberryPi do zásuvky) 

Licence 
Projekt je distribuován pod licencí MIT – umožňuje volné používání, kopírování, úpravy a distribuci 

Odkaz na GIT
https://github.com/M1CH4L69/RFIDsys.git 

Závěr 
Projekt docházkového systému splnil stanovené cíle a poskytuje funkční řešení pro evidenci docházky pomocí RFID technologie. Vývoj probíhal iterativně s důrazem na modularitu a rozšiřitelnost. Testování potvrdilo správnou funkčnost všech klíčových částí. Systém je připraven pro praktické nasazení a díky open-source licenci může být dále vylepšován a přizpůsobován specifickým potřebám uživatelů. 

