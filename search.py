from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time


def get_page_content(url):
    driver = webdriver.Firefox()  # Или другой драйвер
    driver.get(url)
    time.sleep(2)  # Ждём загрузки страницы
    html = driver.page_source
    driver.quit()
    return html


def parse_paragraphs(html):
    soup = BeautifulSoup(html, 'html.parser')
    paragraphs = soup.find_all('p')

    print("\nПросмотр параграфов статьи. Нажмите Enter для продолжения, введите 'q' чтобы выйти.")

    for i, p in enumerate(paragraphs):
        print(f"Параграф {i + 1}:\n{p.get_text()}")

        if (i + 1) % 3 == 0 or i == len(paragraphs) - 1:
            user_input = input("Нажмите Enter, чтобы продолжить... или введите 'q' для выхода: ")
            if user_input.lower() in ['q', 'й']:
                print("Выход из просмотра параграфов.")
                break

def find_related_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    content = soup.find('div', {'id': 'bodyContent'})
    if content:
        for link in content.find_all('a', href=True):
            href = link['href']
            if href.startswith('/wiki/') and ':' not in href:
                full_url = f"https://ru.wikipedia.org{href}"
                links.append((link.get_text(strip=True), full_url))
            if len(links) == 5:  # Ограничиваем выбор до 5 статей
                break
    return links


def main():
    base_url = "https://ru.wikipedia.org/wiki/"
    while True:
        query = input("Введите запрос для поиска на Википедии (или 'выход' для выхода): ")
        if query.lower() in ['выход', 'exit']:
            print("Выход из программы.")
            break

        url = base_url + query.replace(' ', '_')
        html = get_page_content(url)

        while True:
            print("\nВыберите действие:")
            print("1. Листать параграфы текущей статьи")
            print("2. Перейти на связанную страницу")
            print("3. Выйти из программы")

            choice = input("Ваш выбор (1/2/3): ")

            if choice == '1':
                parse_paragraphs(html)
            elif choice == '2':
                related_links = find_related_links(html)
                if not related_links:
                    print("Связанных страниц не найдено.")
                    continue
                print("\nСвязанные страницы:")
                for i, (title, _) in enumerate(related_links):
                    print(f"{i + 1}. {title}")

                link_choice = input("Введите номер связанной страницы или 'назад': ")
                if link_choice.isdigit() and 1 <= int(link_choice) <= len(related_links):
                    new_url = related_links[int(link_choice) - 1][1]
                    html = get_page_content(new_url)
            elif choice == '3':
                print("Выход из программы.")
                return
            else:
                print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()