/*
SQLyog Ultimate v12.08 (64 bit)
MySQL - 8.0.36 
*********************************************************************
*/
/*!40101 SET NAMES utf8 */;

create table `financial_user` (
	`id` bigint (20),
	`character` varchar (150),
	`character_code` varchar (150),
	`create_at` datetime ,
	`update_at` datetime ,
	`create_user` varchar (60),
	`update_user` varchar (60),
	`yu` int (11)
); 
