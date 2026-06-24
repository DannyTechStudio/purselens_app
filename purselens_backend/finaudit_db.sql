-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: finaudit_db
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `account_emailaddress`
--

DROP TABLE IF EXISTS `account_emailaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_emailaddress` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(254) NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `primary` tinyint(1) NOT NULL,
  `user_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account_emailaddress_user_id_email_987c8728_uniq` (`user_id`,`email`),
  KEY `account_emailaddress_email_03be32b2` (`email`),
  CONSTRAINT `account_emailaddress_user_id_2c513194_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_emailaddress`
--

LOCK TABLES `account_emailaddress` WRITE;
/*!40000 ALTER TABLE `account_emailaddress` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_emailaddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_emailconfirmation`
--

DROP TABLE IF EXISTS `account_emailconfirmation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_emailconfirmation` (
  `id` int NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `sent` datetime(6) DEFAULT NULL,
  `key` varchar(64) NOT NULL,
  `email_address_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`),
  KEY `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` (`email_address_id`),
  CONSTRAINT `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` FOREIGN KEY (`email_address_id`) REFERENCES `account_emailaddress` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_emailconfirmation`
--

LOCK TABLES `account_emailconfirmation` WRITE;
/*!40000 ALTER TABLE `account_emailconfirmation` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_emailconfirmation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_emailverificationtoken`
--

DROP TABLE IF EXISTS `accounts_emailverificationtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_emailverificationtoken` (
  `id` char(32) NOT NULL,
  `token` varchar(64) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `expires_at` datetime(6) NOT NULL,
  `user_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token` (`token`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `accounts_emailverifi_user_id_4ff4e6c5_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_emailverificationtoken`
--

LOCK TABLES `accounts_emailverificationtoken` WRITE;
/*!40000 ALTER TABLE `accounts_emailverificationtoken` DISABLE KEYS */;
INSERT INTO `accounts_emailverificationtoken` VALUES ('b056c3f3a42e47b2b130ed593cf68128','d3addfbc2944d59e1eace109bc2dcf3d935bbb1bb944d68084953d09376fd37e','2026-05-27 00:46:43.741362','2026-05-27 01:01:43.740869','f47bc50a298042d0bce3ad50f4ee2db9');
/*!40000 ALTER TABLE `accounts_emailverificationtoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_profile`
--

DROP TABLE IF EXISTS `accounts_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_profile` (
  `id` char(32) NOT NULL,
  `profile_picture` varchar(100) DEFAULT NULL,
  `timezone` varchar(50) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `accounts_profile_user_id_49a85d32_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_profile`
--

LOCK TABLES `accounts_profile` WRITE;
/*!40000 ALTER TABLE `accounts_profile` DISABLE KEYS */;
INSERT INTO `accounts_profile` VALUES ('1a39e3d0183b4d0ba4fa4516f769318c','','Africa/Accra','2026-06-15 14:21:14.298398','2026-06-15 14:21:14.298439','fa4215d523ef40a3b91b52d988ba1c68'),('5bc2da8922cc4cb69e4fc5ca888d312e','','Africa/Accra','2026-05-27 22:49:16.053447','2026-05-27 22:49:16.053467','4050c7b3f1e44253bb1d6ba2d97649a3');
/*!40000 ALTER TABLE `accounts_profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user`
--

DROP TABLE IF EXISTS `accounts_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user` (
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `id` char(32) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `is_verified` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user`
--

LOCK TABLES `accounts_user` WRITE;
/*!40000 ALTER TABLE `accounts_user` DISABLE KEYS */;
INSERT INTO `accounts_user` VALUES ('pbkdf2_sha256$1200000$EJiKpxGPkY8pXxcypEV1bA$nuhBOhdg6QxLVfmtdA5mhk/rLh9pKZOH0+FSg9cLiQ8=',NULL,0,0,'2026-05-27 22:49:15.029637','4050c7b3f1e44253bb1d6ba2d97649a3','David','Smith','davidsmith12@example.com',1,'2026-05-27 22:49:16.047177','2026-05-27 22:49:59.489589',1),('pbkdf2_sha256$1200000$DMKJlKY3vHv4vx5n3nwQ6Q$9700ekjk6bajc33aP0XLMWuOc0Sbf7yHWtj3DoV68z8=',NULL,0,0,'2026-06-15 14:21:12.845614','fa4215d523ef40a3b91b52d988ba1c68','James','Boakye','jamesboakye@example.com',1,'2026-06-15 14:21:14.128619','2026-06-15 14:22:04.918455',1);
/*!40000 ALTER TABLE `accounts_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_groups`
--

DROP TABLE IF EXISTS `accounts_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` char(32) NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_groups_user_id_group_id_59c0b32f_uniq` (`user_id`,`group_id`),
  KEY `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` (`group_id`),
  CONSTRAINT `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `accounts_user_groups_user_id_52b62117_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_groups`
--

LOCK TABLES `accounts_user_groups` WRITE;
/*!40000 ALTER TABLE `accounts_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_user_permissions`
--

DROP TABLE IF EXISTS `accounts_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` char(32) NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_user_permi_user_id_permission_id_2ab516c2_uniq` (`user_id`,`permission_id`),
  KEY `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` (`permission_id`),
  CONSTRAINT `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `accounts_user_user_p_user_id_e4f0a161_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_user_permissions`
--

LOCK TABLES `accounts_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `accounts_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_usersettings`
--

DROP TABLE IF EXISTS `accounts_usersettings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_usersettings` (
  `id` char(32) NOT NULL,
  `preferred_language` varchar(10) NOT NULL,
  `preferred_currency` varchar(3) NOT NULL,
  `is_dark_theme` tinyint(1) NOT NULL,
  `allow_email_notifications` tinyint(1) NOT NULL,
  `allow_budget_alerts` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `accounts_usersettings_user_id_3952da55_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_usersettings`
--

LOCK TABLES `accounts_usersettings` WRITE;
/*!40000 ALTER TABLE `accounts_usersettings` DISABLE KEYS */;
INSERT INTO `accounts_usersettings` VALUES ('c17c943f37e14641852ebe85629d422c','en','GHS',0,1,1,'2026-06-15 14:21:14.309311','2026-06-15 14:21:14.309355','fa4215d523ef40a3b91b52d988ba1c68'),('d5efd7bd5e754669b1839c2271083b13','en','GHS',0,1,1,'2026-05-27 22:49:16.056736','2026-05-27 22:49:16.056777','4050c7b3f1e44253bb1d6ba2d97649a3');
/*!40000 ALTER TABLE `accounts_usersettings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_usersocialaccount`
--

DROP TABLE IF EXISTS `accounts_usersocialaccount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_usersocialaccount` (
  `id` char(32) NOT NULL,
  `provider` varchar(20) NOT NULL,
  `provider_user_id` varchar(200) NOT NULL,
  `is_primary` tinyint(1) NOT NULL,
  `email_at_provider_time` varchar(254) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_at_provider_time` (`email_at_provider_time`),
  UNIQUE KEY `accounts_usersocialaccou_provider_provider_user_i_acbd2b68_uniq` (`provider`,`provider_user_id`),
  KEY `accounts_usersocialaccount_user_id_adcfa0b4_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `accounts_usersocialaccount_user_id_adcfa0b4_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_usersocialaccount`
--

LOCK TABLES `accounts_usersocialaccount` WRITE;
/*!40000 ALTER TABLE `accounts_usersocialaccount` DISABLE KEYS */;
INSERT INTO `accounts_usersocialaccount` VALUES ('060a27195d7b4e84b256cb229e0ec363','local','fa4215d5-23ef-40a3-b91b-52d988ba1c68',1,'jamesboakye@example.com','2026-06-15 14:21:14.396183','fa4215d523ef40a3b91b52d988ba1c68');
/*!40000 ALTER TABLE `accounts_usersocialaccount` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `activity_auditlog`
--

DROP TABLE IF EXISTS `activity_auditlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `activity_auditlog` (
  `id` char(32) NOT NULL,
  `action` varchar(20) NOT NULL,
  `target_model` varchar(20) DEFAULT NULL,
  `target_id` char(32) DEFAULT NULL,
  `description` longtext NOT NULL,
  `old_values` json DEFAULT NULL,
  `new_values` json DEFAULT NULL,
  `ip_address` char(39) DEFAULT NULL,
  `user_agent` varchar(300) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` char(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `activity_auditlog_user_id_aff84297` (`user_id`),
  CONSTRAINT `activity_auditlog_user_id_aff84297_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activity_auditlog`
--

LOCK TABLES `activity_auditlog` WRITE;
/*!40000 ALTER TABLE `activity_auditlog` DISABLE KEYS */;
/*!40000 ALTER TABLE `activity_auditlog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=105 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',3,'add_permission'),(6,'Can change permission',3,'change_permission'),(7,'Can delete permission',3,'delete_permission'),(8,'Can view permission',3,'view_permission'),(9,'Can add group',2,'add_group'),(10,'Can change group',2,'change_group'),(11,'Can delete group',2,'delete_group'),(12,'Can view group',2,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add Blacklisted Token',6,'add_blacklistedtoken'),(22,'Can change Blacklisted Token',6,'change_blacklistedtoken'),(23,'Can delete Blacklisted Token',6,'delete_blacklistedtoken'),(24,'Can view Blacklisted Token',6,'view_blacklistedtoken'),(25,'Can add Outstanding Token',7,'add_outstandingtoken'),(26,'Can change Outstanding Token',7,'change_outstandingtoken'),(27,'Can delete Outstanding Token',7,'delete_outstandingtoken'),(28,'Can view Outstanding Token',7,'view_outstandingtoken'),(29,'Can add user',10,'add_user'),(30,'Can change user',10,'change_user'),(31,'Can delete user',10,'delete_user'),(32,'Can view user',10,'view_user'),(33,'Can add email verification token',8,'add_emailverificationtoken'),(34,'Can change email verification token',8,'change_emailverificationtoken'),(35,'Can delete email verification token',8,'delete_emailverificationtoken'),(36,'Can view email verification token',8,'view_emailverificationtoken'),(37,'Can add profile',9,'add_profile'),(38,'Can change profile',9,'change_profile'),(39,'Can delete profile',9,'delete_profile'),(40,'Can view profile',9,'view_profile'),(41,'Can add user settings',11,'add_usersettings'),(42,'Can change user settings',11,'change_usersettings'),(43,'Can delete user settings',11,'delete_usersettings'),(44,'Can view user settings',11,'view_usersettings'),(45,'Can add access attempt',12,'add_accessattempt'),(46,'Can change access attempt',12,'change_accessattempt'),(47,'Can delete access attempt',12,'delete_accessattempt'),(48,'Can view access attempt',12,'view_accessattempt'),(49,'Can add access log',15,'add_accesslog'),(50,'Can change access log',15,'change_accesslog'),(51,'Can delete access log',15,'delete_accesslog'),(52,'Can view access log',15,'view_accesslog'),(53,'Can add access failure',14,'add_accessfailurelog'),(54,'Can change access failure',14,'change_accessfailurelog'),(55,'Can delete access failure',14,'delete_accessfailurelog'),(56,'Can view access failure',14,'view_accessfailurelog'),(57,'Can add access attempt expiration',13,'add_accessattemptexpiration'),(58,'Can change access attempt expiration',13,'change_accessattemptexpiration'),(59,'Can delete access attempt expiration',13,'delete_accessattemptexpiration'),(60,'Can view access attempt expiration',13,'view_accessattemptexpiration'),(61,'Can add audit log',16,'add_auditlog'),(62,'Can change audit log',16,'change_auditlog'),(63,'Can delete audit log',16,'delete_auditlog'),(64,'Can view audit log',16,'view_auditlog'),(65,'Can add user social account',17,'add_usersocialaccount'),(66,'Can change user social account',17,'change_usersocialaccount'),(67,'Can delete user social account',17,'delete_usersocialaccount'),(68,'Can view user social account',17,'view_usersocialaccount'),(69,'Can add site',18,'add_site'),(70,'Can change site',18,'change_site'),(71,'Can delete site',18,'delete_site'),(72,'Can view site',18,'view_site'),(73,'Can add email address',19,'add_emailaddress'),(74,'Can change email address',19,'change_emailaddress'),(75,'Can delete email address',19,'delete_emailaddress'),(76,'Can view email address',19,'view_emailaddress'),(77,'Can add email confirmation',20,'add_emailconfirmation'),(78,'Can change email confirmation',20,'change_emailconfirmation'),(79,'Can delete email confirmation',20,'delete_emailconfirmation'),(80,'Can view email confirmation',20,'view_emailconfirmation'),(81,'Can add social account',21,'add_socialaccount'),(82,'Can change social account',21,'change_socialaccount'),(83,'Can delete social account',21,'delete_socialaccount'),(84,'Can view social account',21,'view_socialaccount'),(85,'Can add social application',22,'add_socialapp'),(86,'Can change social application',22,'change_socialapp'),(87,'Can delete social application',22,'delete_socialapp'),(88,'Can view social application',22,'view_socialapp'),(89,'Can add social application token',23,'add_socialtoken'),(90,'Can change social application token',23,'change_socialtoken'),(91,'Can delete social application token',23,'delete_socialtoken'),(92,'Can view social application token',23,'view_socialtoken'),(93,'Can add category',25,'add_category'),(94,'Can change category',25,'change_category'),(95,'Can delete category',25,'delete_category'),(96,'Can view category',25,'view_category'),(97,'Can add budget',24,'add_budget'),(98,'Can change budget',24,'change_budget'),(99,'Can delete budget',24,'delete_budget'),(100,'Can view budget',24,'view_budget'),(101,'Can add transaction',26,'add_transaction'),(102,'Can change transaction',26,'change_transaction'),(103,'Can delete transaction',26,'delete_transaction'),(104,'Can view transaction',26,'view_transaction');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `axes_accessattempt`
--

DROP TABLE IF EXISTS `axes_accessattempt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `axes_accessattempt` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_agent` varchar(255) NOT NULL,
  `ip_address` char(39) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `http_accept` varchar(1025) NOT NULL,
  `path_info` varchar(255) NOT NULL,
  `attempt_time` datetime(6) NOT NULL,
  `get_data` longtext NOT NULL,
  `post_data` longtext NOT NULL,
  `failures_since_start` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `axes_accessattempt_username_ip_address_user_agent_8ea22282_uniq` (`username`,`ip_address`,`user_agent`),
  KEY `axes_accessattempt_ip_address_10922d9c` (`ip_address`),
  KEY `axes_accessattempt_user_agent_ad89678b` (`user_agent`),
  KEY `axes_accessattempt_username_3f2d4ca0` (`username`),
  CONSTRAINT `axes_accessattempt_chk_1` CHECK ((`failures_since_start` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `axes_accessattempt`
--

LOCK TABLES `axes_accessattempt` WRITE;
/*!40000 ALTER TABLE `axes_accessattempt` DISABLE KEYS */;
INSERT INTO `axes_accessattempt` VALUES (10,'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36','127.0.0.1',NULL,'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','/admin/login/','2026-06-11 16:32:11.347297','next=/admin/socialaccount/socialapp/1/change/','csrfmiddlewaretoken=fo0TFSbeT5UTAtjCNXiCGkuGRyDxy8gG9ELBQh5mxTtdoUWRjPcyidlJchKuzZAP\nusername=********************\npassword=********************\nnext=/admin/socialaccount/socialapp/1/change/',1);
/*!40000 ALTER TABLE `axes_accessattempt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `axes_accessattemptexpiration`
--

DROP TABLE IF EXISTS `axes_accessattemptexpiration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `axes_accessattemptexpiration` (
  `access_attempt_id` int NOT NULL,
  `expires_at` datetime(6) NOT NULL,
  PRIMARY KEY (`access_attempt_id`),
  CONSTRAINT `axes_accessattemptex_access_attempt_id_6b73a47a_fk_axes_acce` FOREIGN KEY (`access_attempt_id`) REFERENCES `axes_accessattempt` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `axes_accessattemptexpiration`
--

LOCK TABLES `axes_accessattemptexpiration` WRITE;
/*!40000 ALTER TABLE `axes_accessattemptexpiration` DISABLE KEYS */;
/*!40000 ALTER TABLE `axes_accessattemptexpiration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `axes_accessfailurelog`
--

DROP TABLE IF EXISTS `axes_accessfailurelog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `axes_accessfailurelog` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_agent` varchar(255) NOT NULL,
  `ip_address` char(39) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `http_accept` varchar(1025) NOT NULL,
  `path_info` varchar(255) NOT NULL,
  `attempt_time` datetime(6) NOT NULL,
  `locked_out` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `axes_accessfailurelog_user_agent_ea145dda` (`user_agent`),
  KEY `axes_accessfailurelog_ip_address_2e9f5a7f` (`ip_address`),
  KEY `axes_accessfailurelog_username_a8b7e8a4` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `axes_accessfailurelog`
--

LOCK TABLES `axes_accessfailurelog` WRITE;
/*!40000 ALTER TABLE `axes_accessfailurelog` DISABLE KEYS */;
/*!40000 ALTER TABLE `axes_accessfailurelog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `axes_accesslog`
--

DROP TABLE IF EXISTS `axes_accesslog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `axes_accesslog` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_agent` varchar(255) NOT NULL,
  `ip_address` char(39) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `http_accept` varchar(1025) NOT NULL,
  `path_info` varchar(255) NOT NULL,
  `attempt_time` datetime(6) NOT NULL,
  `logout_time` datetime(6) DEFAULT NULL,
  `session_hash` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `axes_accesslog_ip_address_86b417e5` (`ip_address`),
  KEY `axes_accesslog_user_agent_0e659004` (`user_agent`),
  KEY `axes_accesslog_username_df93064b` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `axes_accesslog`
--

LOCK TABLES `axes_accesslog` WRITE;
/*!40000 ALTER TABLE `axes_accesslog` DISABLE KEYS */;
INSERT INTO `axes_accesslog` VALUES (1,'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36','127.0.0.1','archimedes301@gmail.com','text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','/admin/login/','2026-05-27 15:20:43.686977','2026-05-27 16:32:39.278010','24406d594c14d41a923653ccc5155cb1589ce5fabd7bca2dab5dfa8b6777b95d'),(2,'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36','127.0.0.1','archimedes301@gmail.com','text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','/accounts/google/login/callback/','2026-05-31 13:55:34.970170',NULL,'d5f99a2ba2eab4efbd40eadbb73af5d67f5ee7ab19111402075892d23e10c065'),(3,'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36','127.0.0.1','archimedes301@gmail.com','text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','/accounts/google/login/callback/','2026-05-31 14:01:26.261193',NULL,'cd7b43e2efb6ec3368951049115f7b5157076c3f8d613f5558481035e2dc2f9f');
/*!40000 ALTER TABLE `axes_accesslog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (19,'account','emailaddress'),(20,'account','emailconfirmation'),(8,'accounts','emailverificationtoken'),(9,'accounts','profile'),(10,'accounts','user'),(11,'accounts','usersettings'),(17,'accounts','usersocialaccount'),(16,'activity','auditlog'),(1,'admin','logentry'),(2,'auth','group'),(3,'auth','permission'),(12,'axes','accessattempt'),(13,'axes','accessattemptexpiration'),(14,'axes','accessfailurelog'),(15,'axes','accesslog'),(4,'contenttypes','contenttype'),(24,'finances','budget'),(25,'finances','category'),(26,'finances','transaction'),(5,'sessions','session'),(18,'sites','site'),(21,'socialaccount','socialaccount'),(22,'socialaccount','socialapp'),(23,'socialaccount','socialtoken'),(6,'token_blacklist','blacklistedtoken'),(7,'token_blacklist','outstandingtoken');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-05-22 23:54:22.051263'),(2,'contenttypes','0002_remove_content_type_name','2026-05-22 23:54:22.246158'),(3,'auth','0001_initial','2026-05-22 23:54:22.647205'),(4,'auth','0002_alter_permission_name_max_length','2026-05-22 23:54:22.732809'),(5,'auth','0003_alter_user_email_max_length','2026-05-22 23:54:22.740292'),(6,'auth','0004_alter_user_username_opts','2026-05-22 23:54:22.749677'),(7,'auth','0005_alter_user_last_login_null','2026-05-22 23:54:22.758161'),(8,'auth','0006_require_contenttypes_0002','2026-05-22 23:54:22.762773'),(9,'auth','0007_alter_validators_add_error_messages','2026-05-22 23:54:22.773194'),(10,'auth','0008_alter_user_username_max_length','2026-05-22 23:54:22.782436'),(11,'auth','0009_alter_user_last_name_max_length','2026-05-22 23:54:22.794411'),(12,'auth','0010_alter_group_name_max_length','2026-05-22 23:54:22.823465'),(13,'auth','0011_update_proxy_permissions','2026-05-22 23:54:22.834352'),(14,'auth','0012_alter_user_first_name_max_length','2026-05-22 23:54:22.852762'),(15,'accounts','0001_initial','2026-05-22 23:54:23.705630'),(16,'admin','0001_initial','2026-05-22 23:54:23.922146'),(17,'admin','0002_logentry_remove_auto_add','2026-05-22 23:54:23.934097'),(18,'admin','0003_logentry_add_action_flag_choices','2026-05-22 23:54:23.950473'),(19,'sessions','0001_initial','2026-05-22 23:54:24.000491'),(20,'token_blacklist','0001_initial','2026-05-22 23:54:24.228486'),(21,'token_blacklist','0002_outstandingtoken_jti_hex','2026-05-22 23:54:24.306863'),(22,'token_blacklist','0003_auto_20171017_2007','2026-05-22 23:54:24.327118'),(23,'token_blacklist','0004_auto_20171017_2013','2026-05-22 23:54:24.434244'),(24,'token_blacklist','0005_remove_outstandingtoken_jti','2026-05-22 23:54:24.510015'),(25,'token_blacklist','0006_auto_20171017_2113','2026-05-22 23:54:24.545433'),(26,'token_blacklist','0007_auto_20171017_2214','2026-05-22 23:54:24.823756'),(27,'token_blacklist','0008_migrate_to_bigautofield','2026-05-22 23:54:25.174207'),(28,'token_blacklist','0010_fix_migrate_to_bigautofield','2026-05-22 23:54:25.188883'),(29,'token_blacklist','0011_linearizes_history','2026-05-22 23:54:25.192877'),(30,'token_blacklist','0012_alter_outstandingtoken_user','2026-05-22 23:54:25.205171'),(31,'token_blacklist','0013_alter_blacklistedtoken_options_and_more','2026-05-22 23:54:25.225658'),(32,'accounts','0002_alter_user_is_active','2026-05-23 20:06:25.557993'),(33,'activity','0001_initial','2026-05-23 20:06:25.868960'),(34,'axes','0001_initial','2026-05-23 20:06:25.942866'),(35,'axes','0002_auto_20151217_2044','2026-05-23 20:06:26.175159'),(36,'axes','0003_auto_20160322_0929','2026-05-23 20:06:26.194320'),(37,'axes','0004_auto_20181024_1538','2026-05-23 20:06:26.219006'),(38,'axes','0005_remove_accessattempt_trusted','2026-05-23 20:06:26.300437'),(39,'axes','0006_remove_accesslog_trusted','2026-05-23 20:06:26.408134'),(40,'axes','0007_alter_accessattempt_unique_together','2026-05-23 20:06:26.463261'),(41,'axes','0008_accessfailurelog','2026-05-23 20:06:26.668306'),(42,'axes','0009_add_session_hash','2026-05-23 20:06:26.768160'),(43,'axes','0010_accessattemptexpiration','2026-05-23 20:06:26.863443'),(44,'accounts','0003_user_is_verified_usersocialaccount','2026-05-26 23:56:00.649247'),(45,'account','0001_initial','2026-05-27 14:33:08.212438'),(46,'account','0002_email_max_length','2026-05-27 14:33:08.255991'),(47,'account','0003_alter_emailaddress_create_unique_verified_email','2026-05-27 14:33:08.321558'),(48,'account','0004_alter_emailaddress_drop_unique_email','2026-05-27 14:33:08.406435'),(49,'account','0005_emailaddress_idx_upper_email','2026-05-27 14:33:08.456124'),(50,'account','0006_emailaddress_lower','2026-05-27 14:33:08.481570'),(51,'account','0007_emailaddress_idx_email','2026-05-27 14:33:08.557222'),(52,'account','0008_emailaddress_unique_primary_email_fixup','2026-05-27 14:33:08.586265'),(53,'account','0009_emailaddress_unique_primary_email','2026-05-27 14:33:08.606693'),(54,'sites','0001_initial','2026-05-27 14:33:08.635772'),(55,'sites','0002_alter_domain_unique','2026-05-27 14:33:08.665714'),(56,'socialaccount','0001_initial','2026-05-27 14:33:09.303283'),(57,'socialaccount','0002_token_max_lengths','2026-05-27 14:33:09.384371'),(58,'socialaccount','0003_extra_data_default_dict','2026-05-27 14:33:09.400941'),(59,'socialaccount','0004_app_provider_id_settings','2026-05-27 14:33:09.621937'),(60,'socialaccount','0005_socialtoken_nullable_app','2026-05-27 14:33:09.807583'),(61,'socialaccount','0006_alter_socialaccount_extra_data','2026-05-27 14:33:09.918549'),(62,'accounts','0004_alter_user_managers_and_more','2026-05-27 15:05:31.777447'),(63,'finances','0001_initial','2026-06-06 21:09:18.752845'),(64,'finances','0002_remove_budget_unique_user_budget_and_more','2026-06-09 21:40:54.809972'),(65,'activity','0002_alter_auditlog_new_values_alter_auditlog_old_values_and_more','2026-06-22 16:48:49.410740'),(66,'finances','0003_transaction_finances_tr_user_id_5d91a0_idx_and_more','2026-06-24 00:05:14.904666');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('3fw32d35val9j8vijp9b3l6v93porw0q','.eJxVjMsOgyAQRf-FdTE8ZmDorv0RMyBEU4NJxVXTf682Ltq7u49zX6LnrY39tuZnPw3iKjwbDLskEBQJAbIkJC8hJlJO68EGFpdfLHJ65HqwPM9H3HFKy1Zb992c9drddpdrmxK3aan3k_q7Gnkd9x-n3BCtJUtOMfhgwCNCstkgsi5ZxxAVFQiHx6JIF0uRCxrDvpgs3h9la0QA:1wTgjG:EuZR4D9ccM4j6LdjbPDrDsCI4KoLuGQ9qBTpS4fbbPQ','2026-06-14 14:01:26.274548');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_site` (
  `id` int NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_site_domain_a2e37b91_uniq` (`domain`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (2,'127.0.0.1:8000','localhost');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `finances_budget`
--

DROP TABLE IF EXISTS `finances_budget`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `finances_budget` (
  `id` char(32) NOT NULL,
  `title` varchar(50) NOT NULL,
  `budget_amount` decimal(12,2) NOT NULL,
  `period_type` varchar(15) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` char(32) NOT NULL,
  `category_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_user_budget` (`user_id`,`category_id`,`start_date`,`end_date`),
  KEY `finances_bu_user_id_45908a_idx` (`user_id`),
  KEY `finances_bu_period__1d31d6_idx` (`period_type`),
  KEY `finances_bu_user_id_e808b4_idx` (`user_id`,`period_type`),
  KEY `finances_budget_category_id_30185a6c_fk_finances_category_id` (`category_id`),
  CONSTRAINT `finances_budget_category_id_30185a6c_fk_finances_category_id` FOREIGN KEY (`category_id`) REFERENCES `finances_category` (`id`),
  CONSTRAINT `finances_budget_user_id_e03b0a01_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `finances_budget`
--

LOCK TABLES `finances_budget` WRITE;
/*!40000 ALTER TABLE `finances_budget` DISABLE KEYS */;
INSERT INTO `finances_budget` VALUES ('0a05067f740c4456acf699226c10bf91','April transportation budget',600.00,'monthly','2026-04-01','2026-04-30',1,'2026-06-15 15:33:45.740602','2026-06-15 15:33:45.740626','fa4215d523ef40a3b91b52d988ba1c68','bdd2e85744494a3caeb5c7ad0ba55742'),('26ade602afe842ca85e6b031ac154a77','May transportation budget',600.00,'monthly','2026-05-01','2026-05-31',1,'2026-06-15 15:32:07.325265','2026-06-15 15:32:07.325288','fa4215d523ef40a3b91b52d988ba1c68','bdd2e85744494a3caeb5c7ad0ba55742'),('33252ccff9bc4d3cbc3deddd2692d78b','April utilities budget',400.00,'monthly','2026-04-01','2026-04-30',1,'2026-06-15 15:33:47.659022','2026-06-15 15:33:47.659040','fa4215d523ef40a3b91b52d988ba1c68','3b69c9cfb4af4c4eb36fa8a018af14de'),('3cc69abc74c0474e971f7bc674eea038','April food budget',1200.00,'monthly','2026-04-01','2026-04-30',1,'2026-06-15 15:33:43.427237','2026-06-15 15:33:43.427271','fa4215d523ef40a3b91b52d988ba1c68','c2fa03e6e05148938042e09bc5a8c36f'),('5959e1dbabf644f094062a177b11bc41','April shopping budget',800.00,'monthly','2026-04-01','2026-04-30',1,'2026-06-15 15:33:49.419357','2026-06-15 15:33:49.419374','fa4215d523ef40a3b91b52d988ba1c68','b16bc19ca0694f028754137247c6c84c'),('60ff446e3d3f4e5585805cf340097ba7','May shopping budget',800.00,'monthly','2026-05-01','2026-05-31',1,'2026-06-15 15:32:12.070640','2026-06-15 15:32:12.070662','fa4215d523ef40a3b91b52d988ba1c68','b16bc19ca0694f028754137247c6c84c'),('803da435981a444eaab9bcb742fd47ea','June food budget',1200.00,'monthly','2026-06-01','2026-06-30',1,'2026-06-15 15:30:15.263725','2026-06-15 15:30:15.263763','fa4215d523ef40a3b91b52d988ba1c68','c2fa03e6e05148938042e09bc5a8c36f'),('84e6a7cc0d234c749d2dfc32cfc3c33a','May food budget',1200.00,'monthly','2026-05-01','2026-05-31',1,'2026-06-15 15:32:04.141884','2026-06-15 15:32:04.141902','fa4215d523ef40a3b91b52d988ba1c68','c2fa03e6e05148938042e09bc5a8c36f'),('93086681033c41a098eb73bcdc8ea39b','June transportation budget',600.00,'monthly','2026-06-01','2026-06-30',1,'2026-06-15 15:30:30.486061','2026-06-15 15:30:30.486084','fa4215d523ef40a3b91b52d988ba1c68','bdd2e85744494a3caeb5c7ad0ba55742'),('d65e8d016ef14b258b1f78bde014246e','June utilities budget',400.00,'monthly','2026-06-01','2026-06-30',1,'2026-06-15 15:30:32.594575','2026-06-15 15:30:32.594623','fa4215d523ef40a3b91b52d988ba1c68','3b69c9cfb4af4c4eb36fa8a018af14de'),('e2858294f63b4e4da89ea426600a9100','June shopping budget',800.00,'monthly','2026-06-01','2026-06-30',1,'2026-06-15 15:30:35.520759','2026-06-15 15:30:35.520776','fa4215d523ef40a3b91b52d988ba1c68','b16bc19ca0694f028754137247c6c84c'),('e791e3d0e7bb4d8abeaf5d27410feac7','May utilities budget',400.00,'monthly','2026-05-01','2026-05-31',1,'2026-06-15 15:32:10.306527','2026-06-15 15:32:10.306549','fa4215d523ef40a3b91b52d988ba1c68','3b69c9cfb4af4c4eb36fa8a018af14de');
/*!40000 ALTER TABLE `finances_budget` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `finances_category`
--

DROP TABLE IF EXISTS `finances_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `finances_category` (
  `id` char(32) NOT NULL,
  `name` varchar(50) NOT NULL,
  `type` varchar(10) NOT NULL,
  `is_system` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` char(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_user_category` (`user_id`,`name`),
  CONSTRAINT `finances_category_user_id_d74a2e63_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `finances_category`
--

LOCK TABLES `finances_category` WRITE;
/*!40000 ALTER TABLE `finances_category` DISABLE KEYS */;
INSERT INTO `finances_category` VALUES ('225209ebbce145519da2e44cc1f7d4dc','UI UX design gigs','income',0,1,'2026-06-15 14:42:11.693119','2026-06-15 14:42:11.693143','fa4215d523ef40a3b91b52d988ba1c68'),('3b69c9cfb4af4c4eb36fa8a018af14de','Utilities','expense',0,1,'2026-06-15 14:42:33.829781','2026-06-15 15:04:31.024933','fa4215d523ef40a3b91b52d988ba1c68'),('3f714e9c2fb9416db106baae58fbdb3d','salary','income',0,1,'2026-06-15 14:41:56.013710','2026-06-15 14:41:56.013757','fa4215d523ef40a3b91b52d988ba1c68'),('6e6a0d0bdf104b4bb4dbf2257e10a939','food category','expense',0,1,'2026-06-08 20:31:01.467565','2026-06-10 10:53:28.536224','4050c7b3f1e44253bb1d6ba2d97649a3'),('a86bedd556ac41ab803ffbe8e4db3919','Tech training','income',0,1,'2026-06-15 14:42:19.395236','2026-06-15 14:42:19.395257','fa4215d523ef40a3b91b52d988ba1c68'),('b16bc19ca0694f028754137247c6c84c','Shopping','expense',0,1,'2026-06-15 14:42:42.377443','2026-06-15 14:42:42.377474','fa4215d523ef40a3b91b52d988ba1c68'),('b8f72d6dace949abbd27d978e6017612','salary','income',0,1,'2026-06-10 12:07:44.598860','2026-06-10 12:07:44.598915','4050c7b3f1e44253bb1d6ba2d97649a3'),('bdd2e85744494a3caeb5c7ad0ba55742','Transportation','expense',0,1,'2026-06-15 14:42:28.536770','2026-06-15 14:42:28.536850','fa4215d523ef40a3b91b52d988ba1c68'),('c2fa03e6e05148938042e09bc5a8c36f','Food','expense',0,1,'2026-06-15 14:42:23.979978','2026-06-15 14:42:23.980000','fa4215d523ef40a3b91b52d988ba1c68'),('c6f3aa41f4da4432a77ab45553303620','home maintenance','expense',0,1,'2026-06-11 21:54:03.669187','2026-06-11 21:54:03.669215','4050c7b3f1e44253bb1d6ba2d97649a3'),('f1888a49c3da47f89078be57ceca505f','Entertainment','expense',0,1,'2026-06-15 14:42:38.436633','2026-06-15 14:42:38.436663','fa4215d523ef40a3b91b52d988ba1c68'),('fca0129c73f445db9f253820c3fcb2a3','freelance web development','income',0,1,'2026-06-15 14:42:05.550790','2026-06-15 14:42:05.550828','fa4215d523ef40a3b91b52d988ba1c68');
/*!40000 ALTER TABLE `finances_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `finances_transaction`
--

DROP TABLE IF EXISTS `finances_transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `finances_transaction` (
  `id` char(32) NOT NULL,
  `title` varchar(50) NOT NULL,
  `amount` decimal(12,2) NOT NULL,
  `type` varchar(10) NOT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `transaction_date` date NOT NULL,
  `is_recurring` tinyint(1) NOT NULL,
  `frequency` varchar(15) DEFAULT NULL,
  `next_due_date` date DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `category_id` char(32) NOT NULL,
  `user_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `finances_tr_user_id_f3a877_idx` (`user_id`),
  KEY `finances_tr_transac_7a6b2e_idx` (`transaction_date`),
  KEY `finances_tr_user_id_4337b9_idx` (`user_id`,`transaction_date`),
  KEY `finances_transaction_category_id_895a6b54_fk_finances_` (`category_id`),
  KEY `finances_tr_user_id_5d91a0_idx` (`user_id`,`type`),
  KEY `finances_tr_user_id_c411a2_idx` (`user_id`,`type`,`transaction_date`),
  CONSTRAINT `finances_transaction_category_id_895a6b54_fk_finances_` FOREIGN KEY (`category_id`) REFERENCES `finances_category` (`id`),
  CONSTRAINT `finances_transaction_user_id_0ebd4937_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `finances_transaction`
--

LOCK TABLES `finances_transaction` WRITE;
/*!40000 ALTER TABLE `finances_transaction` DISABLE KEYS */;
INSERT INTO `finances_transaction` VALUES ('009276f7eccc4a4aae098248ff31ef80','April: paid for Shatta Wale\'s show',180.00,'expense','payment for Shatta Wale\'s concert show at shoprite','2026-04-19',0,NULL,NULL,1,'2026-06-22 09:56:11.695945','2026-06-22 09:56:11.695975','f1888a49c3da47f89078be57ceca505f','fa4215d523ef40a3b91b52d988ba1c68'),('0a21fe7f19bc4af9bae0717278286fbf','April: groceries shopping',90.00,'expense','went for groceries shopping','2026-04-06',0,NULL,NULL,1,'2026-06-22 09:55:19.977201','2026-06-22 09:55:19.977247','c2fa03e6e05148938042e09bc5a8c36f','fa4215d523ef40a3b91b52d988ba1c68'),('0c0e8e64ca864c3c805a4b035fbf2cdf','April: groceries shopping',110.00,'expense','payment made for groceries shopping','2026-04-28',0,NULL,NULL,1,'2026-06-22 09:57:29.010403','2026-06-22 09:57:29.010423','c2fa03e6e05148938042e09bc5a8c36f','fa4215d523ef40a3b91b52d988ba1c68'),('0cb207611b554a44b5805bbbbe783d1b','June: internet and cable TV bills',150.00,'expense','payment for internet subscription and cable TV monthly bill','2026-06-15',0,NULL,NULL,1,'2026-06-22 10:02:31.737354','2026-06-22 10:02:31.737387','3b69c9cfb4af4c4eb36fa8a018af14de','fa4215d523ef40a3b91b52d988ba1c68'),('13281c2f6b0b4f6abfde4df756a374fc','April: paid for Black Sheriff show',120.00,'expense','purchase ticket for Black Sheriff show','2026-04-05',0,NULL,NULL,1,'2026-06-22 09:55:10.613546','2026-06-22 09:55:10.613592','f1888a49c3da47f89078be57ceca505f','fa4215d523ef40a3b91b52d988ba1c68'),('13e7ccccb5fa435d8be44e77c1115d3d','April freelance dev wage',1200.00,'income','got paid for April web development freelance project.','2026-04-10',0,NULL,NULL,1,'2026-06-21 21:47:49.614688','2026-06-21 21:47:49.614714','fca0129c73f445db9f253820c3fcb2a3','fa4215d523ef40a3b91b52d988ba1c68'),('158c66f1f557433796b008ad746f8975','May tech training wage',500.00,'income','received payment for May tech training program','2026-05-01',0,NULL,NULL,1,'2026-06-21 21:48:28.760941','2026-06-21 21:48:28.760962','a86bedd556ac41ab803ffbe8e4db3919','fa4215d523ef40a3b91b52d988ba1c68'),('189ecba4f1944fab9e4d25b0f1f865b3','June: weekly commute transport fare',120.00,'expense','payment for weekly transport fare to work and back','2026-06-03',0,NULL,NULL,1,'2026-06-22 10:01:28.346844','2026-06-22 10:01:28.346859','bdd2e85744494a3caeb5c7ad0ba55742','fa4215d523ef40a3b91b52d988ba1c68'),('23b26ab40d1a4492bac04029605e962a','April: bought food for workers',140.00,'expense','paid for house maintenance project workers feeding','2026-04-24',0,NULL,NULL,1,'2026-06-22 09:56:30.377941','2026-06-22 09:56:30.377968','c2fa03e6e05148938042e09bc5a8c36f','fa4215d523ef40a3b91b52d988ba1c68'),('242ee6643bbe403c9fed856e5385fda1','May: food items top up',180.00,'expense','bought additional food items and condiments','2026-05-07',0,NULL,NULL,1,'2026-06-22 09:58:36.682556','2026-06-22 09:58:36.682570','c2fa03e6e05148938042e09bc5a8c36f','fa4215d523ef40a3b91b52d988ba1c68'),('263e6e5fcfab4c79a932ab2cd19dfc1b','May freelance development wage',800.00,'income','received payment for May freelance web dev gig','2026-05-01',0,NULL,NULL,1,'2026-06-21 21:48:17.815930','2026-06-21 21:48:17.815948','fca0129c73f445db9f253820c3fcb2a3','fa4215d523ef40a3b91b52d988ba1c68'),('2a9f4c41245d4bf8bfe3d13241db07be','May: monthly grocery shopping',200.00,'expense','purchased food items and provisions to kick off the month','2026-05-02',0,NULL,NULL,1,'2026-06-22 09:57:50.069839','2026-06-22 09:57:50.069889','c2fa03e6e05148938042e09bc5a8c36f','fa4215d523ef40a3b91b52d988ba1c68'),('2d8d0d19da934885b6635ee02efd7737','June UI UX design gig',1000.00,'income','received payment for June UI UX design gig','2026-06-11',0,NULL,NULL,1,'2026-06-21 21:48:43.384292','2026-06-21 21:48:43.384314','225209ebbce145519da2e44cc1f7d4dc','fa4215d523ef40a3b91b52d988ba1c68'),('2e2a163c8ee244d7a1fc75a1c3621eb7','April: paid for transporting tools and workers',75.00,'expense','paid for house maintenance project transport fare','2026-04-22',0,NULL,NULL,1,'2026-06-22 09:56:22.379444','2026-06-22 09:56:22.379560','bdd2e85744494a3caeb5c7ad0ba55742','fa4215d523ef40a3b91b52d988ba1c68'),('3c6d138128894bf6b294056ac0f228c8','April: paid for electricity bill',150.00,'expense','payment for prepaid electricity  and other utilities bills','2026-04-09',0,NULL,NULL,1,'2026-06-22 09:55:29.400782','2026-06-22 09:55:29.400800','3b69c9cfb4af4c4eb36fa8a018af14de','fa4215d523ef40a3b91b52d988ba1c68'),('41e71d73350c4096aaa4397f18832f76','April: paid for house maintenance project',120.00,'expense','paid painters for repainting living room','2026-04-20',0,NULL,NULL,1,'2026-06-22 09:56:19.548935','2026-06-22 09:56:19.548982','3b69c9cfb4af4c4eb36fa8a018af14de','fa4215d523ef40a3b91b52d988ba1c68'),('5005e4428d6c453aae1631bd870522c3','June: electricity and water bills',200.00,'expense','payment for electricity token and water bill','2026-06-05',0,NULL,NULL,1,'2026-06-22 10:01:41.135412','2026-06-22 10:01:41.135426','3b69c9cfb4af4c4eb36fa8a018af14de','fa4215d523ef40a3b91b52d988ba1c68'),('577ed186b7214115a0f714213a92e9f9','May: end of month outing with friends',200.00,'expense','payment for end-of-month celebration outing with friends','2026-05-30',0,NULL,NULL,1,'2026-06-22 10:01:13.695514','2026-06-22 10:01:13.695575','f1888a49c3da47f89078be57ceca505f','fa4215d523ef40a3b91b52d988ba1c68'),('60f21d818fcf48898400b49f794c25d2','April: bought food stuffs',120.00,'expense','went for groceries shopping','2026-04-03',0,NULL,NULL,1,'2026-06-22 09:45:16.307300','2026-06-22 09:45:16.307341','c2fa03e6e05148938042e09bc5a8c36f','fa4215d523ef40a3b91b52d988ba1c68'),('62ad8c26dc864f16bb0b80c2b98caadc','June tech training wage',700.00,'income','received payment for June tech training program','2026-06-15',0,NULL,NULL,1,'2026-06-21 21:48:46.522796','2026-06-21 21:48:46.522853','a86bedd556ac41ab803ffbe8e4db3919','fa4215d523ef40a3b91b52d988ba1c68'),('68b16c3b921944219b3b05d49c0dd38b','May: water and waste disposal bills',130.00,'expense','payment for water bill and waste disposal charges','2026-05-17',0,NULL,NULL,1,'2026-06-22 10:00:02.929333','2026-06-22 10:00:02.929351','3b69c9cfb4af4c4eb36fa8a018af14de','fa4215d523ef40a3b91b52d988ba1c68'),('6946ae30ef4848d6a202d361d1d9f51d','June: fashion shopping at Accra Mall',220.00,'expense','bought new clothes and accessories from Accra Mall','2026-06-04',0,NULL,NULL,1,'2026-06-22 10:01:34.243875','2026-06-22 10:01:34.243896','b16bc19ca0694f028754137247c6c84c','fa4215d523ef40a3b91b52d988ba1c68'),('6a8f60d0590542ffa2feb663d40b07c1','May: internet subscription payment',90.00,'expense','payment for monthly internet subscription','2026-05-24',0,NULL,NULL,1,'2026-06-22 10:00:50.705982','2026-06-22 10:00:50.706000','3b69c9cfb4af4c4eb36fa8a018af14de','fa4215d523ef40a3b91b52d988ba1c68'),('7266595b2c3a408ca1e530efc93bba5e','May: personal clothing purchase',180.00,'expense','bought clothing items from the market','2026-05-06',0,NULL,NULL,1,'2026-06-22 09:58:30.581619','2026-06-22 09:58:30.581634','b16bc19ca0694f028754137247c6c84c','fa4215d523ef40a3b91b52d988ba1c68'),('7c59064a30a54770a47e2f054f2a9108','June salary',5000.00,'income','received June monthly salary for full time job','2026-06-01',0,NULL,NULL,1,'2026-06-21 21:48:34.629665','2026-06-21 21:48:34.629692','3f714e9c2fb9416db106baae58fbdb3d','fa4215d523ef40a3b91b52d988ba1c68'),('87b735c870894ed1807f48353c4f99f2','April: transport fare',80.00,'expense','payment for transport fare for visiting Mum','2026-04-15',0,NULL,NULL,1,'2026-06-22 09:55:54.152523','2026-06-22 09:55:54.152542','bdd2e85744494a3caeb5c7ad0ba55742','fa4215d523ef40a3b91b52d988ba1c68'),('87bff6981ce245e6a207fe290192c2d4','June: shopping for mum',230.00,'expense','bought household items and clothing for mum','2026-06-18',0,NULL,NULL,1,'2026-06-22 10:02:46.939472','2026-06-22 10:02:46.939487','b16bc19ca0694f028754137247c6c84c','fa4215d523ef40a3b91b52d988ba1c68'),('88bbc967d30448a89ad24ad639616f20','May: market day groceries',220.00,'expense','bought fresh produce and food items from the market','2026-05-13',0,NULL,NULL,1,'2026-06-22 09:59:29.322816','2026-06-22 09:59:29.322843','c2fa03e6e05148938042e09bc5a8c36f','fa4215d523ef40a3b91b52d988ba1c68'),('8a92c229e0a6425c9f6ae9764fc2a887','May: bolt ride for errands',80.00,'expense','paid for bolt ride to run errands around Accra','2026-05-14',0,NULL,NULL,1,'2026-06-22 09:59:38.974467','2026-06-22 09:59:38.974488','bdd2e85744494a3caeb5c7ad0ba55742','fa4215d523ef40a3b91b52d988ba1c68'),('8b1f168ec4d84656b99e67d02e28966f','June: household appliance purchase',280.00,'expense','bought a small kitchen appliance and accessories','2026-06-10',0,NULL,NULL,1,'2026-06-22 10:02:08.503988','2026-06-22 10:02:08.504002','b16bc19ca0694f028754137247c6c84c','fa4215d523ef40a3b91b52d988ba1c68'),('8b241ef59f304efd989ebd51bb7b51ec','June: bolt rides for errands',130.00,'expense','payment for bolt rides for various errands around Accra','2026-06-19',0,NULL,NULL,1,'2026-06-22 10:02:51.993671','2026-06-22 10:02:51.993721','bdd2e85744494a3caeb5c7ad0ba55742','fa4215d523ef40a3b91b52d988ba1c68'),('8bb6baaa0d574fd6a545bf8374a7d5eb','April: shopping for girlfriend',180.00,'expense','payment for shopping for girlfriend','2026-04-25',0,NULL,NULL,1,'2026-06-22 09:56:33.900943','2026-06-22 09:56:33.900991','b16bc19ca0694f028754137247c6c84c','fa4215d523ef40a3b91b52d988ba1c68'),('8ee681dddf644f87ab7fbb285b38155c','June: Father\'s Day food shopping',270.00,'expense','purchased food items for Father\'s Day family gathering','2026-06-21',0,NULL,NULL,1,'2026-06-22 10:02:57.688481','2026-06-22 10:02:57.688499','c2fa03e6e05148938042e09bc5a8c36f','fa4215d523ef40a3b91b52d988ba1c68'),('912cb2e38bff44598ba7c8522be0f01a','May: weekend food items',170.00,'expense','purchased food items and snacks for the weekend','2026-05-18',0,NULL,NULL,1,'2026-06-22 10:00:11.296970','2026-06-22 10:00:11.296988','c2fa03e6e05148938042e09bc5a8c36f','fa4215d523ef40a3b91b52d988ba1c68'),('94132e5800f04f029b9057b78b6b5649','May: electricity bill payment',160.00,'expense','prepaid electricity token recharge for the month','2026-05-05',0,NULL,NULL,1,'2026-06-22 09:58:22.877863','2026-06-22 09:58:22.877877','3b69c9cfb4af4c4eb36fa8a018af14de','fa4215d523ef40a3b91b52d988ba1c68'),('947be676f25f47c796a24fbd09ee2bea','June: weekend movie night',200.00,'expense','paid for cinema tickets and refreshments for movie night','2026-06-06',0,NULL,NULL,1,'2026-06-22 10:01:46.089111','2026-06-22 10:01:46.089148','f1888a49c3da47f89078be57ceca505f','fa4215d523ef40a3b91b52d988ba1c68'),('98bb53c0751344cc9d27ba8c0355ba53','June freelance development wage',1500.00,'income','received payment for June freelance web dev gig','2026-06-06',0,NULL,NULL,1,'2026-06-21 21:48:39.389060','2026-06-21 21:48:39.389088','fca0129c73f445db9f253820c3fcb2a3','fa4215d523ef40a3b91b52d988ba1c68'),('a1a80a3665094416993a7ea07d9888b1','April: food stuffs top up',130.00,'expense','went groceries top up','2026-04-18',0,NULL,NULL,1,'2026-06-22 09:56:00.833035','2026-06-22 09:56:00.833072','c2fa03e6e05148938042e09bc5a8c36f','fa4215d523ef40a3b91b52d988ba1c68'),('a703f1d7511145f49c00721bc084e174','April: paid for transport fare',60.00,'expense','paid for transport fare to Cape Coastg','2026-04-04',0,NULL,NULL,1,'2026-06-22 09:54:53.246484','2026-06-22 09:54:53.246503','bdd2e85744494a3caeb5c7ad0ba55742','fa4215d523ef40a3b91b52d988ba1c68'),('ac675837e67b40bc92b275387a647fb3','May: household items purchase',220.00,'expense','bought household supplies and home essentials','2026-05-12',0,NULL,NULL,1,'2026-06-22 09:59:19.691101','2026-06-22 09:59:19.691116','b16bc19ca0694f028754137247c6c84c','fa4215d523ef40a3b91b52d988ba1c68'),('aec8820a2b6c45a0b59b3ac73338c0af','May: mid-week grocery run',150.00,'expense','restocked kitchen supplies and groceries mid-week','2026-05-22',0,NULL,NULL,1,'2026-06-22 10:00:45.581789','2026-06-22 10:00:45.581805','c2fa03e6e05148938042e09bc5a8c36f','fa4215d523ef40a3b91b52d988ba1c68'),('b28b6661464d4e5597942e531e3bbe8e','May: birthday gift shopping',190.00,'expense','bought gifts for a friend\'s birthday celebration','2026-05-29',0,NULL,NULL,1,'2026-06-22 10:01:06.857284','2026-06-22 10:01:06.857314','b16bc19ca0694f028754137247c6c84c','fa4215d523ef40a3b91b52d988ba1c68'),('b99b7dc9b6a74df28cd5db09b65b1e17','May: work trip transport fare',110.00,'expense','payment for transport fare for a work-related trip','2026-05-20',0,NULL,NULL,1,'2026-06-22 10:00:19.384617','2026-06-22 10:00:19.384635','bdd2e85744494a3caeb5c7ad0ba55742','fa4215d523ef40a3b91b52d988ba1c68'),('ba3ffd1163e54c8b818a3519b70c7882','June: monthly grocery shopping',250.00,'expense','purchased food items and provisions to kick off the month','2026-06-02',0,NULL,NULL,1,'2026-06-22 10:01:21.934841','2026-06-22 10:01:21.934876','c2fa03e6e05148938042e09bc5a8c36f','fa4215d523ef40a3b91b52d988ba1c68'),('c069bc896cfc417dbb8da5e1aaf0ddc5','May: cinema outing',200.00,'expense','paid for movie tickets and snacks at the cinema','2026-05-10',0,NULL,NULL,1,'2026-06-22 09:58:51.948457','2026-06-22 09:58:51.948477','f1888a49c3da47f89078be57ceca505f','fa4215d523ef40a3b91b52d988ba1c68'),('cc109926adef4a899b0dedb3a80aa132','April: transport fare to Nsawam',55.00,'expense','payment for full journey transport fare to Nsawam','2026-04-08',0,NULL,NULL,1,'2026-06-22 09:55:25.823349','2026-06-22 09:55:25.823365','bdd2e85744494a3caeb5c7ad0ba55742','fa4215d523ef40a3b91b52d988ba1c68'),('d13a1fd2aab9433ba7ab1a87bce2c3b5','May: Accra to Kumasi transport fare',120.00,'expense','payment for intercity transport fare to Kumasi','2026-05-09',0,NULL,NULL,1,'2026-06-22 09:58:46.255243','2026-06-22 09:58:46.255279','bdd2e85744494a3caeb5c7ad0ba55742','fa4215d523ef40a3b91b52d988ba1c68'),('d6dc3da6da4345839bbd0a68963469d9','April: Mum groceries shopping',160.00,'expense','payment for groceries shopping for mum','2026-04-12',0,NULL,NULL,1,'2026-06-22 09:55:49.802648','2026-06-22 09:55:49.802671','b16bc19ca0694f028754137247c6c84c','fa4215d523ef40a3b91b52d988ba1c68'),('dd4530e31bef4388a8059bd2615dc9ab','June: groceries and food items',230.00,'expense','bought groceries and fresh food items for the household','2026-06-16',0,NULL,NULL,1,'2026-06-22 10:02:41.479302','2026-06-22 10:02:41.479321','c2fa03e6e05148938042e09bc5a8c36f','fa4215d523ef40a3b91b52d988ba1c68'),('e3c5852e7ea74547a4c61b56bb31c2a3','April: bolt ride for shopping',70.00,'expense','payment for bolt ride for girlfriend\'s shopping','2026-04-27',0,NULL,NULL,1,'2026-06-22 09:56:37.604318','2026-06-22 09:56:37.604339','bdd2e85744494a3caeb5c7ad0ba55742','fa4215d523ef40a3b91b52d988ba1c68'),('e4589fb01e0848b88c9acdea170dd8dd','June: mid-month market shopping',280.00,'expense','purchased fresh produce and dry goods from the market','2026-06-11',0,NULL,NULL,1,'2026-06-22 10:02:13.302980','2026-06-22 10:02:13.302999','c2fa03e6e05148938042e09bc5a8c36f','fa4215d523ef40a3b91b52d988ba1c68'),('e5077b9712f348959ddda44e25857632','April: shopping payment',250.00,'expense','payment for clothing and shoes shopping','2026-04-11',0,NULL,NULL,1,'2026-06-22 09:55:41.065796','2026-06-22 09:55:41.065813','b16bc19ca0694f028754137247c6c84c','fa4215d523ef40a3b91b52d988ba1c68'),('ea16b9ade79340f19baf5bf972f81224','June: food items top up',200.00,'expense','bought additional food supplies and household provisions','2026-06-07',0,NULL,NULL,1,'2026-06-22 10:01:54.110790','2026-06-22 10:01:54.110807','c2fa03e6e05148938042e09bc5a8c36f','fa4215d523ef40a3b91b52d988ba1c68'),('ec356630de424d56a70be6113fbd0bf9','June: Stonebwoy concert ticket',250.00,'expense','purchased ticket for Stonebwoy\'s live concert','2026-06-14',0,NULL,NULL,1,'2026-06-22 10:02:25.293417','2026-06-22 10:02:25.293433','f1888a49c3da47f89078be57ceca505f','fa4215d523ef40a3b91b52d988ba1c68'),('ec67fe8f61a949a795868a3c20f8677f','May: transport fare to work',90.00,'expense','payment for daily commute transport fare','2026-05-03',0,NULL,NULL,1,'2026-06-22 09:58:04.994804','2026-06-22 09:58:04.994822','bdd2e85744494a3caeb5c7ad0ba55742','fa4215d523ef40a3b91b52d988ba1c68'),('ed8f885f93e3402eb99de2bfb432d04b','May salary',5000.00,'income','received May monthly salary for full time job','2026-05-01',0,NULL,NULL,1,'2026-06-21 21:48:07.019832','2026-06-21 21:48:07.019851','3f714e9c2fb9416db106baae58fbdb3d','fa4215d523ef40a3b91b52d988ba1c68'),('efd839bfb0dc4a44adb361566a8ab33c','April salary',5000.00,'income','received April monthly salary for full time job','2026-04-01',0,NULL,NULL,1,'2026-06-21 21:46:38.993607','2026-06-21 21:46:38.993666','3f714e9c2fb9416db106baae58fbdb3d','fa4215d523ef40a3b91b52d988ba1c68'),('f272c98207894b869d0abc08019edfb0','May: shoes and accessories',190.00,'expense','bought a pair of shoes and accessories','2026-05-21',0,NULL,NULL,1,'2026-06-22 10:00:29.099833','2026-06-22 10:00:29.099883','b16bc19ca0694f028754137247c6c84c','fa4215d523ef40a3b91b52d988ba1c68'),('f2913658ca694ffca56f8de0ca2247ab','April UI UX design gig',600.00,'income','received payment for April UI UX design gig.','2026-04-18',0,NULL,NULL,1,'2026-06-21 21:47:52.300057','2026-06-21 21:47:52.300077','225209ebbce145519da2e44cc1f7d4dc','fa4215d523ef40a3b91b52d988ba1c68'),('f4d44e4e7f9547969c94817ae732d2cd','June: Accra to Tema transport fare',150.00,'expense','paid for transport fare for a trip to Tema','2026-06-08',0,NULL,NULL,1,'2026-06-22 10:02:03.685241','2026-06-22 10:02:03.685279','bdd2e85744494a3caeb5c7ad0ba55742','fa4215d523ef40a3b91b52d988ba1c68'),('fa43fec8e0e94aab8ccd0ac1f58d8b1b','June: upcountry travel transport fare',180.00,'expense','payment for intercity transport fare to Kumasi and back','2026-06-13',0,NULL,NULL,1,'2026-06-22 10:02:19.039402','2026-06-22 10:02:19.039419','bdd2e85744494a3caeb5c7ad0ba55742','fa4215d523ef40a3b91b52d988ba1c68'),('fbea2257f19647ea8dbc2d8ffb558c41','May: family visit transport fare',140.00,'expense','paid for transport fare to visit family','2026-05-26',0,NULL,NULL,1,'2026-06-22 10:00:55.568270','2026-06-22 10:00:55.568290','bdd2e85744494a3caeb5c7ad0ba55742','fa4215d523ef40a3b91b52d988ba1c68'),('fd068505c83949e0b15390acc2443356','May: weekend hangout payment',150.00,'expense','payment for drinks and food at a social hangout with friends','2026-05-16',0,NULL,NULL,1,'2026-06-22 09:59:47.537650','2026-06-22 09:59:47.537669','f1888a49c3da47f89078be57ceca505f','fa4215d523ef40a3b91b52d988ba1c68'),('ff3c8a607c7c449ea85b407e534fddcd','May: end of month grocery top up',130.00,'expense','purchased remaining grocery items to round up for the month','2026-05-28',0,NULL,NULL,1,'2026-06-22 10:01:00.632105','2026-06-22 10:01:00.632129','c2fa03e6e05148938042e09bc5a8c36f','fa4215d523ef40a3b91b52d988ba1c68');
/*!40000 ALTER TABLE `finances_transaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialaccount`
--

DROP TABLE IF EXISTS `socialaccount_socialaccount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialaccount` (
  `id` int NOT NULL AUTO_INCREMENT,
  `provider` varchar(200) NOT NULL,
  `uid` varchar(191) NOT NULL,
  `last_login` datetime(6) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `extra_data` json NOT NULL,
  `user_id` char(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialaccount_provider_uid_fc810c6e_uniq` (`provider`,`uid`),
  KEY `socialaccount_socialaccount_user_id_8146e70c_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `socialaccount_socialaccount_user_id_8146e70c_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialaccount`
--

LOCK TABLES `socialaccount_socialaccount` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialaccount` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialaccount` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialapp`
--

DROP TABLE IF EXISTS `socialaccount_socialapp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialapp` (
  `id` int NOT NULL AUTO_INCREMENT,
  `provider` varchar(30) NOT NULL,
  `name` varchar(40) NOT NULL,
  `client_id` varchar(191) NOT NULL,
  `secret` varchar(191) NOT NULL,
  `key` varchar(191) NOT NULL,
  `provider_id` varchar(200) NOT NULL,
  `settings` json NOT NULL DEFAULT (_utf8mb4'{}'),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialapp`
--

LOCK TABLES `socialaccount_socialapp` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialapp` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialapp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialapp_sites`
--

DROP TABLE IF EXISTS `socialaccount_socialapp_sites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialapp_sites` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `socialapp_id` int NOT NULL,
  `site_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialapp_sites_socialapp_id_site_id_71a9a768_uniq` (`socialapp_id`,`site_id`),
  KEY `socialaccount_socialapp_sites_site_id_2579dee5_fk_django_site_id` (`site_id`),
  CONSTRAINT `socialaccount_social_socialapp_id_97fb6e7d_fk_socialacc` FOREIGN KEY (`socialapp_id`) REFERENCES `socialaccount_socialapp` (`id`),
  CONSTRAINT `socialaccount_socialapp_sites_site_id_2579dee5_fk_django_site_id` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialapp_sites`
--

LOCK TABLES `socialaccount_socialapp_sites` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialapp_sites` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialapp_sites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialtoken`
--

DROP TABLE IF EXISTS `socialaccount_socialtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialtoken` (
  `id` int NOT NULL AUTO_INCREMENT,
  `token` longtext NOT NULL,
  `token_secret` longtext NOT NULL,
  `expires_at` datetime(6) DEFAULT NULL,
  `account_id` int NOT NULL,
  `app_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq` (`app_id`,`account_id`),
  KEY `socialaccount_social_account_id_951f210e_fk_socialacc` (`account_id`),
  CONSTRAINT `socialaccount_social_account_id_951f210e_fk_socialacc` FOREIGN KEY (`account_id`) REFERENCES `socialaccount_socialaccount` (`id`),
  CONSTRAINT `socialaccount_social_app_id_636a42d7_fk_socialacc` FOREIGN KEY (`app_id`) REFERENCES `socialaccount_socialapp` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialtoken`
--

LOCK TABLES `socialaccount_socialtoken` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialtoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialtoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `token_blacklist_blacklistedtoken`
--

DROP TABLE IF EXISTS `token_blacklist_blacklistedtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `token_blacklist_blacklistedtoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `blacklisted_at` datetime(6) NOT NULL,
  `token_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_id` (`token_id`),
  CONSTRAINT `token_blacklist_blacklistedtoken_token_id_3cc7fe56_fk` FOREIGN KEY (`token_id`) REFERENCES `token_blacklist_outstandingtoken` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `token_blacklist_blacklistedtoken`
--

LOCK TABLES `token_blacklist_blacklistedtoken` WRITE;
/*!40000 ALTER TABLE `token_blacklist_blacklistedtoken` DISABLE KEYS */;
INSERT INTO `token_blacklist_blacklistedtoken` VALUES (1,'2026-05-23 12:39:07.488041',1),(2,'2026-05-23 12:42:30.362012',3),(3,'2026-05-23 13:36:35.071642',6),(4,'2026-05-23 14:38:17.117383',8),(5,'2026-05-23 16:20:39.180943',9),(6,'2026-05-23 16:56:03.121151',10),(7,'2026-05-23 17:00:50.697812',11),(8,'2026-06-09 20:07:21.858462',20),(9,'2026-06-09 21:06:14.383483',21),(10,'2026-06-09 21:41:55.152790',23),(11,'2026-06-10 07:04:03.838474',24),(12,'2026-06-10 10:50:09.766556',25);
/*!40000 ALTER TABLE `token_blacklist_blacklistedtoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `token_blacklist_outstandingtoken`
--

DROP TABLE IF EXISTS `token_blacklist_outstandingtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `token_blacklist_outstandingtoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token` longtext NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `expires_at` datetime(6) NOT NULL,
  `user_id` char(32) DEFAULT NULL,
  `jti` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_uniq` (`jti`),
  KEY `token_blacklist_outs_user_id_83bc629a_fk_accounts_` (`user_id`),
  CONSTRAINT `token_blacklist_outs_user_id_83bc629a_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `token_blacklist_outstandingtoken`
--

LOCK TABLES `token_blacklist_outstandingtoken` WRITE;
/*!40000 ALTER TABLE `token_blacklist_outstandingtoken` DISABLE KEYS */;
INSERT INTO `token_blacklist_outstandingtoken` VALUES (1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MDE0NDI3NSwiaWF0IjoxNzc5NTM5NDc1LCJqdGkiOiIyNDYzNGIxZGQxMDM0MmNhYjk5MTQzZWZmYTNlMTJlNyIsInVzZXJfaWQiOiJkYWZhNjc3YS1jMmMwLTRhNGQtOWE4NC0xNTcxYTdjYjU4ZDkifQ.HaJe5YZy4aBIpxn8r25K7kXYi5E-RiFfLwJXRw1U1FY','2026-05-23 12:31:15.610577','2026-05-30 12:31:15.000000','dafa677ac2c04a4d9a841571a7cb58d9','24634b1dd10342cab99143effa3e12e7'),(2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MDE0NDM4MCwiaWF0IjoxNzc5NTM5NTgwLCJqdGkiOiIyMGZkMGQ1ZmQyZjk0MmY5YTQxNTc0NzVhMGNjNTAwZCIsInVzZXJfaWQiOiJkYWZhNjc3YS1jMmMwLTRhNGQtOWE4NC0xNTcxYTdjYjU4ZDkifQ.eerGzVIvbfV4tgXfEUmN-OLA_vzAu6hSQVlQRxTv53o','2026-05-23 12:33:00.690146','2026-05-30 12:33:00.000000','dafa677ac2c04a4d9a841571a7cb58d9','20fd0d5fd2f942f9a4157475a0cc500d'),(3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MDE0NDc0NywiaWF0IjoxNzc5NTM5OTQ3LCJqdGkiOiJhYjQ5Njk2YjdkZDc0MjBmYTdiYzk5MGVjZjdkZjgzZiIsInVzZXJfaWQiOiJkYWZhNjc3YS1jMmMwLTRhNGQtOWE4NC0xNTcxYTdjYjU4ZDkifQ.oa8_ShNZfWFEaO_g3eHOizuKedb0N88mW9X67mZVtwY','2026-05-23 12:39:07.431494','2026-05-30 12:39:07.000000','dafa677ac2c04a4d9a841571a7cb58d9','ab49696b7dd7420fa7bc990ecf7df83f'),(4,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MDE0NTI5NCwiaWF0IjoxNzc5NTQwNDk0LCJqdGkiOiJkYjIxMjRkYzc2ZmY0YjQ5YmZjNjk1Y2Y2NDYxMzE0YiIsInVzZXJfaWQiOiJkYWZhNjc3YS1jMmMwLTRhNGQtOWE4NC0xNTcxYTdjYjU4ZDkifQ.-kayIOg0zPl8YfkhYR4dl1FXIPFP_wrCBNzsIjPaUmQ','2026-05-23 12:48:14.480834','2026-05-30 12:48:14.000000','dafa677ac2c04a4d9a841571a7cb58d9','db2124dc76ff4b49bfc695cf6461314b'),(5,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MDE0NTk3OCwiaWF0IjoxNzc5NTQxMTc4LCJqdGkiOiIyNmMyNmE0NWNjMGY0ZmYxYjFjMDk2YTRjYmE1YTdkYSIsInVzZXJfaWQiOiJkYWZhNjc3YS1jMmMwLTRhNGQtOWE4NC0xNTcxYTdjYjU4ZDkifQ.SI0I8a5CBg_vEA9XrvkncUWPfYrZITTr0oca131tVx0','2026-05-23 12:59:38.820566','2026-05-30 12:59:38.000000','dafa677ac2c04a4d9a841571a7cb58d9','26c26a45cc0f4ff1b1c096a4cba5a7da'),(6,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MDE0NzAyOSwiaWF0IjoxNzc5NTQyMjI5LCJqdGkiOiI5MWEwNWI0ZjhhZTM0ZTc4ODY0OWY2ODg3ZjY5ZDY3ZiIsInVzZXJfaWQiOiJkYWZhNjc3YS1jMmMwLTRhNGQtOWE4NC0xNTcxYTdjYjU4ZDkifQ.-7mLexD8xAooBvJyxVCXUTmXrbc7Y_swXB7Pv3YpvWU','2026-05-23 13:17:09.343288','2026-05-30 13:17:09.000000','dafa677ac2c04a4d9a841571a7cb58d9','91a05b4f8ae34e788649f6887f69d67f'),(7,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MDE0ODE5NSwiaWF0IjoxNzc5NTQzMzk1LCJqdGkiOiJjMWI1M2ViNGMzZGY0NTAxYThmYWU2YzNjODUyOTZmMCIsInVzZXJfaWQiOiJkYWZhNjc3YS1jMmMwLTRhNGQtOWE4NC0xNTcxYTdjYjU4ZDkifQ.WSyHEf0Wkq81LSUXp5rykQmXyB79Omniq2k3sIkP3_I','2026-05-23 13:36:35.053908','2026-05-30 13:36:35.000000','dafa677ac2c04a4d9a841571a7cb58d9','c1b53eb4c3df4501a8fae6c3c85296f0'),(8,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MDE1MDYyNywiaWF0IjoxNzc5NTQ1ODI3LCJqdGkiOiJjYmFjMDRkYzUxMjE0MWZmYjZhYmZhM2FjMDZiNDMzZCIsInVzZXJfaWQiOiJkYWZhNjc3YS1jMmMwLTRhNGQtOWE4NC0xNTcxYTdjYjU4ZDkifQ.wNO0Om1uQqtXN2U0xzg1VpBkWqXRiBeWvZkSOtBcZJc','2026-05-23 14:17:07.061306','2026-05-30 14:17:07.000000','dafa677ac2c04a4d9a841571a7cb58d9','cbac04dc512141ffb6abfa3ac06b433d'),(9,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MDE1MTg5NywiaWF0IjoxNzc5NTQ3MDk3LCJqdGkiOiIwMGVjOTBkODIwMGY0MzgyOGQxMzk4OTUwNGU2MTMzOCIsInVzZXJfaWQiOiJkYWZhNjc3YS1jMmMwLTRhNGQtOWE4NC0xNTcxYTdjYjU4ZDkifQ.YuAufGH3aOP1STJaeW44-_fPcYXWW6IMOG3lnu8lBYE','2026-05-23 14:38:17.101635','2026-05-30 14:38:17.000000','dafa677ac2c04a4d9a841571a7cb58d9','00ec90d8200f43828d13989504e61338'),(10,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MDE1ODAzOSwiaWF0IjoxNzc5NTUzMjM5LCJqdGkiOiJjZmI2ZTMwNDhhYmM0ZjM0OTI4YWNkMTYxNWM0NjJkMCIsInVzZXJfaWQiOiJkYWZhNjc3YS1jMmMwLTRhNGQtOWE4NC0xNTcxYTdjYjU4ZDkifQ.D_YjGGNfKsIapDmhivsDZHq0QeDj0DpPyBRGTn6NE2g','2026-05-23 16:20:39.153398','2026-05-30 16:20:39.000000','dafa677ac2c04a4d9a841571a7cb58d9','cfb6e3048abc4f34928acd1615c462d0'),(11,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MDE2MDE2MywiaWF0IjoxNzc5NTU1MzYzLCJqdGkiOiI5ZDhhN2QyNWYzMjc0OWMxYTRmMzk0MDRjOWIwMWUwNiIsInVzZXJfaWQiOiJkYWZhNjc3YS1jMmMwLTRhNGQtOWE4NC0xNTcxYTdjYjU4ZDkifQ.PTCQnqYolfI7wx3eWAZIBKludKo5nfVrEpW-axu7C40','2026-05-23 16:56:03.084661','2026-05-30 16:56:03.000000','dafa677ac2c04a4d9a841571a7cb58d9','9d8a7d25f32749c1a4f39404c9b01e06'),(12,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MDE2MDQ1MCwiaWF0IjoxNzc5NTU1NjUwLCJqdGkiOiIxYzlmYmJmZmE5YzI0ZDYxOTRlNDU0YjdkY2U2ZmViNCIsInVzZXJfaWQiOiJkYWZhNjc3YS1jMmMwLTRhNGQtOWE4NC0xNTcxYTdjYjU4ZDkifQ.pYuyopnO4imF_Ddwf9NrRW0NO6EfsPLMfLLYI8kZGX4','2026-05-23 17:00:50.670701','2026-05-30 17:00:50.000000','dafa677ac2c04a4d9a841571a7cb58d9','1c9fbbffa9c24d6194e454b7dce6feb4'),(13,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MDI0OTE2NywiaWF0IjoxNzc5NjQ0MzY3LCJqdGkiOiIwOTNhMWNjNzgzOTM0ZDdlYTAxMjFmYTlkYjAzYmNiZSIsInVzZXJfaWQiOiJkYWZhNjc3YS1jMmMwLTRhNGQtOWE4NC0xNTcxYTdjYjU4ZDkifQ.ccyhwcEMQXU2le5J6BRSQEKCqu5P2tg5rh9EyRYN5v8','2026-05-24 17:39:27.720777','2026-05-31 17:39:27.000000','dafa677ac2c04a4d9a841571a7cb58d9','093a1cc783934d7ea0121fa9db03bcbe'),(14,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MDQ0MzYyNywiaWF0IjoxNzc5ODM4ODI3LCJqdGkiOiIxMjJmOGZlZmFkN2Q0NTUxYmYxNmNiMWZjODhkYzUwNSIsInVzZXJfaWQiOiJkYWZhNjc3YS1jMmMwLTRhNGQtOWE4NC0xNTcxYTdjYjU4ZDkifQ.joySIIKpYvYaAFgtt1IDhZji2k1MFRrU37x4gRJFfms','2026-05-26 23:40:27.332697','2026-06-02 23:40:27.000000','dafa677ac2c04a4d9a841571a7cb58d9','122f8fefad7d4551bf16cb1fc88dc505'),(15,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MDQ0OTIzMSwiaWF0IjoxNzc5ODQ0NDMxLCJqdGkiOiI5YWZlODEzNzc1Njc0NDMxOTU5YTMwODcxOTk5NWJhNiIsInVzZXJfaWQiOiIyMTk4ZDExMi1mODM1LTRjNzAtYTk4Zi02NGE4MzBlY2JmYTQifQ.i2rISsx5nJvH1ML-Kxe5vxcKzXv68lgKspQsQUd30RY','2026-05-27 01:13:51.001677','2026-06-03 01:13:51.000000',NULL,'9afe813775674431959a308719995ba6'),(16,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MDUyNjk5OSwiaWF0IjoxNzc5OTIyMTk5LCJqdGkiOiI3ODJiN2Q1ZTU0Mjg0ZWUxOTE1Yzk0YWMyOTlkMzY1YiIsInVzZXJfaWQiOiI0MDUwYzdiMy1mMWU0LTQyNTMtYmIxZC02YmEyZDk3NjQ5YTMifQ.mvdhcMx7m74Dx7D9NfKz8AEJhsLcoTsv-qAv3BhkTvM','2026-05-27 22:49:59.499845','2026-06-03 22:49:59.000000','4050c7b3f1e44253bb1d6ba2d97649a3','782b7d5e54284ee1915c94ac299d365b'),(17,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MDUyNzA5MSwiaWF0IjoxNzc5OTIyMjkxLCJqdGkiOiJjYzZlNjdmYTdmM2Y0MGY4ODE2ZTFmOWQ3ODYxOWUwZCIsInVzZXJfaWQiOiI0MDUwYzdiMy1mMWU0LTQyNTMtYmIxZC02YmEyZDk3NjQ5YTMifQ.pGBRmdQrto-zuns7OGQi6xM6UBlp2_rNqZGMzaqfZYg','2026-05-27 22:51:31.863297','2026-06-03 22:51:31.000000','4050c7b3f1e44253bb1d6ba2d97649a3','cc6e67fa7f3f40f8816e1f9d78619e0d'),(18,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MDc5NjA3MiwiaWF0IjoxNzgwMTkxMjcyLCJqdGkiOiI2YTRiM2VkNGQwZmI0ODA4YmQ4YWQ5Y2VhOGQ1YTU2MyIsInVzZXJfaWQiOiI0MDUwYzdiMy1mMWU0LTQyNTMtYmIxZC02YmEyZDk3NjQ5YTMifQ.py22EAz5FWcqfdZ-V8O0Z8BM0_1Rdxv0JtqUYu12ERM','2026-05-31 01:34:32.941388','2026-06-07 01:34:32.000000','4050c7b3f1e44253bb1d6ba2d97649a3','6a4b3ed4d0fb4808bd8ad9cea8d5a563'),(19,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MDkyNDUwMCwiaWF0IjoxNzgwMzE5NzAwLCJqdGkiOiJmM2JiNDE3NDQ3YTE0NDUzOWJmZjM0ZmFlMmI3Y2Y5OSIsInVzZXJfaWQiOiI3YTI1OTk5OS00ODRmLTQ5NGUtODU4Ny00YmM4MDYxMWQzOWEifQ.VriWXhqpzn4J8ymc0X9DhKZRglu2adUrISLbSG9Tejw','2026-06-01 13:15:00.585225','2026-06-08 13:15:00.000000',NULL,'f3bb417447a144539bff34fae2b7cf99'),(20,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MTU1NDg1MSwiaWF0IjoxNzgwOTUwMDUxLCJqdGkiOiIyYzhhNjViY2MyNWI0MDBhYWNlZTU3OTY3NGJkMTQwMCIsInVzZXJfaWQiOiI0MDUwYzdiMy1mMWU0LTQyNTMtYmIxZC02YmEyZDk3NjQ5YTMifQ.b3bU4DLyUvg_66Dt_N8fvsKpNKxu926a6D2wXZpErK4','2026-06-08 20:20:51.703614','2026-06-15 20:20:51.000000','4050c7b3f1e44253bb1d6ba2d97649a3','2c8a65bcc25b400aacee579674bd1400'),(21,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MTY0MDQ0MSwiaWF0IjoxNzgxMDM1NjQxLCJqdGkiOiI1YWI3MGYwYzZhMWU0ODc4OWZiYmUxYzhlOGQ3ZmQxZCIsInVzZXJfaWQiOiI0MDUwYzdiMy1mMWU0LTQyNTMtYmIxZC02YmEyZDk3NjQ5YTMifQ.GphgMPZNW_RIPS53pUNXgTOEzZ7UDe306aD_Rc7KXdE','2026-06-09 20:07:21.211067','2026-06-16 20:07:21.000000','4050c7b3f1e44253bb1d6ba2d97649a3','5ab70f0c6a1e48789fbbe1c8e8d7fd1d'),(22,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MTY0Mzk3NCwiaWF0IjoxNzgxMDM5MTc0LCJqdGkiOiI4OTc1MmZkMDU0NWU0NTBjYTMyMjEzZmFhYWEwNjNhMCIsInVzZXJfaWQiOiI0MDUwYzdiMy1mMWU0LTQyNTMtYmIxZC02YmEyZDk3NjQ5YTMifQ.bhmsHfVjSqxXY2m8jPhyewZ36n1nYSgg-2niYwhHD00','2026-06-09 21:06:14.350672','2026-06-16 21:06:14.000000','4050c7b3f1e44253bb1d6ba2d97649a3','89752fd0545e450ca32213faaaa063a0'),(23,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MTY0NDQ1NCwiaWF0IjoxNzgxMDM5NjU0LCJqdGkiOiJjZjQ5MTViZDE5NjE0OWExYWE2YzliOTJmYTAzZGI3YSIsInVzZXJfaWQiOiI0MDUwYzdiMy1mMWU0LTQyNTMtYmIxZC02YmEyZDk3NjQ5YTMifQ.-ZZsgJLNtUYfOwYxvdyMENNx6MBLOB3ZsfiqPXaQBTE','2026-06-09 21:14:14.452368','2026-06-16 21:14:14.000000','4050c7b3f1e44253bb1d6ba2d97649a3','cf4915bd196149a1aa6c9b92fa03db7a'),(24,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MTY0NjExNSwiaWF0IjoxNzgxMDQxMzE1LCJqdGkiOiJiNWZkZjk5MDlkODQ0ZTBjOTY2ZjY5NjBlMjNjNjE1MyIsInVzZXJfaWQiOiI0MDUwYzdiMy1mMWU0LTQyNTMtYmIxZC02YmEyZDk3NjQ5YTMifQ.0L3jfJBGbVdQAgwqT1Mv63DgoM2j5v7u9T1_vfTQ58U','2026-06-09 21:41:55.137129','2026-06-16 21:41:55.000000','4050c7b3f1e44253bb1d6ba2d97649a3','b5fdf9909d844e0c966f6960e23c6153'),(25,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MTY3OTg0MywiaWF0IjoxNzgxMDc1MDQzLCJqdGkiOiIwMWY0ZTE5OTRjMzc0MzcwYmQxN2YzNjY1MjVlMmY4YSIsInVzZXJfaWQiOiI0MDUwYzdiMy1mMWU0LTQyNTMtYmIxZC02YmEyZDk3NjQ5YTMifQ.ybpoT00T8vxwntXsnzYUSecc4ZX_ZUA3n3yN5ZhWu-Q','2026-06-10 07:04:03.797101','2026-06-17 07:04:03.000000','4050c7b3f1e44253bb1d6ba2d97649a3','01f4e1994c374370bd17f366525e2f8a'),(26,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MTY5MzQwOSwiaWF0IjoxNzgxMDg4NjA5LCJqdGkiOiJmMGY5MmIwMDgyZDE0NDNjYjQ4MmNiYTgyYjg4N2QxMiIsInVzZXJfaWQiOiI0MDUwYzdiMy1mMWU0LTQyNTMtYmIxZC02YmEyZDk3NjQ5YTMifQ.6eHNX5Beax19EqkhaDKA6HE2zwCNsb2XrqVq4_TqltA','2026-06-10 10:50:09.645902','2026-06-17 10:50:09.000000','4050c7b3f1e44253bb1d6ba2d97649a3','f0f92b0082d1443cb482cba82b887d12'),(27,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MjEzODEyNCwiaWF0IjoxNzgxNTMzMzI0LCJqdGkiOiI5NzA0NjI1MzA5Mjc0MTkxODdiN2E3MTVmNTgyNDQxYyIsInVzZXJfaWQiOiJmYTQyMTVkNS0yM2VmLTQwYTMtYjkxYi01MmQ5ODhiYTFjNjgifQ.QDuomGxMS64pdVtxfgfFIa6z8TGdl_Z-_30D0c1cvdQ','2026-06-15 14:22:04.943794','2026-06-22 14:22:04.000000','fa4215d523ef40a3b91b52d988ba1c68','970462530927419187b7a715f582441c'),(28,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MjEzOTE5MCwiaWF0IjoxNzgxNTM0MzkwLCJqdGkiOiIzNzcxODc4ZjRhNzQ0MGRjYjNiYjhhZjllZWZlNTVmZSIsInVzZXJfaWQiOiJmYTQyMTVkNS0yM2VmLTQwYTMtYjkxYi01MmQ5ODhiYTFjNjgifQ.Kyalpd2KLUXUGgC-oqeKN6D9KYw19PcASH8obDP_qR4','2026-06-15 14:39:50.825520','2026-06-22 14:39:50.000000','fa4215d523ef40a3b91b52d988ba1c68','3771878f4a7440dcb3bb8af9eefe55fe'),(29,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MjgzMzk3MywiaWF0IjoxNzgyMjI5MTczLCJqdGkiOiJhMmU2MDhlODMyMjI0NDg5YmM4NjJmZDRkNmE3MjhlZiIsInVzZXJfaWQiOiJmYTQyMTVkNS0yM2VmLTQwYTMtYjkxYi01MmQ5ODhiYTFjNjgifQ.mmv6xSICg7uno_j0m2mjquvMRze4AmwJc2cGEPICCYI','2026-06-23 15:39:33.022000','2026-06-30 15:39:33.000000','fa4215d523ef40a3b91b52d988ba1c68','a2e608e832224489bc862fd4d6a728ef');
/*!40000 ALTER TABLE `token_blacklist_outstandingtoken` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-06-24 19:02:21
