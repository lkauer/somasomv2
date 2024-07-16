# Som a Som

## Descrição
**Som a Som** é uma rede independente de distribuição e colaboração sonora. Nossa missão é conectar artistas e ouvintes, proporcionando um espaço para a descoberta e o compartilhamento de novos sons. Acreditamos na força da colaboração e na diversidade de vozes para enriquecer o panorama musical.

## Funcionalidades
- **Cadastro de Artistas:** Permite que artistas criem perfis personalizados com informações e imagens.
- **Cadastro de Sons:** Artistas podem fazer upload de suas músicas, incluindo capa e áudio.
- **Busca e Filtragem:** Usuários podem buscar artistas e sons por nome ou título.
- **Paginação:** Listagens de artistas e sons são paginadas para melhor navegação.
- **Área de Administração:** Artistas têm acesso a um painel para gerenciar seus conteúdos.

## Tecnologias Utilizadas
- **Django:** Framework web utilizado para o desenvolvimento do backend.
- **HTML/CSS:** Linguagens de marcação e estilo para o frontend.
- **JavaScript:** Para interatividade no frontend.
- **SQLite/MySQL:** Bancos de dados utilizados para armazenar informações.

## Instalação e Configuração
### Pré-requisitos
- Python 3.x
- Pipenv ou pip
- Banco de dados SQLite ou MySQL

### Passos para Configuração
1. Clone o repositório:
    ```bash
    git clone https://github.com/lkauer/somasomv2.git
    cd somasomv2
    ```

2. Crie um ambiente virtual e ative-o:
    ```bash
    pipenv shell
    ```

3. Instale as dependências:
    ```bash
    pipenv install
    ```

4. Configure as variáveis de ambiente no arquivo `.env`:
    ```env
    SECRET_KEY=your_secret_key
    DEBUG=True
    DATABASE_URL=sqlite:///db.sqlite3  # ou configure com MySQL
    ```

5. Execute as migrações do banco de dados:
    ```bash
    python manage.py migrate
    ```

6. Inicie o servidor:
    ```bash
    python manage.py runserver
    ```

## Contribuição
### Como Contribuir
1. Faça um fork do projeto
2. Crie uma branch para sua feature ou correção:
    ```bash
    git checkout -b minha-feature
    ```
3. Faça commit das suas alterações:
    ```bash
    git commit -m 'Adiciona minha feature'
    ```
4. Envie para o branch original:
    ```bash
    git push origin minha-feature
    ```
5. Crie um Pull Request

### Issues
Se você encontrar algum problema ou tiver uma sugestão, por favor, abra uma [issue](https://github.com/lkauer/somasomv2/issues).

## Licença
Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Contato
Para mais informações, entre em contato via [lucasgkauer@gmail.com](mailto:lucasgkauer@gmail.com).

---

**Som a Som** - Conectando artistas e ouvintes através da música.
