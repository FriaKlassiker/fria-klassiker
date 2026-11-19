# Publicera Fria klassiker på GitHub

## 1. Huvudrepository

Skapa ett **publikt repository** med namnet `fria-klassiker` under organisationen [https://github.com/FriaKlassiker](https://github.com/FriaKlassiker). Lägg innehållet från denna katalog i **repositoryts rot** (inte i en extra underkatalog). Uteslut `org-profile/` eftersom det är ett separat repository.

1. Skapa repositoryt `FriaKlassiker/fria-klassiker`.
2. Ladda upp samtliga projektfiler eller pusha lokalt med `git`.
3. Öppna **Settings → Pages → Build and deployment → Source → GitHub Actions**.
4. Actions-workflowet `.github/workflows/pages.yml` publicerar `site/` när `main` uppdateras.
5. Efter att arbetsflödet har avslutats: [https://friaklassiker.github.io/fria-klassiker/](https://friaklassiker.github.io/fria-klassiker/).
6. Slå på Issues under repository-inställningarna för rättelser.

Exempel med lokalt Git, om repo redan är skapat:

```bash
git init
git add .
git commit -m "Launch Fria klassiker library"
git branch -M main
git remote add origin https://github.com/FriaKlassiker/fria-klassiker.git
git push -u origin main
```

## 2. Logotyp för organisationens profil

Skapa ett andra publikt repository under organisationen med namnet **`.github`**. Kopiera filerna från `org-profile/` till det repositoryts rot. GitHub visar då `profile/README.md` på https://github.com/FriaKlassiker. Om organisationsprofilen har en avatar kan den sättas till `site/assets/brand-mark.png`.

## 3. Om GitHub-appens åtkomst saknas

Den anslutna GitHub-appen måste installeras eller få rättigheter för organisationen **FriaKlassiker** och dess repositories. Först då kan verktyg som använder denna app skriva i repot direkt. Att kopplingen har åtkomst till ett annat personligt GitHub-konto räcker inte.

## 4. Redaktörsvarningar

- Alla böcker är markerade som **arbetsutgåvor/ej fackgranskade**. Ändra inte detta förrän verken verkligen granskats.
- *Staten* är endast bok I–II, inte hela verket.
- Alla PDF- och EPUB-utgåvor ligger under `site/nedladdning/`.
- En del underlag hänvisar till DOI, ISBN eller en separat JSON för *Staten* som inte finns i paketet. Påstå inte att sådana identifierare/objekt är publicerade.
- Kontrollera källa, licens, medverkande och eventuell upphovsrätt innan en formell lansering.

## 5. Efter att texter eller mallar ändras

`python3 build.py --bara-site` uppdaterar webbtexten i originalmallen. Kör därefter **alltid** `python3 scripts/enhance_site.py` för att återställa den grafiska portalen. För *Staten*-konverteringen gäller `python3 scripts/extract_staten.py`.
