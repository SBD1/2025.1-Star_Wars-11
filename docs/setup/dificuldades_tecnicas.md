# Dificuldades Técnicas e Soluções Implementadas

## 1. Conflito de Porta PostgreSQL

### Problema
- A porta padrão 5432 estava em uso por uma instância local do PostgreSQL
- Múltiplos processos `postgres.exe` rodando simultaneamente
- Tentativas de conexão falhando

### Solução
- Alteração da porta para 5433 no `docker-compose.yml`
- Manutenção da porta interna como 5432
- Atualização da documentação para refletir a nova porta

## 2. Dependências entre Scripts SQL

### Problema
- Erros de chave estrangeira devido à ordem incorreta de execução
- Tabelas sendo referenciadas antes de serem criadas
- Falha na inicialização do banco

### Solução
- Reorganização dos scripts com prefixos numéricos
- Implementação de ordem específica no `docker-compose.yml`
- Documentação clara da ordem de execução

## 3. Healthcheck e Retry Logic

### Problema
- Aplicação tentando conectar antes do banco estar pronto
- Falhas de conexão durante a inicialização

### Solução
- Implementação de healthcheck no serviço do banco
- Adição de retry logic na aplicação Python
- Configuração de depends_on com condition: service_healthy

## 4. Estado do Banco de Dados

### Problema
- Dúvidas sobre persistência de dados
- Comportamento inconsistente após restarts

### Solução
- Documentação clara sobre uso de volumes
- Instruções específicas para reset do banco
- Diferenciação entre `docker-compose down` e `docker-compose down -v`

## Aprendizados

1. **Importância da Ordem**: A sequência de criação de tabelas é crucial em bancos relacionais
2. **Gestão de Portas**: Necessidade de flexibilidade na configuração de portas
3. **Resiliência**: Implementação de mecanismos de retry e healthcheck
4. **Documentação**: Manter documentação atualizada e clara sobre configurações técnicas

## Melhorias Futuras

- [ ] Script automatizado para verificação de portas em uso
- [ ] Sistema de migrations para gerenciar alterações no banco
- [ ] Ambiente de desenvolvimento separado do de produção
- [ ] Backup automatizado dos dados

## Histórico de Versões

| Versão | Data       | Modificações                      | Autor(es)     | Revisor(es) |
|--------|------------|-----------------------------------|---------------|-------------|
| 1.0    | 12/06/2025 | Criação do documento de dificuldades técnicas             | [Artur Mendonça](https://github.com/ArtyMend07) | [Amanda Abreu](https://github.com/Amandaaaaabreu) e [Eduardo Morais](https://github.com/Edumorais08) |
