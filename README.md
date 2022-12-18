# nyj_board_crawl
남양주시립박물관 사이트 크롤링

Table Script
```
CREATE TABLE `board_nyj` ( 
  `SEQ` int(11) NOT NULL AUTO_INCREMENT COMMENT '시퀀스', 
  `BD_NUMBER` int(11) NOT NULL COMMENT '글번호', 
  `LINK_URL` varchar(200) DEFAULT NULL COMMENT 'URL', 
  `TITLE` varchar(200) NOT NULL COMMENT '제목', 
  `WRITER` varchar(50) DEFAULT NULL COMMENT '작성자', 
  `CONTENT` text COMMENT '내용', 
  `READ_COUNT` int(11) NOT NULL COMMENT '조회수', 
  `REG_DATE` VARCHAR(50) NOT NULL COMMENT '등록일', 
  `ATTACH_URL` varchar(2000) DEFAULT NULL COMMENT '첨부파일 URL', 
  PRIMARY KEY (`SEQ`) 
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=UTF8;
```
