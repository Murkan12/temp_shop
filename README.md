temp_shop

Szablon strony sklepu internetowego

Widoki strony:

1. index.html
    
    Widok przedstawia stronę główną, która zawiera produkty znajdujące się w bazie danych, opcje logowania i rejestracji, koszyk z dodanymi przez użytkownika produktami oraz dane kontaktowe firmy.

   Posiada ona również opcję wyszukiwania produktów po ich nazwie oraz możliwość filtrowania produktów w wybranym przez użytkownika przedziale cenowym.
2. login.html

   Strona logowania użytkownika zawieracjąca pola "username" oraz "password" które pozwalają użytkownikowi na zalogowanie się do jego konta, w przypadku, gdy podane przez niego dane będą prawidłowe
3. register.html

   Strona służąca do rejestracji nowych użytkowników. Wymaga ona podania nazwy użytkownika, e-maila oraz hasła zgodnego z podanymi wymaganiami. Po pomyślnej rejestracji tworzy nowego użytkownika
4. cart.html

   Strona wyświetlająca produkty dodane do koszyka przez danego użytkownika. Pozwala ona również na dokonanie płatności za pomocą platformy PayPal w wysokości sumy cen produktów zawartych w koszyku
5. search.html

   Wyświetla produkty przefiltrowane przez użytkownika w wybrany sposób np. poprzez cenę. Pokazuje również wyniki wyszukiwania produktu

Baza danych:

plik temp_shop_ecommerce/models.py - zawiera tabele znajdujące się w bazie danych.

User - przechowuje dane zarejestrowanego użytkownika
Product - reprezentuje produkt, który można kupić na stronie
OrderSummary- reprezentuje koszyk każdego użytkownika
Order - reprezentuje dany produkt znajdujący się w koszyku użytkownika

temp_shop_ecommerce/tests - folder zawierający testy funkcjonalności strony

temp_shop_ecommerce/urls.py - zawiera adresy url, do których jest przekierowywana strona.
register/ - adres rejestracji
email-confirmation-sent/ - wysłanie potwierdzenia pomyślnej rejestracji mailem
activate/<uidb64>/<token>/ - aktywuje użytkownika na stronie
login/ - adres logowania
logout/ - adres wylogowywania
cart/ - adres koszyka użytkownika
create_order/<int:product_id>/ - dodanie produktu do koszyka
delete_item/<int:order_id>/ - usunięcie produktu z koszyka
search/ - wyszukiwania produktów z wybranymi przez użytkownika parametrami
payment/ - przekierowanie do płatności
filter/ - filtrowanie produktów po cenie

Plik settings.py - zawiera ustawienia oraz konfigurację strony, wraz z możliwościami integracji z innymi serwisami (np. paypal, email)

forms.py - zawiera formę rejestracji użytkownika na stronie

requirements.txt - zawiera wszystkie biblioteki wykorzystywane w projekcie

folder static - zawiera plik style.css przechowujący wygląd elementów znajdujących się na stronie

