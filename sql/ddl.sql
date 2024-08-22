DROP TABLE IF EXISTS sess CASCADE;
DROP TABLE IF EXISTS sess_msg_link CASCADE;
DROP TABLE IF EXISTS msg_roles CASCADE;
DROP TABLE IF EXISTS msg CASCADE;

CREATE TABLE sess (
	sess_id SERIAL PRIMARY KEY,
	session_id UUID UNIQUE NOT NULL,
	total_tokens INTEGER
);

CREATE TABLE msg_roles (
	role_id SERIAL PRIMARY KEY,
	role_name TEXT NOT NULL
);


CREATE TABLE msg (
	message_id SERIAL PRIMARY KEY,
	message_content TEXT NOT NULL,
	role_id INTEGER NOT NULL,
	created_at TIMESTAMPTZ DEFAULT current_timestamp,
	FOREIGN KEY (role_id) REFERENCES msg_roles (role_id)
);

CREATE TABLE sess_msg_link (
	link_id SERIAL PRIMARY KEY,
	sess_id INTEGER NOT NULL,
	message_id INTEGER NOT NULL,
	FOREIGN KEY (sess_id) REFERENCES sess (sess_id) ON DELETE CASCADE,
	FOREIGN KEY (message_id) REFERENCES msg (message_id) ON DELETE CASCADE
);

INSERT INTO msg_roles (role_name)
VALUES
	('system'),
	('user'),
	('assistant');