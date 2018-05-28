-- -----------------------------------------------------
-- Schema worldcup_2018
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `worldcup_2018` ;

-- -----------------------------------------------------
-- Schema worldcup_2018
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `worldcup_2018` DEFAULT CHARACTER SET utf8 ;
USE `worldcup_2018` ;

-- ------------------------------------------------------
-- Drop chain.
-- ------------------------------------------------------
DROP TABLE IF EXISTS `worldcup_2018`.`worldcup` ;
DROP TABLE IF EXISTS `worldcup_2018`.`predictions` ;
DROP TABLE IF EXISTS `worldcup_2018`.`matches` ;
DROP TABLE IF EXISTS `worldcup_2018`.`stages` ;
DROP TABLE IF EXISTS `worldcup_2018`.`stadiums` ;
DROP TABLE IF EXISTS `worldcup_2018`.`users` ;
DROP TABLE IF EXISTS `worldcup_2018`.`teams` ;

-- -----------------------------------------------------
-- Table `worldcup_2018`.`stadiums`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `worldcup_2018`.`stadiums` ;

CREATE TABLE IF NOT EXISTS `worldcup_2018`.`stadiums` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `lat` DOUBLE NULL,
  `lng` DOUBLE NULL,
  `name` VARCHAR(255) NOT NULL,
  `city` VARCHAR(255) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `worldcup_2018`.`teams`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `worldcup_2018`.`teams` ;

CREATE TABLE IF NOT EXISTS `worldcup_2018`.`teams` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `iso2` VARCHAR(45) NULL,
  `flag_url` VARCHAR(255) NULL,
  `eliminated` TINYINT(1) NULL DEFAULT 0,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `worldcup_2018`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `worldcup_2018`.`users` ;

CREATE TABLE IF NOT EXISTS `worldcup_2018`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(255) NOT NULL,
  `name` VARCHAR(255) NULL,
  `entity` VARCHAR(255) NULL,
  `picture_url` VARCHAR(255) NULL,
  `worldcup_winner` INT NULL,
  `points` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  INDEX `fk_users_teams_idx` (`worldcup_winner` ASC),
  CONSTRAINT `fk_users_teams`
    FOREIGN KEY (`worldcup_winner`)
    REFERENCES `worldcup_2018`.`teams` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `worldcup_2018`.`stages`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `worldcup_2018`.`stages` ;

CREATE TABLE IF NOT EXISTS `worldcup_2018`.`stages` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `opening_time` TIMESTAMP NOT NULL,
  `closing_time` TIMESTAMP NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `worldcup_2018`.`matches`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `worldcup_2018`.`matches` ;

CREATE TABLE IF NOT EXISTS `worldcup_2018`.`matches` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `stages_id` INT NOT NULL,
  `match_time` TIMESTAMP NULL,
  `team_1` INT NULL,
  `team_2` INT NULL,
  `placeholder_1` VARCHAR(255) NULL,
  `placeholder_2` VARCHAR(255) NULL,
  `stadiums_id` INT NOT NULL,
  `score` VARCHAR(45) NULL,
  `winner` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_matches_stages1_idx` (`stages_id` ASC),
  INDEX `fk_matches_stadiums1_idx` (`stadiums_id` ASC),
  INDEX `fk_matches_teams1_idx` (`winner` ASC),
  INDEX `fk_matches_teams2_idx` (`team_1` ASC),
  INDEX `fk_matches_teams3_idx` (`team_2` ASC),
  CONSTRAINT `fk_matches_stages1`
    FOREIGN KEY (`stages_id`)
    REFERENCES `worldcup_2018`.`stages` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_matches_stadiums1`
    FOREIGN KEY (`stadiums_id`)
    REFERENCES `worldcup_2018`.`stadiums` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_matches_winner`
    FOREIGN KEY (`winner`)
    REFERENCES `worldcup_2018`.`teams` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_matches_team1`
    FOREIGN KEY (`team_1`)
    REFERENCES `worldcup_2018`.`teams` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_matches_team2`
    FOREIGN KEY (`team_2`)
    REFERENCES `worldcup_2018`.`teams` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `worldcup_2018`.`predictions`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `worldcup_2018`.`predictions` ;

CREATE TABLE IF NOT EXISTS `worldcup_2018`.`predictions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `matches_id` INT NOT NULL,
  `score` VARCHAR(45) NULL,
  `winner` INT NULL,
  `users_id` INT NOT NULL,
  PRIMARY KEY (`id`, `users_id`),
  INDEX `fk_predictions_matches1_idx` (`matches_id` ASC),
  INDEX `fk_predictions_teams1_idx` (`winner` ASC),
  INDEX `fk_predictions_users1_idx` (`users_id` ASC),
  CONSTRAINT `fk_predictions_matches1`
    FOREIGN KEY (`matches_id`)
    REFERENCES `worldcup_2018`.`matches` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_predictions_teams1`
    FOREIGN KEY (`winner`)
    REFERENCES `worldcup_2018`.`teams` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_predictions_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `worldcup_2018`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `worldcup_2018`.`worldcup`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `worldcup_2018`.`worldcup` ;

CREATE TABLE IF NOT EXISTS `worldcup_2018`.`worldcup` (
  `winner` INT NULL,
  `opening_time` TIMESTAMP NULL,
  `closing_time` TIMESTAMP NULL,
  INDEX `fk_worldcup_teams1_idx` (`winner` ASC),
  CONSTRAINT `fk_worldcup_teams1`
    FOREIGN KEY (`winner`)
    REFERENCES `worldcup_2018`.`teams` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
