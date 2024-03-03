begin;
create table access_logs
(
    request_id uuid primary key,
    host       text                     not null,
    client_ip  inet                     not null,
    time       timestamp with time zone not null,
    method     varchar(10)              not null,
    path       text,
    query      text,
    status     int,
    referer    text,
    user_agent text
);

create index on access_logs (time, host);
create index on access_logs (path);

commit;