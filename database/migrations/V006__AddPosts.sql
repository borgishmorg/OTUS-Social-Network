create table posts(
	id uuid primary key default gen_random_uuid(),
	user_id uuid references users(id) not null,
	text    text not null
);
