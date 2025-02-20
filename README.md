# pasta-digital
Aplicação para ajudar formadores do Ensino Profissional de Moçambique a fazer o registro das avaliações dos formandos e a geral a documentação nomeadamente  RI 1 e Folha de rosto para cada formando, e a pauta final do módulo.

## Setup
1. Instalar Dependências
   ```bash
   pip install django
   ```
   or
   ```bash
   pipenv install
   ```
2. Realizar as migrações do banco de dados(Local SQLite)
   ```bash
   python manage.py migrate
   ```
3. Criar  superusuário
   ```bash
   python manage.py createsuperuser
   ```
4. inicializar o servidor
   ```bash
   python manage.py runserver
   ```
## Como Usar
- Accéder o Painel de Administração
- Adicionar nova Turma e Registrar os estudantes
- Adicionar novo Módulo
- Na lista de Módulos, clique em **Resultados** para atribuir ou alterar os resultados das avaliações dos formandos conforme necessário.
 ![Imagem do Painel Resultados](https://github.com/madodadev/pasta-digital/blob/main/imagens/painel%20resultados.png?raw=true)

### Salvar PDF com RI e Folha de Rosto do Formando
- Clique no nome do formando para salvar o PDF com o RI e a folha de rosto do formando.
  ![Imagem do RI 1 e Folha de Rosto](https://github.com/madodadev/pasta-digital/blob/main/imagens/RI1-FolhaRosto.png?raw=true)

### Baixar Pauta do Módulo
- Clique no botão **Baixar Pauta** para salvar o PDF da pauta do módulo.
   ![Imagem da Pauta](https://github.com/madodadev/pasta-digital/blob/main/imagens/pauta.png?raw=true)
