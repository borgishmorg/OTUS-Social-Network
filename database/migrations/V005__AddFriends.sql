create table user_friends(
	user_id   uuid references users(id) not null,
	friend_id uuid references users(id) not null,
	primary key (user_id, friend_id)
);
