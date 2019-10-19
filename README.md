Coding Challenge
conEEct Four

NAČIN POKRETANJA 
	--Prvi nacin za pokretanje igre, generisao sam .exe fajl kom mozete direktno pristupiti na bilo kom računaru
	--Drugi nacin je da instalirate pyp na vaš računar, kao i potrebne biblioteke u kojima sam radio, pygame, numpy... Kada isntalirate sve potrebne biblioteke i python na vaš računar bićete u mogućnosti da pokrenete kod, dvoklikom na .py datoteku pokrenuce se konzola kao i GUI aplikacija.

NAČIN IGRANJA 	
	--Igranje je vrlo intuitivno, pomeranjem miša levo desno možete da izaberete kolonu u koju želite da spustite token(ZETON), klikom na kolonu automacki će se popuniti prvi slobodan red sa žetonom, zatim je na redu implementirani AI algoritam i tako nazimenično se smenjujute. Ko ce biti prvi na potezuje AI ili vi, o tome odlučuje RANDOM generator.

OPIS ALGORITMA
	--Implementirao sam jedan od boljih algoritama pod nazivom Minmaks. Minimaks algoritam je rekurzivni algoritam za odabir sledećeg poteza u n-igrača igrama, uglavnom za dva igrača. Vrednost je povezana sa svakom pozicijom ili stanjem igre. Ova vednost se izračunava pomoću funkcije evaluacije pozicije i pokazuje koliko ta pozicija može značiti igračima. Igrač onda pravi potez koji maksimizuje minimalnu vrednost položaja protivnikovih mogućih poteza. Ako se A pokrenuo, A daje vrednost svakom od njegovih legalnih poteza.
	Moguća alokacija metoda se sastoji iz dodeljivanja pobede za A kao +1 i za B kao −1.Alternativno korišćenje pravila je ako je rezultat poteza pobeda za A dodeljuje se pozitivna beskonačnost i, ako je rezultat pobeda za B, dodeljuje se negativna beskonačnost. Vrednost A bilo kog sledećeg poteza je minimum vrednosti koje su nastale od svakog od B's mogućih odgovora. Iz ovog razloga, A zovemo maximizing player i B zovemo minimizing player, otuda naziv minimaks algoritam.
	Ovo može biti prošireno ako možemo da pružimo heurističnu evaluaciju funkcija koje dodeljuju vrednosti ne završnom potezu bez uzimanja u obzir sve mogućnosti pratećih kompletnih sekvenci. Tako možemo ograničiti minimaks algoritam tako što gledamo samo određeni broj poteza napred. Ovaj broj se zove "look-ahead", meren u "plies (Ply (chess))". Algoritam se može posmatrati kao istraživanje čvorova (node (computer science)) kod drveta igara(game tree). Efikasan faktor grananja (branching factor) drveta je srednja vrednost dete čvora svakog čvora (tj. srednja vrednost legalnih poteza na poziciju). Broj čvorova koji se uglavnom istražuju se povećavaju eksponencijalno (exponential growth) sa brojem slojeva(manje je od eksponencijalnog ako se evaluira grub potez ili ponavljanje pozicija). Broj čvorova koji se istražuju za analize igre je dakle približno faktor grananja povećao do jačine broja slojeva. On je dakle nepraktičan (Computational complexity theory#Intractability) da bi se završila analiza igara kao što je šah koristeći minimaks algoritam.
	Performanse naivnog minimaks algoritma mogu biti dramatično unapređene, bez odražavanja na rezultat, koristeći alfa-beta pretragu. Ostale heurističke metode mogu takođe da se koriste, ali ne može se za sve njih garatnovati da će dati rezultate kao nepromenjena pretraga.