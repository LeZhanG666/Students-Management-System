/*
SQLyog Ultimate v12.09 (64 bit)
MySQL - 8.0.33 : Database - sms
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`sms` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `sms`;

/*Table structure for table `exams` */

CREATE TABLE `exams` (
  `exam_id` int NOT NULL AUTO_INCREMENT,
  `exam_name` varchar(100) NOT NULL,
  `exam_date` date NOT NULL,
  PRIMARY KEY (`exam_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `exams` */

/*Table structure for table `examsubjects` */

CREATE TABLE `examsubjects` (
  `exam_subject_id` int NOT NULL AUTO_INCREMENT,
  `exam_id` int NOT NULL,
  `subject_id` int NOT NULL,
  PRIMARY KEY (`exam_subject_id`),
  KEY `exam_id` (`exam_id`),
  KEY `subject_id` (`subject_id`),
  CONSTRAINT `examsubjects_ibfk_1` FOREIGN KEY (`exam_id`) REFERENCES `exams` (`exam_id`),
  CONSTRAINT `examsubjects_ibfk_2` FOREIGN KEY (`subject_id`) REFERENCES `subjects` (`subject_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `examsubjects` */

/*Table structure for table `notices` */

CREATE TABLE `notices` (
  `notice_id` int NOT NULL AUTO_INCREMENT,
  `content` text NOT NULL,
  `created_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`notice_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `notices` */

/*Table structure for table `scores` */

CREATE TABLE `scores` (
  `score_id` int NOT NULL AUTO_INCREMENT,
  `student_id` varchar(20) NOT NULL,
  `exam_id` int NOT NULL,
  `total_score` float NOT NULL,
  PRIMARY KEY (`score_id`),
  KEY `student_id` (`student_id`),
  KEY `exam_id` (`exam_id`),
  CONSTRAINT `scores_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`),
  CONSTRAINT `scores_ibfk_2` FOREIGN KEY (`exam_id`) REFERENCES `exams` (`exam_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `scores` */

/*Table structure for table `students` */

CREATE TABLE `students` (
  `student_id` varchar(20) NOT NULL,
  `name` varchar(50) NOT NULL,
  `age` int NOT NULL,
  `gender` enum('男','女') NOT NULL,
  `grade` varchar(10) NOT NULL,
  `major` varchar(100) NOT NULL,
  `class_name` varchar(50) NOT NULL,
  PRIMARY KEY (`student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `students` */

/*Table structure for table `subjects` */

CREATE TABLE `subjects` (
  `subject_id` int NOT NULL AUTO_INCREMENT,
  `subject_name` varchar(100) NOT NULL,
  PRIMARY KEY (`subject_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `subjects` */

/*Table structure for table `subjectscores` */

CREATE TABLE `subjectscores` (
  `subject_score_id` int NOT NULL AUTO_INCREMENT,
  `score_id` int NOT NULL,
  `subject_id` int NOT NULL,
  `score` float NOT NULL,
  PRIMARY KEY (`subject_score_id`),
  KEY `score_id` (`score_id`),
  KEY `subject_id` (`subject_id`),
  CONSTRAINT `subjectscores_ibfk_1` FOREIGN KEY (`score_id`) REFERENCES `scores` (`score_id`),
  CONSTRAINT `subjectscores_ibfk_2` FOREIGN KEY (`subject_id`) REFERENCES `subjects` (`subject_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `subjectscores` */

/*Table structure for table `teachers` */

CREATE TABLE `teachers` (
  `teacher_id` varchar(20) NOT NULL,
  `name` varchar(50) NOT NULL,
  `age` int NOT NULL,
  `gender` enum('男','女') NOT NULL,
  `major` varchar(100) NOT NULL,
  `class_name` varchar(50) NOT NULL,
  `grade` varchar(10) NOT NULL,
  PRIMARY KEY (`teacher_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `teachers` */

/*Table structure for table `users` */

CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `password` varchar(120) NOT NULL,
  `role` enum('student','teacher','admin') NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `users` */

insert  into `users`(`id`,`username`,`password`,`role`) values (1,'admin','admin666','admin');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
