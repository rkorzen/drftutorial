from datetime import datetime
from pony.orm import Database, Required, Optional, Set, PrimaryKey, db_session, desc
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

db = Database()

# Pobieramy dostępne języki i style z pygments
LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = {item[1][0]: item[0] for item in LEXERS}
STYLE_CHOICES = {style: style for style in get_all_styles()}

class Snippet(db.Entity):
    _table_ = "snippets_snippet"
    
    id = PrimaryKey(int, auto=True)
    created = Required(datetime, default=lambda: datetime.utcnow())
    title = Optional(str, max_len=100)
    code = Required(str)
    linenos = Required(bool, default=False)
    language = Required(str, default="python")
    style = Required(str, default="friendly")
    highlighted = Optional(str)
    owner = Required('User', column='owner_id')  # Określamy nazwę kolumny

    def before_insert(self):
        self._highlight_code()
    
    def before_update(self):
        self._highlight_code()
        
    def _highlight_code(self):
        """Podświetlanie kodu przy zapisie."""
        lexer = get_lexer_by_name(self.language)
        linenos = "table" if self.linenos else False
        options = {"title": self.title} if self.title else {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos, full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)

class User(db.Entity):
    _table_ = "auth_user"
    
    id = PrimaryKey(int, auto=True)
    username = Required(str, unique=True)
    snippets = Set(Snippet)

# Konfiguracja bazy danych
db.bind(provider='sqlite', filename='db.sqlite3', create_db=True)
db.generate_mapping(create_tables=True)

# Przykład użycia
@db_session
def create_snippet():
    # Znajdź lub utwórz użytkownika
    user = User.get(username="rkorzen") or User(username="rkorzen")
    
    # Utwórz nowy snippet
    snippet = Snippet(
        title="Hello World in Python",
        code='print("Hello, Rafał!")',
        language="python",
        style="monokai",
        owner=user
    )

    last_snippet = Snippet.select().order_by(desc(Snippet.id)).first()
    
    print("Podświetlony kod:", last_snippet.highlighted)

if __name__ == "__main__":
    create_snippet()