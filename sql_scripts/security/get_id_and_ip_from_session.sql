SELECT user_id, ip_address
    FROM sessions 
    WHERE session = %s AND valid > %s::timestamp;

