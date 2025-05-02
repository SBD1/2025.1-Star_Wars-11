# Dicionário de Dados - Jogo Star Wars 

### Entidade: Personagem
#### Descrição: Personagem jogável.

| Atributo    | Obrigatoriedade  | Tipo     | Tamanho | Descrição                                       | Exemplo          |
|-------------|------------------|----------|---------|-------------------------------------------------|------------------|
| id_Player   | Obrigatório      | int      | 4       | Identificador único do jogador                  | 1                |
| Dano_Base   | Obrigatório      | int      | 4       | Quantidade de dano que o personagem da          | 40               |
| nome_planeta| Obrigatório      | varchar  | 20      | Referência ao planeta onde o jogador está       | Tatooine         |
| level       | Obrigatório      | int      | 4       | Nível do jogador                                | 12               |
| Vida_Base   | Obrigatório      | int      | 4       | Pontos de vida atuais                           | 85               |
| nome_classe | Obrigatório      | varchar  | 20      | Classe (Jedi, Sith, Caçador, etc.)              | Jedi             |
| xp          | Obrigatório      | int      | 4       | experiência do player                           | 32               |
| gcs         | Obrigatório      | int      | 4       | dinheiro do universo                            | 50               |

---

### Entidade: Classe
#### Descrição: Classe que um personagem pode ter.

| Atributo    | Obrigatoriedade  | Tipo     | Tamanho | Descrição                                       | Exemplo          |
|-------------|------------------|----------|---------|-------------------------------------------------|------------------|
| nome_classe | Obrigatório      | varchar  | 20      | Classe (Jedi, Sith, Caçador, etc.)              | Jedi             |
| Determinação| Obrigatório      | int      | 4       | quanto o jogador está disposto a continuar tentando | 5            |

---

### Entidade: Jedi
#### Descrição: tipo de personagem, com habilidades específicas.

| Atributo    | Obrigatoriedade  | Tipo     | Tamanho | Descrição                                       | Exemplo          |
|-------------|------------------|----------|---------|-------------------------------------------------|------------------|
| nome_classe | Obrigatório      | varchar  | 20      | nome da Classe                                  | Jedi             |
| Force_Heal  | Obrigatório      | BOOLEAN  | 2       | Pode curar com a força                          | true             |
| Force_Vision| Obrigatório      | BOOLEAN  | 2       | Tem visões                                      | true             |
| Defensive_Force_Shield| Obrigatório | BOOLEAN | 2   | Cria escudo de força defensivo                  | true             |    
 
---

### Entidade: Sith
#### Descrição: tipo de personagem, com habilidades específicas.

| Atributo    | Obrigatoriedade  | Tipo     | Tamanho | Descrição                                       | Exemplo          |
|-------------|------------------|----------|---------|-------------------------------------------------|------------------|
| nome_classe | Obrigatório      | varchar  | 20      | nome da Classe                                  | Jedi             |
| Force_Corruption | Obrigatório | BOOLEAN  | 2       | corrompe inimigos com a força                   | true             |
| Force_Lightning | Obrigatório  | BOOLEAN  | 2       | Usa raios da força                              | true             |
| Essence_Transfer| Obrigatório  | BOOLEAN  | 2       | Transfere a essência para outro corpo           | true             |    
 
---

### Entidade: Caçador de Recompensas
#### Descrição: tipo de personagem, com habilidades específicas.

| Atributo    | Obrigatoriedade  | Tipo     | Tamanho | Descrição                                       | Exemplo          |
|-------------|------------------|----------|---------|-------------------------------------------------|------------------|
| nome_classe | Obrigatório      | varchar  | 20      | nome da Classe                                  | Jedi             |
| Arsenal     | Obrigatório      | varchar  | 20      | Lista de armas disponíveis                      | Turbolaser       |
| Master_Tracker | Obrigatório   | BOOLEAN  | 2       | habilidade de rastreamento                      | true             |
| Clocking_Device | Obrigatório  | BOOLEAN  | 2       | Transfere a essência para outro corpo           | true             |    
 
---

### Entidade: Planeta
#### Descrição: Mundos habitáveis, cada um pertencente a um sistema estelar.

| Atributo    | Obrigatoriedade | Tipo    | Tamanho | Descrição                                       | Exemplo      |
|-------------|------------------|---------|---------|-------------------------------------------------|--------------|
| hábitavel   | Obrigatório      | BOOLEAN | 2       | Se o planeta é habitável ou não                 | true         |
| nome_planeta| Obrigatório      | varchar | 40      | Nome do planeta                                 | Tatooine     |
| clima       | Opcional         | text    | -       | Descrição do clima do planeta                   | Planeta desértico|
| id_sistema  | Obrigatório      | int     | 4       | Sistema ao qual o planeta pertence              | 4            |

---

### Entidade: Sistema
#### Descrição: Sistemas estelares que agrupam planetas.

