DROP TABLE IF EXISTS `movies`;

CREATE TABLE `movies` (
  `movie_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `movie_name` varchar(255) NOT NULL DEFAULT '',
  `movie_year` int(4) NOT NULL,
  `movie_rating` varchar(10) NOT NULL DEFAULT '',
  `movie_overview` varchar(255) DEFAULT NULL,
  `movie_img` varchar(200) NOT NULL,
  PRIMARY KEY (`movie_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `movies` WRITE;


INSERT INTO `movies` (`movie_id`, `movie_name`, `movie_year`, `movie_rating`, `movie_overview`, `movie_img`)
VALUES
	(1,'Godzilla VS Kong',2021,'G','In a time when monsters walk the Earth, humanity’s fight for its future sets Godzilla and Kong on a collision course that will see the two most powerful forces of nature on the planet collide in a spectacular battle for the ages.','https://image.tmdb.org/t/p/w1280/pgqgaUx1cJb5oZQQ5v0tNARCeBp.jpg'),
	(2,'RAYA and The Last Dragon',2021,'PG-13','Long ago, in the fantasy world of Kumandra, humans and dragons lived together in harmony. But when an evil force threatened the land, the dragons sacrificed themselves to save humanity. Now, 500 years later, that same evil has returned and it’s up to a lone warrior, Raya, to track down the legendary last dragon to restore the fractured land and its divided people.','https://image.tmdb.org/t/p/w1280/lPsD10PP4rgUGiGR4CCXA6iY0QQ.jpg'),
	(3,'Avengers END-GAME',2020,'PG-13','After the devastating events of Avengers: Infinity War, the universe is in ruins due to the efforts of the Mad Titan, Thanos. With the help of remaining allies, the Avengers must assemble once more in order to undo Thanos" actions and restore order to the universe once and for all, no matter what consequences may be in store.','https://image.tmdb.org/t/p/w1280/or06FN3Dka5tukK1e9sl16pB3iy.jpg'),
	(4,'Spider-Man',2007,'PG','Following the events of Captain America: Civil War, Peter Parker, with the help of his mentor Tony Stark, tries to balance his life as an ordinary high school student in Queens, New York City, with fighting crime as his superhero alter ego Spider-Man as a new threat, the Vulture, emerges.','https://image.tmdb.org/t/p/w1280/c24sv2weTHPsmDa7jEMN0m2P3RT.jpg'),
	(5,'The pursuit of happyness',2006,'R','(A struggling salesman takes custody of his son as hes poised to begin a life-changing professional career.)','https://image.tmdb.org/t/p/w1280/lBYOKAMcxIvuk9s9hMuecB9dPBV.jpg'),
  (6,'The Mitchells vs. The Machines',2021,'G',"A quirky, dysfunctional family's road trip is upended when they find themselves in the middle of the robot apocalypse and suddenly become humanity's unlikeliest last hope.",'https://image.tmdb.org/t/p/w1280/mI2Di7HmskQQ34kz0iau6J1vr70.jpg' ),
  (7,'Parasite',2020,'PG',"All unemployed, Ki-taek's family takes peculiar interest in the wealthy and glamorous Parks for their livelihood until they get entangled in an unexpected incident.",'https://image.tmdb.org/t/p/w1280/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg'),
  (8, 'TENET',2020,'PG',"Armed with only one word - Tenet - and fighting for the survival of the entire world, the Protagonist journeys through a twilight world of international espionage on a mission that will unfold in something beyond real time.",'https://image.tmdb.org/t/p/w1280/k68nPLbIST6NP96JmTxmZijEvCA.jpg');


UNLOCK TABLES;


DROP TABLE IF EXISTS `reviews`;

CREATE TABLE `reviews` (
  `review_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `review_movie_id` int(11) unsigned NOT NULL,
  `review_rating` int(11) NOT NULL,
  `review_description` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`review_id`),
  KEY `movies_foreign_key` (`review_movie_id`),
  CONSTRAINT `movies_foreign_key` FOREIGN KEY (`review_movie_id`) REFERENCES `movies` (`movie_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `reviews` WRITE;


INSERT INTO `reviews` (`review_id`, `review_movie_id`, `review_rating`, `review_description`)
VALUES
	(1,5,5,'This is one of my favorite movies of all time!'),
  (2,1,4,'Despite the cast putting their best efforts into their respective roles, there are hardly any emotionally impactful elements in the film. Some of the characters are merely filler, having little to no consequence. The roles played by Eiza González, Demián Bichir and Kyle Chandler come to mind. The most compelling angle is the bond between Jia and Kong, but it does not have much room for exploration before the next action sequence. Despite its shortcomings, ‘Godzilla vs. Kong’ is exactly as advertised. It certainly delivers on its promise as a massive monster clash, and adrenaline-driven movie lovers will be visually rewarded for catching this spectacle in cinemas.'),
  (3,8,3,'Just like most Nolan films, this one too demands full attention from its viewer, yet there is no guarantee you will comprehend the film’s nuanced narrative in its totality. But that doesn’t take away from enjoying the cinematic experience of Nolan’s vivid imagination that is skillfully portrayed on the big screen. The secret to enjoy ‘Tenet’ lies in what a scientist, who is explaining inversion tells the Protagonist, "Dont try to understand, feel it."');

UNLOCK TABLES;

DROP TABLE IF EXISTS `feedback`;

CREATE TABLE `feedback` (
  `feedback_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `feedback_pname` text(11) NOT NULL,
  `feedback_pemail` varchar(20) NOT NULL,
  `feedback_pmessage` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`feedback_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `feedback` WRITE;

INSERT INTO `feedback` (`feedback_id`, `feedback_pname`, `feedback_pemail`, `feedback_pmessage`)
VALUES
	(1,'taran','taran@gmail.com','This website is useful to check movie reviews and also to write reviews by this site i knowed a lot!'),
  (2,'ronny','ronny@abc.com','superb content!');

UNLOCK TABLES;

