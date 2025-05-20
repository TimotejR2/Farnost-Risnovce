SELECT DISTINCT
    d.id            AS datum_id,
    d.datum,
    d.nazov         AS nazov_dna,
    u.cas,
    u.miesto,
    u.popis         AS udalost_popis
FROM oznamy_datum d
LEFT JOIN oznamy_udalost u 
    ON d.id = u.datum_id
WHERE d.tyzden_id = (SELECT MAX(tyzden_id) FROM oznamy_datum)
ORDER BY d.datum, u.cas;