| Atributo    | Obrigatoriedade  | Tipo    | Tamanho | Descrição                                       | Exemplo      |
|-------------|------------------|---------|---------|-------------------------------------------------|--------------|
| id_sistema  | Obrigatório      | varchar | 30      | Sistema ao qual o planeta pertence              | 4            |

---

### Entidade: Nave
#### Descrição: Modelos de naves disponíveis, associadas aos personagens.

| Atributo      | Obrigatoriedade | Tipo    | Tamanho | Descrição                                    | Exemplo           |
|---------------|------------------|---------|---------|----------------------------------------------|-------------------|
| modelo        | Obrigatório      | varchar | 30      | Nome da nave                                 | Falcão Milenar    |
| Id_Player     | Opcional         | int     | 4       | ID do jogador dono da nave                   | 1                 |
| velocidade    | Obrigatório      | int     | 4       | Velocidade da nave                           | 900               |
| capacidade    | Obrigatório      | int     | 4       | Capacidade de carga                          | 1000              |

---

### Entidade: X WING T-65
#### Descrição: Nave de combate ágil e precisa.

| Atributo      | Obrigatoriedade | Tipo    | Tamanho | Descrição                                    | Exemplo           |
|---------------|------------------|---------|---------|----------------------------------------------|-------------------|
| modelo        | Obrigatório      | varchar | 30      | Nome da nave                                 | X WING T-65       |

---

### Entidade: YT - 1300
#### Descrição: Nave de carga versátil

| Atributo      | Obrigatoriedade | Tipo    | Tamanho | Descrição                                    | Exemplo           |
|---------------|------------------|---------|---------|----------------------------------------------|-------------------|
| modelo        | Obrigatório      | varchar | 30      | Nome da nave                                 | YT - 1300         |

---

### Entidade: Fregata Corelliana CR90
#### Descrição: Nave capital de suporte

| Atributo      | Obrigatoriedade | Tipo    | Tamanho | Descrição                                    | Exemplo           |
|---------------|------------------|---------|---------|----------------------------------------------|-------------------|
| modelo        | Obrigatório      | varchar | 30      | Nome da nave                                 | Fregata Corelliana CR90|

---

### Entidade: Lambda-class Shuttle
#### Descrição: Nave de transporte imperial

| Atributo      | Obrigatoriedade | Tipo    | Tamanho | Descrição                                    | Exemplo           |
|---------------|------------------|---------|---------|----------------------------------------------|-------------------|
| modelo        | Obrigatório      | varchar | 30      | Nome da nave                                 | Lambda-class Shuttle|

---

### Entidade: Inventário
#### Descrição: Gerencia os itens possuídos pelos personagens.

| Atributo     | Obrigatoriedade | Tipo     | Tamanho | Descrição                                 | Exemplo       |
|--------------|------------------|----------|---------|--------------------------------------------|---------------|
| Id_PLayerIn  | Obrigatório      | int      | 4       | Identificador do inventário                | 1             |
| Id_Player    | Obrigatório      | int      | 4       | Identificador do jogador                   | 2             |
| Espaco_Maximo| Obrigatório      | int      | 4       | Número máximo de itens                     | 5             |
| Peso_Total   | Obrigatório      | int      | 4       | Peso total carregado                       | 10            |

---

### Entidade: Item
#### Descrição: Objetos que podem ser coletados, utilizados ou comercializados.

| Atributo     | Obrigatoriedade | Tipo    | Tamanho | Descrição                                 | Exemplo       |
|--------------|------------------|---------|---------|--------------------------------------------|---------------|
| id_item      | Obrigatório      | int     | 4       | Identificador do item                      | 1             |
| Peso         | Obrigatório      | int     | 4       | Peso do item                               | 50            |
| tipo         | Obrigatório      | varchar | 20      | Tipo (arma, armadura, recurso, etc.)       | arma          |
| preço        | Opcional         | int     | 4       | Valor monetário em GCS                     | 5000          |

---

### Entidade: Missao
#### Descrição: Tarefas que podem ser aceitas pelos personagens, com recompensas e requisitos.

| Atributo    | Obrigatoriedade | Tipo     | Tamanho | Descrição                                     | Exemplo                |
|-------------|------------------|----------|---------|----------------------------------------------|------------------------|
| Id_Missao   | Obrigatório      | int      | 4       | Identificador único da missão                | 1                      |
| Valor_Recompensa| Obrigatório  | int      | 4       | Recompensa em GCS                            | 45                     |
| Status      | Obrigatório      | varchar  | 20      | Status da missão (ativa/concluída)           | concluída              |
| nome_planeta| Obrigatório      | varchar  | 20      | Referência ao planeta onde a missão  está    | Tatooine               |
| Id_npc      | Obrigatório      | int      | 4       | NPC que oferece a missão                     | 1                      |
| Level_Minimo| Obrigatório      | int      | 4       | Level mínimo para aceitar a missão           | 10              |

---

### Entidade: NPC 
#### Descrição: Personagens não jogáveis, podendo ser mercantes ou mecânicos.

