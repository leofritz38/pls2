L'objectif primaire de ce projet est de mesurer l'état de santé de culture d'algue unicellulaire.

Le procesus est le suivant : 
1. mesure de le rETR à 10 intensités lumineuses (E) 
2. prédictions des valeurs de paramètres sur cette séquence 
3. Interprétation des valeurs de paramètres

L'objectif secondaire de ce projet est de créer un environnement de travail facile à adapter aux besoins et aux habitudes de l'utilisateur.
Cela s'exprime par la possibilité d'implémenter de nouveaux modèles, de nouvelles distances qui peuvent prendre en entrée des mesures différentes de E et des paramètres différents.

L'organisation du répertoire est la suivante : 
1. models.py --> Fichier où sont définis les modèles selon la structure type décrite au début du fichier
2. distance.py --> Fichier où sont définis les distances selon la structure type décrite au début du code
3. Optimizer.py --> Ensemble de fonctions qui permettent de générer des paramètres optimisé associée à un modèle par distance
4. data_loading.py --> Fonction permettant d'observer l'évolution des paramètres au cours du temps afin de s'assurer au bon fonctionnement de l'optimisation au cours du temps (uniquement testé avec la distance least_square et Model2)
5. decision_making.py --> Fonction permettant de simuler l'optimisation à partir de paramètres choisi par l'utilisateur et pseudo_prise de décision (pas de données à confronter)
6. interpret_data.py --> Graphique sur les données

Pour l'instant seul les fichiers models, distance et optimizer possèdent des fonctions généralisées