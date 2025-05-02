@"
## 📌 Descrição

Descreva brevemente o que essa PR faz e por quê.

## ✅ Tipo de mudança

- [ ] Bug fix
- [ ] Nova feature
- [ ] Refatoração
- [ ] Documentação
- [ ] Testes
- [ ] Outra (descreva):

## 🧪 Como testar

Descreva como testar essa alteração, comandos, rotas, exemplos etc.

## 🔗 Issue relacionada

Relacione a issue (se houver):
Closes #número_da_issue

## 📷 Capturas de tela (se aplicável)

Adicione imagens para facilitar a revisão.

## 📋 Checklist

- [ ] O código segue o padrão do projeto
- [ ] Testei localmente
- [ ] Atualizei a documentação
- [ ] Não quebrei nada que estava funcionando
"@ | Out-File -FilePath .github\pull_request_template.md -Encoding utf8
