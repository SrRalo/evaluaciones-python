-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema evaluacionesTI
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema evaluacionesTI
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `evaluacionesTI` DEFAULT CHARACTER SET utf8 ;
USE `evaluacionesTI` ;

-- -----------------------------------------------------
-- Table `evaluacionesTI`.`Carreras`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `evaluacionesTI`.`Carreras` (
  `id_carrera` INT NOT NULL,
  `nombre_carrera` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_carrera`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `evaluacionesTI`.`Estudiante`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `evaluacionesTI`.`Estudiante` (
  `id_estudiante` INT NOT NULL,
  `nombre_estudiante` VARCHAR(45) NOT NULL,
  `contacto_estudiante` VARCHAR(45) NOT NULL,
  `id_carrera` INT NOT NULL,
  PRIMARY KEY (`id_estudiante`),
  INDEX `fk_Estudiante_Carreras1_idx` (`id_carrera` ASC) VISIBLE,
  CONSTRAINT `fk_Estudiante_Carreras1`
    FOREIGN KEY (`id_carrera`)
    REFERENCES `evaluacionesTI`.`Carreras` (`id_carrera`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `evaluacionesTI`.`Docentes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `evaluacionesTI`.`Docentes` (
  `id_docente` INT NOT NULL,
  `nombre_docente` VARCHAR(45) NOT NULL,
  `contacto_docente` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_docente`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `evaluacionesTI`.`Evaluacion_Asiganada`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `evaluacionesTI`.`Evaluacion_Asiganada` (
  `id_evaluacion_asignada` INT NOT NULL,
  `tipo_evaluacion` VARCHAR(45) NOT NULL,
  `nombre_evaluacion` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_evaluacion_asignada`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `evaluacionesTI`.`Detalle_EvaEstudiante`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `evaluacionesTI`.`Detalle_EvaEstudiante` (
  `id_evaEstudiante` INT NOT NULL,
  `nota_evaEstudiante` FLOAT NOT NULL,
  `id_estudiante` INT NOT NULL,
  `id_evaluacion_asignada` INT NOT NULL,
  PRIMARY KEY (`id_evaEstudiante`),
  INDEX `fk_Detalle_EvaEstudiante_Estudiante_idx` (`id_estudiante` ASC) VISIBLE,
  INDEX `fk_Detalle_EvaEstudiante_Evaluacion_Asiganada1_idx` (`id_evaluacion_asignada` ASC) VISIBLE,
  CONSTRAINT `fk_Detalle_EvaEstudiante_Estudiante`
    FOREIGN KEY (`id_estudiante`)
    REFERENCES `evaluacionesTI`.`Estudiante` (`id_estudiante`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Detalle_EvaEstudiante_Evaluacion_Asiganada1`
    FOREIGN KEY (`id_evaluacion_asignada`)
    REFERENCES `evaluacionesTI`.`Evaluacion_Asiganada` (`id_evaluacion_asignada`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `evaluacionesTI`.`Detalle_EvaDocente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `evaluacionesTI`.`Detalle_EvaDocente` (
  `id_evaDocente` INT NOT NULL,
  `nota_evaDocente` FLOAT NOT NULL,
  `id_docente` INT NOT NULL,
  `id_evaluacion_asignada` INT NOT NULL,
  PRIMARY KEY (`id_evaDocente`),
  INDEX `fk_Detalle_EvaDocente_Docentes1_idx` (`id_docente` ASC) VISIBLE,
  INDEX `fk_Detalle_EvaDocente_Evaluacion_Asiganada1_idx` (`id_evaluacion_asignada` ASC) VISIBLE,
  CONSTRAINT `fk_Detalle_EvaDocente_Docentes1`
    FOREIGN KEY (`id_docente`)
    REFERENCES `evaluacionesTI`.`Docentes` (`id_docente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Detalle_EvaDocente_Evaluacion_Asiganada1`
    FOREIGN KEY (`id_evaluacion_asignada`)
    REFERENCES `evaluacionesTI`.`Evaluacion_Asiganada` (`id_evaluacion_asignada`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `evaluacionesTI`.`Usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `evaluacionesTI`.`Usuarios` (
  `username` VARCHAR(10) NOT NULL,
  `password` VARCHAR(10) NOT NULL,
  `user_role` VARCHAR(45) NOT NULL)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
