drop table if exists bookmarks
create table bookmarks (
    id integer primary key autoincrement,
    title text not null,
    link text not null,
    note text
);