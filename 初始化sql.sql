
use book;
-- 用户表
create table if not exists User(
    user_id integer primary key auto_increment,
    user_name varchar(20) unique not null ,
    user_type tinyint not null,
    passwd char(64) not null
);
-- 图书信息表
create table if not exists BookInfo(
    book_info_id bigint primary key auto_increment,
    author varchar(50),
    book_name varchar(60) not null,
    publish_house varchar(60) not null,
    book_amounts int default 0 check ( book_amounts>=0 ),
    book_score float4 default null check ( book_score>=0 and book_score<=10)
);
-- 图书表
create table if not exists Book(
    book_id bigint primary key auto_increment, -- 书籍编号
    book_info_id bigint, -- 书籍id
    is_borrowed char(4) default '否' not null, -- 是否借出
    constraint bookInfoFk foreign key(book_info_id)
                 references BookInfo(book_info_id) on delete cascade
);

-- 借阅表
create table if not exists Borrow(
    user_id integer not null ,
    book_id bigint not null ,
    primary key (user_id,book_id),
    constraint BorBookFk foreign key (book_id)
                                 references Book(book_id) on delete cascade ,
    constraint BorUserFk foreign key (user_id)
                                 references User(user_id)
        on delete cascade on update cascade
);
-- 图书评价表
create table if not exists Evaluation(
    user_id integer,
    book_info_id bigint,
    scores tinyint not null,
    primary key (user_id,book_info_id),
    constraint UidFk foreign key (user_id)
        references User(user_id) on delete cascade on update cascade,
    constraint BInfoFk foreign key (book_info_id)
        references BookInfo(book_info_id) on delete cascade
);
-- 索引
create unique index BookInfoIdIndex on BookInfo(book_info_id);
create index  BookNameIndex on BookInfo(book_name);

create unique index BookIdIndex on Book(book_id);

-- 视图
create view  DetailBookInfo as
    select BookInfo.book_info_id as infoid,book_id,book_name,author,
           publish_house,book_amounts,book_score,is_borrowed from BookInfo,Book
        where BookInfo.book_info_id=Book.book_info_id;

create view BorrowInfo as
select User.user_name,Book.book_id as bookId,book_name,author,publish_house from User,Borrow,BookInfo,Book
    where Book.book_id=Borrow.book_id
        and Book.book_info_id=BookInfo.book_info_id
        and User.user_id=Borrow.user_id;


-- 存储过程

-- 删除单本书籍
create procedure if not exists delDetailBook(in bookId bigint)
    begin
        declare num int default 0;
        declare infoId bigint default -1;
         select book_info_id into infoId from Book where book_id=bookId limit 1;
        select count(book_info_id) into num from Book where book_info_id=infoId;
        if num>0 then
        -- 删除书籍
        delete from Book where book_id=bookId;
        -- 修正数量
        update BookInfo set book_amounts=num-1 where book_info_id=infoId;
        end if;
    end;

create procedure if not exists borrowBook(in bookId bigint,in userId integer)
    begin
        insert into Borrow (book_id,user_id) values (bookId,userId);
        update Book set is_borrowed='是' where book_id=bookId;
    end;

create procedure if not exists returnBook(in bookId bigint,in userId integer)
    begin
        delete from Borrow where book_id=bookId and user_id=userId;
        update Book set is_borrowed='否' where book_id=bookId;
    end;








-- 触发器
-- 添加评分时触发
create trigger if not exists insert_eval after insert
    on Evaluation for each row
    begin
        declare avg_s float4 default 0.0;
        select avg(scores) into avg_s from Evaluation where book_info_id=NEW.book_info_id;
        update BookInfo set book_score=avg_s where book_info_id=NEW.book_info_id;
    end;

-- 修改评分时触发
create trigger if not exists update_eval after update
    on Evaluation for each row
    begin
        declare avg_s float4 default 0.0;
        select avg(scores) into avg_s from Evaluation where book_info_id=NEW.book_info_id;
        update BookInfo set book_score=avg_s where book_info_id=NEW.book_info_id;
    end;
