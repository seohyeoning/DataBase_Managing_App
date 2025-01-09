-- Role과 User 추가와 삭제
-- 1. user1 이라는 새로운 계정을 생성
use library_db;
create user 'user1'@'localhost' identified by '1user'; -- identified by ' ' 이 계정에 대한 패스워드
grant all privileges on library_db.* to 'user1'@'localhost';

