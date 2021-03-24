from bs4 import BeautifulSoup
from datetime import datetime
import re

TAG = '[HTML PARSER]'

extensions = ["gif", "tif", "tiff", "bmp", "jpg", "jpeg", "png", "eps", "raw", "cr2", "nef", "orf", "sr2"]


def Find(string):
    # findall() has been used
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]


class HTMLParser:
    def __init__(self):
        self.soup = None

    def set_working_html(self, html):
        self.soup = BeautifulSoup(html, features='html.parser')
        self.soup.prettify()

    def get_links(self):
        href_links = [i.get("href") for i in self.soup.find_all(href=True)]
        js_links = []
        rez = href_links
        for i in self.soup.find_all(onclick=True):
            parsed = Find(i.get("onclick"))
            if len(parsed) > 0:
                js_links.append(parsed)
        for l in js_links:
            rez += l
        return rez

    def get_images(self):
        images = [(img.get("src"), img.get("src").split(".")[-1], datetime.now()) for img in self.soup.find_all('img') if img.get("src").split(".")[-1] in extensions]
        return images

    def get_content(self):
        # TODO: get text from html, remove stop words and stem them. Also content type if != html don't parse text
        #  just remember content type (pdf, docx, ppt, ...).
        pass


temp = HTMLParser()
temp.set_working_html("""
<!doctype html>
<!--[if lt IE 7]><html class="no-js lt-ie9 lt-ie8 lt-ie7" lang="sl"><![endif]-->
<!--[if IE 7]><html class="no-js lt-ie9 lt-ie8" lang="sl"><![endif]-->
<!--[if IE 8]><html class="no-js lt-ie9" lang="sl"><![endif]-->
<!--[if gt IE 8]><![endif]-->
<html class="no-js" lang="sl" x-ms-format-detection="none">
<head>
	<base href="https://www.gov.si/"><!--[if lte IE 6]></base><![endif]-->
	<title>Portal GOV.SI</title>
	<meta charset="UTF-8">
	<meta http-equiv="x-ua-compatible" content="ie=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<meta name="generator" content="SilverStripe - https://www.silverstripe.org" />
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<link rel="alternate" hreflang="de" href="https://www.gov.si/de/" />

	<link rel="alternate" hreflang="en" href="https://www.gov.si/en/" />

	<link rel="alternate" hreflang="es" href="https://www.gov.si/es/" />

	<link rel="alternate" hreflang="fr" href="https://www.gov.si/fr/" />

	<link rel="alternate" hreflang="hu" href="https://www.gov.si/hu/" />

	<link rel="alternate" hreflang="it" href="https://www.gov.si/it/" />

	<link rel="alternate" hreflang="pt" href="https://www.gov.si/pt/" />

	<link rel="alternate" hreflang="ru" href="https://www.gov.si/ru/" />

	<link rel="alternate" hreflang="sl" href="https://www.gov.si/" />


	
	<meta property="og:type" content="article" />
<meta property="og:title" content="Portal GOV.SI | GOV.SI" />

<meta property="og:url" content="https://www.gov.si/" />
<meta property="og:image" content="https://www.gov.si/assets/sistem/gov.si.share.and.social.media.jpg" />
<meta property="og:site_name" content="Portal GOV.SI" /> 

<meta name="twitter:card" content="summary" />
<meta name="twitter:title" content="Portal GOV.SI | GOV.SI" />

<meta name="twitter:image" content="https://www.gov.si/assets/sistem/gov.si.share.and.social.media.jpg" />
<meta name="twitter:site" content="@vladaRS" />
	<link rel="apple-touch-icon" sizes="57x57" href="/resources/themes/gov/images/favicon/apple-icon-57x57.png">
<link rel="apple-touch-icon" sizes="60x60" href="/resources/themes/gov/images/favicon/apple-icon-60x60.png">
<link rel="apple-touch-icon" sizes="72x72" href="/resources/themes/gov/images/favicon/apple-icon-72x72.png">
<link rel="apple-touch-icon" sizes="76x76" href="/resources/themes/gov/images/favicon/apple-icon-76x76.png">
<link rel="apple-touch-icon" sizes="114x114" href="/resources/themes/gov/images/favicon/apple-icon-114x114.png">
<link rel="apple-touch-icon" sizes="120x120" href="/resources/themes/gov/images/favicon/apple-icon-120x120.png">
<link rel="apple-touch-icon" sizes="144x144" href="/resources/themes/gov/images/favicon/apple-icon-144x144.png">
<link rel="apple-touch-icon" sizes="152x152" href="/resources/themes/gov/images/favicon/apple-icon-152x152.png">
<link rel="apple-touch-icon" sizes="180x180" href="/resources/themes/gov/images/favicon/apple-icon-180x180.png">
<link rel="apple-touch-icon" href="/resources/themes/gov/images/favicon/apple-icon.png">
<link rel="apple-touch-icon-precomposed" href="/resources/themes/gov/images/favicon/apple-icon.png">
<link rel="icon" type="image/png" sizes="192x192"  href="/resources/themes/gov/images/favicon/android-icon-192x192.png">
<link rel="icon" type="image/png" sizes="32x32" href="/resources/themes/gov/images/favicon/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="96x96" href="/resources/themes/gov/images/favicon/favicon-96x96.png">
<link rel="icon" type="image/png" sizes="16x16" href="/resources/themes/gov/images/favicon/favicon-16x16.png">
<link rel="shortcut icon" href="/favicon.ico" />
<link rel="icon" href="/favicon.ico" type="image/x-icon" />
<meta name="msapplication-TileColor" content="#ffffff">
<meta name="msapplication-TileImage" content="/resources/themes/gov/images/favicon/ms-icon-144x144.png">
<meta name="theme-color" content="#ffffff">

	
	<link rel="canonical" href="https://www.gov.si/" />

	<script src="/resources/themes/gov/javascript/libs/modernizr.js?m=1555668158"></script>
	
	
	<link rel="preload" href="/resources/themes/gov/fonts/Republika/ver1.2/republika-bold-webfont.woff2?v=4" as="font" crossorigin="anonymous" />
	<link rel="preload" href="/resources/themes/gov/fonts/Republika/ver1.2/republika-regular-webfont.woff2?v=4" as="font" crossorigin="anonymous" />
	<link rel="preload" href="/resources/themes/gov/fonts/Icons/GovIcons.woff?v=5" as="font" crossorigin="anonymous" />

	
		<link rel="stylesheet" href="/resources/themes/gov/css/style.css?m=1614590762" media="(min-width: 2px)"/>
		<link rel="stylesheet" href="/resources/themes/gov/css/print.css?m=1552647259"/>
	

	<!--[if lt IE 9]>
		<link rel="stylesheet" href="/resources/themes/gov/css/style-ie.css?m=1614590762">
	<![endif]-->
	
	
<script type="text/javascript">
	var _paq = window._paq || [];

	_paq.push(['trackPageView']);
	_paq.push(['enableLinkTracking']);

	(function() {
		var u="//www.gov.si/analitika/";
		_paq.push(['setTrackerUrl', u + 'matomo.php']);
		_paq.push(['setSiteId', '1']);
		var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
		g.type='text/javascript'; g.async=true; g.defer=true; g.src=u+'matomo.js'; s.parentNode.insertBefore(g,s);
	}) ();
</script>
	
</head>



<body class="HomePage">




<div id="wrapper">
	<header class="header">
	
	
	<div class="adapt">
		
		<a class="skip-to-content" href="/#content"
		   aria-label="Skoči do osrednje vsebine"
		   data-string-open="Skoči do osrednje vsebine"><span class="skip-to-content-hide">Skoči do osrednje vsebine</span></a>
		<a aria-label="Na vstopno stran" href="/" class="brand sl_SI" rel="home">
			<h1>
				
				
				
				
				<img src="/resources/themes/gov/images/RS_gov_si-logo.gif"
					 srcset="
						 /resources/themes/gov/images/svg2png/RS_gov_si-logo.png 1x,
						 /resources/themes/gov/images/svg2png/RS_gov_si-logo2x.png 2x,
						 /resources/themes/gov/images/svg2png/RS_gov_si-logo4x.png 3x"
					 class="logo" alt="GOV.SI">
				
				

				
				
				
				
				
				
				
				<span aria-hidden="true" class="visuallyhidden">GOV.SI</span>
			</h1>
		</a>

		<nav class="navigation">
	<button class="navi-btn open-search search-btn search-btn-mobile ficon-search" data-disclosure aria-controls="search-popup" aria-expanded="false" aria-label="Iskalnik"><span class="visuallyhidden">Išči</span></button>
	<button class="navi-btn open-navigation"
			aria-label="Odpri meni z navigacijo"
			data-string-close="Zapri navigacijo"
			data-string-open="Odpri navigacijo"><span class="visuallyhidden">Odpri navigacijo</span></button>
	<div class="inner">
		<button aria-label="Zapri meni z navigacijo" type="button" class="close-navigation-btn close-popup-btn close-navigation"><span class="visuallyhidden">Zapri menu</span></button>
		<div class="menus">
			
			
				<ul class="primary">
					
						<li class="link">
							<a href="/podrocja/">Področja</a>
						</li>
					
						<li class="link">
							<a href="/drzavni-organi/">Državni organi</a>
						</li>
					
						<li class="link">
							<a href="/zbirke/">Zbirke</a>
						</li>
					
						<li class="link">
							<a href="/dogodki/">Dogodki</a>
						</li>
					
						<li class="link">
							<a href="/novice/">Novice</a>
						</li>
					
				</ul>
			

			
			
				<ul class="support">
					
						
							<li class="link">
								<a href="/sodelujte/">Sodelujte</a>
							</li>
						
					
						
							<li class="link">
								<a href="/dostopnost/">Dostopnost</a>
							</li>
						
					
						
							<li class="link">
								<a href="/o-spletiscu/">O spletišču</a>
							</li>
						
					
				</ul>
			
			
			
		</div>

		
			<button class="open-search btn-default search-btn search-btn-desktop search" data-disclosure aria-controls="search-popup" aria-expanded="false" aria-label="Iskalnik"><i class="ficon-search"></i><span>Išči</span></button>
		

		<ul class="support-links">
			<li class="lang-menu">
				<button aria-label="Odpri izbirnik za jezik" data-disclosure aria-controls="language-popup" aria-expanded="false" class="open-language open-language-btn"><i class="ficon-translate"> </i><span>Slovenščina</span></button>
			</li>
			<li class="language-select-dd">
				
				
<label for="language-select" class="visuallyhidden">Izberite jezik</label>
<select id="language-select" name="language-select" aria-label="Izberite jezik">
	
	<option value="/en/" lang="en">English</option>
	
	<option value="/" selected lang="sl">Slovenščina</option>
	
	
	<optgroup label="  ----  ">
		
		<option value="/hu/" lang="hu">Magyar</option>
		
		<option value="/it/" lang="it">Italiano</option>
		
	</optgroup>
</select>




				
			</li>
			
		</ul>
	</div>

</nav>



	</div>
</header>





	<main id="content" class="main">
		<article class="homepage topic-page">
	<div class="home-page-head adapt v-adapt">
		<div class="cols">
			<div class="col left grid-col-6 adapt v-adapt">
				<h1>Portal GOV.SI</h1>
				<p>Spletišče državne uprave s celovitimi informacijami o njenem delovanju in preprostim dostopom do storitev.</p>
			</div>
			
			
			
			<div class="col right">
				<ul class="exposed-links adapt v-adapt">
					
					<li>
						
						<a href="/drzavni-organi/vlada/" class="link SiteTree">
							<span>Informacije o delu vlade</span><i class="icon"></i>
						</a>
						
					</li>
					
					<li>
						
						<a href="/zbirke/delovna-mesta/" class="link SiteTree">
							<span>Prosta delovna mesta v državni upravi</span><i class="icon"></i>
						</a>
						
					</li>
					
					<li>
						
						<a href="/drzave/" class="link SiteTree">
							<span>Informacije za popotnike</span><i class="icon"></i>
						</a>
						
					</li>
					
					<li>
						
						<a href="/teme/drzavni-prazniki-in-dela-prosti-dnevi/" class="link SiteTree">
							<span>Državni prazniki</span><i class="icon"></i>
						</a>
						
					</li>
					
					<li>
						
						<a href="/zbirke/javne-objave/" class="link SiteTree">
							<span>Javni razpisi</span><i class="icon"></i>
						</a>
						
					</li>
					
				</ul>
			</div>
			
			
		</div>
	</div>
	
	

	<div class="notifications top-adapt">
		
			<section class="notification alert">
				<div class="adapt">
					<div class="inner">
						<div class="notif-wrap">
							<div class="notif-icon">
								<i class="icon ficon-notification-alert" aria-hidden="true"	aria-label="Opozorilo"></i>
							</div>
							<div class="notif-text">
								<h2>Koronavirus (SARS-CoV-2)</h2>
								<p><a href="/teme/koronavirus-sars-cov-2/">Aktualne informacije in navodila najdete <b>na strani Koronavirus (SARS-CoV-2)</b></a>.</p><p><a href="/teme/koronavirus-sars-cov-2/cepljenje-proti-covid-19/"><strong>Se želite cepiti proti covid-19? Prijavite se!</strong></a></p><p><a href="/teme/koronavirus-sars-cov-2/mobilna-aplikacija-ostanizdrav/"><b>Na pametne telefone si namestimo aplikacijo #OstaniZdrav</b>, ki nam sporoči, ali smo bili v stiku z okuženo osebo.</a></p><p>Nosimo zaščitno masko, redno si umivajmo in razkužujmo roke, poskrbimo za pravilno higieno kašlja ter ohranimo medosebno razdaljo dveh metrov.</p>
							</div>
						</div>
					</div>
				</div>
			</section>
		
			<section class="notification highlight">
				<div class="adapt">
					<div class="inner">
						<div class="notif-wrap">
							<div class="notif-icon">
								<i class="icon ficon-notification-highlight" aria-hidden="true"	aria-label="Izpostavitev"></i>
							</div>
							<div class="notif-text">
								<h2>30 let - Slovenija država</h2>
								<p><a href="/zbirke/projekti-in-programi/30-let-samostojnosti-slovenije/">Ponosni na Slovenijo izpostavljamo prelomne dogodke, ki so omogočili izvedbo prvih demokratičnih volitev in osamosvojitev Slovenije. Aktualne informacije o obeleževanju 30. obletnice naše države najdete <strong>na strani 30 let samostojnosti Slovenije</strong>.</a></p>
							</div>
						</div>
					</div>
				</div>
			</section>
		
	</div>





	<div class="adapt top-adapt">
		<h2 aria-label="Seznam področij" class="visuallyhidden">Seznam področij</h2>
		
			
	<nav class="subtopic-navigation">
		<ul>
			
				<li>
					<a href="/podrocja/druzina-otroci-in-zakonska-zveza/">
						
							<h3>Družina, otroci in zakonska zveza</h3>
						
						<p>Rojstvo, starševstvo, rejništvo, skrbništvo, posvojitev, prejemki družine, preprečevanje nasilja v družini, zakonska in partnerska zveza</p>
						
					</a>
				</li>
			
				<li>
					<a href="/podrocja/zaposlovanje-delo-in-upokojitev/">
						
							<h3>Zaposlovanje, delo in upokojitev</h3>
						
						<p>Delovna razmerja, trg dela, pravice delavcev, prost pretok delovne sile, poklicni standardi, zavarovanje za primer brezposelnosti, izobraževanje odraslih</p>
						
					</a>
				</li>
			
				<li>
					<a href="/podrocja/kmetijstvo-gozdarstvo-in-prehrana/">
						
							<h3>Kmetijstvo, gozdarstvo in hrana</h3>
						
						<p>Razvoj podeželja, lovstvo, ribištvo, označevanje in zaščita pridelkov in živil, sheme kakovosti, promocija lokalne hrane, veterinarstvo, varstvo rastlin</p>
						
					</a>
				</li>
			
				<li>
					<a href="/podrocja/socialna-varnost/">
						
							<h3>Socialna varnost </h3>
						
						<p>Socialna pravičnost, socialno varstvo, spodbujanje enakih možnosti, solidarnost, preprečevanje socialne izključenosti, izboljšanje položaja socialno šibkejših</p>
						
					</a>
				</li>
			
				<li>
					<a href="/podrocja/drzava-in-druzba/">
						
							<h3>Država in družba</h3>
						
						<p>Državljanstvo, dokumenti, registri, volitve, referendumi, lokalna samouprava, regionalni razvoj, javni sektor, človekove pravice, informacijska družba, priseljevanje</p>
						
					</a>
				</li>
			
				<li>
					<a href="/podrocja/pravna-drzava-in-pravosodje/">
						
							<h3>Pravna država in pravosodje</h3>
						
						<p>Pravni red, izvrševanje kazenskih sankcij, poprava krivic žrtvam kaznivih dejanj, varstvo integritete, varstvo osebnih podatkov, alternativno reševanje sporov</p>
						
					</a>
				</li>
			
				<li>
					<a href="/podrocja/promet-in-energetika/">
						
							<h3>Promet in energetika</h3>
						
						<p>Cestni, železniški, letalski, pomorski promet, infrastruktura, žičniške naprave za prevoz oseb, potniški promet, oskrba z energijo, obnovljivi viri energije, energetska učinkovitost, naftni derivati</p>
						
					</a>
				</li>
			
				<li>
					<a href="/podrocja/izobrazevanje-znanost-in-sport/">
						
							<h3>Izobraževanje, znanost in šport</h3>
						
						<p>Predšolska vzgoja, osnovna, srednja in višja šola, univerza, izobraževanje otrok s posebnimi potrebami, izobraževanje odraslih, študijske izmenjave, štipendije</p>
						
					</a>
				</li>
			
				<li>
					<a href="/podrocja/kultura/">
						
							<h3>Kultura</h3>
						
						<p>Kultura, umetnost, ohranjanje in varstvo kulturne dediščine, urejanje medijskega prostora, jezikovna politika, ljubiteljska kultura</p>
						
					</a>
				</li>
			
				<li>
					<a href="/podrocja/zdravje/">
						
							<h3>Zdravje</h3>
						
						<p>Javno zdravstvo, skrb za zdravje, pravice pacientov, zdravstveno varstvo, dolgotrajna oskrba, zdravila in medicinski pripomočki, skrajševanje čakalnih vrst</p>
						
					</a>
				</li>
			
				<li>
					<a href="/podrocja/finance-in-davki/">
						
							<h3>Finance in davki</h3>
						
						<p>Državni proračun, finančni sistem, davki, carine, druge dajatve, finančni sistem, javno premoženje, javno naročanje, javna plačila, zakladništvo, državne pomoči, sredstva EU</p>
						
					</a>
				</li>
			
				<li>
					<a href="/podrocja/podjetnistvo-in-gospodarstvo/">
						
							<h3>Podjetništvo in gospodarstvo</h3>
						
						<p>Podjetništvo, mednarodno gospodarsko sodelovanje, turizem, varstvo potrošnikov, varstvo konkurence, meroslovje, intelektualna lastnina<br />
</p>
						
					</a>
				</li>
			
				<li>
					<a href="/podrocja/okolje-in-prostor/">
						
							<h3>Okolje in prostor</h3>
						
						<p>Narava, biotska raznovrstnost, naravni parki in rezervati, podnebne spremembe, hrup, onesnaženje, urbani razvoj in zemljiška politika, nepremičnine<br />
</p>
						
					</a>
				</li>
			
				<li>
					<a href="/podrocja/obramba-varnost-in-javni-red/">
						
							<h3>Obramba, varnost in javni red</h3>
						
						<p>Vojska, obveščevalno varnostna dejavnost, informacijska in kibernetska varnost, varstvo pred naravnimi in drugimi nesrečami, sistem obveščanja, civilna zaščita, gasilstvo</p>
						
					</a>
				</li>
			
				<li>
					<a href="/podrocja/zunanje-zadeve/">
						
							<h3>Zunanje zadeve</h3>
						
						<p>Zunanja politika, mednarodne organizacije,  mednarodne pogodbe, arbitražni sporazum, nasledstvo SFRJ, razvojna in humanitarna pomoč, informacije za popotnike</p>
						
					</a>
				</li>
			
		</ul>
	</nav>

		
	</div>

	<div class="adapt article">
		<div class="cols article-cols">
			<div class="content col left grid-col-8 elements">
				

			</div>

			<div class="content-sidebar col right grid-col-4 elements">
				

			</div>
			
			<div class="content-footer col grid-col-12 elements no-adapt">
				
    
       <div class="teasers-grid-element__teaser teasers-grid-module" id="e78394">
	<div class="top-adapt">
		<div class="inner">
			
			
			<ul class="teasers-grid no-title-margin">
				
				
				<li class="one-teaser-grid">
					<a href="https://play.google.com/store/apps/details?id=si.gov.ostanizdrav" aria-hidden="true" tabindex="-1">
					<span class="image">
						
							<img src="/assets/vlada/Koronavirus-zbirno-infografike-vlada/APP-OstaniZdrav/OstaniZdrav__FillWzQ0MCwyOTIsImE0MWM0MTc0OGUiXQ.png" alt="Prenos mobilne aplikacije #OstaniZdrav iz trgovine Google Play">
						
					</span>
					</a>
					
					<h3><a href="https://play.google.com/store/apps/details?id=si.gov.ostanizdrav">Mobilna aplikacija #OstaniZdrav</a>
					</h3>
					<p>Naložimo si aplikacijo za varovanje zdravja na pametne telefone.</p>
					
				</li>
				
			</ul>
		</div>
	</div>
</div>
    
       <div class="teasers-grid-element__teaser teasers-grid-module" id="e25621">
	<div class="top-adapt">
		<div class="inner">
			
			<h2 class="element-title">Storitveni portali</h2>
			
			
			<ul class="teasers-grid">
				
				
				<li>
					<a href="https://e-uprava.gov.si/" aria-hidden="true" tabindex="-1">
					<span class="image">
						
							<img src="/assets/vladne-sluzbe/UKOM/gov.si/Fotografije/spletisca/E-uprava-GettyImages-992747452-hocus-focus__FillWzQ0MCwyOTIsIjhiMTU0Zjk1MTUiXQ.jpg" alt="Portal eUprava">
						
					</span>
					</a>
					
					<h3><a href="https://e-uprava.gov.si/">eUprava </a>
					</h3>
					<p>Državni portal za različne storitve, ki jih lahko kot državljani opravite pri državnih organih ali organih javne uprave.</p>
					
				</li>
				
				
				<li>
					<a href="https://spot.gov.si/" aria-hidden="true" tabindex="-1">
					<span class="image">
						
							<img src="/assets/vladne-sluzbe/UKOM/gov.si/Fotografije/spletisca/spot__FillWzQ0MCwyOTIsIjc0MTVlNTBmZTEiXQ.jpg" alt="Portal SPOT - Slovenska poslovna točka">
						
					</span>
					</a>
					
					<h3><a href="https://spot.gov.si/">SPOT - Slovenska poslovna točka</a>
					</h3>
					<p>Državni portal za podjetja in podjetnike, namenjen preprostemu, hitremu in brezplačnemu poslovanju z javno upravo.</p>
					
				</li>
				
				
				<li>
					<a href="https://edavki.durs.si/" aria-hidden="true" tabindex="-1">
					<span class="image">
						
							<img src="/assets/vladne-sluzbe/UKOM/gov.si/Fotografije/spletisca/edavki-mobilni__FillWzQ0MCwyOTIsImJlZjFhZDMzMjciXQ.jpg" alt="Portal eDavki">
						
					</span>
					</a>
					
					<h3><a href="https://edavki.durs.si/">eDavki</a>
					</h3>
					<p>Državni portal, ki omogoča udobno, preprosto in varno izpolnjevanje ter oddajanje davčnih obrazcev.</p>
					
				</li>
				
			</ul>
		</div>
	</div>
</div>
    
       <div class="teasers-grid-element__teaser teasers-grid-module" id="e15256">
	<div class="top-adapt">
		<div class="inner">
			
			<h2 class="element-title">Sodelujte</h2>
			
			
			<ul class="teasers-grid">
				
				
				<li>
					<a href="https://predlagam.vladi.si/" aria-hidden="true" tabindex="-1">
					<span class="image">
						
							<img src="/assets/vladne-sluzbe/UKOM/gov.si/Fotografije/sodeluj/2cd0df73d1/GettyImages-647657344-xxmmxx__FillWzQ0MCwyOTIsIjJjZDBkZjczZDEiXQ.jpg" alt="Povezava na predlagam.vladi.si">
						
					</span>
					</a>
					
					<h3><a href="https://predlagam.vladi.si/">Predlagam.vladi.si</a>
					</h3>
					<p>Pošljite svoj predlog za ureditev vsebine v pristojnosti vlade, ki je po vašem mnenju neustrezno urejena.</p>
					
				</li>
				
				
				<li>
					<a href="http://www.stopbirokraciji.si/" aria-hidden="true" tabindex="-1">
					<span class="image">
						
							<img src="/assets/vladne-sluzbe/UKOM/gov.si/Fotografije/sodeluj/a52572c516/GettyImages-166000471-republica__FillWzQ0MCwyOTIsImE1MjU3MmM1MTYiXQ.jpg" alt="Povezava na spletno mesto Stop birokraciji">
						
					</span>
					</a>
					
					<h3><a href="http://www.stopbirokraciji.si/">Stop birokraciji</a>
					</h3>
					<p>Opišite svojo izkušnjo nedopustne birokratske prakse ter tako prispevajte k enostavnejšim, preglednejšim in hitrejšim postopkom.</p>
					
				</li>
				
				
				<li>
					<a href="https://e-uprava.gov.si/drzava-in-druzba/e-demokracija.html" aria-hidden="true" tabindex="-1">
					<span class="image">
						
							<img src="/assets/vladne-sluzbe/UKOM/gov.si/Fotografije/sodeluj/bc0dfa4ae6/GettyImages-886945776-Astrakan-Images__FillWzQ0MCwyOTIsImJjMGRmYTRhZTYiXQ.jpg" alt="Povezava na portal e-demokracija">
						
					</span>
					</a>
					
					<h3><a href="https://e-uprava.gov.si/drzava-in-druzba/e-demokracija.html">eDemokracija</a>
					</h3>
					<p>Oddajte svoja mnenja in pripombe na predpise v pripravi ter tako vplivajte na končno sistemsko ureditev vsebinskega področja.</p>
					
				</li>
				
				
				<li>
					<a href="/drzavni-organi/vlada/seje-vlade/gradiva-v-obravnavi/" aria-hidden="true" tabindex="-1">
					<span class="image">
						
							<img src="/assets/vladne-sluzbe/UKOM/gov.si/Fotografije/sodeluj/9523f669f7/GettyImages-136722192-kyoshino__FillWzQ0MCwyOTIsIjk1MjNmNjY5ZjciXQ.jpg" alt="Povezava odpre gradiva v obravnavi.">
						
					</span>
					</a>
					
					<h3><a href="/drzavni-organi/vlada/seje-vlade/gradiva-v-obravnavi/">Gradiva v vladni obravnavi</a>
					</h3>
					<p>Spremljajte postopke priprave in sprejemanja vladnih odločitev in preverite upoštevanje pripomb in predlogov civilne javnosti.</p>
					
				</li>
				
			</ul>
		</div>
	</div>
</div>
    


			</div>
		</div>
	</div>


</article>
	</main>
	<div class="adapt">
		<div class="scroll-top-wrapper">
			<button href="#content" class="scroll-top-btn hidden smooth-anchor is-hidden cant-show"><i class="icon ficon-arrow_up"></i><span class="visuallyhidden">Na vrh strani...</span></button>
		</div>
	</div>
	<footer class="footer">
	
	<div class="feedback-block">
		<div class="adapt v-adapt">
			
			<div class="feedback">
			
				<div class="question">
					<p><strong>Pomagajte nam izboljšati spletišče</strong></p>
					<p>Ali vam je ta stran koristila? <a class="trigger" aria-label="Odgovor DA" data-type="yes" href="/#DA">DA</a> <a aria-label="Odgovor NE" class="trigger" data-type="no" href="/#NE">NE</a></p>
				</div>
				
				<div class="form" style="display: none;">

					<form action="/home/feedback" id="feedback-form" method="post">
						<fieldset>
							<legend class="visuallyhidden">Obrazec za odziv</legend>
							<div aria-hidden="true" class="field name hidden">
								<textarea aria-label="Skrivna šifra" aria-hidden="true" name="name"></textarea>
							</div>
							
							<div class="field">
								<label for="feedback-comment">Vaš komentar / utemeljitev</label>
								<textarea aria-label="Vaš komentar / utemeljitev" name="comment" id="feedback-comment"></textarea>
							</div>
							
							<div class="action">
								<input aria-hidden="true" type="hidden" name="type" class="type">
								<input aria-hidden="true" type="hidden" name="url" value="https://www.gov.si/">
								<input aria-label="Pošlji" type="submit" value="Pošlji">
								<button aria-label="Zapri" class="close btn-blank feedback-close" href="#">Zapri</button>
							</div>
						</fieldset>
					</form>
				</div>
				
				<p class="success" style="display: none;">Hvala za vaš odziv.</p>
			</div>
			
		
		</div>
	</div>
	
	<div class="inner">
		<div class="adapt">
			<div class="page-meta-details">
	
	
	
	
	
</div>
			<p class="copyright">&copy; 2021 GOV.SI</p>
		</div>
	
	</div>	
	
</footer>
</div>


<div id="search-popup" class="search-popup" hidden>
	<form action="/iskanje/">
		<fieldset>
			<legend class="visuallyhidden">Iskalnik</legend>
			<div class="field">
				<input type="text" id="search-input" name="q" aria-label="Vnesite iskalni niz" placeholder="Išči">
			</div>
			<div class="action">
				<button type="submit" name="submit" class="submit ficon-search" aria-label="Sprožite iskanje"><span class="visuallyhidden">Išči</span></button>
			</div>
		</fieldset>
	</form>
	<button aria-label="Zapri iskalnik" type="button" class="close-search-btn close-popup-btn close-search "><span class="visuallyhidden">Zapri iskalnik</span></button>
</div>

<div id="language-popup" class="language-popup" hidden>
	
	
<div class="language-select-list">
	<h3 class="sr-only">Izberite jezik</h3>
	<ul class="languages-exposed">
		
		<li>
			<a class="lang-start-tab" href="/en/" rel="alternate" hreflang="en" lang="en">English</a>
		</li>
		
		<li class="selected">
			<a  href="/" rel="alternate" hreflang="sl" lang="sl">Slovenščina</a>
		</li>
		
	</ul>
	<ul class="languages">
		
		<li>
			<a href="/hu/" rel="alternate" hreflang="hu" lang="hu">Magyar</a>
		</li>
		
		<li>
			<a href="/it/" rel="alternate" hreflang="it" lang="it">Italiano</a>
		</li>
		
	</ul>
</div>




	
	<button aria-label="Zapri izbirnik za jezik" type="button" class="close-language-btn close-popup-btn close-language"><span class="visuallyhidden">Zapri izbirnik jezika</span></button>
</div>


<script type="application/javascript" src="/resources/themes/gov/javascript/libs/jquery-3.4.1.min.js?m=1559200532"></script>
<script type="application/javascript" src="/resources/themes/gov/javascript/libs/ligatures.js?m=1552647259"></script>
<script type="application/javascript" src="/resources/themes/gov/javascript/libs/underscore.min.js?m=1552647259"></script>
<script type="application/javascript" src="/resources/themes/gov/javascript/libs/plugins/jquery.advancedtables.v2.1.0.js?m=1552647259"></script>
<script type="application/javascript" src="/resources/themes/gov/javascript/libs/plugins/jquery.fancybox.min.js?m=1555506797"></script>
<script type="application/javascript" src="/resources/themes/gov/javascript/libs/plugins/jquery.fancybox.i18n.js?m=1607330237"></script>
<script type="application/javascript" src="/resources/themes/gov/javascript/libs/plugins/slick.min.js?m=1552647259"></script>
<script type="application/javascript" src="/resources/themes/gov/javascript/libs/plugins/select2-4.1.0-rc0.full.min.js?m=1613372778"></script>
<script type="application/javascript" src="/resources/themes/gov/javascript/functions.min.js?m=1614590762"></script>
</body>
</html>
""")
print(temp.get_links())
