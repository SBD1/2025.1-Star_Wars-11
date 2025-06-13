SELECT p.id_player, 
       p.vida_base, 
       p.level, 
       p.dano_base, 
       p.xp, 
       p.gcs,
       p.nome_classe,
       p.nome_planeta,
       c.Determinacao
FROM Personagem p
LEFT JOIN Classe c ON p.nome_classe = c.nome_classe;