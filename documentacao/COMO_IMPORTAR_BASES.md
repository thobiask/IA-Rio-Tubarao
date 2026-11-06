# Importação dos dados hidrológicos pendentes

**Situação:** o GitHub contém documentação, códigos e métricas; as oito bases hidrológicas grandes ainda precisam ser transferidas.

## Pacotes disponíveis na conversa
- `IA_Rio_Tubarao_GitHub_organizado.zip`: scripts, resultados, documentação, inventário e cópias dos CSVs.
- `IA_Rio_Tubarao_bases_hidrologicas_8_arquivos.zip`: oito bases CSV em `dados/chuva/` e `dados/processados/`.
- `Enviar_IA_Rio_Tubarao_GitHub.ps1`: importador Windows que preserva arquivos existentes, compara SHA-256 e envia apenas os ausentes à branch `revisao-inicial`.

## Como executar no Windows
1. Baixar os dois ZIPs e o script PowerShell da conversa para a pasta **Downloads**, sem renomeá-los.
2. Clonar `thobiask/IA-Rio-Tubarao` pelo GitHub Desktop; abrir a branch `revisao-inicial`.
3. Abrir PowerShell na pasta Downloads e executar:

```powershell
powershell -ExecutionPolicy Bypass -File .\Enviar_IA_Rio_Tubarao_GitHub.ps1 -RepositorioLocal "C:\CAMINHO\IA-Rio-Tubarao"
```

4. Confirmar o resultado no Pull Request #1.

O importador não sobrescreve arquivos diferentes que já existam no repositório, não faz merge e não altera `main`. Arquivos divergentes são listados para revisão posterior. Antes de publicar fora do repositório privado, auditar procedência e termos de redistribuição.

**Nota de integridade:** o inventário em `inventario/BASES_HIDROLOGICAS_PENDENTES.md` contém os hashes SHA-256 esperados das oito bases. Após o envio, conferir cada arquivo contra esses valores.

**Limitação:** o acesso automatizado usado nesta conversa permite editar arquivos de texto no GitHub, mas não tem acesso direto aos bytes dos ZIPs locais. Este procedimento é a etapa necessária para importar os dados completos, sem alegar que já estejam no GitHub.
