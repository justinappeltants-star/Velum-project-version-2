L'histoire de la cabane secrète

Imagine que tu veux parler avec tes copains sans que personne d'autre ne puisse écouter, même pas le facteur qui porte tes lettres.

La clé magique : tu inventes une clé secrète, très très longue, avec plein de lettres et de chiffres. Personne ne peut la deviner, même en essayant pendant des millions d'années.
Le cadenas : avant d'envoyer un message, ton ordinateur le met dans une boîte fermée avec un cadenas. Le message devient un charabia du genre « x8Kp2!qZ… ».
Le facteur aveugle : notre serveur est comme un facteur qui ne sait pas lire et n'a jamais la clé. Il prend les boîtes fermées et les distribue aux copains de la cabane, sans savoir ce qu'il y a dedans.
Le déchiffrage : tes copains ont la même clé. Leur ordinateur ouvre la boîte, et le message redevient lisible, seulement chez eux.
La cabane qui disparaît : tu choisis combien de temps la cabane existe (15 minutes, 1 heure, 7 jours…). Quand le temps est fini, pouf ! elle disparaît avec tous les messages. Si personne ne parle pendant 5 minutes (quand tu coches cette option), elle disparaît aussi.
Comment j'ai construit le projet, de A à Z

A. L'idée. Une messagerie sans compte, sans mémoire, où personne ne peut lire les messages, pas même celui qui héberge le site.

B. Le plan. Il faut deux morceaux :

Le visage (index.html) : la page que les gens voient, avec les boutons, l'explication et le chat. C'est aussi là que se fait le chiffrement.
Le cerveau (server.py, en Python) : il crée les salons, passe les messages chiffrés et détruit les salons quand le temps est fini.

C. La clé. Quand quelqu'un crée un salon, son navigateur fabrique 32 octets au hasard. Ça donne le code de 43 caractères. Cette clé reste dans le navigateur et n'est jamais envoyée au serveur.

D. L'adresse du salon. Le serveur doit quand même reconnaître le salon. On lui donne donc une empreinte du code (SHA-256), comme une empreinte de doigt : elle identifie la clé mais ne permet pas de la retrouver.

E. Le chiffrement. Chaque message est chiffré avec AES-256-GCM, un cadenas ultra solide. Chaque message a un numéro unique (l'IV), donc deux messages identiques ne donnent jamais le même charabia. Le mode GCM ajoute un sceau anti-triche : si quelqu'un modifie la boîte, elle refuse de s'ouvrir.

F. Le tuyau direct. Les messages voyagent par WebSocket, un tuyau toujours ouvert entre le navigateur et le serveur. C'est ce qui rend le chat instantané.

G. Le minuteur. Le serveur vérifie toutes les 2 secondes si un salon a dépassé son temps (15 min à 7 jours) ou s'il est resté 5 minutes sans message, quand l'option est cochée. Si oui, il le supprime et prévient tout le monde.

H. Les protections. J'ai ajouté des limites : 20 messages par 10 secondes, 50 personnes maximum par salon, pas plus de 10 créations par minute et par personne. Il y a aussi des en-têtes de sécurité qui empêchent d'autres sites d'espionner ou d'intégrer Velum.

I. La mise en ligne. On loue un petit serveur, on achète un nom de domaine, on lance le programme, et Caddy ajoute automatiquement le cadenas HTTPS. Ensuite tout le monde peut y accéder.

Ton texte de présentation (environ 2 minutes)

« Bonjour à tous. Je vais vous présenter Velum.

Velum, c'est une messagerie anonyme, éphémère et chiffrée. Pas de compte, pas d'e-mail, pas d'historique.

Comment ça marche ? Cinq idées.

Un : la clé. Quand je crée un salon, mon navigateur génère un code secret de 256 bits. Ce code ne quitte jamais mon appareil. C'est la seule clé d'entrée.

Deux : le cadenas. Chaque message est chiffré avec AES-256-GCM avant de partir. Ce standard est utilisé par les banques et les gouvernements. Trouver la clé par force brute est impossible en pratique. Et si quelqu'un modifie un message, il est automatiquement rejeté.

Trois : le facteur aveugle. Notre serveur ne voit que du charabia. Il transmet les messages sans pouvoir les lire, parce qu'il n'a jamais la clé. On appelle ça le zéro connaissance.

Quatre : le minuteur. À la création, on choisit la durée du salon : de 15 minutes à 7 jours. On peut aussi activer une destruction après 5 minutes d'inactivité.

Cinq : la disparition. Quand le temps est écoulé, le salon est effacé de la mémoire du serveur, et la clé et les messages sont effacés du navigateur. Rien n'est stocké sur disque, donc il n'y a rien à retrouver ni à voler.

Soyons honnêtes sur les limites. Aucun système n'est parfait à 100 %. Si quelqu'un obtient le code, il peut lire le salon. Une capture d'écran reste possible. Et pour cacher son adresse IP, il faut utiliser Tor ou un VPN.

Velum, c'est donc une cabane secrète numérique : une clé, un cadenas, un facteur qui ne sait pas lire, et un minuteur qui détruit tout. Merci ! »

Pour le retenir facilement

Retiens 5 mots dans l'ordre : Clé → Cadenas → Facteur aveugle → Minuteur → Disparition.

Répète-les en imaginant une cabane : tu fabriques une clé, tu fermes le cadenas, le facteur aveugle passe la boîte, le minuteur sonne, la cabane disparaît. Avec cette image, tu peux improviser chaque partie avec tes propres mots.

Questions probables du public
« Le serveur peut-il lire mes messages ? » Non, il n'a jamais la clé.
« Que se passe-t-il si le serveur est piraté ? » Le pirate ne trouve que du charabia et aucune clé. Le serveur n'écrit rien sur disque, et tout ce qui est en mémoire disparaît au redémarrage.
« Peut-on récupérer un salon détruit ? » Non, c'est voulu.
« Est-ce anonyme à 100 % ? » Le contenu est protégé. Pour cacher l'adresse IP, il faut ajouter Tor.
