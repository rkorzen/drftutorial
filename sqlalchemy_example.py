from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy.ext.declarative import declared_attr
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from sqlalchemy import create_engine

Base = declarative_base()

# Pobieramy dostępne języki i style z pygments
LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = {item[1][0]: item[0] for item in LEXERS}
STYLE_CHOICES = {style: style for style in get_all_styles()}

class Snippet(Base):
    __tablename__ = "snippets_snippet"

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.utcnow)
    title = Column(String(100), nullable=True)
    code = Column(Text, nullable=False)
    linenos = Column(Boolean, default=False)
    language = Column(String(100), default="python")
    style = Column(String(100), default="friendly")
    owner_id = Column(Integer, ForeignKey("auth_user.id"))
    highlighted = Column(Text)

    owner = relationship("User", back_populates="snippets")

    def save(self, session):
        """Podświetlanie kodu przy zapisie."""
        lexer = get_lexer_by_name(self.language)
        linenos = "table" if self.linenos else False
        options = {"title": self.title} if self.title else {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos, full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)

        session.add(self)
        session.commit()

class User(Base):
    __tablename__ = "auth_user"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)

    snippets = relationship("Snippet", back_populates="owner")

# Konfiguracja bazy danych
engine = create_engine("sqlite:///db.sqlite3")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Przykład dodania nowego Snippeta
user = session.query(User).filter_by(username="rkorzen").first()

snippet = Snippet(
    title="Hello World in Python",
    code='print("Hello, World!")',
    language="python",
    style="monokai",
    owner=user
)

snippet.save(session)
print("Podświetlony kod:", snippet.highlighted)
