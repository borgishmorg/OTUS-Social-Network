CREATE INDEX users_lower_first_name_collate_c_idx ON users(lower(first_name) COLLATE "C");
CREATE INDEX users_lower_second_name_collate_c_idx ON users(lower(second_name) COLLATE "C");
