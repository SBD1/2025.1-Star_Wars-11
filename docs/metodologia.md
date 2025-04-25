# Metodologia do Projeto – Banco de Dados (Star Wars)

## Introdução

Este documento descreve a metodologia adotada pelo grupo para o desenvolvimento do trabalho de modelagem de banco de dados voltado para um **jogo ambientado no universo de Star Wars**. Após a análise das necessidades do projeto e das práticas de desenvolvimento ágil, optamos por utilizar o **Scrum**, dada sua capacidade de organizar e evoluir projetos de forma incremental, promovendo transparência e colaboração entre os membros da equipe.

O Scrum possibilita entregas frequentes e feedback contínuo, facilitando os ajustes necessários durante a modelagem, implementação e otimização do banco de dados.

## Escopo da Metodologia

Este documento contempla:
- A definição da metodologia adotada.
- A estrutura e os papéis atribuídos no Scrum.
- Os fluxos de trabalho e os padrões/convenções utilizados na gestão dos artefatos, como controle de versão com Github.
- Os processos para criação e gerenciamento de issues e pull requests.

**O que é Scrum?**  
Scrum é um framework ágil para o gerenciamento e desenvolvimento de projetos, estruturado em ciclos de trabalho chamados *sprints*. Cada sprint permite uma entrega incremental do produto, promovendo feedback constante e adaptação rápida às necessidades do projeto. O Scrum valoriza a colaboração, a transparência e a adaptabilidade, fatores essenciais para o desenvolvimento eficaz do banco de dados deste jogo.

## Abordagem e Estrutura do Scrum

No Scrum, o trabalho é dividido em ciclos curtos (*sprints*) que facilitam a revisão constante e a entrega incremental do produto. Para este projeto, os papéis foram definidos da seguinte forma:

- **Scrum Master:**  
  - **Artur Mendonça**  
  - Responsável por facilitar os processos, remover impedimentos e assegurar a aplicação correta dos princípios do Scrum.

- **Equipe de Desenvolvimento:**  
  - Composta pelos demais membros do grupo, que executam as atividades de modelagem, implementação e documentação do banco de dados.

## Padrões e Convenções de Desenvolvimento

Para manter a qualidade e a rastreabilidade dos artefatos, adotamos as seguintes práticas:

- **GitHub:**
  - **Pull Requests (PRs):** Alterações são submetidas via PRs para permitir a revisão colaborativa e garantir a integração contínua das modificações.
  - **Issues:** Utilizadas para reportar e gerenciar tarefas, bugs e solicitações de melhorias, contendo descrições detalhadas e critérios de aceitação.
  - **Branches:** Nomeadas conforme o padrão `<tipo>/<descricao-breve>`, por exemplo, `docs/modelo-entidade-relacionamento` ou `feat/normalizacao-tabelas`.
  - **Histórico de Versões:** Atualizado de forma padronizada para documentar as mudanças realizadas, bem como os responsáveis por elas.

- **Tipos de Branches – Padrões Comuns**

| Tipo        | Uso                                                   | Exemplo                               |
|-------------|--------------------------------------------------------|---------------------------------------|
| `feat`      | Adição de nova funcionalidade                          | `feat/adicionar-tabela-personagens`  |
| `fix`       | Correção de bugs                                       | `fix/erro-relacionamento-planetas`   |
| `docs`      | Atualizações na documentação                           | `docs/diagrama-er`                   |
| `style`     | Mudanças de estilo (semântica, formatação, etc)        | `style/ajuste-formatacao-sql`        |
| `refactor`  | Refatorações (sem mudança de comportamento)            | `refactor/otimizar-consultas`        |
| `test`      | Inclusão ou modificação de testes                      | `test/teste-integridade-tabelas`     |
| `chore`     | Tarefas de manutenção (ex: dependências, configs)      | `chore/configuracao-banco`           |
| `hotfix`    | Correção urgente diretamente em produção               | `hotfix/corrige-chave-estrangeira`   |

Fonte: Tabela elaborada pelo autor – Artur, 2025.

- **Commits:**  
  As mensagens de commit seguem um padrão similar ao das branches, utilizando `:` como separador:
  - `docs: atualizar documentação do modelo lógico`
  - `feat: criar tabela de facções`
  - `bugfix: corrigir relacionamento entre jedis e sabres`

- **Labels Padrão:**  
  Utilizadas para categorizar e priorizar issues e PRs:
  - `documentation`, `bug`, `duplicate`, `enhancement`, `good first issue`, `help wanted`, `invalid`, `question`, `wontfix`, `ata`, `ponto de controle`.

## Gestão de Issues e Pull Requests

### Criação de Issues

As issues seguem template localizado em `.github/ISSUE_TEMPLATE/`. Devem conter:

1. **Título claro e descritivo**
2. **Descrição detalhada**
3. **Checklist de tarefas**
4. **Labels apropriadas**
5. **Responsáveis**
6. **Prazo de entrega**
7. **Pull Request vinculado**

### Hierarquia de Issues

- **Issues Mães (Parent Issues):**  
  - Representam entregas maiores, como modelagem conceitual ou criação do banco.  
  - Ex: "Entrega Final – Banco de Dados"

- **Issues Filhas (Child Issues):**  
  - Detalham as subtarefas, como "Criar modelo entidade-relacionamento".


### Pull Requests (PRs)

Devem:

1. Explicar claramente as mudanças
2. Designar revisores
3. Incluir prints ou diagramas, se aplicável


## Referências Bibliográficas

- Schwaber, K.; Sutherland, J. *The Scrum Guide*. Disponível em: [https://www.scrumguides.org/](https://www.scrumguides.org/)
- Rubin, K. S. *Essential Scrum*. Addison-Wesley, 2012.
- Sommerville, I. *Engenharia de Software*, 9ª ed. Pearson, 2019.
- GITHUB. *Docs – Issues e Pull Requests*. [https://docs.github.com/en/issues](https://docs.github.com/en/issues)
- Chacon, S.; Straub, B. *Pro Git*. Apress, 2014. [https://git-scm.com/book/en/v2](https://git-scm.com/book/en/v2)
- ATLASSIAN. *Linking Issues*. [https://support.atlassian.com/jira-software-cloud/docs/link-issues/](https://support.atlassian.com/jira-software-cloud/docs/link-issues/)
- CONVENTIONAL COMMITS. [https://www.conventionalcommits.org/](https://www.conventionalcommits.org/)
- IEEE. *IEEE Standard for Software Reviews and Audits*, 1028-2008. [https://standards.ieee.org/standard/1028-2008.html](https://standards.ieee.org/standard/1028-2008.html)

## Histórico de Versões

| Versão | Data       | Modificações                                      | Autor(es)     | Revisor(es) |
|--------|------------|---------------------------------------------------|---------------|-------------|
| 1.0    | 25/04/2025 | Criação do documento de metodologia  | [Artur Mendonça](https://github.com/ArtyMend07) |  [Eduardo Morais](https://github.com/Edumorais08) | 
