create table users(
	id uuid primary key default gen_random_uuid(),
	first_name text not null,
	second_name text not null,
	birthdate date not null,
	biography text not null,
	city text not null,
	password_hash bytea not null
);
