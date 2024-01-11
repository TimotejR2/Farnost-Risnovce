INSERT INTO sessions (user_id, session, valid, ip_address) 
VALUES (
    (SELECT user_id FROM users WHERE user_name = %s LIMIT 1), 
    %s, 
    %s, 
    %s
);
