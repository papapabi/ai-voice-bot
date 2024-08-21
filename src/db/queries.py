CHECK_SESSION_EXISTS = """
SELECT 1 FROM sess WHERE session_id = %s LIMIT 1
"""

GET_ALL_MESSAGES_BY_SESSION_ID = """
SELECT 
    msg.message_content AS content,
    msg_roles.role_name AS role
FROM sess
JOIN sess_msg_link ON sess.sess_id = sess_msg_link.sess_id
JOIN msg ON sess_msg_link.message_id = msg.message_id
JOIN msg_roles ON msg.role_id = msg_roles.role_id
WHERE sess.session_id = %s;
"""

GET_N_MOST_RECENT_MESSAGES_BY_SESSION_ID = """
SELECT 
    msg.message_content AS content,
    msg_roles.role_name AS role
FROM sess
JOIN sess_msg_link ON sess.sess_id = sess_msg_link.sess_id
JOIN msg ON sess_msg_link.message_id = msg.message_id
JOIN msg_roles ON msg.role_id = msg_roles.role_id
WHERE sess.session_id = %s
ORDER BY msg.created_at DESC
LIMIT %s;
"""

INSERT_SESS = """
INSERT INTO sess (session_id)
VALUES (%s)
RETURNING sess_id
"""

INSERT_TOTAL_TOKENS = """
INSERT INTO sess (total_tokens)
VALUES (%s)
"""

GET_ROLE_ID = """
SELECT role_id
FROM msg_roles
WHERE role_name = %s
"""

GET_SESS_ID = """
SELECT sess_id
FROM sess
WHERE session_id = %s
"""

INSERT_MSG = """
INSERT INTO msg (message_content, role_id)
VALUES (%s, %s)
RETURNING message_id
"""

INSERT_SESS_MSG_LINK = """
INSERT INTO sess_msg_link (sess_id, message_id)
VALUES (%s, %s)
"""

DELETE_SESS_MSG_LINK = """
DELETE FROM sess_msg_link
USING sess
WHERE sess_msg_link.sess_id = sess.sess_id
AND sess.session_id = %s
"""

DELETE_MSG = """
DELETE FROM msg
WHERE msg.message_id IN (
    SELECT msg.message_id
    FROM msg
    LEFT JOIN sess_msg_link ON msg.message_id = sess_msg_link.message_id
    WHERE sess_msg_link.message_id IS NULL
)
"""

DELETE_SESS = """
DELETE FROM sess
WHERE session_id = %s
"""
