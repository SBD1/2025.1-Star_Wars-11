## Dicionário de Dados - Jogo Star Wars MUD

### Entidade: Jogador

| Atributo    | Obrigatoriedade | Tipo     | Tamanho | Descrição                                       | Exemplo          |
|-------------|------------------|----------|---------|-------------------------------------------------|------------------|
| id_jogador  | Obrigatório      | int      | 4       | Identificador único do jogador                  | 1                |
| nome        | Obrigatório      | varchar  | 50      | Nome do personagem                              | Raan Vos         |
| planeta_atual | Obrigatório    | int      | 4       | Referência ao planeta onde o jogador está       | 3                |
| nivel       | Obrigatório      | int      | 4       | Nível de experiência                            | 12               |
| pontos_vida | Obrigatório      | int      | 4       | Pontos de vida atuais                           | 85               |
| classe      | Obrigatório      | varchar  | 20      | Classe (Jedi, Sith, Caçador, etc.)              | Jedi             |
| faccao      | Opcional         | varchar  | 20      | Nome da facção (se aplicável)                   | Nova República   |

---

### Entidade: Planeta

| Atributo    | Obrigatoriedade | Tipo    | Tamanho | Descrição                                       | Exemplo      |
|-------------|------------------|---------|---------|-------------------------------------------------|--------------|
| id_planeta  | Obrigatório      | int     | 4       | Identificador único do planeta                  | 3            |
| nome        | Obrigatório      | varchar | 40      | Nome do planeta                                 | Tatooine     |
| descricao   | Opcional         | text    | -       | Descrição do planeta                            | Planeta desértico |
| sistema     | Opcional         | varchar | 30      | Sistema estelar                                 | Arkanis       |

---

### Entidade: Nave

| Atributo      | Obrigatoriedade | Tipo    | Tamanho | Descrição                                    | Exemplo           |
|---------------|------------------|---------|---------|----------------------------------------------|-------------------|
| id_nave       | Obrigatório      | int     | 4       | Identificador único da nave                  | 1                 |
| nome          | Obrigatório      | varchar | 30      | Nome da nave                                 | Falcão Milenar    |
| jogador_id    | Opcional         | int     | 4       | ID do jogador dono da nave                   | 1                 |
| velocidade    | Obrigatório      | int     | 4       | Velocidade da nave                           | 900               |
| capacidade    | Obrigatório      | int     | 4       | Capacidade de carga                          | 1000              |

---

### Entidade: Inventário

| Atributo     | Obrigatoriedade | Tipo     | Tamanho | Descrição                                 | Exemplo       |
|--------------|------------------|----------|---------|--------------------------------------------|---------------|
| id_inventario| Obrigatório      | int      | 4       | Identificador do inventário                | 1             |
| jogador_id   | Obrigatório      | int      | 4       | Identificador do jogador                   | 1             |

---

### Entidade: Item

| Atributo     | Obrigatoriedade | Tipo    | Tamanho | Descrição                                 | Exemplo       |
|--------------|------------------|---------|---------|--------------------------------------------|---------------|
| id_item      | Obrigatório      | int     | 4       | Identificador do item                      | 1             |
| nome         | Obrigatório      | varchar | 40      | Nome do item                               | Sabre de Luz  |
| tipo         | Obrigatório      | varchar | 20      | Tipo (arma, armadura, recurso, etc.)       | arma          |
| valor        | Opcional         | int     | 4       | Valor monetário em créditos                | 5000          |

---

### Entidade: Inventario_Item

| Atributo       | Obrigatoriedade | Tipo | Tamanho | Descrição                                | Exemplo |
|----------------|------------------|------|---------|-------------------------------------------|---------|
| inventario_id  | Obrigatório      | int  | 4       | ID do inventário                          | 1       |
| item_id        | Obrigatório      | int  | 4       | ID do item                                | 2       |
| quantidade     | Obrigatório      | int  | 4       | Quantidade do item                        | 3       |

---

### Entidade: Missao

| Atributo    | Obrigatoriedade | Tipo     | Tamanho | Descrição                                    | Exemplo               |
|-------------|------------------|----------|---------|-----------------------------------------------|------------------------|
| id_missao   | Obrigatório      | int      | 4       | Identificador único da missão                | 1                      |
| nome        | Obrigatório      | varchar  | 60      | Nome da missão                               | Escolta no Sistema Hoth |
| descricao   | Opcional         | text     | -       | Descrição detalhada da missão                | Proteger o comboio     |
| planeta_id  | Obrigatório      | int      | 4       | Planeta onde ocorre a missão                 | 2                      |

---

### Entidade: Personagem (NPC ou Inimigo)

| Atributo     | Obrigatoriedade | Tipo     | Tamanho | Descrição                                 | Exemplo           |
|--------------|------------------|----------|---------|--------------------------------------------|-------------------|
| id_personagem| Obrigatório      | int      | 4       | Identificador do personagem                | 10                |
| nome         | Obrigatório      | varchar  | 50      | Nome do personagem                         | Darth Vader       |
| tipo         | Obrigatório      | varchar  | 15      | Tipo (NPC ou Inimigo)                      | Inimigo           |
| planeta_id   | Opcional         | int      | 4       | Planeta onde ele pode ser encontrado       | 4                 |
| nivel        | Opcional         | int      | 4       | Nível de dificuldade/combate               | 20                |

---

### Entidade: Viagem

| Atributo      | Obrigatoriedade | Tipo | Tamanho | Descrição                                   | Exemplo |
|---------------|------------------|------|---------|----------------------------------------------|---------|
| id_viagem     | Obrigatório      | int  | 4       | Identificador da viagem                      | 1       |
| jogador_id    | Obrigatório      | int  | 4       | Jogador que iniciou a viagem                 | 1       |
| origem_id     | Obrigatório      | int  | 4       | ID do planeta de origem                      | 3       |
| destino_id    | Obrigatório      | int  | 4       | ID do planeta de destino                     | 5       |
| tempo_voo     | Obrigatório      | int  | 4       | Tempo estimado de viagem (em segundos)       | 120     |

---

### Entidade: PvP

| Atributo        | Obrigatoriedade | Tipo | Tamanho | Descrição                                | Exemplo |
|------------------|------------------|------|---------|-------------------------------------------|---------|
| id_pvp          | Obrigatório      | int  | 4       | Identificador do combate PvP              | 1       |
| jogador_1_id    | Obrigatório      | int  | 4       | ID do jogador atacante                    | 1       |
| jogador_2_id    | Obrigatório      | int  | 4       | ID do jogador defensor                    | 2       |
| vencedor_id     | Opcional         | int  | 4       | ID do jogador vencedor                    | 1       |