| Atributo     | Obrigatoriedade | Tipo     | Tamanho | Descrição                                 | Exemplo           |
|--------------|------------------|----------|---------|--------------------------------------------|-------------------|
| id_npc       | Obrigatório      | int      | 4       | Identificador do npc                       | 10                |
| nome_planeta | Obrigatório      | varchar  | 20      | Referência ao planeta onde o npc     está  | Tatooine          |

---

### Entidade: Mercante 
#### Descrição: NPCs que vendem itens.

| Atributo     | Obrigatoriedade | Tipo     | Tamanho | Descrição                                 | Exemplo           |
|--------------|------------------|----------|---------|--------------------------------------------|-------------------|
| id_npc       | Obrigatório      | int      | 4       | Identificador do npc                       | 10                |
| itens_disponíveis | Obrigatório | varchar  | 20      | Lista de itens disponíveis                 | arma              |

---

### Entidade: Mecânico 
#### Descrição: NPCs que oferecem serviços.

| Atributo     | Obrigatoriedade | Tipo     | Tamanho | Descrição                                 | Exemplo           |
|--------------|------------------|----------|---------|--------------------------------------------|-------------------|
| id_npc       | Obrigatório      | int      | 4       | Identificador do npc                       | 10                |
| serviços_disponíveis | Obrigatório | varchar  | 20   | Lista de serviços disponíveis              | arma              |

---

### Entidade: MOB
#### Descrição: Inimigos do jogo, classificados em normal, elite ou boss.

| Atributo     | Obrigatoriedade | Tipo     | Tamanho | Descrição                                 | Exemplo           |
|--------------|------------------|----------|---------|--------------------------------------------|-------------------|
| id_mob       | Obrigatório      | int      | 4       | Identificador do mob                       | 10                |
| Dano_Base    | Obrigatório      | int      | 4       | Dano base do mob                           | 50                |
| Vida_Base    | Obrigatório      | int      | 4       | Vida base do mob                           | 150               |
| Xp           | Obrigatório      | int      | 4       | Experiência concedida ao ser derrotado     | 15                |
| nome_planeta | Obrigatório      | varchar  | 20      | Referência ao planeta onde o mob     está  | Tatooine          |
| level        | Obrigatório      | int      | 4       | Nível do mob                               | 20                |
| GCS          | Obrigatório      | int      | 4       | GCS concedido ao ser derrotado             | 15                |

---

### Entidade: Inventário_IA
#### Descrição: Gerencia os itens possuídos pelo MOB.

| Atributo     | Obrigatoriedade | Tipo     | Tamanho | Descrição                                 | Exemplo       |
|--------------|------------------|----------|---------|--------------------------------------------|---------------|
| Id_IAIn      | Obrigatório      | int      | 4       | Identificador do inventário do MOB         | 1             |
| id_mob       | Obrigatório      | int      | 4       | Identificador do mob                       | 10            |
| Espaco_Maximo| Obrigatório      | int      | 4       | Número máximo de itens                     | 5             |

--- 

### Entidade: Normal
#### Descrição: Subtipo de MOB comum.

| Atributo     | Obrigatoriedade | Tipo     | Tamanho | Descrição                                 | Exemplo           |
|--------------|------------------|----------|---------|--------------------------------------------|-------------------|
| id_mob       | Obrigatório      | int      | 4       | Identificador do mob                       | 10                |

---

### Entidade: Elite
#### Descrição: Subtipo de MOB com buffs especiais.

| Atributo     | Obrigatoriedade | Tipo     | Tamanho | Descrição                                 | Exemplo           |
|--------------|------------------|----------|---------|--------------------------------------------|-------------------|
| id_mob       | Obrigatório      | int      | 4       | Identificador do mob                       | 10                |
| Buff_Especial| Obrigatório      | BOOLEAN  | 2       | Buff especial do MOB elite                 | true              |

---

### Entidade: Boss
#### Subtipo de MOB com habilidades especiais e recompensas raras.

| Atributo     | Obrigatoriedade | Tipo     | Tamanho | Descrição                                 | Exemplo           |
|--------------|------------------|----------|---------|--------------------------------------------|-------------------|
| id_mob       | Obrigatório      | int      | 4       | Identificador do mob                       | 10                |
| Habilidade_Especial| Obrigatório| BOOLEAN  | 2       | habilidade especial do MOB boss            | true              |
| Drop_Raro    | Obrigatório      | varchar  | 20      | Itens especiais que podem ser dropados     | arma              |

---

## Histórico de Versões

| Versão | Data       | Modificações                                      | Autor(es)     | Revisor(es) |
|--------|------------|---------------------------------------------------|---------------|-------------|
| 1.0    | 02/05/2025 | Criação do documento de modelo relacional | [Eduardo Morais](https://github.com/Edumorais08), [Renan Pariz](https://github.com/renanpariiz) | [Artur Mendonça](https://github.com/ArtyMend07) |



